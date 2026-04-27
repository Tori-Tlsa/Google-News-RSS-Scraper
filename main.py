import os
import time
import pandas as pd
import feedparser
from datetime import datetime, timedelta
from urllib.parse import quote

def get_news_to_df(start_date, end_date, keywords):
    all_news = []
    print(f"\n🚀 수집 시작: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
    
    for kw in keywords:
        print(f"🔍 키워드 검색 중: {kw}")
        current_date = start_date
        
        while current_date <= end_date:
            d_str = current_date.strftime("%Y-%m-%d")
            next_d_str = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
            
            query = quote(f"{kw} after:{d_str} before:{next_d_str}")
            rss_url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
            
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries:
                all_news.append({
                    "날짜": current_date, 
                    "키워드": kw,
                    "제목": entry.title,
                    "링크": entry.link,
                    "매체": entry.source.title if hasattr(entry, 'source') else "알수없음",
                    "요약": entry.summary if hasattr(entry, 'summary') else "", 
                    "게시시간": entry.published if hasattr(entry, 'published') else "" 
                })
            
            current_date += timedelta(days=1)
            time.sleep(1) 
            
    df = pd.DataFrame(all_news)
    
    if not df.empty:
        df = df.drop_duplicates(subset=['제목'], keep='first')
        df['날짜'] = pd.to_datetime(df['날짜'])
        
    return df

def get_valid_date_input(prompt_msg):
    while True:
        user_input = input(prompt_msg)
        try:
            year, month, day = map(int, user_input.split(','))
            return datetime(year, month, day)
        except ValueError:
            print("❌ 형식 오류입니다. 콤마(,)를 사용하여 다시 입력해주세요. (예: 2026,04,01)\n")

if __name__ == "__main__":
    print("="*50)
    print(" 📰 Google News Scraper ")
    print("="*50)
    
    start = get_valid_date_input("1️⃣ 조회 시작 날짜를 입력하세요 (예: 2026,04,01): ")
    end = get_valid_date_input("2️⃣ 조회 종료 날짜를 입력하세요 (예: 2026,04,27): ")
    
    if end < start:
        print("\n⚠️ 종료일이 시작일보다 빠릅니다. 두 날짜를 자동으로 교체하여 진행합니다.")
        start, end = end, start

    kw_input = input("\n3️⃣ 검색할 키워드를 쉼표(,)로 구분하여 입력하세요 (예: 금리,환율,주식): ")
    search_keywords = [kw.strip() for kw in kw_input.split(',') if kw.strip()]
    
    if not search_keywords:
        print("⚠️ 키워드가 입력되지 않아 '경제' 단일 키워드로 진행합니다.")
        search_keywords = ["경제"]

    df = get_news_to_df(start, end, search_keywords)

    if not df.empty:
        print(f"\n✅ 총 {len(df)}개의 고유 기사를 수집했습니다.")
        
        # 결과 저장 폴더 생성 로직
        output_dir = "results"
        os.makedirs(output_dir, exist_ok=True)
        
        # 파일 경로 설정 및 저장
        file_name = f"news_result_{start.strftime('%Y%m%d')}_{end.strftime('%Y%m%d')}.xlsx"
        output_path = os.path.join(output_dir, file_name)
        
        df.to_excel(output_path, index=False)
        print(f"💾 파일 저장 완료: {output_path}")
    else:
        print("\n⚠️ 수집된 데이터가 없습니다.")