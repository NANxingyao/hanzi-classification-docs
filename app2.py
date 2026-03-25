import streamlit as st
import pandas as pd

# --------------------------
# 页面配置
# --------------------------
st.set_page_config(
    page_title="名词属性判断工具",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("📝 名词属性判断系统")
st.markdown("### 请判断每个词语**作为名词**时是否符合规则，系统自动计分")
st.divider()

# --------------------------
# 8条名词规则（严格按你给的分值）
# --------------------------
rules = [
    {"desc": "可以受数量词的修饰", "yes": 10, "no": 0},
    {"desc": "不能受副词的修饰", "yes": 20, "no": -20},
    {"desc": "可以作典型的主语或宾语", "yes": 20, "no": 0},
    {"desc": "可以作中心语受其他名词修饰，或作定语直接修饰其他名词", "yes": 10, "no": 0},
    {"desc": "可以后附助词“的”构成“的”字结构", "yes": 10, "no": 0},
    {"desc": "可以后附方位词构成处所结构", "yes": 10, "no": 0},
    {"desc": "不能作谓语和谓语核心（不含省略语境）", "yes": 10, "no": -10},
    {"desc": "不能作补语，一般不能作状语直接修饰动词性成分", "yes": 10, "no": 0},
]

# --------------------------
# 24个名词（你给的全部词汇）
# --------------------------
words = [
    "主张", "企业", "余热", "保险", "关系", "出版", "发言", "奔波",
    "学习", "工会", "希望", "帮助", "开业", "归纳", "抗击", "插画",
    "救治", "来源", "游戏", "生活", "研究", "移民", "经历", "铅笔"
]

# --------------------------
# 初始化会话状态（存储选择结果）
# --------------------------
if "results" not in st.session_state:
    st.session_state.results = {}

# --------------------------
# 开始答题
# --------------------------
all_results = []

for word in words:
    st.subheader(f"🔍 测试词语：{word}（名词）")
    scores = []
    all_selected = True  # 标记当前词是否所有规则都已选择
    
    for idx, rule in enumerate(rules):
        # 关键：设置 index=None 实现初始空选
        choice = st.radio(
            f"规则{idx+1}：{word} → {rule['desc']}",
            ["符合", "不符合"],
            key=f"{word}_{idx}",
            horizontal=True,
            index=None  # 清空默认预填
        )
        
        if choice is None:
            all_selected = False
            scores.append(None)  # 未选择时记为 None
        else:
            # 计分
            s = rule["yes"] if choice == "符合" else rule["no"]
            scores.append(s)
    
    # 只有全部选完才显示总分
    if all_selected:
        total = sum(scores)
        st.success(f"✅ {word} 最终得分：{total} 分")
        st.session_state.results[word] = scores + [total]
    else:
        st.info("ℹ️ 请完成所有规则的判断后查看总分")
    
    st.divider()

# --------------------------
# 构建结果表（只统计已完成的词语）
# --------------------------
columns = [
    "词语", "规则1", "规则2", "规则3", "规则4",
    "规则5", "规则6", "规则7", "规则8", "总分"
]

df_data = []
for word in words:
    if word in st.session_state.results:
        df_data.append([word] + st.session_state.results[word])

df = pd.DataFrame(df_data, columns=columns)

# --------------------------
# 显示已完成结果总表
# --------------------------
st.markdown("## 📊 已完成词语得分总表")
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("暂无完成判断的词语数据")

# --------------------------
# 导出 CSV（无依赖，不报错）
# --------------------------
if not df.empty:
    st.download_button(
        label="📥 导出完整结果（Excel可打开）",
        data=df.to_csv(index=False).encode('utf-8-sig'),
        file_name="名词判断结果.csv",
        mime="text/csv"
    )

st.markdown("<br><center>✅ 工具制作完成 | 数据仅本地保存</center>", unsafe_allow_html=True)
