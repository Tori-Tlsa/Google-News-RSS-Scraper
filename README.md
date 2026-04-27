# Google News RSS Scraper

특정 기간과 키워드를 기반으로 구글 뉴스 기사를 수집하여 엑셀(`.xlsx`)로 추출하는 Python CLI 툴입니다.

## Features
- **대화형 CLI**: 실행 시 터미널에서 시작일, 종료일, 다중 키워드를 직접 입력받아 구동합니다.
- **중복 제거**: 수집된 기사 중 제목이 동일한 기사를 자동으로 필터링합니다.
- **자동 폴더 분류**: 수집 완료 시 `results` 폴더를 자동 생성하고 엑셀 파일을 저장합니다.

## Installation

1. 저장소 클론 및 폴더 이동
```bash
git clone [https://github.com/YourUsername/google-news-scraper.git](https://github.com/YourUsername/google-news-scraper.git)
cd google-news-scraper