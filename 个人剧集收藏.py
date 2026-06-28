import streamlit as st
import pandas as pd

# ========== 页面配置 ==========
st.set_page_config(
    page_title="我的腐剧收藏夹",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io',
        'Report a bug': "https://docs.streamlit.io",
        'About': "🌈 个人腐剧收藏夹 - 泰兰德的夏天永不停歇"
    }
)

# ========== 自定义CSS ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    h1, h2, h3 {
        color: #e8d5f5 !important;
        text-shadow: 0 0 20px rgba(200, 150, 255, 0.3);
    }
    .stMarkdown p {
        color: #c8b6e2 !important;
        font-size: 1.05rem;
        line-height: 1.8;
    }
    .drama-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .drama-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(180, 100, 255, 0.2);
    }
    .drama-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f0c8ff;
        margin-bottom: 8px;
    }
    .drama-country {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 8px;
    }
    .country-泰剧 { background: rgba(255, 183, 77, 0.25); color: #ffb74d; border: 1px solid rgba(255, 183, 77, 0.4); }
    .country-韩剧 { background: rgba(129, 212, 250, 0.25); color: #81d4fa; border: 1px solid rgba(129, 212, 250, 0.4); }
    .country-日剧 { background: rgba(244, 143, 177, 0.25); color: #f48fb1; border: 1px solid rgba(244, 143, 177, 0.4); }
    .country-中国 { background: rgba(129, 199, 132, 0.25); color: #81c784; border: 1px solid rgba(129, 199, 132, 0.4); }
    .drama-tag {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        color: #ce93d8;
        background: rgba(206, 147, 216, 0.15);
        border: 1px solid rgba(206, 147, 216, 0.3);
    }
    .stat-box {
        background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.03));
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #e1bee7;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #9e8cb5;
        margin-top: 6px;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a2e, #0f3460);
    }
    .hero-banner {
        background: linear-gradient(135deg, rgba(156, 39, 176, 0.3), rgba(63, 81, 181, 0.3));
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 30px;
    }
    .trend-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ========== 剧集数据 ==========
drama_data = [
    {"剧名": "将杀", "国家": "韩剧", "类型": "偏执女王×腹黑小狗攻", "emoji": "👑"},
    {"剧名": "伪装的真实之吻", "国家": "日剧", "类型": "要颜值有颜值，要剧情有颜值", "emoji": "🎭"},
    {"剧名": "第二次恋爱才完美", "国家": "日剧", "类型": "颜值高", "emoji": "💕"},
    {"剧名": "乞救之噬覆食殆尽", "国家": "日剧", "类型": "男女但变态颜值高", "emoji": "🖤"},
    {"剧名": "检察官的提亲", "国家": "韩剧", "类型": "海情天颜值高高干", "emoji": "⚖️"},
    {"剧名": "努力克服自卑的我们", "国家": "韩剧", "类型": "男女有深度", "emoji": "🌱"},
    {"剧名": "新版双城", "国家": "中国", "类型": "副CP可", "emoji": "🏙️"},
    {"剧名": "沦陷", "国家": "中国", "类型": "未知", "emoji": "🌀"},
    {"剧名": "当我看向你", "国家": "中国", "类型": "未知", "emoji": "👀"},
    {"剧名": "春山镜", "国家": "中国", "类型": "氛围感", "emoji": "🪞"},
    {"剧名": "床伴", "国家": "泰剧", "类型": "尺度", "emoji": "🔥"},
    {"剧名": "那年夏天", "国家": "泰剧", "类型": "细糠", "emoji": "☀️"},
    {"剧名": "铁拳教育", "国家": "韩剧", "类型": "爽", "emoji": "👊"},
    {"剧名": "天堂篇", "国家": "泰剧", "类型": "细糠", "emoji": "😇"},
    {"剧名": "偿还", "国家": "泰剧", "类型": "火", "emoji": "🔥"},
    {"剧名": "四方极爱", "国家": "泰剧", "类型": "暗恋", "emoji": "💜"},
]

df = pd.DataFrame(drama_data)

# ========== 侧边栏 ==========
with st.sidebar:
    st.logo("images/彩虹图片.jpg", size="large")
    st.markdown("## 🌈 导航菜单")
    page = st.radio("选择页面", ["🏠 首页", "📺 剧集列表", "🎬 媒体墙"], label_visibility="collapsed")

    st.divider()
    st.markdown("## 🔍 剧集筛选")
    selected_country = st.multiselect(
        "按国家/地区筛选",
        options=df["国家"].unique().tolist(),
        default=df["国家"].unique().tolist()
    )
    search_keyword = st.text_input("搜索剧名", placeholder="输入关键词...")

    st.divider()
    st.markdown("""
    <div style="text-align:center; padding: 20px 0; color: #9e8cb5;">
        <p>🌈 泰兰德的夏天永不停歇</p>
        <p style="font-size: 0.8rem;">Made with ❤️ & Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

# ========== 数据筛选 ==========
filtered_df = df[df["国家"].isin(selected_country)]
if search_keyword:
    filtered_df = filtered_df[filtered_df["剧名"].str.contains(search_keyword, na=False)]

# ========== 首页 ==========
if page == "🏠 首页":
    st.markdown("""
    <div class="hero-banner">
        <h1 style="font-size: 2.8rem; margin-bottom: 10px;">🏳️‍🌈 我的腐剧收藏夹</h1>
        <p style="font-size: 1.2rem; color: #ce93d8;">泰兰德的夏天永不停歇 🌴</p>
        <p style="color: #b39ddb;">精选抖音收藏佳作 · 随时查阅 · 持续更新中</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="stat-box"><div class="stat-number">{len(df)}</div><div class="stat-label">📺 收藏总数</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stat-box"><div class="stat-number">{df['国家'].nunique()}</div><div class="stat-label">🌍 国家/地区</div></div>""", unsafe_allow_html=True)
    with col3:
        thai_count = len(df[df["国家"] == "泰剧"])
        st.markdown(f"""<div class="stat-box"><div class="stat-number">{thai_count}</div><div class="stat-label">🇹🇭 泰剧数量</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="stat-box"><div class="stat-number">2026</div><div class="stat-label">📅 年度榜单</div></div>""", unsafe_allow_html=True)

    st.markdown("## 📊 年度三大趋势")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("""<div class="trend-card"><div style="font-size:2rem;">🎥</div><h3>制作升级</h3><p>电影级画面质感成为标配</p></div>""", unsafe_allow_html=True)
    with t2:
        st.markdown("""<div class="trend-card"><div style="font-size:2rem;">🎨</div><h3>题材多元</h3><p>悬疑、奇幻、历史等元素大胆融入</p></div>""", unsafe_allow_html=True)
    with t3:
        st.markdown("""<div class="trend-card"><div style="font-size:2rem;">✨</div><h3>演技在线</h3><p>从"工业糖精"进化到"自然发糖"</p></div>""", unsafe_allow_html=True)

    st.markdown("## 🔥 超爱CP")
    rec1, rec2, rec3, rec4 = st.columns(4)
    with rec1:
        st.image("images/picture1.jpg", use_container_width=True)
    with rec2:
        st.image("images/picture2.jpg", use_container_width=True)
    with rec3:
        st.image("images/BV.jpg", use_container_width=True)
    with rec4:
        st.image("images/南肯.jpg", use_container_width=True)

# ========== 剧集列表页 ==========
elif page == "📺 剧集列表":
    st.markdown("## 📺 我的收藏剧集")
    st.caption(f"共 {len(filtered_df)} 部剧集")

    for _, row in filtered_df.iterrows():
        country_class = f"country-{row['国家']}"
        st.markdown(f"""
        <div class="drama-card">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 1.8rem;">{row['emoji']}</span>
                <div>
                    <div class="drama-title">{row['剧名']}</div>
                    <span class="drama-country {country_class}">{row['国家']}</span>
                    <span class="drama-tag">{row['类型']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ========== 媒体墙页 ==========
elif page == "🎬 媒体墙":
    st.markdown("## 🎬 剧照 ")

    st.markdown("### 📸 精彩剧照")
    img1, img2, img3 = st.columns(3)
    with img1:
        st.image("images/偿还.jpg", use_container_width=True)
    with img2:
        st.image("images/天堂票.jpg", use_container_width=True)
    with img3:
        st.image("images/检察官的提案.jpg", use_container_width=True)


