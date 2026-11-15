# Changelog

## 1.0.0 - 2026-11-15
- 단일 스크립트(`R6_Server.py`)를 파이썬 패키지 `r6_server` 로 정리 (`pip install .` → `r6-server`)
- 서버 목록을 게임 `GameSettings.ini` 주석 기준 `gamelift/*` 코드로 교체 (옛 `playfab/*` 는 `uaenorth` 만 유지)
- ini 주석에 새 코드가 생기면 목록에 자동 추가, 목록에 없는 현재 값도 표시
- 버그 수정: 현재 서버를 리스트로 읽어 강조 표시가 안 되던 문제
- 버그 수정: `DataCenterHint` 가 없을 때 `[ONLINE]` 섹션을 중복 추가하던 문제 (기존 섹션 아래에 삽입)
- 원본 줄바꿈(LF/CRLF) 보존, 서버 목록 스크롤 지원
- PyInstaller 단일 exe 빌드 스크립트 (`build_exe.ps1`)
