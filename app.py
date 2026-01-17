import pandas as pd
import streamlit as st
import plotly.express as px

# ---------------------------
# Page
# ---------------------------
st.set_page_config(page_title="IT 직무 채용 난이도 구조 분석", layout="wide")

# ---------------------------
# Light Branding CSS
# ---------------------------
st.markdown("""
<style>
.block-container {padding-top: 1.8rem; padding-bottom: 3rem;}
h1 {font-size: 2.15rem !important; letter-spacing: -0.7px; margin-bottom: 0.25rem;}
h2 {letter-spacing: -0.4px;}
h3 {letter-spacing: -0.2px;}
.sub {color:#667085; font-size: 0.98rem; line-height: 1.45; margin-top: 0.2rem;}
.hr {height:1px; background:#EAECF0; margin: 16px 0 18px 0;}

.badge {
  display:inline-block; padding: 3px 10px; border-radius: 999px;
  background:#F2F4F7; color:#344054; font-size: 0.78rem; border:1px solid #EAECF0;
  vertical-align: middle;
}

.kpi {
  border: 1px solid #EAECF0;
  background: #FFFFFF;
  padding: 14px 16px;
  border-radius: 14px;
  box-shadow: 0 1px 2px rgba(16,24,40,0.06);
}
.kpi .label {color:#667085; font-size: 0.85rem;}
.kpi .value {font-size: 1.55rem; font-weight: 750; margin-top: 4px; letter-spacing: -0.3px;}
.kpi .note {color:#98A2B3; font-size: 0.82rem; margin-top: 2px;}

.card {
  border: 1px solid #EAECF0;
  background: #FFFFFF;
  padding: 14px 16px;
  border-radius: 14px;
  box-shadow: 0 1px 2px rgba(16,24,40,0.06);
}
.card .title {font-weight: 750; letter-spacing: -0.2px; margin-bottom: 6px;}
.card .body {color:#344054; line-height: 1.45;}
.small {color:#667085; font-size: 0.85rem;}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Data (your values)
# ---------------------------
df_difficulty = pd.DataFrame([
    ["PM",1458],["Other",1327],["QA",450],["Data Engineer",370],
    ["Backend",205],["ML Engineer",200],["Frontend",164],
    ["Mobile",78],["MLOps",70],["DevOps/Infra",22]
], columns=["직무","난이도지수"])

df_benefit = pd.DataFrame([
    ["성과급/인센티브",256],
    ["재택근무",88],
    ["리프레시 휴가",78],
    ["교육/컨퍼런스",8],
    ["스톡옵션",-19],
    ["유연근무",-41],
    ["복지포인트",-93]
], columns=["키워드","관심도 증가율(%)"])

df_title = pd.DataFrame([
    ["스택 기반",2.35],
    ["기타",1.79],
    ["임팩트 중심",0.97],
    ["직무 기반",0.36],
    ["문화/성장",0.09]
], columns=["제목유형","평균스크랩"])

df_sim = pd.DataFrame([
    ["스택X/복지X",1.51],
    ["스택X/복지O",1.05],
    ["스택O/복지O",7.77]
], columns=["JD구성","평균스크랩"])

TOP3 = ["성과급/인센티브", "재택근무", "리프레시 휴가"]

# ---------------------------
# Helpers
# ---------------------------
def base_layout(fig, ytitle="", xtitle="", height=420):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=18, b=10),
        xaxis_title=xtitle,
        yaxis_title=ytitle,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(size=13),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#F2F4F7", zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig

def insight_card(title: str, body: str, foot: str | None = None):
    foot_html = f"<div class='small' style='margin-top:8px'>{foot}</div>" if foot else ""
    st.markdown(
        f"""
        <div class="card">
          <div class="title">{title}</div>
          <div class="body">{body}</div>
          {foot_html}
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------
# Header (Portfolio badge 유지)
# ---------------------------
st.markdown("## IT 직무 채용 난이도의 구조적 원인 분석  <span class='badge'>Portfolio Case</span>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub'>원티드 IT 직무 JD(3,299건)를 기반으로, "
    "<b>채용 난이도(수요/관심)</b>와 <b>JD 설계 요소(복지 키워드·제목 구조)</b>가 "
    "관심도(스크랩)에 미치는 영향을 정량적으로 비교·해석했습니다.</div>",
    unsafe_allow_html=True
)
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

tabs = st.tabs([
    "① 채용 난이도 지수(RDI)",
    "② 복지 키워드 영향",
    "③ JD 제목 구조",
    "④ JD 구조 시뮬레이션"
])

# ---------------------------
# Tab 1: Difficulty (여기에서만 KPI 카드 노출)
# ---------------------------
with tabs[0]:
    # KPI strip (탭 1 전용)
    top_job = df_difficulty.sort_values("난이도지수", ascending=False).iloc[0]
    pm_val = int(df_difficulty.loc[df_difficulty["직무"]=="PM", "난이도지수"].iloc[0])
    qa_val = int(df_difficulty.loc[df_difficulty["직무"]=="QA", "난이도지수"].iloc[0])

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="kpi">
          <div class="label">최고 난이도 직무</div>
          <div class="value">{top_job['직무']}</div>
          <div class="note">RDI 최댓값 기준</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi">
          <div class="label">PM 난이도 지수 (RDI)</div>
          <div class="value">{pm_val:,}</div>
          <div class="note">수요 대비 관심 낮음</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi">
          <div class="label">QA 난이도 지수 (RDI)</div>
          <div class="value">{qa_val:,}</div>
          <div class="note">구조적 난이도 상위</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.25, 0.75])

    with left:
        st.markdown("### 직무별 채용 난이도 지수 (RDI)")
        st.caption("RDI(Recruiting Difficulty Index) = 공고 수(수요) ÷ 평균 스크랩(관심) · 값이 높을수록 ‘수요 대비 관심이 낮은’ 직무입니다.")

        df = df_difficulty.sort_values("난이도지수", ascending=True)
        fig = px.bar(
            df,
            x="난이도지수",
            y="직무",
            orientation="h",
            text="난이도지수",
            color="난이도지수",
            color_continuous_scale="Reds"
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(coloraxis_showscale=False)
        fig = base_layout(fig, xtitle="난이도 지수(RDI)", ytitle="", height=480)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        insight_card(
            "해석",
            "PM, QA, Data Engineer는 공고 대비 관심이 낮아, 단순 공고 확대로 해결되기 어렵습니다. "
            "<b>JD 구조 개선</b>과 <b>타겟 소싱</b>을 병행하는 접근이 필요합니다.",
            "※ 난이도는 ‘시장 경쟁’뿐 아니라 ‘관심 유입 구조’의 영향도 포함합니다."
        )
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        insight_card(
            "실무 적용 포인트",
            "상위 직무군은 (1) 제목 구조 정비 → (2) 역할/기대성과 명확화 → (3) 정보 구조 개선(보상·근무조건) 순으로 "
            "전환율을 끌어올리는 것이 효율적입니다."
        )

# ---------------------------
# Tab 2: Benefits impact (KPI 없음)
# ---------------------------
with tabs[1]:
    left, right = st.columns([1.25, 0.75])

    with left:
        st.markdown("### 복지·근무조건 키워드의 관심도 영향")
        st.caption("복지 키워드 포함 여부에 따른 평균 스크랩 차이를 기반으로, 관심도 변화에 영향이 큰 항목을 비교했습니다.")

        df = df_benefit.copy()

        def classify(row):
            k, v = row["키워드"], row["관심도 증가율(%)"]
            if v < 0:
                return "감소 영향"
            if k in TOP3:
                return "영향 큼"
            return "영향 제한적"

        df["분류"] = df.apply(classify, axis=1)

        fig = px.bar(
            df,
            x="키워드",
            y="관심도 증가율(%)",
            color="분류",
            text="관심도 증가율(%)",
            color_discrete_map={
                "영향 큼": "#D92D20",        # 강조
                "영향 제한적": "#D0D5DD",    # 중립
                "감소 영향": "#1570EF"       # 감소(방향)
            }
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig = base_layout(fig, ytitle="관심도 증가율(%)", xtitle="", height=460)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        insight_card(
            "핵심 결과",
            "<b>성과급/인센티브·재택근무·리프레시 휴가</b>는 관심도 상승 폭이 커, 타 항목 대비 영향이 큰 요소로 확인되었습니다.",
            "※ 영향도가 낮거나 감소 효과를 보인 항목은 JD 상단 강조보다는 보조 정보로 배치하는 전략이 적절합니다."
        )
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        insight_card(
            "권장 노출 방식",
            "관심도에 영향이 큰 항목은 JD 상단에서 정보 구조를 명확히 제시하고, "
            "기타 항목은 신뢰/기본 제공 요소로 하단에 배치하는 구성이 효율적입니다."
        )

# ---------------------------
# Tab 3: Title structure (KPI 없음)
# ---------------------------
with tabs[2]:
    left, right = st.columns([1.25, 0.75])

    with left:
        st.markdown("### JD 제목 구조별 평균 스크랩 비교")
        st.caption("제목 구성은 검색·노출에 직접 연결됩니다. 카테고리별 평균 스크랩을 비교해, 관심 유입에 유리한 제목 구조를 확인했습니다.")

        df = df_title.sort_values("평균스크랩", ascending=True)

        fig = px.bar(
            df,
            x="평균스크랩",
            y="제목유형",
            orientation="h",
            text="평균스크랩",
            color="평균스크랩",
            color_continuous_scale="Blues"
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(coloraxis_showscale=False)
        fig = base_layout(fig, ytitle="", xtitle="평균 스크랩 수", height=430)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        insight_card(
            "해석",
            "제목은 ‘역할(직무명)’ 자체보다, <b>기술 스택을 명시해 검색·노출 가능성을 높였는지</b>가 "
            "관심도(스크랩) 차이를 크게 만드는 요인으로 해석할 수 있습니다."
        )
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        insight_card(
            "권장 템플릿",
            "<b>기술 스택 명시형 제목</b>을 기본으로 두고, "
            "임팩트/문화 메시지는 제목이 아닌 <b>서브타이틀·상단 요약</b>으로 분리하는 구성이 안정적입니다."
        )

# ---------------------------
# Tab 4: Simulation (KPI 없음)
# ---------------------------
with tabs[3]:
    left, right = st.columns([1.25, 0.75])

    with left:
        st.markdown("### JD 구조 시뮬레이션 (백엔드 예시)")
        st.caption("제목 구조(기술 스택 명시 여부)와 복지 요소 조합에 따른 관심도(평균 스크랩) 변화를 시뮬레이션했습니다.")

        fig = px.bar(
            df_sim,
            x="JD구성",
            y="평균스크랩",
            text="평균스크랩",
            color="평균스크랩",
            color_continuous_scale="Greens"
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(coloraxis_showscale=False)
        fig = base_layout(fig, ytitle="평균 스크랩 수", xtitle="", height=430)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        insight_card(
            "핵심 결론",
            "복지 요소는 단독으로 작동하기보다, <b>제목 구조(기술 스택 명시)</b>와 결합될 때 "
            "관심도에 대한 영향력이 더 크게 나타났습니다.",
            "즉, ‘제목으로 유입 → 구성 요소로 설득’ 구조가 성과에 유리합니다."
        )
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        insight_card(
            "실행 제안",
            "우선순위는 (1) 제목 구조 정비 → (2) 역할/성과 기대치 명확화 → (3) 복지 요소의 정보 구조 최적화 "
            "순으로 설계하는 것이 효율적입니다."
        )

# Footer
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
st.markdown("<div class='small'>※ 본 대시보드는 포트폴리오 목적의 요약 시각화이며, 지표 정의/분모 보정 등 전처리 로직은 분석 노트 기준으로 적용했습니다.</div>", unsafe_allow_html=True)
