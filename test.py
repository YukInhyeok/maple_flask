import requests
from datetime import date, timedelta

today = date.today()
yesterday = today - timedelta(days=1)
print(yesterday)

headers = {
    "x-nxopen-api-key": "test_220c33e40b65c92482e029516373f544dc8910fc39d0853f3ee728c02de95589bffac000d9444c05b54ecbf051285bb5"
}

characterName = "Ho영원"
urlString = "https://open.api.nexon.com/maplestory/v1/id?character_name=" + characterName
# '단솜' 유저를 대상으로 ocid 값을 구한다.
response = requests.get(urlString, headers=headers)

# 조회한 ocid 값을 변수에 저장한다.
ocid = response.json()['ocid']

# 단솜유저의 ocid값과 조회 기준일을 파라미터로 넘겨, 기본정보 조회하는 API를 호출 /maplestory/v1/character/skill
urlString = "https://open.api.nexon.com/maplestory/v1/character/skill?ocid=" + ocid + "&date=2024-04-28&character_skill_grade=6"
# 단솜유저의 기본정보 조회 결과값 저장
response = requests.get(urlString, headers=headers)

# 기본정보 출력
print(response.json())
