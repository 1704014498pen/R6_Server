"""서버(데이터센터) 코드 목록.

코드는 게임이 GameSettings.ini 의 [ONLINE] 섹션 주석에 직접 적어 두는 값을 기준으로 한다.
게임이 목록을 바꾸면 settings.parse_hint_codes() 가 주석에서 새 코드를 읽어 보충한다.
"""

DEFAULT_CODE = "default"

# (설정값, 표시 이름) - 표시 순서
SERVERS = [
    (DEFAULT_CODE, "자동 / 핑 기준 (default)"),
    ("gamelift/ap-northeast-2", "한국 서울 (ap-northeast-2)"),
    ("gamelift/ap-northeast-1", "일본 도쿄 (ap-northeast-1)"),
    ("gamelift/ap-northeast-3", "일본 오사카 (ap-northeast-3)"),
    ("gamelift/ap-east-1", "홍콩 (ap-east-1)"),
    ("gamelift/ap-southeast-1", "싱가포르 (ap-southeast-1)"),
    ("gamelift/ap-southeast-2", "호주 시드니 (ap-southeast-2)"),
    ("gamelift/ap-south-1", "인도 뭄바이 (ap-south-1)"),
    ("gamelift/us-west-1", "미국 서부 N.캘리포니아 (us-west-1)"),
    ("gamelift/us-west-2", "미국 서부 오리건 (us-west-2)"),
    ("gamelift/us-east-1", "미국 동부 버지니아 (us-east-1)"),
    ("gamelift/us-east-2", "미국 동부 오하이오 (us-east-2)"),
    ("gamelift/ca-central-1", "캐나다 중부 (ca-central-1)"),
    ("gamelift/sa-east-1", "브라질 상파울루 (sa-east-1)"),
    ("gamelift/eu-west-1", "아일랜드 (eu-west-1)"),
    ("gamelift/eu-west-2", "영국 런던 (eu-west-2)"),
    ("gamelift/eu-west-3", "프랑스 파리 (eu-west-3)"),
    ("gamelift/eu-central-1", "독일 프랑크푸르트 (eu-central-1)"),
    ("gamelift/eu-north-1", "스웨덴 스톡홀름 (eu-north-1)"),
    ("gamelift/eu-south-1", "이탈리아 밀라노 (eu-south-1)"),
    ("gamelift/af-south-1", "남아공 케이프타운 (af-south-1)"),
    ("playfab/uaenorth", "중동 UAE 북부 (uaenorth)"),
]

KNOWN_CODES = {code for code, _ in SERVERS}


def build_server_list(extra_codes=(), current_code=None):
    """기본 목록 + ini 주석에서 찾은 새 코드 + (목록에 없는) 현재 값을 합친다."""
    result = list(SERVERS)
    seen = set(KNOWN_CODES)
    for code in extra_codes:
        if code not in seen:
            result.append((code, f"{code} (게임 목록)"))
            seen.add(code)
    if current_code and current_code not in seen:
        result.append((current_code, f"{current_code} (현재 값 - 목록에 없음)"))
    return result
