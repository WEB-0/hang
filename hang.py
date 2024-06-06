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

st.set_page_config(
    page_title="행발 도우미✍️",
    page_icon="✍️"
)

st.title("행발 도우미🏫")
st.subheader("행발 초안 작성기-제작 김가현 공유 금지!👊")

auto_complete = st.checkbox("👈누르면 예시가 나옵니다.")

example = {
    "attitude": "문화적 감수성이 풍부하고 차분한",
    "study": "스스로 학습 계획을 세우고 적극적으로 실행",
    "question": "효과적인 시간 관리를 통해 학업과 여가 시간을 잘 조율",
    "friendship": "다양한 친구들과 잘 어울리며, 원만한 대인 관계",
    "career": "다양한 직업 탐색 활동에 참여하며 자신의 진로를 적극적으로 탐구"
}

prompt_template = """
학생의 성격 및 태도, 책임감 및 자발적인 행동, 학업에 대한 태도 및 탐구 정신, 학교생활에서의 역할 및 참여도, 교우관계, 진로 및 진학을 포함한 종합의견을 작성해야합니다.

유저가 적은 내용을 바탕으로 종합의견을 언어 이음말 없이 자연스럽고 풍부하게 답변해주세요. 
반드시 모든 문장의 어미은 명사형으로 작성해야합니다.(~학생임, ~노력함)
예시 형식을 참고해서 작성
[예시 1:사교성이 좋고 성격이 활달하여 인간관계 형성 능력이 뛰어나며 어려운 친구를 잘 도와주고 맡은 일에 , 책임감이 강한 학생임 자신만의 학습 계획을 수립하고 꾸준히 실천하는 학습 습관을 지니고 있어 앞으. 로 높은 성취 가능성이 기대됨 몸이 민첩하고 순발력이 좋아 체육활동에서 두각을 나타내었으며 학교. , 스포츠클럽 중 줄넘기부에서 활동하며 남다른 승부욕으로 높은 집중도를 보임 단체줄넘기의 기록을 갱. 신하는 과정에서 잘하지 못하는 학생을 소외시키지 않고 독려하여 다함께 성취감을 갖도록 하는데 중간자적 역할을 하여 학급의 화합에 기여함.
예시 2:상대방을 존중하면서도 재치 있는 말과 행동으로 주변을 즐겁게 하여 친구들의 호감을 얻고 있어 교우관계가 좋은 학생임 학급 자치회의에서 학급 문화의 개선 방향에 대해 토의하는 과정에서 자신과 다르. 다고 하여 멀리하는 것이 아니라 함께 살아가는 방법에 대해 의견을 제시하여 친구들로부터 신뢰를 얻음 축구에도 관심이 많아 방과후학교 스포츠클럽활동에 참여하여 각종 기본 기술 및 경기 규칙을 습득. 하고 공격수로서 탁월한 경기 운영 능력을 지녀 각종 체육활동에서 실력을 발휘함 경기 과정에서 팀이 , . 지고 있을 때도 좌절하지 않고 최선을 다할 수 있도록 구호를 외쳐 팀원들을 격려하여 스포츠맨 정신을
실천함 학업 성적이 전반적으로 낮은 편이었으나 체육교사라는 꿈을 갖게 되면서부터 학업에서도 열정. , 적 투지를 발휘하여 성적이 꾸준히 향상되고 있어서 앞으로의 성장이 기대되는 학생임.
]


---
성격 및 태도: {attitude}
학업 및 학습태도: {study}
학교 생활 및 생활습관: {question}
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
            "학업 및 학습태도",
            value=example["study"] if auto_complete else "",
            placeholder=example["study"])
    question = st.text_area(
        "학교 생활 및 생활습관",
        value=example["question"] if auto_complete else "",
        placeholder=example["question"])
    
    friendship = st.text_area(
            "교우관계",
            value=example["friendship"] if auto_complete else "",
            placeholder=example["friendship"])

    career = st.text_area(
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
    elif not friendship:
        st.error("학생의 교우관계를 입력해주세요.")
    elif not career:
        st.error("학생의 진로 및 진학을 입력해주세요.")
    else:
        prompt = prompt_template.format(
            attitude=attitude,
            study=study,
            question=question,
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
