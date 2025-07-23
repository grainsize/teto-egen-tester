import streamlit as st
import random
import plotly.graph_objects as go

# 질문 목록 (카테고리는 계산에만 사용되고 사용자에게는 보이지 않음)
questions = [
    ("나는 감정을 드러내기보다 속으로 처리하는 편이다.", "teto"),
    ("논쟁에서는 상대를 이기고 싶다는 생각이 든다.", "teto"),
    ("일을 할 때 누가 더 잘하나 경쟁심이 생긴다.", "teto"),
    ("나는 위로보다는 해결책을 주는 쪽이다.", "teto"),
    ("리더가 되는 자리를 부담스럽게 느끼지 않는다.", "teto"),
    ("감정에 휘둘리는 사람을 보면 불편하다.", "teto"),
    ("조직 내에서 서열과 룰이 명확해야 편하다.", "teto"),
    ("관계보다 나 자신을 먼저 챙겨야 한다고 생각한다.", "teto"),
    ("상대의 말보다 표정이나 분위기를 먼저 읽는다.", "egen"),
    ("친구가 울면 나도 눈물이 핑 돈 적이 있다.", "egen"),
    ("누군가 다쳤을 때 먼저 감정적으로 반응한다.", "egen"),
    ("감정적으로 힘든 사람에게 오래 공감해줄 수 있다.", "egen"),
    ("내 기분은 주변 사람의 분위기에 따라 잘 변한다.", "egen"),
    ("주변 사람과 갈등이 생기면 먼저 화해를 시도한다.", "egen"),
    ("감정 표현을 솔직하게 하는 게 오히려 관계를 좋게 만든다.", "egen")
]

# 질문 섞기
random.seed(42)
random.shuffle(questions)

options = ["매우 그렇다", "그렇다", "아니다", "전혀 아니다"]
score_map = {"매우 그렇다": 3, "그렇다": 2, "아니다": 1, "전혀 아니다": 0}

def calculate_result(gender, teto_score, egen_score):
    total_score = teto_score + egen_score
    if total_score == 0:
        teto_percent = egen_percent = 50
    else:
        teto_percent = (teto_score / total_score) * 100
        egen_percent = (egen_score / total_score) * 100

    if teto_percent > 50:
        if gender == "남성":
            return "테토남", teto_percent, egen_percent
        else:
            return "테토녀", teto_percent, egen_percent
    elif egen_percent > 50:
        if gender == "남성":
            return "에겐남", teto_percent, egen_percent
        else:
            return "에겐녀", teto_percent, egen_percent
    else:
        return "혼합형", teto_percent, egen_percent

# Streamlit 앱 시작
st.title("🧠 테토/에겐 성향 테스트")

gender = st.radio("당신의 성별은?", ["남성", "여성"])

st.subheader("📝 아래 문항에 응답해주세요")
teto_score = 0
egen_score = 0

for i, (q, category) in enumerate(questions):
    answer = st.radio(q, options, key=f"q_{i}")
    score = score_map[answer]
    if category == "teto":
        teto_score += score
    else:
        egen_score += score

if st.button("결과 보기"):
    result_type, teto_percent, egen_percent = calculate_result(gender, teto_score, egen_score)

    st.markdown("---")
    st.header(f"✅ 당신은 '{result_type}'입니다.")
    st.write(f"테토 성향 비율: {teto_percent:.1f}%")
    st.write(f"에겐 성향 비율: {egen_percent:.1f}%")

    # 원형 그래프 그리기 (Plotly)
    fig = go.Figure(data=[
        go.Pie(labels=['테토', '에겐'], values=[teto_percent, egen_percent],
               marker=dict(colors=['#4B8BBE', '#FFB6C1']),
               hoverinfo='label+percent', textinfo='label+percent')
    ])
    st.plotly_chart(fig)

    descriptions = {
        "테토남": "논리적이고 목표 지향적인 남성 성향. 경쟁, 이성, 구조를 중시합니다.",
        "에겐남": "감성적이고 공감력이 뛰어난 남성 성향. 관계와 감정 표현에 능합니다.",
        "테토녀": "이성적이고 주도적인 여성 성향. 계획과 효율을 선호합니다.",
        "에겐녀": "감성적이고 배려심 깊은 여성 성향. 감정 중심의 소통을 중시합니다.",
        "혼합형": "이성과 감성의 균형을 잘 맞추는 성향입니다. 상황에 따라 유연하게 반응합니다."
    }

    st.success(descriptions[result_type])
