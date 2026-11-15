"""레식 설정 폴더 위치 찾기.

문서 폴더는 OneDrive 백업이나 '위치 이동'으로 ~\\Documents 가 아닐 수 있어서
Windows Known Folder API 로 실제 위치를 받는다. 그래도 못 찾으면 사용자가 고른 경로를
%APPDATA%\\R6_Server\\config.json 에 기억한다.
"""

import glob
import json
import os
import sys

GAME_DIR = os.path.join("My Games", "Rainbow Six - Siege")
INI_NAME = "GameSettings.ini"
CONFIG_PATH = os.path.join(
    os.environ.get("APPDATA") or os.path.expanduser("~"), "R6_Server", "config.json"
)

# FOLDERID_Documents
_DOCUMENTS_GUID = "{FDD39AD0-238F-46AF-ADB4-6C85480369C7}"


def known_documents_dir():
    """Windows 가 알고 있는 실제 문서 폴더. 실패하면 None."""
    if sys.platform != "win32":
        return None
    try:
        import ctypes
        from ctypes import wintypes

        class GUID(ctypes.Structure):
            _fields_ = [("d1", wintypes.DWORD), ("d2", wintypes.WORD),
                        ("d3", wintypes.WORD), ("d4", ctypes.c_ubyte * 8)]

        guid = GUID()
        ctypes.oledll.ole32.CLSIDFromString(_DOCUMENTS_GUID, ctypes.byref(guid))
        out = ctypes.c_wchar_p()
        ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(guid), 0, None, ctypes.byref(out))
        try:
            return out.value or None
        finally:
            ctypes.windll.ole32.CoTaskMemFree(out)
    except Exception:
        return None


def has_ini(base_dir):
    return bool(base_dir) and bool(glob.glob(os.path.join(base_dir, "*", INI_NAME)))


def normalize(path):
    """사용자가 고른 폴더를 'Rainbow Six - Siege' 폴더로 맞춘다. 못 맞추면 None.

    받는 것: 레식 폴더 / 계정(UUID) 폴더 / My Games / 문서 폴더 / GameSettings.ini 파일.
    """
    if not path:
        return None
    path = os.path.normpath(path)
    if os.path.isfile(path) and os.path.basename(path).lower() == INI_NAME.lower():
        path = os.path.dirname(path)
    candidates = [
        path,
        os.path.dirname(path),  # 계정 폴더를 고른 경우
        os.path.join(path, "Rainbow Six - Siege"),  # My Games 를 고른 경우
        os.path.join(path, GAME_DIR),  # 문서 폴더를 고른 경우
    ]
    for c in candidates:
        if has_ini(c):
            return c
    return None


def candidate_dirs():
    """자동 탐색 후보 (우선순위 순, 중복 제거)."""
    home = os.path.expanduser("~")
    docs = [
        known_documents_dir(),
        os.path.join(home, "Documents"),
        os.path.join(home, "OneDrive", "Documents"),
        os.path.join(home, "OneDrive", "문서"),
    ]
    out = []
    for d in docs:
        if d:
            c = os.path.normpath(os.path.join(d, GAME_DIR))
            if c not in out:
                out.append(c)
    return out


def load_saved():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("base_dir")
    except (OSError, ValueError, AttributeError):
        return None


def save(base_dir):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"base_dir": base_dir}, f, ensure_ascii=False, indent=2)


def get_base_dir():
    """저장된 경로 → 자동 탐색 순으로 ini 가 있는 곳. 없으면 첫 후보(안내용)."""
    saved = load_saved()
    if has_ini(saved):
        return saved
    cands = candidate_dirs()
    for c in cands:
        if has_ini(c):
            return c
    return cands[0]
