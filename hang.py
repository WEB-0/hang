import streamlit as st
import openai

def request_chat_completion(
    prompt, 
    system_role="Your role is to be a competent teacher assistant.", 
    model="gpt-4o", 
    # gpt-3.5-turbo
    stream=False
):
    messages=[
        {"role": "system", "content": system_role},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    stream=stream
    )
    return response

def print_streaming_response(response):
    message = ""
    placeholder = st.empty()
    for chunk in response:
        delta = chunk.choices[0]["delta"]
        if "content" in delta:
            message += delta["content"]
            placeholder.markdown(message + "✒️")
        else:
            break
    placeholder.markdown(message)
    return message

def print_streaming_response_console(response):
    message = ""
    for chunk in response:
        delta = chunk.choices[0]["delta"]
        if "content" in delta:
            message += delta["content"]
            print(delta["content"], end="")
        else:
            break
    return message

st.set_page_config(
    page_title="행발 도우미✍️",
    page_icon="✍️"
)

st.title("행발 도우미🏫")
st.subheader("행발 초안 작성기-제작 김가현!👊")
auto_complete = st.toggle("👈누르면 예시가 나옵니다.")

example = {
    "school": "성격",
    "department": "학업",
    "max_length": 700,
    "question": "학교 생활",
    "answer": "어린 시절부터 요리 좋아했고 음식을 나누는 것에 기쁨을 느낌."
    # "answer": "저는 음식을 통해 사람들에게 기쁨과 만족을 주는 것에 열정을 느끼고 있습니다. 어린 시절부터 가정에서 요리를 통해 사람들을 행복하게 해본 경험이 있고, 음식을 창조하는 과정과 예술적 표현에 흥미를 느끼고 있습니다. 조리학 공부를 통해 음식을 예술로써 표현하고 사회적으로 소통과 이해를 촉진하는 방법을 배우고 싶습니다. 최종적으로, 레스토랑 쉐프로서 사람들에게 즐거움을 주는 직업을 향해 나아가고 싶습니다."
}

prompt_template="""
학생의 성격 및 태도, 책임감 및 자발적인 행동, 학업에 대한 태도 및 탐구 정신, 학교생활에서의 역할 및 참여도를 포함한 종합의견을 작성해주세요. 각 항목은 다음 단어들을 사용해 작성해주세요. 문장의 어미는 명사형으로 적어주세요.


---
성격:{school}
학업:{department}
학교 생활: {question}
---
""".strip()

with st.form("form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        school = st.text_input(
            "성격",
            value=example["school"] if auto_complete else "",
            placeholder=example["school"])
    with col2:
        department = st.text_input(
            "학업",
            value=example["department"] if auto_complete else "",
            placeholder=example["department"])
    with col3:
        max_length= st.number_input(
            "최대 길이",
            min_value=100,
            max_value=2000,
            step=100,
            value=700
    )
    question = st.text_area(
        "학교 생활",
        value=example["question"] if auto_complete else "",
            placeholder=example["question"])
    submit = st.form_submit_button("제출하기")
if submit:
    if not school:
        st.error("지원하는 학교를 입력해주세요.")
    elif not department:
        st.error("지원하는 과를 입력해주세요")
    elif not question:
        st.error("예상 면접 문항을 입력해주세요.")
    else:
        prompt = prompt_template.format(
            school = school,
            department = department,
            max_length = max_length // 6,
            question = question,
        )
        system_role = "Your role is to be a competent teacher assistant."
        response = request_chat_completion(
            prompt=prompt,
            system_role=system_role,
            stream=True
        )
        message = print_streaming_response(response)
        st.markdown(f"**공백 포함 글자 수: {len(message)}**")
