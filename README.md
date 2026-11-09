# 앱 리뷰 수집기

Google Play와 Apple App Store의 한국어 리뷰를 CSV로 저장하는 두 개의 작은 스크립트입니다. 앱 사용자의 불편 사항을 직접 확인하거나 기간별 평점 변화를 분석할 때 사용합니다.

## 실행

Python 3.11 이상에서 가상환경을 만든 뒤 설치합니다.

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

- Google Play: `python Google_play_app_review_crawler.py` 실행 후 앱 패키지 ID를 입력합니다. 예: `com.example.app`.
- App Store: `python App_store_app_review_crawler.py` 실행 후 앱 이름 또는 숫자 앱 ID를 입력합니다.

결과는 실행한 폴더의 `Google_play_<패키지ID>_reviews.csv` 또는 `AppStore_<이름>_reviews.csv`에 저장됩니다. 두 스크립트의 출력 열은 서로 다르므로 합쳐서 분석할 때 열 이름과 날짜 형식을 먼저 맞춰야 합니다.

## 활용과 주의

1. 수집 목적, 앱 ID, 수집일, 국가·언어를 분석 노트에 기록합니다.
2. 리뷰의 개인정보를 확인하고 공유용 데이터에서는 제거합니다. 생성된 CSV는 Git에 올리지 않습니다.
3. 스토어 화면과 비공식 스크레이퍼의 동작이 바뀌면 수집이 중단될 수 있습니다. 결과 건수와 날짜 범위를 확인합니다.
4. Google Play 스크립트는 가능한 리뷰 전체를 가져오므로 앱에 따라 오래 걸릴 수 있습니다.

이 저장소의 가치는 크롤러 코드 자체보다 **같은 앱의 리뷰를 반복 수집해 변화와 문제를 비교하는 절차**에 있습니다. 분석 결과에는 대표 문제, 근거 리뷰 수, 기간, 해석의 한계를 짧게 남겨 재사용합니다.
