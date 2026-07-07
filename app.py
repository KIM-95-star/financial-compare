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
    
    # [수정] 아래 if-else 문의 들여쓰기 라인을 col2 안으로 올바르게 정렬했습니다.
    if generate_btn:
        if not user_input.strip():
            st.warning("비교할 상품 내용을 입력해 주세요!")
        else:
            with st.spinner("AI가 금융상품을 꼼꼼하게 분석 중입니다... 잠시만 기다려주세요."):
                try:
                    # 최신 지원 모델 설정
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    
                    prompt = f"""
                    당신은 전문 금융 자산관리사(FP)입니다. 
                    다음 제공된 금융상품 정보를 바탕으로 소비자가 한눈에 비교할 수 있도록 깔끔한 마크다운(Markdown) 표로 요약해 주세요.
                    
                    [포함해야 할 항목]
                    1. 상품명 및 제조사(은행/증권 등)
                    2. 기본 금리 및 최고 금리 (우대 금리 조건 포함)
                    3. 가입 대상 및 가입 기간/금액 제한
                    4. 주요 특징 및 장점
                    5. 주의해야 할 단점이나 위험요소
                    6. 한 줄 총평 (어떤 사람에게 유리한가?)

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
                    st.error(f"오류가 발생했습니다. API 키나 입력을 확인해 주세요. (에러 내용: {e})")
    else:
        st.info("왼쪽에 상품 정보를 입력하고 버튼을 누르면 여기에 비교표가 나타납니다.")
