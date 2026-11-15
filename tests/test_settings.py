import os
import time

from r6_server import settings
from r6_server.servers import build_server_list

SAMPLE = (
    "[DISPLAY]\nFPS=144\n\n[ONLINE]\n;DataCenterHint => \n;    default (ping based)\n"
    ";    gamelift/ap-northeast-2\n;    gamelift/xx-new-9\n;    playfab/uaenorth\n\n"
    ";comment\nDataCenterHint=default\n"
)


def make_account(base, name, text):
    d = base / name
    d.mkdir()
    p = d / "GameSettings.ini"
    p.write_bytes(text.encode("utf-8"))
    return p


def test_read_hint_returns_value(tmp_path):
    p = make_account(tmp_path, "a", SAMPLE.replace("=default", "=gamelift/ap-northeast-2"))
    assert settings.read_hint(str(p)) == "gamelift/ap-northeast-2"


def test_commented_hint_is_ignored(tmp_path):
    p = make_account(tmp_path, "a", "[ONLINE]\n;DataCenterHint=gamelift/us-east-1\n")
    assert settings.read_hint(str(p)) == "default"


def test_replace_preserves_rest_and_lf():
    out = settings.set_hint_text(SAMPLE, "gamelift/ap-northeast-1")
    assert out == SAMPLE.replace("DataCenterHint=default", "DataCenterHint=gamelift/ap-northeast-1")
    assert "\r" not in out


def test_replace_preserves_crlf():
    crlf = SAMPLE.replace("\n", "\r\n")
    out = settings.set_hint_text(crlf, "gamelift/eu-west-1")
    assert out == crlf.replace("DataCenterHint=default", "DataCenterHint=gamelift/eu-west-1")


def test_insert_under_existing_section():
    out = settings.set_hint_text("[A]\nx=1\n[ONLINE]\ny=2\n", "gamelift/ap-east-1")
    assert out == "[A]\nx=1\n[ONLINE]\nDataCenterHint=gamelift/ap-east-1\ny=2\n"
    assert out.count("[ONLINE]") == 1


def test_append_section_when_missing():
    out = settings.set_hint_text("[A]\nx=1", "default")
    assert out == "[A]\nx=1\n\n[ONLINE]\nDataCenterHint=default\n"


def test_apply_to_all_and_current_code(tmp_path):
    a = make_account(tmp_path, "a", SAMPLE)
    b = make_account(tmp_path, "b", "[ONLINE]\n")
    assert settings.apply_to_all("gamelift/ap-northeast-2", str(tmp_path)) == 2
    assert settings.read_hint(str(a)) == "gamelift/ap-northeast-2"
    assert settings.read_hint(str(b)) == "gamelift/ap-northeast-2"
    t = time.time()
    os.utime(a, (t + 10, t + 10))
    assert settings.current_code(str(tmp_path)) == "gamelift/ap-northeast-2"


def test_no_files(tmp_path):
    assert settings.find_ini_files(str(tmp_path / "nope")) == []
    assert settings.current_code(str(tmp_path)) is None


def test_parse_codes_and_merge(tmp_path):
    make_account(tmp_path, "a", SAMPLE)
    codes = settings.parse_hint_codes(str(tmp_path))
    assert codes == ["gamelift/ap-northeast-2", "gamelift/xx-new-9", "playfab/uaenorth"]
    merged = [c for c, _ in build_server_list(codes, "playfab/koreacentral")]
    assert merged.count("gamelift/ap-northeast-2") == 1
    assert "gamelift/xx-new-9" in merged
    assert merged[-1] == "playfab/koreacentral"
