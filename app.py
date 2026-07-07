import streamlit as st
import google.generativeai as genai

# 웹페이지 기본 설정
st.set_page_config(page_title="금융상품 1분 비교표 생성기", page_icon="💰", layout="wide")

st.title("💰 금융상품 1분 비교표 생성기")
st.write("비교하고 싶은 금융상품 정보나 뉴스 기사를 넣으면 AI가 한눈에 보기 쉽게 표로 정리해 드립니다.")

# Streamlit Cloud의 Secrets에서 API 키를 안전하게 불러옵니다.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"비밀키 설정 에러: {e}")

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
                    # 버전을 타지 않는 가장 안정적인 모델 호출 방식입니다.
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    
                    prompt = f"다음 금융상품 정보를 바탕으로 소비자가 보기 편하게 마크다운 표로 비교 요약해줘:\n\n{user_input}"
                    
                    response = model.generate_content(prompt)
                    
                    # 결과 출력
                    if response.text:
                        st.markdown(response.text)
                        st.success("비교표 생성이 완료되었습니다!")
                    else:
                        st.error("AI가 답변을 생성하지 못했습니다. 다시 시도해 주세요.")
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다. (에러 내용: {e})")
    else:
        st.info("왼쪽에 상품 정보를 입력하고 버튼을 누르면 여기에 비교표가 나타납니다.")
