import textwrap
import google.generativeai as genai
import streamlit as st
import toml
import pathlib

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
api_key = secrets.get("AIzaSyBSPxMrQPTR5PHA2GKN6rdKSQR3AjbmIXI")

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# few-shot 프롬프트 구성 함수 수정
def try_generate_content(api_key, prompt):
    # API 키를 설정
    genai.configure(api_key=api_key)
   
    # 설정된 모델 변경
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config={
                                      "temperature": 0.9,
                                      "top_p": 1,
                                      "top_k": 1,
                                      "max_output_tokens": 2048,
                                  },
                                  safety_settings=[
                                      {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  ])
    try:
        # 콘텐츠 생성 시도
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 예외 발생시 None 반환
        print(f"API 호출 실패: {e}")
        return None

st.title("체세포 분열 단계 퀴즈 🧬")

st.write("체세포 분열의 단계를 올바른 순서대로 나열해 보세요.")

# 단계 설명
steps = {
    "전기": "핵막이 사라지고 염색체가 응축되어 나타납니다.",
    "중기": "염색체가 세포 중앙에 배열됩니다.",
    "후기": "염색 분체가 나뉘어 양극으로 이동합니다.",
    "말기": "응축되어 있던 염색체가 풀리고 핵막이 생깁니다.",
    "세포질 분열": "세포질이 분열되어 두 개의 딸세포가 만들어집니다."
}

# 단계 순서
correct_order = ["전기", "중기", "후기", "말기", "세포질 분열"]

# 단계 설명을 표시
st.write("체세포 분열의 각 단계에 대한 설명입니다:")
for step, description in steps.items():
    st.markdown(f"### {step}")
    st.markdown(to_markdown(description))

st.write("단계를 올바른 순서로 나열해 보세요.")

# 사용자 입력
user_order = [st.selectbox(f"단계 {i+1}", list(steps.keys()), key=i) for i in range(5)]

if st.button("제출"):
    if user_order == correct_order:
        st.success("정답입니다! 체세포 분열의 단계를 올바르게 나열했습니다.")
    else:
        st.error("틀렸습니다. 다시 시도해 보세요.")
