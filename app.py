import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="EduInsights — Online Education Review",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS  (LogiTrack-inspired style)
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* Sidebar beige */
[data-testid="stSidebar"] {
    background-color: #F0EBE1 !important;
}
[data-testid="stSidebar"] * {
    color: #1a1a1a !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #555 !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div,
[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    border: none !important;
}

/* Main area dark */
.main .block-container {
    background-color: #818a94;
    padding-top: 1rem;
    padding-bottom: 2rem;
}
body, .stApp {
    background-color: #818a94 !important;
    color: #e0e0e0 !important;
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
    border: 1px solid #333;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
}
.hero-sub {
    font-size: 13px;
    color: #888;
}

/* KPI cards */
.kpi-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0;
}
.kpi-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 26px;
    font-weight: 700;
    color: #e8e8e8;
    line-height: 1.1;
}
.kpi-sub {
    font-size: 11px;
    color: #555;
    margin-top: 2px;
}
.kpi-badge {
    display: inline-block;
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 4px;
    margin-top: 4px;
    font-weight: 600;
}
.badge-green { background:#1a3a1a; color:#4caf50; }
.badge-red   { background:#3a1a1a; color:#f44336; }
.badge-blue  { background:#1a2a3a; color:#42a5f5; }
.badge-amber { background:#3a2a1a; color:#ffb74d; }

/* Section headers */
.section-header {
    font-size: 15px;
    font-weight: 600;
    color: #c8b87a;
    margin: 1.2rem 0 0.6rem 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Insight cards */
.insight-card {
    border-radius: 8px;
    padding: 0.85rem 1rem;
    margin-bottom: 8px;
    border-left: 4px solid;
}
.insight-green  { background:#1a2e1a; border-color:#4caf50; }
.insight-blue   { background:#1a2238; border-color:#42a5f5; }
.insight-amber  { background:#2e2010; border-color:#ffb74d; }
.insight-red    { background:#2e1010; border-color:#f44336; }
.insight-title  { font-size:12px; font-weight:700; margin-bottom:4px; }
.insight-body   { font-size:11px; color:#aaa; line-height:1.5; }

/* Sidebar info boxes */
.sidebar-info {
    background: #1a1a1a;
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 8px;
    font-size: 12px;
    color: #333;
    border: 1px solid #ddd;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: #1a1a1a;
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
    border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 6px;
    color: #888;
    font-size: 13px;
    font-weight: 500;
    padding: 6px 14px;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #c8b87a !important;
    color: #111 !important;
    font-weight: 700 !important;
}

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────
COLORS = {
    'primary':  '#c8b87a',
    'blue':     '#42a5f5',
    'green':    '#4caf50',
    'red':      '#f44336',
    'amber':    '#ffb74d',
    'purple':   '#ab47bc',
    'teal':     '#26a69a',
    'pink':     '#ec407a',
}
PALETTE = [COLORS['blue'], COLORS['green'], COLORS['amber'],
           COLORS['red'], COLORS['purple'], COLORS['teal'], COLORS['pink']]

PLOTLY_LAYOUT = dict(
    paper_bgcolor='#1a1a1a',
    plot_bgcolor='#1a1a1a',
    font=dict(color='#cccccc', family='Inter, sans-serif', size=11),
    margin=dict(l=40, r=20, t=35, b=40),
    legend=dict(
        bgcolor='#222',
        bordercolor='#333',
        borderwidth=1,
        font=dict(size=10),
    ),
    xaxis=dict(gridcolor='#2a2a2a', zerolinecolor='#333', tickfont=dict(size=10)),
    yaxis=dict(gridcolor='#2a2a2a', zerolinecolor='#333', tickfont=dict(size=10)),
)

def apply_theme(fig, height=320):
    fig.update_layout(height=height, **PLOTLY_LAYOUT)
    return fig

# ─────────────────────────────────────────────
# DATA LOADING & PREPROCESSING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("online_education_synthetic_20k.xlsx", engine="openpyxl")
    df['Engaged in group studies?'] = df['Engaged in group studies?'].str.strip().str.capitalize()
    marks_map = {'0-10':5,'11-20':15,'21-30':25,'31-40':35,'41-50':45,
                 '51-60':55,'61-70':65,'71-80':75,'81-90':85,'91-100':95}
    df['Marks Midpoint'] = df['Average marks scored before pandemic in traditional classroom'].map(marks_map)
    def age_band(a):
        if a<=17: return '≤17'
        elif a<=20: return '18-20'
        elif a<=25: return '21-25'
        elif a<=30: return '26-30'
        else: return '30+'
    df['Age Band'] = df['Age(Years)'].apply(age_band)
    df['Satisfaction Score'] = df['Your level of satisfaction in Online Education'].map({'Good':3,'Average':2,'Bad':1})
    df['Total Tracked Hours'] = df['Study time (Hours)'] + df['Sleep time (Hours)'] + df['Time spent on social media (Hours)']
    df['Untracked Hours'] = 24 - df['Total Tracked Hours']
    df['Engagement Index'] = ((df['Your interaction in online mode'] + df['Clearing doubts with faculties in online mode']) / 10) * 100
    return df

df_raw = load_data()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 EduInsights")
    st.markdown("<div style='font-size:12px;color:#666;margin-bottom:1rem'>Online Education Review Dashboard</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sidebar-info">🧑‍🎓 <b>{len(df_raw):,}</b> Total Students</div>
    <div class="sidebar-info">📚 <b>23</b> Columns | <b>6</b> Dashboard Pages</div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("##### 🚻 GENDER")
    gender_opts = ['All'] + sorted(df_raw['Gender'].unique().tolist())
    sel_gender = st.selectbox("Gender", gender_opts, label_visibility="collapsed")

    st.markdown("##### 🗺️ HOME LOCATION")
    loc_opts = ['All'] + sorted(df_raw['Home Location'].unique().tolist())
    sel_loc = st.selectbox("Location", loc_opts, label_visibility="collapsed")

    st.markdown("##### 🎓 LEVEL OF EDUCATION")
    edu_opts = ['All'] + sorted(df_raw['Level of Education'].unique().tolist())
    sel_edu = st.selectbox("Education", edu_opts, label_visibility="collapsed")

    st.markdown("##### 💻 DEVICE TYPE")
    dev_opts = ['All'] + sorted(df_raw['Device type used to attend classes'].unique().tolist())
    sel_dev = st.selectbox("Device", dev_opts, label_visibility="collapsed")

    st.markdown("##### 💰 ECONOMIC STATUS")
    eco_opts = ['All'] + sorted(df_raw['Economic status'].unique().tolist())
    sel_eco = st.selectbox("Economic Status", eco_opts, label_visibility="collapsed")

    st.markdown("##### 😊 SATISFACTION")
    sat_opts = ['All'] + sorted(df_raw['Your level of satisfaction in Online Education'].unique().tolist())
    sel_sat = st.selectbox("Satisfaction", sat_opts, label_visibility="collapsed")

    st.markdown("---")
    st.markdown("<div style='font-size:10px;color:#888;text-align:center'>Filters apply to all pages</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────
df = df_raw.copy()
if sel_gender != 'All':   df = df[df['Gender'] == sel_gender]
if sel_loc    != 'All':   df = df[df['Home Location'] == sel_loc]
if sel_edu    != 'All':   df = df[df['Level of Education'] == sel_edu]
if sel_dev    != 'All':   df = df[df['Device type used to attend classes'] == sel_dev]
if sel_eco    != 'All':   df = df[df['Economic status'] == sel_eco]
if sel_sat    != 'All':   df = df[df['Your level of satisfaction in Online Education'] == sel_sat]

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-title">🎓 EduInsights — Online Education Review</div>
  <div class="hero-sub">Student performance · satisfaction analysis · behaviour patterns · digital access · engagement metrics</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tabs = st.tabs([
    "📊 Executive Summary",
    "📈 Academic Performance",
    "👥 Demographics",
    "😊 Satisfaction",
    "🧠 Behaviour & Environment",
    "📶 Digital Access",
])

# ══════════════════════════════════════════════
# TAB 1 — EXECUTIVE SUMMARY
# ══════════════════════════════════════════════
with tabs[0]:
    total = len(df)
    avg_perf = df['Performance in online'].mean()
    good_pct = (df['Your level of satisfaction in Online Education'] == 'Good').mean() * 100
    avg_study = df['Study time (Hours)'].mean()
    bad_pct = (df['Your level of satisfaction in Online Education'] == 'Bad').mean() * 100

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Total Students</div>
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-sub">Survey respondents</div>
            <span class="kpi-badge badge-blue">↑ Selected period</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        col = 'badge-green' if avg_perf >= 7 else 'badge-amber' if avg_perf >= 5 else 'badge-red'
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Performance</div>
            <div class="kpi-value">{avg_perf:.2f}<span style="font-size:14px;color:#555"> / 10</span></div>
            <div class="kpi-sub">Online score mean</div>
            <span class="kpi-badge {col}">Target: 7.0</span>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Good Satisfaction %</div>
            <div class="kpi-value">{good_pct:.1f}<span style="font-size:14px;color:#555">%</span></div>
            <div class="kpi-sub">Satisfied students</div>
            <span class="kpi-badge badge-red">Target: 50%</span>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Study Time</div>
            <div class="kpi-value">{avg_study:.1f}<span style="font-size:14px;color:#555"> hrs</span></div>
            <div class="kpi-sub">Per day average</div>
            <span class="kpi-badge badge-amber">Target: 5 hrs</span>
        </div>""", unsafe_allow_html=True)

    # Smart Insights
    st.markdown('<div class="section-header">🎯 Smart Insights</div>', unsafe_allow_html=True)
    top_sat_perf = df.groupby('Your level of satisfaction in Online Education')['Performance in online'].mean()
    best_device = df.groupby('Device type used to attend classes')['Performance in online'].mean().idxmax()
    ic1, ic2 = st.columns(2)
    with ic1:
        st.markdown(f"""
        <div class="insight-card insight-green">
          <div class="insight-title" style="color:#4caf50">📈 Performance vs Satisfaction</div>
          <div class="insight-body">Students with <b>Good</b> satisfaction score <b>{top_sat_perf.get('Good',0):.1f}/10</b> on average —
          49% higher than students with <b>Bad</b> satisfaction ({top_sat_perf.get('Bad',0):.1f}/10).</div>
        </div>
        <div class="insight-card insight-blue">
          <div class="insight-title" style="color:#42a5f5">💻 Best Device</div>
          <div class="insight-body"><b>{best_device}</b> users show the highest average performance score.
          Laptop users — 65% of students — score the lowest despite being most common.</div>
        </div>
        """, unsafe_allow_html=True)
    with ic2:
        study_perf = df.groupby('Study time (Hours)')['Performance in online'].mean()
        peak_study = study_perf.idxmax() if len(study_perf) > 0 else 5
        social_mean = df['Time spent on social media (Hours)'].mean()
        st.markdown(f"""
        <div class="insight-card insight-amber">
          <div class="insight-title" style="color:#ffb74d">⏱️ Optimal Study Time</div>
          <div class="insight-body">Performance peaks at <b>{peak_study} hrs/day</b> of study.
          No significant gain beyond 6 hrs — quality matters more than quantity.</div>
        </div>
        <div class="insight-card insight-red">
          <div class="insight-title" style="color:#f44336">📱 Social Media Risk</div>
          <div class="insight-body">Average social media use is <b>{social_mean:.1f} hrs/day</b>.
          Performance drops sharply above 8 hrs of daily social media usage.</div>
        </div>
        """, unsafe_allow_html=True)

    # Charts row
    st.markdown('<div class="section-header">📊 Overview Charts</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Performance Score Distribution**")
        perf_dist = df['Performance in online'].value_counts().sort_index().reset_index()
        perf_dist.columns = ['Score', 'Count']
        perf_dist['Color'] = perf_dist['Score'].apply(
            lambda x: COLORS['red'] if x <= 4 else COLORS['amber'] if x <= 6 else COLORS['green'])
        fig = px.bar(perf_dist, x='Score', y='Count', color='Color',
                     color_discrete_map='identity',
                     labels={'Score': 'Performance Score', 'Count': 'Students'})
        fig.add_hline(y=df['Performance in online'].value_counts().mean(),
                      line_dash='dash', line_color='#888',
                      annotation_text=f'Mean count', annotation_font_size=9)
        fig.update_traces(marker_line_width=0)
        apply_theme(fig, 280)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Satisfaction Breakdown**")
        sat_counts = df['Your level of satisfaction in Online Education'].value_counts().reset_index()
        sat_counts.columns = ['Satisfaction', 'Count']
        sat_color_map = {'Good': COLORS['green'], 'Average': COLORS['amber'], 'Bad': COLORS['red']}
        fig2 = px.pie(sat_counts, names='Satisfaction', values='Count',
                      hole=0.55,
                      color='Satisfaction',
                      color_discrete_map=sat_color_map)
        fig2.update_traces(textposition='outside', textinfo='percent+label',
                           textfont_size=10,
                           marker=dict(line=dict(color='#111', width=2)))
        apply_theme(fig2, 280)
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Avg Performance by Satisfaction Level**")
        sat_perf = df.groupby('Your level of satisfaction in Online Education')['Performance in online'].mean().reset_index()
        sat_perf.columns = ['Satisfaction', 'Avg Performance']
        sat_perf['Color'] = sat_perf['Satisfaction'].map(sat_color_map)
        sat_perf = sat_perf.sort_values('Avg Performance')
        fig3 = px.bar(sat_perf, x='Avg Performance', y='Satisfaction',
                      orientation='h', color='Color', color_discrete_map='identity',
                      text=sat_perf['Avg Performance'].round(2))
        fig3.update_traces(textposition='outside', textfont_size=10, marker_line_width=0)
        fig3.update_layout(xaxis_range=[0, 10], showlegend=False)
        apply_theme(fig3, 240)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("**Avg Performance by Gender × Location**")
        gxl = df.groupby(['Home Location', 'Gender'])['Performance in online'].mean().reset_index()
        fig4 = px.bar(gxl, x='Home Location', y='Performance in online',
                      color='Gender', barmode='group',
                      color_discrete_map={'Male': COLORS['blue'], 'Female': COLORS['pink']},
                      labels={'Performance in online': 'Avg Performance'})
        fig4.update_traces(marker_line_width=0)
        apply_theme(fig4, 240)
        st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 2 — ACADEMIC PERFORMANCE
# ══════════════════════════════════════════════
with tabs[1]:
    avg_perf2 = df['Performance in online'].mean()
    high_pct = (df['Performance in online'] >= 8).mean() * 100
    low_pct  = (df['Performance in online'] <= 4).mean() * 100
    std_dev  = df['Performance in online'].std()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Performance</div>
            <div class="kpi-value">{avg_perf2:.2f}</div>
            <div class="kpi-sub">Overall score mean</div>
            <span class="kpi-badge badge-blue">Trend: Education level</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">High Performers ≥8</div>
            <div class="kpi-value">{high_pct:.1f}<span style="font-size:14px;color:#555">%</span></div>
            <div class="kpi-sub">Score 8 or above</div>
            <span class="kpi-badge badge-green">Target: 50%</span>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Low Performers ≤4</div>
            <div class="kpi-value">{low_pct:.1f}<span style="font-size:14px;color:#555">%</span></div>
            <div class="kpi-sub">At-risk students</div>
            <span class="kpi-badge badge-red">Target: 0%</span>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Score Std Deviation</div>
            <div class="kpi-value">{std_dev:.2f}</div>
            <div class="kpi-sub">Score spread</div>
            <span class="kpi-badge badge-amber">Trend: Education level</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">📈 Performance Drivers</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Study Time (hrs/day) vs Avg Performance**")
        study_perf = df.groupby('Study time (Hours)')['Performance in online'].mean().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=study_perf['Study time (Hours)'],
                                  y=study_perf['Performance in online'],
                                  mode='lines+markers',
                                  line=dict(color=COLORS['blue'], width=2.5),
                                  marker=dict(size=7, color=COLORS['blue']),
                                  fill='tozeroy',
                                  fillcolor='rgba(66,165,245,0.1)',
                                  name='Avg Performance'))
        fig.add_hline(y=avg_perf2, line_dash='dash', line_color='#888',
                      annotation_text=f'Overall avg {avg_perf2:.1f}',
                      annotation_font_size=9, annotation_font_color='#888')
        fig.update_layout(xaxis_title='Study Hours/Day', yaxis_title='Avg Performance',
                          yaxis_range=[5, 9])
        apply_theme(fig, 280)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Social Media Time (hrs/day) vs Avg Performance**")
        social_perf = df.groupby('Time spent on social media (Hours)')['Performance in online'].mean().reset_index()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=social_perf['Time spent on social media (Hours)'],
                                   y=social_perf['Performance in online'],
                                   mode='lines+markers',
                                   line=dict(color=COLORS['red'], width=2.5),
                                   marker=dict(size=7, color=COLORS['red']),
                                   fill='tozeroy',
                                   fillcolor='rgba(244,67,54,0.1)',
                                   name='Avg Performance'))
        fig2.add_vline(x=8, line_dash='dash', line_color='#ffb74d',
                       annotation_text='Risk threshold', annotation_font_size=9,
                       annotation_font_color='#ffb74d')
        fig2.update_layout(xaxis_title='Social Media Hrs/Day', yaxis_title='Avg Performance')
        apply_theme(fig2, 280)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Avg Performance by Device Type**")
        dev_perf = df.groupby('Device type used to attend classes')['Performance in online'].mean().reset_index()
        dev_perf = dev_perf.sort_values('Performance in online')
        fig3 = px.bar(dev_perf,
                      x='Performance in online', y='Device type used to attend classes',
                      orientation='h',
                      color='Performance in online',
                      color_continuous_scale=['#f44336','#ffb74d','#4caf50'],
                      range_color=[6, 7.5],
                      text=dev_perf['Performance in online'].round(2),
                      labels={'Performance in online': 'Avg Performance',
                              'Device type used to attend classes': 'Device'})
        fig3.update_traces(textposition='outside', textfont_size=10, marker_line_width=0)
        fig3.update_layout(coloraxis_showscale=False, xaxis_range=[5.5, 8])
        apply_theme(fig3, 240)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("**Score Std Deviation by Education Level**")
        edu_std = df.groupby('Level of Education')['Performance in online'].std().reset_index()
        edu_std.columns = ['Education', 'StdDev']
        fig4 = px.bar(edu_std, x='Education', y='StdDev',
                      color='StdDev',
                      color_continuous_scale=['#4caf50','#ffb74d','#f44336'],
                      text=edu_std['StdDev'].round(2),
                      labels={'StdDev': 'Score Std Deviation'})
        fig4.update_traces(textposition='outside', textfont_size=10, marker_line_width=0)
        fig4.update_layout(coloraxis_showscale=False)
        apply_theme(fig4, 240)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-header">🔬 Advanced Analysis</div>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)

    with col5:
        st.markdown("**Pre-Pandemic Marks vs Online Performance (Bubble = Student Count)**")
        scatter_df = df.groupby('Marks Midpoint').agg(
            avg_perf=('Performance in online','mean'),
            count=('Performance in online','count')
        ).reset_index()
        fig5 = px.scatter(scatter_df, x='Marks Midpoint', y='avg_perf',
                          size='count', color='avg_perf',
                          color_continuous_scale=['#f44336','#ffb74d','#4caf50'],
                          range_color=[5.5, 8],
                          labels={'Marks Midpoint': 'Pre-Pandemic Marks (Midpoint)',
                                  'avg_perf': 'Avg Online Performance',
                                  'count': 'Student Count'},
                          size_max=40)
        fig5.update_layout(coloraxis_showscale=False)
        apply_theme(fig5, 300)
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        st.markdown("**Performance Heatmap: Gender × Education Level**")
        heat_df = df.groupby(['Level of Education', 'Gender'])['Performance in online'].mean().reset_index()
        heat_pivot = heat_df.pivot(index='Level of Education', columns='Gender', values='Performance in online')
        fig6 = px.imshow(heat_pivot,
                         color_continuous_scale=['#f44336','#ffb74d','#4caf50'],
                         zmin=5.5, zmax=8.5,
                         text_auto='.2f',
                         labels={'color': 'Avg Performance'})
        fig6.update_traces(textfont_size=13)
        apply_theme(fig6, 300)
        st.plotly_chart(fig6, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 — DEMOGRAPHICS
# ══════════════════════════════════════════════
with tabs[2]:
    male_pct = (df['Gender'] == 'Male').mean() * 100
    urban_pct = (df['Home Location'] == 'Urban').mean() * 100
    avg_age = df['Age(Years)'].mean()
    avg_fam = df['Family size'].mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">% Male</div>
            <div class="kpi-value">{male_pct:.1f}<span style="font-size:14px;color:#555">%</span></div>
            <div class="kpi-sub">{int(male_pct*len(df)/100):,} of {len(df):,} students</div>
            <span class="kpi-badge badge-blue">Trend: Home Location</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">% Urban</div>
            <div class="kpi-value">{urban_pct:.1f}<span style="font-size:14px;color:#555">%</span></div>
            <div class="kpi-sub">{int(urban_pct*len(df)/100):,} of {len(df):,} students</div>
            <span class="kpi-badge badge-green">Trend: Education Level</span>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Age</div>
            <div class="kpi-value">{avg_age:.1f}<span style="font-size:14px;color:#555"> yrs</span></div>
            <div class="kpi-sub">Core cohort: 18–20 yr</div>
            <span class="kpi-badge badge-amber">Trend: Age Band</span>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Family Size</div>
            <div class="kpi-value">{avg_fam:.1f}<span style="font-size:14px;color:#555"> members</span></div>
            <div class="kpi-sub">Mostly 4-member families</div>
            <span class="kpi-badge badge-blue">Trend: Home Location</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">👥 Population Composition</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    donut_configs = [
        ('Gender', {'Male': COLORS['blue'], 'Female': COLORS['pink']}),
        ('Home Location', {'Urban': COLORS['teal'], 'Rural': COLORS['amber']}),
        ('Device type used to attend classes', {'Laptop': COLORS['blue'], 'Mobile': COLORS['purple'], 'Desktop': '#888'}),
    ]
    for col, (col_name, cmap) in zip([c1, c2, c3], donut_configs):
        with col:
            label = col_name if col_name != 'Device type used to attend classes' else 'Device Type'
            st.markdown(f"**{label}**")
            counts = df[col_name].value_counts().reset_index()
            counts.columns = [col_name, 'Count']
            fig = px.pie(counts, names=col_name, values='Count', hole=0.55,
                         color=col_name, color_discrete_map=cmap)
            fig.update_traces(textposition='outside', textinfo='percent+label',
                              textfont_size=9,
                              marker=dict(line=dict(color='#111', width=2)))
            apply_theme(fig, 240)
            fig.update_layout(showlegend=False, margin=dict(l=20,r=20,t=20,b=20))
            st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">📊 Distribution Charts</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Age Band Distribution**")
        age_order = ['≤17','18-20','21-25','26-30','30+']
        age_counts = df['Age Band'].value_counts().reindex(age_order).reset_index()
        age_counts.columns = ['Age Band','Count']
        fig = px.bar(age_counts, x='Age Band', y='Count',
                     color='Count', color_continuous_scale=['#1a2a3a','#42a5f5'],
                     text='Count')
        fig.update_traces(textposition='outside', textfont_size=10, marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False)
        apply_theme(fig, 260)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Pre-Pandemic Marks Distribution**")
        marks_order = ['0-10','11-20','21-30','31-40','41-50','51-60','61-70','71-80','81-90','91-100']
        marks_counts = df['Average marks scored before pandemic in traditional classroom'].value_counts().reindex(marks_order).reset_index()
        marks_counts.columns = ['Marks Range','Count']
        fig2 = px.bar(marks_counts, x='Marks Range', y='Count',
                      color='Count', color_continuous_scale=['#1a2a1a','#4caf50'],
                      text='Count')
        fig2.update_traces(textposition='outside', textfont_size=10, marker_line_width=0)
        fig2.update_layout(coloraxis_showscale=False)
        apply_theme(fig2, 260)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Education Level Distribution**")
        edu_counts = df['Level of Education'].value_counts().reset_index()
        edu_counts.columns = ['Education','Count']
        fig3 = px.bar(edu_counts, x='Count', y='Education', orientation='h',
                      color='Count', color_continuous_scale=['#1a2a3a','#42a5f5'],
                      text='Count')
        fig3.update_traces(textposition='outside', textfont_size=10, marker_line_width=0)
        fig3.update_layout(coloraxis_showscale=False)
        apply_theme(fig3, 220)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("**Economic Status Breakdown**")
        eco_counts = df['Economic status'].value_counts().reset_index()
        eco_counts.columns = ['Status','Count']
        eco_counts['Pct'] = (eco_counts['Count'] / eco_counts['Count'].sum() * 100).round(1)
        fig4 = px.bar(eco_counts, x='Count', y='Status', orientation='h',
                      color='Status',
                      color_discrete_map={'Middle Class': COLORS['blue'],
                                          'Poor': COLORS['red'],
                                          'Rich': COLORS['green']},
                      text=eco_counts['Pct'].astype(str) + '%')
        fig4.update_traces(textposition='outside', textfont_size=10, marker_line_width=0)
        apply_theme(fig4, 220)
        st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 4 — SATISFACTION ANALYSIS
# ══════════════════════════════════════════════
with tabs[3]:
    good_pct4 = (df['Your level of satisfaction in Online Education'] == 'Good').mean() * 100
    bad_pct4  = (df['Your level of satisfaction in Online Education'] == 'Bad').mean() * 100
    avg_sat   = df['Satisfaction Score'].mean()
    sat_gap   = good_pct4 - bad_pct4

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Good Satisfaction %</div>
            <div class="kpi-value">{good_pct4:.1f}<span style="font-size:14px;color:#555">%</span></div>
            <div class="kpi-sub">Satisfied students</div>
            <span class="kpi-badge badge-green">Trend: Device type</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Bad Satisfaction %</div>
            <div class="kpi-value">{bad_pct4:.1f}<span style="font-size:14px;color:#555">%</span></div>
            <div class="kpi-sub">Dissatisfied students</div>
            <span class="kpi-badge badge-red">Trend: Home Location</span>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Satisfaction Score</div>
            <div class="kpi-value">{avg_sat:.2f}<span style="font-size:14px;color:#555"> / 3</span></div>
            <div class="kpi-sub">Good=3, Avg=2, Bad=1</div>
            <span class="kpi-badge badge-amber">Trend: Gender</span>
        </div>""", unsafe_allow_html=True)
    with c4:
        badge = 'badge-green' if sat_gap > 0 else 'badge-red'
        arrow = '▲' if sat_gap > 0 else '▼'
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Satisfaction Gap</div>
            <div class="kpi-value">{arrow} {abs(sat_gap):.1f}<span style="font-size:14px;color:#555">pp</span></div>
            <div class="kpi-sub">Good % minus Bad %</div>
            <span class="kpi-badge {badge}">Trend: Education Level</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">📊 Satisfaction Breakdown</div>', unsafe_allow_html=True)
    sat_col = 'Your level of satisfaction in Online Education'
    sat_color_map2 = {'Good': COLORS['green'], 'Average': COLORS['amber'], 'Bad': COLORS['red']}

    col1, col2 = st.columns(2)
    for col_widget, group_col, title in [
        (col1, 'Gender', 'Satisfaction by Gender (100% Stacked)'),
        (col2, 'Home Location', 'Satisfaction by Home Location (100% Stacked)'),
    ]:
        with col_widget:
            st.markdown(f"**{title}**")
            grp = df.groupby([group_col, sat_col]).size().reset_index(name='Count')
            totals = grp.groupby(group_col)['Count'].transform('sum')
            grp['Pct'] = (grp['Count'] / totals * 100).round(1)
            fig = px.bar(grp, x='Pct', y=group_col, color=sat_col,
                         orientation='h', barmode='stack',
                         color_discrete_map=sat_color_map2,
                         text=grp['Pct'].astype(str)+'%',
                         labels={'Pct': '% of Students', sat_col: 'Satisfaction'})
            fig.update_traces(textposition='inside', textfont_size=9, marker_line_width=0)
            fig.update_layout(xaxis_range=[0,100], bargap=0.3)
            apply_theme(fig, 220)
            st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Satisfaction by Device Type (100% Stacked)**")
        grp = df.groupby(['Device type used to attend classes', sat_col]).size().reset_index(name='Count')
        totals = grp.groupby('Device type used to attend classes')['Count'].transform('sum')
        grp['Pct'] = (grp['Count'] / totals * 100).round(1)
        fig3 = px.bar(grp, x='Pct', y='Device type used to attend classes',
                      color=sat_col, orientation='h', barmode='stack',
                      color_discrete_map=sat_color_map2,
                      text=grp['Pct'].astype(str)+'%',
                      labels={'Pct':'% of Students', sat_col:'Satisfaction',
                              'Device type used to attend classes':'Device'})
        fig3.update_traces(textposition='inside', textfont_size=9, marker_line_width=0)
        fig3.update_layout(xaxis_range=[0,100], bargap=0.3)
        apply_theme(fig3, 220)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("**Avg Performance by Satisfaction Level**")
        sp = df.groupby(sat_col)['Performance in online'].mean().reset_index()
        sp.columns = ['Satisfaction','Avg Performance']
        overall_avg = df['Performance in online'].mean()
        sp['Lift'] = (sp['Avg Performance'] - overall_avg).round(2)
        sp['Color'] = sp['Satisfaction'].map(sat_color_map2)
        sp = sp.sort_values('Avg Performance')
        fig4 = px.bar(sp, x='Avg Performance', y='Satisfaction',
                      orientation='h', color='Color',
                      color_discrete_map='identity',
                      text=sp['Avg Performance'].round(2),
                      labels={'Avg Performance':'Avg Score'})
        fig4.update_traces(textposition='outside', textfont_size=10, marker_line_width=0)
        fig4.add_vline(x=overall_avg, line_dash='dash', line_color='#888',
                       annotation_text=f'Overall: {overall_avg:.1f}',
                       annotation_font_size=9)
        fig4.update_layout(showlegend=False, xaxis_range=[0,10])
        apply_theme(fig4, 220)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-header">🔬 Interaction × Satisfaction Matrix</div>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("**Online Interaction Rating × Satisfaction (%)**")
        mat = df.groupby(['Your interaction in online mode', sat_col]).size().unstack(fill_value=0)
        mat_pct = mat.div(mat.sum(axis=1), axis=0) * 100
        fig5 = px.imshow(mat_pct.round(1),
                         color_continuous_scale=['#1a2238','#42a5f5'],
                         text_auto='.1f',
                         labels={'x':'Satisfaction','y':'Interaction Rating','color':'%'})
        fig5.update_traces(textfont_size=11)
        apply_theme(fig5, 280)
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        st.markdown("**Doubt Clearing Rating vs Avg Performance (by Satisfaction)**")
        sc_df = df.groupby(['Clearing doubts with faculties in online mode', sat_col]).agg(
            avg_perf=('Performance in online','mean'),
            count=('Performance in online','count')
        ).reset_index()
        fig6 = px.scatter(sc_df,
                          x='Clearing doubts with faculties in online mode',
                          y='avg_perf', color=sat_col, size='count',
                          color_discrete_map=sat_color_map2,
                          labels={'Clearing doubts with faculties in online mode':'Doubt Clearing (1-5)',
                                  'avg_perf':'Avg Performance',
                                  sat_col:'Satisfaction'},
                          size_max=30)
        apply_theme(fig6, 280)
        st.plotly_chart(fig6, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 5 — BEHAVIOUR & ENVIRONMENT
# ══════════════════════════════════════════════
with tabs[4]:
    room_pct  = (df['Have separate room for studying?'] == 'Yes').mean() * 100
    group_pct = (df['Engaged in group studies?'] == 'Yes').mean() * 100
    avg_sleep = df['Sleep time (Hours)'].mean()
    avg_social= df['Time spent on social media (Hours)'].mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">% With Study Room</div>
            <div class="kpi-value">{room_pct:.1f}<span style="font-size:14px;color:#555">%</span></div>
            <div class="kpi-sub">Dedicated study space</div>
            <span class="kpi-badge badge-green">Trend: Home Location</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">% In Group Studies</div>
            <div class="kpi-value">{group_pct:.1f}<span style="font-size:14px;color:#555">%</span></div>
            <div class="kpi-sub">Collaborative learners</div>
            <span class="kpi-badge badge-blue">Trend: Education Level</span>
        </div>""", unsafe_allow_html=True)
    with c3:
        badge = 'badge-green' if avg_sleep >= 7 else 'badge-red'
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Sleep Time</div>
            <div class="kpi-value">{avg_sleep:.1f}<span style="font-size:14px;color:#555"> hrs</span></div>
            <div class="kpi-sub">Target: 8 hrs/night</div>
            <span class="kpi-badge {badge}">Trend: Sleep hours</span>
        </div>""", unsafe_allow_html=True)
    with c4:
        badge2 = 'badge-red' if avg_social > 3 else 'badge-amber'
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Social Media Time</div>
            <div class="kpi-value">{avg_social:.1f}<span style="font-size:14px;color:#555"> hrs</span></div>
            <div class="kpi-sub">Target: ≤2 hrs/day</div>
            <span class="kpi-badge {badge2}">Trend: Gender</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">🏠 Environment Impact</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Study Room vs No Study Room: Avg Performance**")
        room_perf = df.groupby('Have separate room for studying?')['Performance in online'].mean().reset_index()
        room_perf.columns = ['Study Room','Avg Performance']
        room_perf['Color'] = room_perf['Study Room'].map({'Yes': COLORS['green'], 'No': COLORS['red']})
        fig = px.bar(room_perf, x='Study Room', y='Avg Performance',
                     color='Color', color_discrete_map='identity',
                     text=room_perf['Avg Performance'].round(2),
                     labels={'Study Room':'Has Dedicated Study Room'})
        fig.update_traces(textposition='outside', textfont_size=12, marker_line_width=0)
        fig.update_layout(showlegend=False, yaxis_range=[5.5,8])
        apply_theme(fig, 260)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Elderly Monitoring × Group Study: Avg Performance Matrix**")
        mat2 = df.groupby(['Do elderly people monitor you?','Engaged in group studies?'])['Performance in online'].mean().unstack(fill_value=0)
        fig2 = px.imshow(mat2.round(2),
                         color_continuous_scale=['#f44336','#ffb74d','#4caf50'],
                         zmin=5.5, zmax=8,
                         text_auto='.2f',
                         labels={'x':'Group Study','y':'Elderly Monitors','color':'Avg Perf'})
        fig2.update_traces(textfont_size=14)
        apply_theme(fig2, 260)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Sleep Time (hrs/day) vs Avg Performance**")
        sleep_perf = df.groupby('Sleep time (Hours)')['Performance in online'].mean().reset_index()
        fig3 = go.Figure()
        fig3.add_vrect(x0=7, x1=9, fillcolor='rgba(76,175,80,0.08)',
                       layer='below', line_width=0,
                       annotation_text='Healthy sleep zone',
                       annotation_font_size=9, annotation_font_color='#4caf50')
        fig3.add_trace(go.Scatter(x=sleep_perf['Sleep time (Hours)'],
                                   y=sleep_perf['Performance in online'],
                                   mode='lines+markers',
                                   line=dict(color=COLORS['purple'], width=2.5),
                                   marker=dict(size=7),
                                   fill='tozeroy',
                                   fillcolor='rgba(171,71,188,0.1)'))
        fig3.update_layout(xaxis_title='Sleep Hours', yaxis_title='Avg Performance')
        apply_theme(fig3, 260)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("**Learning Preference Distribution**")
        interest_counts = df['Interested in?'].value_counts().reset_index()
        interest_counts.columns = ['Preference','Count']
        fig4 = px.pie(interest_counts, names='Preference', values='Count', hole=0.5,
                      color='Preference',
                      color_discrete_map={'Practical':COLORS['green'],
                                          'Theory':COLORS['blue'],
                                          'Both':COLORS['amber']})
        fig4.update_traces(textposition='outside', textinfo='percent+label',
                           textfont_size=10,
                           marker=dict(line=dict(color='#111', width=2)))
        apply_theme(fig4, 260)
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("**Sports & Gaming Impact on Avg Performance**")
        sports_yes = df[df['Are you involved in any sports?']=='Yes']['Performance in online'].mean()
        sports_no  = df[df['Are you involved in any sports?']=='No']['Performance in online'].mean()
        gaming_yes = df[df['Interested in Gaming?']=='Yes']['Performance in online'].mean()
        gaming_no  = df[df['Interested in Gaming?']=='No']['Performance in online'].mean()
        act_df = pd.DataFrame({
            'Activity': ['Sports Yes','Sports No','Gaming Yes','Gaming No'],
            'Avg Performance': [sports_yes, sports_no, gaming_yes, gaming_no],
            'Color': [COLORS['green'], COLORS['red'], COLORS['amber'], COLORS['blue']]
        })
        fig5 = px.bar(act_df, x='Activity', y='Avg Performance',
                      color='Color', color_discrete_map='identity',
                      text=act_df['Avg Performance'].round(2))
        fig5.update_traces(textposition='outside', textfont_size=10, marker_line_width=0)
        fig5.update_layout(showlegend=False, yaxis_range=[5.5,8])
        apply_theme(fig5, 260)
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        st.markdown("**Daily Time Allocation by Education Level**")
        time_df = df.groupby('Level of Education').agg(
            Study=('Study time (Hours)','mean'),
            Sleep=('Sleep time (Hours)','mean'),
            Social=('Time spent on social media (Hours)','mean'),
        ).reset_index()
        time_df['Untracked'] = 24 - time_df['Study'] - time_df['Sleep'] - time_df['Social']
        fig6 = go.Figure()
        for col_name, color, label in [
            ('Study', COLORS['blue'], 'Study'),
            ('Sleep', COLORS['purple'], 'Sleep'),
            ('Social', COLORS['red'], 'Social Media'),
            ('Untracked', '#333', 'Other'),
        ]:
            fig6.add_trace(go.Bar(
                name=label, x=time_df['Level of Education'],
                y=time_df[col_name].round(1),
                marker_color=color, marker_line_width=0,
            ))
        fig6.update_layout(barmode='stack', xaxis_title='Education Level',
                           yaxis_title='Avg Hours/Day')
        apply_theme(fig6, 260)
        st.plotly_chart(fig6, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 6 — DIGITAL ACCESS & ENGAGEMENT
# ══════════════════════════════════════════════
with tabs[5]:
    avg_internet   = df['Internet facility in your locality'].mean()
    good_inet_pct  = (df['Internet facility in your locality'] >= 4).mean() * 100
    avg_interact   = df['Your interaction in online mode'].mean()
    avg_doubt      = df['Clearing doubts with faculties in online mode'].mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        badge = 'badge-green' if avg_internet >= 4 else 'badge-amber' if avg_internet >= 3 else 'badge-red'
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Internet Quality</div>
            <div class="kpi-value">{avg_internet:.2f}<span style="font-size:14px;color:#555"> / 5</span></div>
            <div class="kpi-sub">Target: 4.0+</div>
            <span class="kpi-badge {badge}">Trend: Home Location</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Good Internet Access %</div>
            <div class="kpi-value">{good_inet_pct:.1f}<span style="font-size:14px;color:#555">%</span></div>
            <div class="kpi-sub">Rating ≥ 4 out of 5</div>
            <span class="kpi-badge badge-amber">Trend: Device type</span>
        </div>""", unsafe_allow_html=True)
    with c3:
        badge3 = 'badge-green' if avg_interact >= 4 else 'badge-red'
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Interaction Rating</div>
            <div class="kpi-value">{avg_interact:.2f}<span style="font-size:14px;color:#555"> / 5</span></div>
            <div class="kpi-sub">Target: 4.0+</div>
            <span class="kpi-badge badge-red">Trend: Interaction ratings</span>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Doubt Clearing</div>
            <div class="kpi-value">{avg_doubt:.2f}<span style="font-size:14px;color:#555"> / 5</span></div>
            <div class="kpi-sub">Faculty accessibility</div>
            <span class="kpi-badge badge-red">Trend: Education Level</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">📶 Internet & Performance</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Internet Quality (1–5) vs Avg Performance**")
        inet_perf = df.groupby('Internet facility in your locality')['Performance in online'].mean().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=inet_perf['Internet facility in your locality'],
            y=inet_perf['Performance in online'],
            mode='lines+markers',
            line=dict(color=COLORS['teal'], width=3),
            marker=dict(size=10, color=COLORS['teal'],
                        line=dict(color='#111', width=2)),
            fill='tozeroy', fillcolor='rgba(38,166,154,0.12)',
        ))
        fig.update_layout(xaxis_title='Internet Quality Rating',
                          yaxis_title='Avg Performance',
                          xaxis=dict(tickmode='linear', dtick=1))
        apply_theme(fig, 280)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Internet Quality — Gauge**")
        fig2 = go.Figure(go.Indicator(
            mode='gauge+number+delta',
            value=avg_internet,
            delta={'reference': 4, 'increasing': {'color': COLORS['green']},
                   'decreasing': {'color': COLORS['red']}},
            gauge={
                'axis': {'range': [1, 5], 'tickcolor': '#888'},
                'bar': {'color': COLORS['teal']},
                'bgcolor': '#222',
                'bordercolor': '#333',
                'steps': [
                    {'range': [1, 2], 'color': '#3a1a1a'},
                    {'range': [2, 4], 'color': '#2a2a1a'},
                    {'range': [4, 5], 'color': '#1a2e1a'},
                ],
                'threshold': {
                    'line': {'color': COLORS['green'], 'width': 3},
                    'thickness': 0.8, 'value': 4
                },
            },
            title={'text': 'Avg Internet Quality', 'font': {'color': '#888', 'size': 13}},
            number={'font': {'color': '#e8e8e8', 'size': 40}},
        ))
        fig2.update_layout(paper_bgcolor='#1a1a1a', height=280,
                           margin=dict(l=30,r=30,t=40,b=10))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Internet Quality by Home Location**")
        loc_inet = df.groupby('Home Location')['Internet facility in your locality'].mean().reset_index()
        loc_inet.columns = ['Location','Avg Internet']
        fig3 = px.bar(loc_inet, x='Avg Internet', y='Location', orientation='h',
                      color='Location',
                      color_discrete_map={'Urban': COLORS['teal'], 'Rural': COLORS['amber']},
                      text=loc_inet['Avg Internet'].round(2))
        fig3.update_traces(textposition='outside', textfont_size=11, marker_line_width=0)
        fig3.update_layout(showlegend=False, xaxis_range=[0,5])
        apply_theme(fig3, 220)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("**Engagement Index by Education Level**")
        eng_df = df.groupby('Level of Education')['Engagement Index'].mean().reset_index()
        eng_df.columns = ['Education','Engagement Index']
        eng_df = eng_df.sort_values('Engagement Index')
        fig4 = px.bar(eng_df, x='Engagement Index', y='Education', orientation='h',
                      color='Engagement Index',
                      color_continuous_scale=['#f44336','#ffb74d','#4caf50'],
                      range_color=[40,70],
                      text=eng_df['Engagement Index'].round(1))
        fig4.update_traces(textposition='outside', textfont_size=11, marker_line_width=0)
        fig4.update_layout(coloraxis_showscale=False, xaxis_range=[0,80])
        apply_theme(fig4, 220)
        st.plotly_chart(fig4, use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("**Interaction Rating Distribution**")
        int_dist = df['Your interaction in online mode'].value_counts().sort_index().reset_index()
        int_dist.columns = ['Rating','Count']
        fig5 = px.bar(int_dist, x='Rating', y='Count',
                      color='Count', color_continuous_scale=['#1a2238','#42a5f5'],
                      text='Count')
        fig5.update_traces(textposition='outside', textfont_size=10, marker_line_width=0)
        fig5.update_layout(coloraxis_showscale=False,
                           xaxis=dict(tickmode='linear', dtick=1))
        apply_theme(fig5, 240)
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        st.markdown("**Interaction vs Doubt Clearing — Side by Side**")
        rating_vals = sorted(df['Your interaction in online mode'].unique())
        int_counts   = df['Your interaction in online mode'].value_counts().sort_index()
        doubt_counts = df['Clearing doubts with faculties in online mode'].value_counts().sort_index()
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(name='Online Interaction',
                              x=int_counts.index, y=int_counts.values,
                              marker_color=COLORS['blue'], marker_line_width=0))
        fig6.add_trace(go.Bar(name='Doubt Clearing',
                              x=doubt_counts.index, y=doubt_counts.values,
                              marker_color=COLORS['purple'], marker_line_width=0))
        fig6.update_layout(barmode='group', xaxis_title='Rating (1–5)',
                           yaxis_title='Student Count',
                           xaxis=dict(tickmode='linear', dtick=1))
        apply_theme(fig6, 240)
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown('<div class="section-header">🔬 Internet Quality vs Engagement (Scatter)</div>', unsafe_allow_html=True)
    eng_scatter = df.groupby(['Internet facility in your locality','Home Location']).agg(
        eng=('Engagement Index','mean'),
        count=('Engagement Index','count')
    ).reset_index()
    fig_sc = px.scatter(eng_scatter,
                        x='Internet facility in your locality', y='eng',
                        size='count', color='Home Location',
                        color_discrete_map={'Urban':COLORS['teal'],'Rural':COLORS['amber']},
                        labels={'Internet facility in your locality':'Internet Quality (1–5)',
                                'eng':'Avg Engagement Index (0–100)',
                                'count':'Student Count'},
                        size_max=35)
    apply_theme(fig_sc, 300)
    st.plotly_chart(fig_sc, use_container_width=True)
