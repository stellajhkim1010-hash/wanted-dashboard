import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="채용 난이도 & JD 분석", layout="wide")

st.title("채용 난이도 & JD 분석 대시보드")
st.caption("원티드 IT 직무 JD 데이터 기반 분석 결과")

tab1, tab2, tab3, tab4 = st.tabs([
    "채용 난이도 지수",
    "복지 키워드 영향",
    "JD 제목 유형",
    "JD 구조 시뮬레이션"
])

# -------------------
# 1) 채용 난이도 지수
# -------------------
with tab1:
    df = pd.DataFrame([
        ["PM",1458],["Other",1327],["QA",450],["Data Engineer",370],
        ["Backend",205],["ML Engineer",200],["Frontend",164],
        ["Mobile",78],["MLOps",70],["DevOps/Infra",22]
    ], columns=["직무","난이도지수"])

    df = df.sort_values("난이도지수", ascending=True)

    fig = px.bar(
        df,
        x="난이도지수",
        y="직무",
        orientation="h",
        color="난이도지수",
        color_continuous_scale="Reds",
        text="난이도지수"
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        xaxis_title="채용 난이도 지수",
        yaxis_title="",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info("PM·QA·Data Engineer 직무는 수요 대비 관심도가 낮아 전략적 채용 접근이 필요")

# -------------------
# 2) 복지 키워드 영향 (Top3 진하게 강조)
# -------------------
with tab2:
    df = pd.DataFrame([
        ["성과급/인센티브",256],
        ["재택근무",88],
        ["리프레시 휴가",78],
        ["교육/컨퍼런스",8],
        ["스톡옵션",-19],
        ["유연근무",-41],
        ["복지포인트",-93]
    ], columns=["키워드","관심도 증가율(%)"])

    top3 = ["성과급/인센티브", "재택근무", "리프레시 휴가"]

    def group_row(row):
        k = row["키워드"]
        v = row["관심도 증가율(%)"]
        if v < 0:
            return "감소(-)"
        if k in top3:
            return "Top3 훅(+)"
        return "기타(+)"

    df["그룹"] = df.apply(group_row, axis=1)

    fig = px.bar(
        df,
        x="키워드",
        y="관심도 증가율(%)",
        color="그룹",
        text="관심도 증가율(%)",
        color_discrete_map={
            "Top3 훅(+)": "#d62728",  # 진한 빨강 (강조)
            "기타(+)": "#d9d9d9",     # 연한 회색
            "감소(-)": "#1f77b4"      # 파랑
        }
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        yaxis_title="관심도 증가율(%)",
        xaxis_title="",
        legend_title_text=""
    )

    st.plotly_chart(fig, use_container_width=True)
    st.success("성과급/인센티브, 재택근무, 리프레시 휴가는 JD 상단 노출 가치가 가장 높은 복리후생 요소")

# -------------------
# 3) JD 제목 유형
# -------------------
with tab3:
    df = pd.DataFrame([
        ["스택 기반",2.35],
        ["기타",1.79],
        ["임팩트 중심",0.97],
        ["직무 기반",0.36],
        ["문화/성장",0.09]
    ], columns=["제목유형","평균스크랩"])

    df = df.sort_values("평균스크랩", ascending=True)

    fig = px.bar(
        df,
        x="평균스크랩",
        y="제목유형",
        orientation="h",
        color="평균스크랩",
        color_continuous_scale="Blues",
        text="평균스크랩"
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        xaxis_title="평균 스크랩 수",
        yaxis_title="",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------
# 4) JD 구조 시뮬레이션
# -------------------
with tab4:
    df = pd.DataFrame([
        ["스택X/복지X",1.51],
        ["스택X/복지O",1.05],
        ["스택O/복지O",7.77]
    ], columns=["JD구성","평균스크랩"])

    fig = px.bar(
        df,
        x="JD구성",
        y="평균스크랩",
        color="평균스크랩",
        color_continuous_scale="Greens",
        text="평균스크랩"
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        yaxis_title="평균 스크랩 수",
        xaxis_title="",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)
    st.success("JD 제목이 매력적일 때, 복리후생 요소는 지원자 관심도를 추가로 증폭시키는 보조 레버로 작동")
