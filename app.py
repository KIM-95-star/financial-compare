import streamlit as st
import google.generativeai as genai

# Streamlit Cloud의 Secrets에서 API 키를 안전하게 불러옵니다.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Secrets에 'GEMINI_API_KEY'가 설정되지 않았거나 올바르지 않습니다.")

# 웹페이지 기본 설정
st.set_page_config(page_title="금융상품 1분 비교표 생성기", page_icon="💰", layout="wide")

st.title("💰 금융상품 1분 비교표 생성기")
st.write("비교하고 싶은 금융상품 정보나 뉴스 기사를 넣으면 AI가 한눈에 보기 쉽게 표로 정리해 드립니다.")

# 레이아웃 나누기 (왼쪽: 입력창, 오른쪽: 결과창)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 금융상품 정보 입력")
    user_input = st.text_area(
        "비교할 금융상품들의 상세 설명, 약관, 혹은 관련 뉴스 기사를 입력해 주세요.",
        placeholder="예시: A은행 정기예금은 금리 연 4.0%에 우대조건은~ B저축은행 적금은 금리 연 5.5%인데~",
        height=400
    )
    
    generate_btn = st.button("📊 1분 비교표 생성하기", type="primary")

with col2:
    st.subheader("✨ AI 분석 및 비교표 결과")
    
    if generate_btn:
        if not user_input.strip():
            st.warning("비교할 상품 내용을 입력해 주세요!")
        else:
            with st.spinner("AI가 금융상품을 꼼꼼하게 분석 중입니다... 잠시만 기다려주세요."):
                try:
                    # [수정] 최신 google-generativeai 라이브러리의 올바른 호출 방식입니다.
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    
                    # [수정] 예적금뿐만 아니라 고객님이 입력하신 '펀드' 상품도 완벽히 비교하도록 항목을 정교화했습니다.
                    prompt = f"""
                    당신은 전문 금융 자산관리사(FP)입니다. 
                    다음 제공된 금융상품 정보를 바탕으로 소비자가 한눈에 비교할 수 있도록 깔끔한 마크다운(Markdown) 표로 요약해 주세요.
                    
                    [포함해야 할 항목]
                    1. 상품명 (펀드명/금융상품명)
                    2. 운용사 및 판매채널
                    3. 펀드 유형 및 설정일 / 규모
                    4. 보수율 및 수수료 (총보수, 판매수수료, 환매수수료 등 핵심 비용 비교)
                    5. 매입/환매 정보 (출금 가능일 등 안내)
                    6. 과세 종류 및 투자 유형
                    7. 핵심 장단점 및 한 줄 총평 (어떤 투자자에게 적합한가?)

                    [주의사항]
                    - 정보가 부족한 부분은 '정보 없음'으로 표기하되, 절대 허위 정보를 지어내지 마세요.
                    - 가독성이 좋게 표 형식과 이모지를 적절히 활용해 주세요.

                    [대상 정보]
                    {user_input}
                    """
                    
                    response = model.generate_content(prompt)
                    
                    # 결과 출력
                    st.markdown(response.text)
                    st.success("비교표 생성이 완료되었습니다!")
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다. 스트림릿 비밀메뉴(Secrets)의 API 키를 확인해 주세요. (에러 내용: {e})")
    else:
        st.info("왼쪽에 상품 정보를 입력하고 버튼을 누르면 여기에 비교표가 나타납니다.")
