import os
import sys
import sqlite3

# Type2 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import NewsDatabase

def test_type2_bulk_save():
    db_path = "news_assistant.db"
    db = NewsDatabase(db_path)
    
    # 1. 기존 테이블 및 메서드 확인
    print("Checking database structure...")
    
    # 2. Bulk 저장 테스트
    test_news = [
        {"title": "Type2 테스트 뉴스 1", "url": "https://type2-test.com/1", "category": "정치", "source_name": "Type2테스터"},
        {"title": "Type2 테스트 뉴스 2", "url": "https://type2-test.com/2", "category": "경제", "source_name": "Type2테스터"}
    ]
    
    added_count = db.save_crawled_news(test_news)
    print(f"✅ {added_count}개의 뉴스가 대량 저장되었습니다.")
    
    # 3. 중복 확인
    added_count_retry = db.save_crawled_news(test_news)
    print(f"ℹ️ 중복 저장 시도 결과: {added_count_retry}개 추가됨 (0이어야 함)")
    
    # 4. 데이터 조회
    scraped = db.get_scraped_news(limit=5)
    print(f"✅ 최근 수집된 뉴스 (상위 5개):")
    for item in scraped:
        if item['source_name'] == 'Type2테스터':
            print(f"   - {item['title']} [{item['source_name']}]")

if __name__ == "__main__":
    test_type2_bulk_save()
