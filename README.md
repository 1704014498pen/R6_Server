# R6_Server

레인보우 식스 시즈의 접속 서버(`DataCenterHint`)를 GUI로 고르는 Windows 도구.

`%USERPROFILE%\Documents\My Games\Rainbow Six - Siege\<계정 UUID>\GameSettings.ini` 의
`[ONLINE]` 섹션 `DataCenterHint` 값을 **모든 계정 폴더에 한 번에** 바꿉니다.

## 사용 — exe 하나면 끝 (설치 불필요)

1. [Releases](../../releases/latest) 에서 `R6_Server.exe` 를 받아 더블클릭.
   파이썬 등 아무것도 설치할 필요 없습니다.
   - 서명 없는 exe 라 처음에 SmartScreen("Windows의 PC 보호")이 뜰 수 있습니다 → **추가 정보 → 실행**.
2. 목록에서 서버를 고르고 **저장** → 현재 적용 중인 서버는 파란색으로 강조됩니다.
3. 게임이 켜져 있었다면 재시작해야 적용됩니다.

게임을 한 번 이상 실행해 `GameSettings.ini` 가 생성돼 있어야 합니다.

### 설정 폴더를 못 찾을 때

문서 폴더 위치는 Windows 에서 직접 받아 오므로 OneDrive 백업이나 다른 드라이브로 옮긴 경우도 자동으로 찾습니다.
그래도 "설정 파일을 못 찾았습니다" 가 뜨면 **📁 폴더 선택** 으로
`문서\My Games\Rainbow Six - Siege` 폴더(또는 문서 / My Games / 계정 폴더)를 고르세요.
고른 경로는 `%APPDATA%\R6_Server\config.json` 에 기억됩니다.

## 서버 코드

게임이 ini 주석에 적어 두는 목록(`gamelift/*` + `playfab/uaenorth`)을 기본으로 씁니다.
게임 업데이트로 주석에 새 코드가 생기면 목록 아래에 자동으로 추가됩니다.

| 코드 | 위치 |
|---|---|
| `default` | 핑 기준 자동 |
| `gamelift/ap-northeast-2` | 서울 |
| `gamelift/ap-northeast-1` / `-3` | 도쿄 / 오사카 |
| `gamelift/ap-east-1` | 홍콩 |
| `gamelift/ap-southeast-1` / `-2` | 싱가포르 / 시드니 |
| `gamelift/ap-south-1` | 뭄바이 |
| `gamelift/us-west-1` / `-2` | N.캘리포니아 / 오리건 |
| `gamelift/us-east-1` / `-2` | 버지니아 / 오하이오 |
| `gamelift/ca-central-1` | 캐나다 |
| `gamelift/sa-east-1` | 상파울루 |
| `gamelift/eu-west-1` / `-2` / `-3` | 아일랜드 / 런던 / 파리 |
| `gamelift/eu-central-1` | 프랑크푸르트 |
| `gamelift/eu-north-1` / `eu-south-1` | 스톡홀름 / 밀라노 |
| `gamelift/af-south-1` | 케이프타운 |
| `playfab/uaenorth` | UAE |

## 개발

```powershell
pip install -e .[dev]
python -m pytest
.\build_exe.ps1      # → dist\R6_Server.exe
r6-server            # 또는: python -m r6_server
```

## 면책 조항 (Disclaimer)

- 이 프로그램은 **비공식 팬 제작 도구**이며 Ubisoft 및 Rainbow Six Siege 와 아무 관련이 없습니다.
- **어떠한 보증도 없이 "있는 그대로" 제공**됩니다.
- 이 프로그램의 사용으로 발생하는 **모든 결과 — 밴(계정 정지·영구 정지), 경고·랭크 제재 등
  게임사의 모든 제재, 설정 파일 손상, 접속·매칭 문제, 데이터 손실 등 직·간접적 손해 일체 —
  에 대한 책임은 전적으로 사용자에게 있으며, 제작자는 어떠한 책임도 지지 않습니다.**
- 게임사의 이용약관·정책은 언제든 바뀔 수 있습니다. 사용 여부는 사용자가 스스로 판단하세요.
- 사용 전 설정 파일을 직접 백업해 두는 것을 권장합니다.

This is an unofficial fan-made tool, not affiliated with Ubisoft. It is provided "AS IS" without warranty
of any kind. **You use it entirely at your own risk; the author is not liable for any damage or
consequence arising from its use, including account bans, suspensions or any other sanctions**
(see [LICENSE](LICENSE)).
