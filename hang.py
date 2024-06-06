import streamlit as st
import openai

def request_chat_completion(
    prompt, 
    system_role="Your role is to be a competent teacher assistant.", 
    model="gpt-4o", 
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

auto_complete = st.toggle("👈누르면 예시가 나옵니다.")

example = {
    "attitude": "문화적 감수성이 풍부하고 차분한",
    "study": "어려운 과제에도 포기하지 않고 끝까지 최선을 다해 노력함",
    "question": "학교 규칙을 준수하며 모범적인 학생으로 인정",
    "habit": "효과적인 시간 관리를 통해 학업과 여가 시간을 잘 조율",
    "friendship": "다양한 친구들과 잘 어울리며, 원만한 대인 관계를 유지",
    "career": "다양한 직업 탐색 활동에 참여하며 자신의 진로를 적극적으로 탐구"
}

prompt_template = """
학생의 성격 및 태도, 책임감 및 자발적인 행동, 학업에 대한 태도 및 탐구 정신, 학교생활에서의 역할 및 참여도, 생활습관, 교우관계, 진로 및 진학을 포함한 종합의견을 작성해야합니다.

유저가 적은 내용을 바탕으로 문장의 어미는 명사형으로 자연스러운 답변을 작성해주세요.

---
성격 및 태도: {attitude}
학업 및 학습태도: {study}
학교 생활: {question}
생활습관: {habit}
교우관계: {friendship}
진로 및 진학: {career}
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
            "학업 및 학습 태도",
            value=example["study"] if auto_complete else "",
            placeholder=example["study"])
    question = st.text_area(
        "학교 생활",
        value=example["question"] if auto_complete else "",
        placeholder=example["question"])
    col3, col4, col5 = st.columns(3)
    with col3:
        habit = st.text_input(
            "생활습관",
            value=example["habit"] if auto_complete else "",
            placeholder=example["habit"])
    with col4:
        friendship = st.text_input(
            "교우관계",
            value=example["friendship"] if auto_complete else "",
            placeholder=example["friendship"])
    with col5:
        career = st.text_input(
            "진로 및 진학",
            value=example["career"] if auto_complete else "",
            placeholder=example["career"])
    submit = st.form_submit_button("작성하기")

if submit:
    if not attitude:
        st.error("학생의 성격 및 태도를 입력해주세요.")
    elif not study:
        st.error("학생의 학업과 관련된 부분을 입력해주세요")
    elif not question:
        st.error("학생의 학교 생활을 입력해주세요.")
    elif not habit:
        st.error("학생의 생활습관을 입력해주세요.")
    elif not friendship:
        st.error("학생의 교우관계를 입력해주세요.")
    elif not career:
        st.error("학생의 진로 및 진학을 입력해주세요.")
    else:
        prompt = prompt_template.format(
            attitude=attitude,
            study=study,
            question=question,
            habit=habit,
            friendship=friendship,
            career=career
        )
        system_role = "Your role is to be a competent teacher assistant."
        response = request_chat_completion(
            prompt=prompt,
            system_role=system_role,
            stream=True
        )
        message = print_streaming_response(response)
        st.markdown(f"**공백 포함 글자 수: {len(message)}**")

