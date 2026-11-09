# 앱 리뷰 수집기

Google Play와 App Store의 공개 리뷰를 **개수·기간을 제한해** CSV로 저장합니다. 두 스크립트는 같은 열을 출력하므로 앱별 불편 사항, 평점, 기간별 변화를 함께 분석할 수 있습니다.

## 설치와 실행

Python 3.11에서 가상환경을 만듭니다.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python Google_play_app_review_crawler.py com.example.app --limit 200 --after 2026-11-01
.\.venv\Scripts\python App_store_app_review_crawler.py --app-id 123456789 --limit 200 --after 2026-11-01
```

App Store는 `--app-name "정확한 앱 이름"`으로도 찾을 수 있습니다. 동일한 이름의 앱이 여럿이면 숫자 ID를 사용합니다. `--output 결과.csv`로 저장 위치를 지정합니다. Google Play는 `--lang ko --country kr`가 기본값입니다. 날짜는 포함 기준이며 `--after`를 생략하면 최신 리뷰부터 최대 200건을 가져옵니다. 두 수집기의 출력 열은 `store, app_id, review_id, review, score, review_date, app_version, thumbs_up_count, title`입니다. 스토어가 제공하지 않는 값은 빈 칸으로 남깁니다.

## 분석할 때

1. 앱 ID, 국가·언어, 수집 날짜, 기간, 실제 저장 건수를 함께 기록합니다.
2. `review_id`로 이전 CSV와 중복을 제거하고, 기간별 불만 유형과 평점 변화를 봅니다.
3. 공개 리뷰에도 개인정보가 들어갈 수 있습니다. 공유용 데이터에서는 내용을 검토하고 생성된 CSV는 Git에 올리지 않습니다.

Google Play는 [라이브러리의 페이지 처리](https://github.com/JoMingyu/google-play-scraper#app-reviews)를 사용합니다. App Store 이름 확인에는 [Apple의 검색 API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/)를, 리뷰에는 공개 RSS 피드를 사용합니다. **공개 RSS는 Apple의 공식 App Store Connect 리뷰 API가 아니며 제공 형식·건수에 보장이 없습니다.** 본인 소유 앱의 안정적인 수집에는 [App Store Connect Customer Reviews API](https://developer.apple.com/documentation/appstoreconnectapi/customer-reviews)를 검토하세요. 수집 실패나 빈 결과가 나오면 앱 ID·스토어 접근 상태·피드 변경을 확인하세요. 모든 리뷰를 완전하게 수집한다는 보장은 없습니다.

외부 접속 없이 수집·CSV 처리 경로를 확인하려면 `py -3.11 -m unittest -v test_crawlers.py`를 실행합니다.
