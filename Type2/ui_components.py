"""
UI 컴포넌트 관련 기능
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import openai

def test_openai_api(api_key):
    """OpenAI API 키 테스트 - 참고프로젝트 apitest.py 기반"""
    if not api_key or not api_key.strip():
        return {"success": False, "error": "API 키가 입력되지 않았습니다."}
    
    try:
        # 참고프로젝트 apitest.py와 동일한 방식으로 클라이언트 초기화
        from openai import OpenAI
        client = OpenAI(api_key=api_key.strip())
        
        # 간단한 테스트 요청 (참고프로젝트와 유사한 구조)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다."},
                {"role": "user", "content": "Hello"}
            ],
            max_tokens=10,
            temperature=0.7
        )
        
        # 응답 확인
        if response and response.choices and len(response.choices) > 0:
            return {"success": True, "error": None}
        else:
            return {"success": False, "error": "API 응답이 비어있습니다."}
            
    except openai.AuthenticationError as e:
        return {"success": False, "error": "API 키가 유효하지 않습니다. 키를 다시 확인해주세요."}
    except openai.RateLimitError as e:
        return {"success": False, "error": "API 사용량 한도를 초과했습니다. 잠시 후 다시 시도해주세요."}
    except openai.APIConnectionError as e:
        return {"success": False, "error": "API 연결에 실패했습니다. 네트워크 연결을 확인해주세요."}
    except openai.APIError as e:
        return {"success": False, "error": f"OpenAI API 오류: {str(e)}"}
    except Exception as e:
        error_msg = str(e)
        if "proxies" in error_msg:
            return {"success": False, "error": "OpenAI 클라이언트 초기화 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}
        return {"success": False, "error": f"API 테스트 실패: {error_msg}"}

def render_header():
    """헤더 렌더링 - PPT 이미지 스타일 적용"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #60a5fa 100%); border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);">
        <h1 style="color: white; margin: 0; font-size: 2.8rem; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
            📰 AI 뉴스 어시스턴트
        </h1>
        <p style="color: #e0f2fe; margin: 1rem 0 0 0; font-size: 1.3rem; font-weight: 500;">
            STREAMLIT, PYTHON, LANGCHAIN, GPT API 활용
        </p>
        <div style="margin-top: 1.5rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; color: white; font-size: 0.9rem; margin: 0 0.5rem;">
                🤖 AI 뉴스 요약
            </span>
        </div>
        <p style="color: #cbd5e1; margin: 1rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">📅 {}</p>
    </div>
    """.format(datetime.now().strftime("%Y년 %m월 %d일 %H:%M")), unsafe_allow_html=True)

def render_navigation():
    """네비게이션 버튼 렌더링 - PPT 스타일"""
    st.markdown("""
    <style>
    .nav-button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("📰 뉴스 요약", key="btn_news", use_container_width=True, type="primary"):
            st.session_state.current_page = 'news'
            st.rerun()
    with col2:
        if st.button("📰 언론사 설정", key="btn_sources", use_container_width=True, type="primary"):
            st.session_state.current_page = 'sources'
            st.rerun()

