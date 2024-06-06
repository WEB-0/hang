import streamlit as st
import openai
import pandas as pd



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
st.subheader("행발 초안 작성기-제작 김가현 공유 금지!👊")

st.write("행발 키워드 추천")
st.write(pd.DataFrame({
    '성격 및 태도': [
        '친절한', '성실한', '적극적인', '밝은', '신중한', '침착한', '책임감 있는', '활기찬', '창의적인', '결단력 있는',
        '유쾌한', '온화한', '관대한', '호기심 많은', '진취적인', '열정적인', '정직한', '신뢰할 수 있는', '외향적인', '인내심 있는',
        '협력적인', '존경심 있는', '학구열이 높은', '주도적인', '규율을 잘 지키는', '긍정적인', '배려심 있는', '끈기 있는', '성취지향적인', '열정적인'
    ],
    'second column': [10, 20, 30, 40]
}))


auto_complete = st.toggle("👈누르면 예시가 나옵니다.")

example = {
    "attitude": "문화적 감수성이 풍부하고 차분한",
    "study": "학업",
    "question": "학교 생활",
}


prompt_template="""
학생의 성격 및 태도, 책임감 및 자발적인 행동, 학업에 대한 태도 및 탐구 정신, 학교생활에서의 역할 및 참여도를 포함한 종합의견을 작성해야합니다.

유저가 적은 내용을 바탕으로 문장의 어미는 명사형으로 자연스러운 답변을 작성해주세요.

---
성격 및 태도:{attitude}
학업:{study}
학교 생활: {question}
---
""".strip()

with st.form("form"):
    col1, col2 = st.columns(2)
    with col1:
        attitude = st.text_input(
            "성격 및 태도",
            value=example["attitude"] if auto_complete else "",
            placeholder=example["attitude"])
    with col2:
        study = st.text_input(
            "학업",
            value=example["study"] if auto_complete else "",
            placeholder=example["study"])
    question = st.text_area(
        "학교 생활",
        value=example["question"] if auto_complete else "",
            placeholder=example["question"])
    submit = st.form_submit_button("작성하기")
if submit:
    if not attitude:
        st.error("학생의 성격 및 태도를 입력해주세요.")
    elif not study:
        st.error("학생의 학업과 관련된 부분을 입력해주세요")
    elif not question:
        st.error("학생의 학교 생활을 입력해주세요.")
    else:
        prompt = prompt_template.format(
            attitude = attitude,
            study = study,
            question = question
        )
        system_role = "Your role is to be a competent teacher assistant."
        response = request_chat_completion(
            prompt=prompt,
            system_role=system_role,
            stream=True
        )
        message = print_streaming_response(response)
        st.markdown(f"**공백 포함 글자 수: {len(message)}**")



