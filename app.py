import streamlit as st
import pandas as pd
from io import BytesIO

# --------------------------
# 页面配置
# --------------------------
st.set_page_config(
    page_title="动词属性判断工具",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("📝 动词属性判断系统")
st.markdown("### 请对每个词语作为动词时，判断是否符合规则")
st.divider()

# --------------------------
# 9 条规则（严格按你的要求）
# --------------------------
rules = [
    {"desc": "可以受否定副词“不”或“没有”修饰", "yes": 10, "no": 0},
    {"desc": "可以后附或中间插入时体助词“着、了、过”，或进入“……了没有”格式", "yes": 10, "no": 0},
    {"desc": "可以带真宾语，或通过“和、为、对、向、拿、于”引导必有论元", "yes": 20, "no": 0},
    {"desc": "不能受“很”修饰，或能同时受“很”修饰且带宾语", "yes": 10, "no": -10},
    {"desc": "可以有 V一V、V了V、V不V、V了没有 等重叠形式", "yes": 10, "no": 0},
    {"desc": "可以作谓语或谓语核心", "yes": 10, "no": -10},
    {"desc": "不能作状语直接修饰动词性成分", "yes": 10, "no": 0},
    {"desc": "可跟在“怎么、怎样/这么、这样”后表方式提问或回答", "yes": 10, "no": 0},
    {"desc": "不能跟在“多”后问程度，不能跟在“多么”后表感叹", "yes": 10, "no": -10},
]

# --------------------------
# 24 个词语
# --------------------------
words = [
    "主张", "企业", "余热", "保险", "关系", "出版", "发言", "奔波",
    "学习", "工会", "希望", "帮助", "开业", "归纳", "抗击", "插画",
    "救治", "来源", "游戏", "生活", "研究", "移民", "经历", "铅笔"
]

# --------------------------
# 开始答题
# --------------------------
all_results = []

for word in words:
    st.subheader(f"🔍 测试词语：{word}")
    scores = []

    for idx, rule in enumerate(rules):
        choice = st.radio(
            f"规则{idx+1}：{rule['desc']}",
            ["符合", "不符合"],
            key=f"{word}_{idx}",
            horizontal=True
        )

        # 计分
        if choice == "符合":
            s = rule["yes"]
        else:
            s = rule["no"]

        scores.append(s)

    # 计算当前词总分
    total = sum(scores)
    st.success(f"✅ {word} 最终得分：{total} 分")
    st.divider()

    # 保存一行数据
    all_results.append([word] + scores + [total])

# --------------------------
# 构建结果表
# --------------------------
columns = [
    "词语", "规则1", "规则2", "规则3", "规则4", "规则5",
    "规则6", "规则7", "规则8", "规则9", "总分"
]

df = pd.DataFrame(all_results, columns=columns)

# --------------------------
# 显示总表
# --------------------------
st.markdown("## 📊 全部词语得分总表")
st.dataframe(df, use_container_width=True)

# --------------------------
# 导出 Excel 文件
# --------------------------
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

excel_data = to_excel(df)

st.download_button(
    label="📥 导出完整结果（Excel）",
    data=excel_data,
    file_name="动词判断结果.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.markdown("<br><center>✅ 工具制作完成 | 数据仅本地保存</center>", unsafe_allow_html=True)
