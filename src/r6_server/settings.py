"""GameSettings.ini 읽기/쓰기. GUI 와 분리해 테스트 가능하게 둔다."""

import glob
import os
import re

from r6_server import paths
from r6_server.servers import DEFAULT_CODE

INI_NAME = paths.INI_NAME
SECTION = "[ONLINE]"

_HINT_RE = re.compile(r"^\s*DataCenterHint\s*=(.*)$")
# 주석 속 코드 목록:  ";    gamelift/ap-northeast-2"
_COMMENT_CODE_RE = re.compile(r"^\s*;\s*((?:gamelift|playfab)/[A-Za-z0-9-]+)\s*$")


def find_ini_files(base_dir=None):
    """계정(UUID 폴더)별 GameSettings.ini 경로 목록. base_dir 생략 시 자동 탐색."""
    base_dir = base_dir or paths.get_base_dir()
    if not os.path.isdir(base_dir):
        return []
    return sorted(glob.glob(os.path.join(base_dir, "*", INI_NAME)))


def _read_text(path):
    # newline="" : 원본 줄바꿈(LF/CRLF)을 그대로 보존
    with open(path, "r", encoding="utf-8", errors="ignore", newline="") as f:
        return f.read()


def read_hint(path):
    """파일의 DataCenterHint 값. 항목이 없으면 'default'."""
    for line in _read_text(path).splitlines():
        m = _HINT_RE.match(line)
        if m:
            return m.group(1).strip() or DEFAULT_CODE
    return DEFAULT_CODE


def current_code(base_dir=None):
    """가장 최근에 수정된 ini 의 값. ini 가 없거나 못 읽으면 None."""
    files = find_ini_files(base_dir)
    if not files:
        return None
    latest = max(files, key=os.path.getmtime)
    try:
        return read_hint(latest)
    except OSError:
        return None


def parse_hint_codes(base_dir=None):
    """ini 주석에 게임이 적어 둔 서버 코드 목록 (순서 유지, 중복 제거)."""
    codes = []
    for path in find_ini_files(base_dir):
        try:
            text = _read_text(path)
        except OSError:
            continue
        for line in text.splitlines():
            m = _COMMENT_CODE_RE.match(line)
            if m and m.group(1) not in codes:
                codes.append(m.group(1))
    return codes


def set_hint_text(text, code):
    """ini 텍스트에서 DataCenterHint 를 code 로 바꾼 새 텍스트를 돌려준다."""
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines(keepends=True)
    new_line = f"DataCenterHint={code}"

    found = False
    for i, line in enumerate(lines):
        if _HINT_RE.match(line.rstrip("\r\n")):
            ending = line[len(line.rstrip("\r\n")):] or nl
            lines[i] = new_line + ending
            found = True
    if found:
        return "".join(lines)

    # 항목이 없으면 [ONLINE] 섹션 헤더 바로 아래에 넣는다
    for i, line in enumerate(lines):
        if line.strip().upper() == SECTION:
            if not line.endswith(("\n", "\r")):
                lines[i] = line + nl
            lines.insert(i + 1, new_line + nl)
            return "".join(lines)

    # 섹션도 없으면 파일 끝에 섹션째 추가
    tail = "" if (not text or text.endswith(("\n", "\r"))) else nl
    return text + tail + nl + SECTION + nl + new_line + nl


def write_hint(path, code):
    text = _read_text(path)
    new_text = set_hint_text(text, code)
    if new_text != text:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_text)


def apply_to_all(code, base_dir=None):
    """모든 계정 ini 에 적용. 적용한 파일 수를 돌려준다. 실패 시 OSError."""
    files = find_ini_files(base_dir)
    for path in files:
        write_hint(path, code)
    return len(files)
