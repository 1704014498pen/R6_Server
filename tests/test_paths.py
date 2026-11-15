import os

import pytest

from r6_server import paths


@pytest.fixture
def docs(tmp_path, monkeypatch):
    """가짜 문서 폴더 + 계정 1개, config 는 tmp 로."""
    game = tmp_path / "Docs" / "My Games" / "Rainbow Six - Siege"
    acct = game / "uuid-1"
    acct.mkdir(parents=True)
    (acct / "GameSettings.ini").write_text("[ONLINE]\nDataCenterHint=default\n", encoding="utf-8")
    monkeypatch.setattr(paths, "CONFIG_PATH", str(tmp_path / "cfg" / "config.json"))
    return tmp_path / "Docs", game, acct


@pytest.mark.parametrize("pick", ["game", "acct", "mygames", "docs", "ini"])
def test_normalize_accepts_any_level(docs, pick):
    d, game, acct = docs
    chosen = {
        "game": game, "acct": acct, "mygames": game.parent, "docs": d,
        "ini": acct / "GameSettings.ini",
    }[pick]
    assert paths.normalize(str(chosen)) == os.path.normpath(str(game))


def test_normalize_rejects_unrelated(tmp_path):
    assert paths.normalize(str(tmp_path)) is None
    assert paths.normalize("") is None


def test_known_folder_is_used(docs, monkeypatch):
    d, game, _ = docs
    monkeypatch.setattr(paths, "known_documents_dir", lambda: str(d))
    assert paths.get_base_dir() == os.path.normpath(str(game))


def test_saved_path_wins_and_survives(docs, monkeypatch):
    _, game, _ = docs
    monkeypatch.setattr(paths, "known_documents_dir", lambda: None)
    monkeypatch.setattr(paths.os.path, "expanduser", lambda p: "/nonexistent-home")
    paths.save(str(game))
    assert paths.load_saved() == str(game)
    assert paths.get_base_dir() == str(game)


def test_stale_saved_path_falls_back(docs, monkeypatch, tmp_path):
    d, game, _ = docs
    paths.save(str(tmp_path / "gone"))
    monkeypatch.setattr(paths, "known_documents_dir", lambda: str(d))
    assert paths.get_base_dir() == os.path.normpath(str(game))


def test_corrupt_config_is_ignored(docs):
    os.makedirs(os.path.dirname(paths.CONFIG_PATH), exist_ok=True)
    with open(paths.CONFIG_PATH, "w") as f:
        f.write("{not json")
    assert paths.load_saved() is None
