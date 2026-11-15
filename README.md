# R6_Server

레인보우 식스 시즈의 접속 서버(`DataCenterHint`)를 GUI로 고르는 Windows 도구.

`%USERPROFILE%\Documents\My Games\Rainbow Six - Siege\<계정 UUID>\GameSettings.ini` 의
`[ONLINE]` 섹션 `DataCenterHint` 값을 **모든 계정 폴더에 한 번에** 바꿉니다.

## 사용

- **exe**: [Releases](../../releases) 에서 `R6_Server.exe` 를 받아 실행
- **파이썬**:
  ```powershell
  pip install .
  r6-server            # 또는: python -m r6_server
  ```

1. 게임을 한 번 이상 실행해 `GameSettings.ini` 가 생성돼 있어야 합니다.
2. 목록에서 서버를 고르고 **저장** → 현재 적용 중인 서버는 파란색으로 강조됩니다.
3. 게임이 켜져 있었다면 재시작해야 적용됩니다.

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
```

비공식 팬 제작 도구이며 Ubisoft 와 관련이 없습니다.