def render_sidebar():
    """사이드바 렌더링 - PPT 스타일 적용"""
    # 초기값 설정 (NameError 방지)
    final_sources = st.session_state.get('source_multiselect_key', ["전체"])
    final_categories = st.session_state.get('category_multiselect_key', ["전체"])
    
    with st.sidebar:
        # PPT 스타일 CSS 적용
        st.markdown("""
        <style>
        .sidebar-header {
            color: white;
            padding: 0.5rem 0;
            margin-bottom: 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 1.1rem;
        }
        .sidebar-section {
            padding: 0.5rem 0;
            margin-bottom: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 0. 네비게이션 (최상단)
        if st.button("🏠 홈 (뉴스 요약)", use_container_width=True, type="primary"):
            st.session_state.current_page = 'news'
            st.rerun()
            
        st.markdown("---")
        
        # 1. 설정
        st.markdown('<div class="sidebar-header"><h3>⚙️ 설정</h3></div>', unsafe_allow_html=True)
        
        # GPT API 키 입력
        api_key = st.text_input("🔑 OpenAI API 키", type="password", help="OpenAI API 키를 입력하세요")
        if api_key:
            st.session_state.api_key = api_key
        
        # API 키 테스트 버튼
        if st.button("🔍 API 키 테스트", use_container_width=True):
            with st.spinner("API 키를 테스트하는 중..."):
                test_result = test_openai_api(api_key)
                if test_result["success"]:
                    st.success("✅ API 키 등록 성공!")
                    # 세션에 API 키 저장
                    st.session_state.api_key = api_key
                    st.session_state.api_key_valid = True
                    st.session_state.api_key_tested = True
                    # 모든 AI 관련 객체들을 새로 초기화
                    if 'summarizer' in st.session_state:
                        del st.session_state.summarizer
                    if 'enhanced_summarizer' in st.session_state:
                        del st.session_state.enhanced_summarizer
                    if 'content_generator' in st.session_state:
                        del st.session_state.content_generator
                    st.rerun()
                else:
                    st.error(f"❌ API 키 등록 실패: {test_result['error']}")
                    st.session_state.api_key_valid = False
                    st.session_state.api_key_tested = False
        
        # API 키 상태 표시
        if st.session_state.get('api_key_valid'):
            st.success("✅ API 키가 유효합니다 - 뉴스 요약을 사용할 수 있습니다!")
        elif st.session_state.get('api_key_tested') == False:
            st.error("❌ API 키 테스트에 실패했습니다")
        elif st.session_state.get('api_key'):
            st.warning("⚠️ API 키를 테스트해주세요")
        else:
            st.info("ℹ️ API 키를 입력하고 테스트해주세요")
        
        # 뉴스 업체 변경 콜백
        def on_source_change():
            current = st.session_state.source_multiselect_key
            prev = st.session_state.get('prev_sources', ["전체"])
            final = current
            if "전체" in current and len(current) > 1:
                if "전체" not in prev: final = ["전체"]
                else: final = [s for s in current if s != "전체"]
            elif not current: final = ["전체"]
            
            st.session_state.source_multiselect_key = final
            st.session_state.prev_sources = final
            st.session_state.source_select = final

        # 2. 뉴스 업체 선택 (2번째 위치)
        st.markdown('<div class="sidebar-header"><h3>📰 뉴스 업체 선택</h3></div>', unsafe_allow_html=True)
        from database import NewsDatabase
        db = NewsDatabase()
        
        all_sources = db.get_news_sources()
        if all_sources:
            source_options = ["전체"] + sorted(list(set([s['source_name'] for s in all_sources])))
            if 'prev_sources' not in st.session_state:
                st.session_state.prev_sources = ["전체"]
            
            st.multiselect(
                "뉴스 업체 선택", 
                source_options, 
                default=st.session_state.prev_sources,
                key="source_multiselect_key",
                on_change=on_source_change
            )
            # app.py와 동기화
            st.session_state.source_select = st.session_state.get('source_multiselect_key', ["전체"])
        else:
            st.session_state.source_select = ["전체"]
            st.info("📝 등록된 뉴스 소스가 없습니다.")
        
        # 카테고리 변경 콜백
        def on_category_change():
            current = st.session_state.category_multiselect_key
            prev = st.session_state.get('prev_categories', ["전체"])
            final = current
            if "전체" in current and len(current) > 1:
                if "전체" not in prev: final = ["전체"]
                else: final = [s for s in current if s != "전체"]
            elif not current: final = ["전체"]
            
            st.session_state.category_multiselect_key = final
            st.session_state.prev_categories = final
            st.session_state.selected_category = final

        # 3. 뉴스 주제 선택 (3번째 위치)
        st.header("📰 뉴스 주제 선택")
        categories = {"정치": "🏛️", "경제": "💼", "사회": "👥", "국제": "🌍", "문화": "🎭", "연예": "🎬", "스포츠": "⚽", "사람": "👤", "라이프": "🏠", "오피니언": "💭"}
        category_options = ["전체"] + list(categories.keys())
        
        if 'prev_categories' not in st.session_state:
            st.session_state.prev_categories = ["전체"]
            
        st.multiselect(
            "카테고리 선택", 
            category_options, 
            default=st.session_state.prev_categories,
            key="category_multiselect_key",
            on_change=on_category_change
        )
        # 최종 선택값 가져오기 (app.py와 동기화)
        final_sources = st.session_state.get('source_multiselect_key', ["전체"])
        final_categories = st.session_state.get('category_multiselect_key', ["전체"])
        
        st.session_state.source_select = final_sources
        st.session_state.selected_category = final_categories
        
        st.markdown("---")
        
        # 언론사 설정 이동 버튼
        if st.button("📰 언론사 설정", use_container_width=True, key="btn_sources_sidebar"):
            st.session_state.current_page = 'sources'
            st.rerun()
        
        return final_categories, final_sources, False

def render_news_table(news_list, category, default_select=False):
    """뉴스 테이블 렌더링 - PPT 스타일 적용"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);">
        <h3 style="margin: 0; font-size: 1.5rem;">📰 {category} 카테고리 주요 뉴스</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 데이터베이스 연결
    from database import NewsDatabase
    db = NewsDatabase()
    
    # DataFrame 생성
    df_data = []
    for i, news in enumerate(news_list, 1):
        # 요약 상태 아이콘 설정
        summary_status = "✅ 요약완료" if news.get('is_summarized') else "⏳ 미요약"
        
        df_data.append({
            '상태': summary_status,
            '선택': default_select,
            '뉴스 업체': news.get('source_name', '기본'),
            '카테고리': news['category'],
            '제목': news['title'],
            'URL': news['url']
        })
    
    df = pd.DataFrame(df_data)
    
    # 컬럼 순서 재배치 (상태 | 선택 | 뉴스업체 | 카테고리 | 제목 | 기사링크)
    cols = ['상태', '선택', '뉴스 업체', '카테고리', '제목', 'URL']
    df = df[cols]
    
    # PPT 스타일 (배경색 등)은 data_editor에서는 제한적일 수 있음.
    # 하지만 일단 기능이 우선이므로 data_editor 사용.
    
    edited_df = st.data_editor(
        df,
        column_config={
            "선택": st.column_config.CheckboxColumn(
                "선택",
                help="요약할 뉴스를 선택하세요",
                default=False,
            ),
            "상태": st.column_config.TextColumn(
                "상태",
                width="small",
                help="기존에 요약된 이력이 있는지 표시합니다"
            ),
            "URL": st.column_config.LinkColumn(
                "기사 링크",
                help="클릭하여 뉴스 기사로 이동",
                validate="^https://.*",
            ),
            "제목": st.column_config.TextColumn(
                "제목",
                width="large"
            ),
            "뉴스 업체": st.column_config.TextColumn(
                "뉴스 업체",
                width="medium"
            ),
            "카테고리": st.column_config.TextColumn(
                "카테고리",
                width="small"
            )
        },
        disabled=["상태", "뉴스 업체", "카테고리", "제목", "URL"], # 선택 컬럼만 수정 가능
        hide_index=True,
        use_container_width=True,
        key="news_editor"
    )
    
    return edited_df



def render_summary_result(summary, category):
    """요약 결과 렌더링"""
    st.markdown(f"""
    <div class="summary-box">
        <h3>🎯 {category} 카테고리 오늘의 주요 뉴스</h3>
        <p style="font-size: 1.1rem; line-height: 1.6;">{summary}</p>
    </div>
    """, unsafe_allow_html=True)

def render_detailed_news_summary(summary):
    """상세 뉴스 요약 결과 렌더링"""
    st.markdown("### 📄 뉴스 상세 요약")
    st.markdown(summary)


def render_db_news_selection():
    """DB에 저장된 뉴스 리스트 선택 UI"""
    st.subheader("📚 저장된 뉴스에서 선택")
    
    # 데이터베이스에서 모든 뉴스 요약본 조회
    from database import NewsDatabase
    db = NewsDatabase()
    all_news = db.get_all_news_summaries()
    
    if not all_news:
        st.warning("⚠️ 저장된 뉴스가 없습니다. 먼저 뉴스를 요약해주세요.")
        return None, None
    
    # 카테고리 필터
    categories = list(set([news['category'] for news in all_news]))
    selected_category = st.selectbox("카테고리 필터", ["전체"] + categories)
    
    # 카테고리별 필터링
    if selected_category != "전체":
        filtered_news = [news for news in all_news if news['category'] == selected_category]
    else:
        filtered_news = all_news
    
    if not filtered_news:
        st.warning(f"⚠️ '{selected_category}' 카테고리에 저장된 뉴스가 없습니다.")
        return None, None
    
    # 뉴스 선택 (기본값: 기사 선택해 주세요)
    news_options = {"기사 선택해 주세요": None}
    for news in filtered_news:
        key = f"{news['title'][:50]}... ({news['source_name']}) - {news['created_at'][:10]}"
        news_options[key] = news
    
    selected_key = st.selectbox("저장된 뉴스를 선택하세요", list(news_options.keys()), index=0)
    
    if selected_key and news_options[selected_key]:
        selected_news_data = news_options[selected_key]
        selected_summary = selected_news_data['summary']
        
        st.info(f"**선택된 뉴스**: {selected_news_data['title']}")
        st.info(f"**뉴스 링크**: {selected_news_data['url']}")
        st.info(f"**카테고리**: {selected_news_data['category']}")
        st.info(f"**뉴스 소스**: {selected_news_data['source_name']}")
        st.info(f"**요약 생성일**: {selected_news_data['created_at']}")
        
        return selected_news_data, selected_summary
    
    return None, None

def render_grouped_agency_buttons(sources, news_counts=None):
    """뉴스 언론사별 그룹화 버튼 렌더링 (가로: 언론사, 세로: 카테고리)
    Args:
        sources: 소스 리스트
        news_counts: {(source_name, category): count} 형태의 딕셔너리. None이면 카운트 표시 안함.
    """
    st.subheader("📰 뉴스 언론사 및 카테고리 선택")
    
    if not sources:
        st.info("등록된 언론사가 없습니다.")
        return None
    
    # 언론사별로 그룹화
    agency_dict = {}
    for source in sources:
        name = source['source_name']
        if name not in agency_dict:
            agency_dict[name] = []
        agency_dict[name].append(source)
    
    agency_names = list(agency_dict.keys())
    
    if not agency_names:
        return None

    # 4열로 배치 (필요에 따라 조정 가능)
    cols = st.columns(4)
    selected_source = None
    
    for i, agency in enumerate(agency_names):
        col_idx = i % 4
        with cols[col_idx]:
            # 언론사 이름 (헤더) 및 총 뉴스 건수 계산
            agency_header = f"#### {agency}"
            if news_counts is not None:
                agency_total = 0
                for source in agency_dict[agency]:
                    agency_total += news_counts.get((agency, source['category']), 0)
                agency_header += f" ({agency_total})"
            
            st.markdown(agency_header)
            
            # 해당 언론사의 카테고리 버튼들 (세로 배치)
            for source in agency_dict[agency]:
                category = source['category']
                label = category
                is_disabled = False
                
                # 뉴스 카운트 정보가 있으면 라벨 수정 및 비활성화 여부 결정
                if news_counts is not None:
                    count = news_counts.get((agency, category), 0)
                    label = f"{category} ({count})"
                    if count == 0:
                        is_disabled = True
                        
                if st.button(
                    label, 
                    key=f"btn_{agency}_{category}", 
                    use_container_width=True,
                    disabled=is_disabled
                ):
                    selected_source = source
    
    return selected_source
