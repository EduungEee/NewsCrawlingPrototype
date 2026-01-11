"""
AI 뉴스 어시스턴트 - 리팩터링된 메인 애플리케이션
"""
import streamlit as st
import pandas as pd
from datetime import datetime

# 로컬 모듈 임포트
from database import NewsDatabase
from news_scraper import NewsScraper

from enhanced_news_summarizer import EnhancedNewsSummarizer
from ui_components import (
    render_header, render_navigation, render_sidebar,
    render_news_table, render_summary_result,
    render_detailed_news_summary,
    render_db_news_selection, render_grouped_agency_buttons
)
# PPT 스타일 전역 CSS 적용
st.markdown("""
<style>
    /* PPT 이미지 스타일 적용 */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* 버튼 스타일 개선 */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* 데이터프레임 스타일 */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* 성공/에러 메시지 스타일 */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 1px solid #10b981;
        border-radius: 8px;
        color: #065f46; /* 짙은 녹색 텍스트 */
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 1px solid #ef4444;
        border-radius: 8px;
        color: #991b1b; /* 짙은 빨간색 텍스트 */
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 1px solid #f59e0b;
        border-radius: 8px;
        color: #92400e; /* 짙은 주황색 텍스트 */
    }
    
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 1px solid #3b82f6;
        border-radius: 8px;
        color: #1e40af; /* 짙은 파란색 텍스트 */
    }

    /* 사이드바 텍스트 흰색 강제 적용 */
    [data-testid="stSidebar"] {
        color: white !important;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: white !important;
    }
    
    /* 사이드바 입력 필드 라벨 */
    .st-emotion-cache-16idsys p {
        color: white !important;
    }
    
    /* 기본 텍스트 색상 강제 (라이트 모드 기준) */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
        color: #1e293b !important;
    }
    
    /* 헤더나 특정 컴포넌트의 흰색 텍스트는 유지해야 함으로 구체성 높임 */
    .main-header h1, .main-header p {
        color: white !important;
    }
    
    .summary-box h3, .summary-box p {
        color: white !important;
    }
    
    .stButton > button {
        color: white !important;
    }

    /* Expander 스타일 개선 */
    .stExpander {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    .stExpander > details > summary {
        color: #000000 !important;
        font-weight: 600;
        background: transparent !important;
    }

    .stExpander > details > summary:hover {
        color: #3b82f6 !important;
    }

    .stExpander [data-testid="stExpanderDetails"] {
        background: transparent !important;
        color: #000000 !important;
        padding-top: 0;
    }

    /* 검색 결과 및 필터 텍스트 색상 강제 */
    .stExpander p, .stExpander span, .stExpander label, .stExpander h1, .stExpander h2, .stExpander h3, .stExpander h4 {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .page-button {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: bold;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .page-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .news-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .summary-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .content-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """세션 상태 초기화"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'news'
    if 'selected_news' not in st.session_state:
        st.session_state.selected_news = None
    if 'news_summary' not in st.session_state:
        st.session_state.news_summary = None
    if 'db' not in st.session_state:
        st.session_state.db = NewsDatabase()
    
    # AI 요약기 초기화 (API 키가 있는 경우)
    if 'enhanced_summarizer' not in st.session_state and st.session_state.get('api_key'):
        from enhanced_news_summarizer import EnhancedNewsSummarizer
        st.session_state.enhanced_summarizer = EnhancedNewsSummarizer(st.session_state.api_key)

def show_news_page():
    """뉴스 요약 페이지"""
    # 헤더 제거됨
    # st.header("📰 뉴스 요약")
    
    # 1. 상단: 뉴스 수집 및 가시성 필터링 영역 (항상 표시)
    
    # 사이드바에서 선택된 언론사 확인
    selected_sources = st.session_state.get('source_select', ['전체'])
    if isinstance(selected_sources, str):
        selected_sources = [selected_sources]

    # 사이드바에서 선택된 카테고리 확인
    selected_categories = st.session_state.selected_category if 'selected_category' in st.session_state else ["전체"]
    if isinstance(selected_categories, str):
        selected_categories = [selected_categories]
        
    if not selected_categories:
        st.info("👈 왼쪽 사이드바에서 **카테고리**를 선택해 주세요.")
        return

    db = st.session_state.db
    all_db_sources = db.get_news_sources()
    
    # [수집 대상 필터링] 사이드바 옵션에 따라 수집 대상 소스 목록 선정
    target_sources = all_db_sources
    if "전체" not in selected_categories:
        target_sources = [s for s in target_sources if s['category'] in selected_categories]
    if "전체" not in selected_sources:
        target_sources = [s for s in target_sources if s['source_name'] in selected_sources]
    
    # [뉴스 수집 및 DB 조회 버튼 영역]
    # use_container_width 이슈 대응: 각 컬럼 내부 버튼은 full width 사용
    col_db, col_fetch = st.columns(2)
    
    with col_db:
        if st.button("📂 저장된 뉴스 보기 (DB)", use_container_width=True):
            with st.spinner("💾 저장된 뉴스를 불러오는 중..."):
                saved_news = db.get_scraped_news(limit=300) # 최근 300개
                
                # 현재 선택된 필터 적용 (옵션)
                # 만약 사이드바 필터에 맞춰서 보여주고 싶다면 여기서 필터링
                filtered_saved = []
                for news in saved_news:
                    # 카테고리 필터
                    if "전체" not in selected_categories and news['category'] not in selected_categories:
                        continue
                    # 소스 필터
                    if "전체" not in selected_sources and news['source_name'] not in selected_sources:
                        continue
                    filtered_saved.append(news)
                
                if filtered_saved:
                    st.session_state.news_list = filtered_saved
                    st.session_state.view_filter = None
                    st.success(f"✅ 저장된 뉴스 {len(filtered_saved)}개를 불러왔습니다.")
                    st.rerun()
                else:
                    st.warning("⚠️ 조건에 맞는 저장된 뉴스가 없습니다.")

    with col_fetch:
        if st.button("🔄 뉴스 새로 가져오기 (Scrape)", type="primary", use_container_width=True): 
            if not target_sources:
                st.warning("⚠️ 선택된 조건에 맞는 뉴스 소스가 없습니다.")
            else:
                with st.spinner("🔍 뉴스를 수집하는 중입니다... 잠시만 기다려주세요."):
                    scraper = NewsScraper()
                    all_news = []
                    new_count = 0
                    
                    # 진행 상황 표시
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    total_sources = len(target_sources)
                    
                    for idx, source in enumerate(target_sources):
                        status_text.text(f"📡 수집 중 ({idx+1}/{total_sources}): {source['source_name']} - {source['category']}")
                        try:
                            # 1. 뉴스 수집
                            news_items = scraper.get_news_by_category(source['category'], source['source_name'])
                            
                            if news_items:
                                # 2. DB 저장 (Bulk)
                                added_count = db.save_crawled_news(news_items)
                                new_count += added_count
                                
                                all_news.extend(news_items)
                        except Exception as e:
                            print(f"Error scraping {source['source_name']}: {e}")
                        
                        progress_bar.progress((idx + 1) / total_sources)
                    
                    if all_news:
                        st.session_state.news_list = all_news
                        st.session_state.view_filter = None # 필터 초기화
                        
                        msg = f"✅ 총 {len(all_news)}개의 뉴스를 가져왔습니다!"
                        if new_count > 0:
                            msg += f" (새로운 뉴스 {new_count}개 저장)"
                        else:
                            msg += " (모두 이미 저장된 뉴스입니다)"
                        
                        st.success(msg)
                        st.rerun()
                    else:
                        st.warning("⚠️ 뉴스를 찾을 수 없습니다.")
                        progress_bar.empty()
                        status_text.empty()

    st.markdown("---")

    # [보기 필터 버튼] 수집된 뉴스 내에서 필터링
    # 현재 수집된 뉴스 리스트가 없으면, DB의 소스 목록을 보여주되 클릭해도 효과 없음(또는 안내)
    # 하지만 UX상 버튼은 항상 보이고, 클릭 시 '필터'가 적용된다는 것을 보여줘야 함.
    
    with st.expander("🔍 뉴스 언론사 및 카테고리 선택", expanded=True):
        # 버튼 렌더링용 소스는 '수집 대상 소스'와 동일하게 유지
        st.markdown(f"**👁️ 뷰 필터 (클릭하여 결과 좁혀보기)**")
        
        # [뉴스 카운트 계산]
        # 수집된 뉴스가 있는 경우, 각 (언론사, 카테고리)별 기사 수를 계산하여 버튼에 표시
        news_counts = None
        if 'news_list' in st.session_state and st.session_state.news_list:
            news_counts = {}
            for news in st.session_state.news_list:
                key = (news['source_name'], news['category'])
                news_counts[key] = news_counts.get(key, 0) + 1
                
        # 버튼 렌더링 및 선택 처리 (뷰 필터 업데이트)
        # render_grouped_agency_buttons가 클릭된 소스를 반환함.
        # 클릭 시 view_filter 업데이트
        clicked_source = render_grouped_agency_buttons(target_sources, news_counts=news_counts)
        
        if clicked_source:
            # 뷰 필터 설정
            st.session_state.view_filter = {
                'source_name': clicked_source['source_name'],
                'category': clicked_source['category']
            }
            st.toast(f"필터 적용: {clicked_source['source_name']} - {clicked_source['category']}")
            # st.rerun() # 버튼 클릭 시 이미 리런되므로 필요 없을 수 있음, 하지만 명시적으로 상태 반영 위해
    
    # 필터 해제 버튼 (필터가 설정된 경우에만 표시)
    if st.session_state.get('view_filter'):
        if st.button("❌ 필터 해제 (전체 보기)", type="secondary"):
            st.session_state.view_filter = None
            st.rerun()

    # 2. 하단: 뉴스 리스트 및 요약 영역 (데이터가 있을 때만 표시)
    if 'news_list' in st.session_state and st.session_state.news_list:
        news_list = st.session_state.news_list
        
        # [필터링 적용] 사이드바 필터 + 뷰 필터
        display_list = news_list
        
        # 1. 사이드바 필터 (카테고리)
        if "전체" not in selected_categories:
            display_list = [n for n in display_list if n['category'] in selected_categories]
        
        # 2. 사이드바 필터 (언론사)
        if "전체" not in selected_sources:
            display_list = [n for n in display_list if n['source_name'] in selected_sources]
            
        # 3. 뷰 필터 (언론사-카테고리 버튼 선택)
        view_filter = st.session_state.get('view_filter')
        if view_filter:
            display_list = [
                n for n in display_list 
                if n['source_name'] == view_filter['source_name'] 
                and n['category'] == view_filter['category']
            ]
            filter_info = f"{view_filter['source_name']} > {view_filter['category']}"
        else:
            sidebar_active = ("전체" not in selected_categories) or ("전체" not in selected_sources)
            filter_info = "사이드바 필터 적용됨" if sidebar_active else "전체"
            
        if not display_list:
             st.info(f"ℹ️ '{filter_info}'에 해당하는 수집된 뉴스가 없습니다. (전체 {len(news_list)}개 중)")
        else:
            # [요약 상태 확인] 각 뉴스 항목에 대해 DB 확인 (성능 고려하여 이 시점에 수행)
            db = st.session_state.db
            for news in display_list:
                existing = db.get_news_by_url(news['url'])
                news['is_summarized'] = True if existing else False
                if existing:
                    news['summary_content'] = existing.get('summary') # 종합 분석용으로 저장

            with st.expander(f"📊 검색 결과 ({len(display_list)}건) - {filter_info}", expanded=True):
                # 카테고리 표시 문자열 생성
                categories = st.session_state.selected_category
                if isinstance(categories, list):
                    category_display = ", ".join(categories)
                else:
                    category_display = categories
                
                # '전체 선택' 체크박스 추가
                select_all = st.checkbox("모두 선택", value=False, key="select_all_news")
                    
                # 뉴스 테이블 렌더링 (체크박스 포함 editable dataframe)
                edited_df = render_news_table(display_list, category_display, default_select=select_all)
                
                # 1. 개별 뉴스 요약 & 상세보기 (Fold/Unfold 그룹화)
                with st.expander("📄 개별 뉴스 요약 & 상세보기", expanded=False):
                    selected_rows_for_action = pd.DataFrame() # 초기화
                    if edited_df is not None:
                        if '선택' in edited_df.columns:
                            selected_rows_for_action = edited_df[edited_df['선택'] == True]
                    
                    if not selected_rows_for_action.empty:
                        selected_count = len(selected_rows_for_action)
                        st.markdown(f"**선택된 뉴스: {selected_count}건**")
                        
                        # 개별 요약하기
                        if st.button(f"📄 선택한 뉴스 ({selected_count}건) 개별 요약하기", type="primary", use_container_width=True, key="btn_individual_summarize"):
                            if not st.session_state.get('api_key'):
                                st.error("❌ OpenAI API 키가 필요합니다.")
                            else:
                                progress_container = st.container()
                                with progress_container:
                                    progress_bar = st.progress(0)
                                    status_text = st.empty()
                                    if 'enhanced_summarizer' not in st.session_state:
                                        from enhanced_news_summarizer import EnhancedNewsSummarizer
                                        st.session_state.enhanced_summarizer = EnhancedNewsSummarizer(st.session_state.api_key)
                                    summarizer = st.session_state.enhanced_summarizer
                                    db = st.session_state.db
                                    results = []
                                    failed = []
                                    for i, (_, row) in enumerate(selected_rows_for_action.iterrows()):
                                        title = row['제목']
                                        url = row['URL']
                                        source_name = row['뉴스 업체']
                                        category = row['카테고리']
                                        status_text.text(f"📝 요약 확인 중 ({i+1}/{selected_count}): {title[:20]}...")
                                        existing_news = db.get_news_by_url(url)
                                        if existing_news and existing_news.get('summary'):
                                            results.append({
                                                'title': title, 'url': url, 'source_name': source_name,
                                                'category': category, 'summary': existing_news['summary'],
                                                'created_at': existing_news['created_at']
                                            })
                                        else:
                                            status_text.text(f"🪄 요약 생성 중 ({i+1}/{selected_count}): {title[:20]}...")
                                            try:
                                                result = summarizer.summarize_news_detailed(url, title)
                                                if isinstance(result, dict):
                                                    db.save_news_summary(title=title, url=url, category=category, source_name=source_name, summary=result['summary'])
                                                    result['source_name'] = source_name
                                                    result['category'] = category
                                                    result['created_at'] = result['scraped_at']
                                                    results.append(result)
                                                else:
                                                    failed.append(f"{title} (요약 실패)")
                                            except Exception as e:
                                                failed.append(f"{title} (오류: {str(e)})")
                                        progress_bar.progress((i + 1) / selected_count)
                                    status_text.text("✅ 작업 완료!")
                                    if results:
                                        st.success(f"총 {len(results)}개의 요약이 준비되었습니다.")
                                        for res in results:
                                            with st.expander(f"📄 {res['title']} ({res['source_name']})", expanded=True):
                                                st.markdown(f"**URL:** {res['url']}")
                                                st.markdown(f"**카테고리:** {res['category']} | **작성일:** {res['created_at']}")
                                                st.markdown("### 📝 요약 내용")
                                                st.write(res['summary'])
                                        if st.button("🔄 테이블 상태 새로고침"):
                                            st.rerun()
                                    if failed:
                                        st.error(f"⚠️ 다음 {len(failed)}건 처리에 실패했습니다: " + ", ".join(failed))
                    else:
                        st.info("👆 위 목록에서 요약할 뉴스를 선택(체크)해주세요.")

                    st.markdown("---")
                    
                    # 요약된 뉴스 상세보기
                    summarized_news = [n for n in display_list if n.get('is_summarized')]
                    if summarized_news:
                        selected_for_view = st.selectbox(
                            "📖 요약된 뉴스 상세보기 (기사를 선택하면 아래에 내용이 표시됩니다)",
                            options=summarized_news,
                            format_func=lambda x: f"✅ {x['title']} ({x['source_name']})",
                            key="view_summary_selectbox"
                        )
                        if selected_for_view:
                            st.markdown(f"### 🎯 요약 리포트: {selected_for_view['title']}")
                            st.info(selected_for_view.get('summary_content', "요약 내용을 불러오는 중..."))
                            st.caption(f"출처: {selected_for_view['source_name']} | URL: {selected_for_view['url']}")
                    else:
                        st.info("💡 아직 요약된 뉴스가 없습니다. 요약할 항목을 선택하고 버튼을 눌러주세요.")

                # 2. 종합 분석 리포트 (Expander 아래에 위치)
                selected_rows_for_action = pd.DataFrame() 
                if edited_df is not None:
                    if '선택' in edited_df.columns:
                        selected_rows_for_action = edited_df[edited_df['선택'] == True]
                
                if not selected_rows_for_action.empty:
                    selected_count = len(selected_rows_for_action)
                    if st.button(f"🧠 선택한 뉴스 ({selected_count}건) 종합 분석 리포트", type="primary", use_container_width=True, key="btn_comprehensive_analysis"):
                        if not st.session_state.get('api_key'):
                            st.error("❌ OpenAI API 키가 필요합니다.")
                        else:
                            if 'enhanced_summarizer' not in st.session_state:
                                from enhanced_news_summarizer import EnhancedNewsSummarizer
                                st.session_state.enhanced_summarizer = EnhancedNewsSummarizer(st.session_state.api_key)
                            summarizer = st.session_state.enhanced_summarizer
                            db = st.session_state.db
                            unsummarized_items = []
                            ready_items = []
                            for _, row in selected_rows_for_action.iterrows():
                                url = row['URL']
                                title = row['제목']
                                existing = db.get_news_by_url(url)
                                if existing and existing.get('summary'):
                                    ready_items.append({'title': title, 'summary': existing['summary']})
                                else:
                                    unsummarized_items.append({'title': title, 'url': url, 'category': row['카테고리'], 'source_name': row['뉴스 업체']})

                            if unsummarized_items:
                                st.info(f"⏳ {len(unsummarized_items)}건의 기사에 요약이 없어 요약을 먼저 생성합니다...")
                                summarize_progress = st.progress(0)
                                summarize_status = st.empty()
                                for i, item in enumerate(unsummarized_items):
                                    summarize_status.text(f"🪄 요약 생성 중 ({i+1}/{len(unsummarized_items)}): {item['title'][:20]}...")
                                    try:
                                        result = summarizer.summarize_news_detailed(item['url'], item['title'])
                                        if isinstance(result, dict):
                                            db.save_news_summary(title=item['title'], url=item['url'], category=item['category'], source_name=item['source_name'], summary=result['summary'])
                                            ready_items.append({'title': item['title'], 'summary': result['summary']})
                                        else:
                                            ready_items.append({'title': item['title'], 'summary': "(요약 실패)"})
                                    except Exception as e:
                                        ready_items.append({'title': item['title'], 'summary': f"(Error: {str(e)})"})
                                    summarize_progress.progress((i + 1) / len(unsummarized_items))
                                summarize_status.text("✅ 요약 완료!")

                            with st.spinner("🧐 종합 분석 중..."):
                                analysis_result = summarizer.analyze_multi_news(ready_items)
                                st.markdown("---")
                                st.markdown("## 🧐 뉴스 종합 분석 리포트")
                                st.markdown(analysis_result)
                                st.download_button(
                                    label="📥 분석 리포트 다운로드 (.md)",
                                    data=analysis_result,
                                    file_name=f"news_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                    mime="text/markdown",
                                    use_container_width=True
                                )
                                if unsummarized_items:
                                    st.button("🔄 테이블 상태 새로고침 (분석용)")
        
    with st.expander("🔧 스크래핑 문제 해결 가이드"):
        st.markdown("""
        **뉴스 스크래핑이 작동하지 않는 경우:**
        
        1. **네트워크 연결 확인**: 인터넷 연결이 안정적인지 확인하세요
        2. **뉴스 소스 등록**: 뉴스 소스 관리에서 신뢰할 수 있는 뉴스 사이트를 등록하세요
        3. **다른 카테고리 시도**: 일부 카테고리는 접근이 제한될 수 있습니다
        4. **샘플 데이터 사용**: 스크래핑이 실패해도 샘플 데이터로 기능을 테스트할 수 있습니다
        
        **지원하는 뉴스 사이트:**
        - 한국일보: https://www.hankookilbo.com/News/Politics
        - 연합뉴스: https://www.yna.co.kr/news?site=navi_latest_depth01
        - ZDNet: https://zdnet.co.kr/news/
        - 조선일보: https://www.chosun.com/politics/
        - 중앙일보: https://www.joongang.co.kr/politics
        """)



def show_sources_page():
    """언론사 설정 페이지"""
    st.header("📰 언론사 설정")
    
    db = st.session_state.db
    
    # 탭 생성 (단일 탭으로 변경)
    st.subheader("📝 새로운 언론사 등록")
        
    col1, col2 = st.columns(2)
    with col1:
        source_name = st.text_input("언론사명", placeholder="예: 한국일보, 조선일보, 중앙일보")
    
    with col2:
        categories = ["정치", "경제", "사회", "국제", "문화", "연예", "스포츠", "사람", "라이프", "오피니언"]
        category = st.selectbox("카테고리", categories)
    
    url = st.text_input("뉴스 페이지 URL", placeholder="https://example.com/news/category")
    
    if st.button("💾 언론사 등록", use_container_width=True):
        if source_name and category and url:
            success = db.add_news_source(source_name, category, url)
            if success:
                st.success(f"✅ {source_name}의 {category} 카테고리가 등록되었습니다!")
                st.rerun()
            else:
                st.error("❌ 언론사 등록에 실패했습니다.")
        else:
            st.warning("⚠️ 모든 필드를 입력해주세요.")
    
    st.markdown("---")
    
    # 등록된 언론사 목록
    st.subheader("📋 등록된 언론사 목록")
    
    # 카테고리별 필터
    all_categories = db.get_categories()
    if all_categories:
        col1, col2 = st.columns(2)
        with col1:
            selected_category_filter = st.selectbox("카테고리 필터", ["전체"] + all_categories)
        with col2:
            # 업체별 필터
            all_sources = db.get_news_sources()
            all_source_names = list(set([s['source_name'] for s in all_sources]))
            selected_source_filter = st.selectbox("언론사 필터", ["전체"] + all_source_names)
        
        if selected_category_filter == "전체":
            sources = db.get_news_sources()
        else:
            sources = db.get_news_sources(selected_category_filter)
        
        # 업체별 필터링
        if selected_source_filter != "전체":
            sources = [s for s in sources if s['source_name'] == selected_source_filter]
        
        if sources:
            # DataFrame으로 표시
            df_data = []
            for source in sources:
                df_data.append({
                    '언론사': source['source_name'],
                    '카테고리': source['category'],
                    'URL': source['url'],
                    '등록일': source['created_at'][:10]
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # 삭제 기능
            st.subheader("🗑️ 언론사 삭제")
            delete_options = [f"{s['source_name']} - {s['category']}" for s in sources]
            selected_delete = st.selectbox("삭제할 언론사를 선택하세요", delete_options)
            
            if st.button("🗑️ 선택한 언론사 삭제", type="secondary"):
                if selected_delete:
                    source_name, category = selected_delete.split(" - ")
                    success = db.delete_news_source(source_name, category)
                    if success:
                        st.success(f"✅ {source_name}의 {category} 카테고리가 삭제되었습니다!")
                        st.rerun()
                    else:
                        st.error("❌ 언론사 삭제에 실패했습니다.")
        else:
            st.info("📝 등록된 언론사가 없습니다.")
    else:
        st.info("📝 등록된 언론사가 없습니다.")
    



def main():
    """메인 애플리케이션"""
    # 세션 상태 초기화
    initialize_session_state()
    
    # 헤더 렌더링 (제거됨)
    # render_header()
    
    # 네비게이션 렌더링 (사이드바로 이동됨)
    # render_navigation()
    
    # 사이드바 렌더링 (뉴스 가져오기 버튼 로직 제거)
    selected_categories, selected_sources, _ = render_sidebar()
    
    # 사이드바 옵션 변경 감지 및 초기화
    if 'last_sidebar_checksum' not in st.session_state:
        st.session_state.last_sidebar_checksum = (selected_categories, selected_sources)
        
    current_checksum = (selected_categories, selected_sources)
    if st.session_state.last_sidebar_checksum != current_checksum:
        st.session_state.last_sidebar_checksum = current_checksum
        # 옵션이 바뀌면 뉴스 리스트 초기화? 아니면 유지? 
        # 사용자가 "가져오기"를 눌러야 리스트가 갱신되는 것이 명확함.
        # 다만 필터 상태는 초기화하는 것이 좋음.
        st.session_state.view_filter = None

    # 세션 상태에 뷰 필터 초기화
    if 'view_filter' not in st.session_state:
        st.session_state.view_filter = None
    
    # 카테고리 변경 시 초기화
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = selected_categories
    elif st.session_state.selected_category != selected_categories:
        st.session_state.selected_category = selected_categories
        # 뉴스 리스트 초기화는 하지 않음 (기존 리스트 유지하되 필터만 바뀜? 아니면 리스트도?)
        # 사용자 경험상 옵션 바꾸고 '가져오기' 안누르면 오해 소지.
        # 하지만 일단 유지.
    
    
    # 메인 컨텐츠
    # 메인 컨텐츠
    if st.session_state.current_page == 'news':
        show_news_page()
    elif st.session_state.current_page == 'sources':
        show_sources_page()

if __name__ == "__main__":
    main()
