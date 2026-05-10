from flask import Flask, render_template_string
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar
import json
import os
import pandas as pd

app = Flask(__name__)

# --- 核心逻辑 1：读取项目一扫描出的真实风险数据 ---
def get_real_scan_stats():
    # 路径说明：这里使用相对路径读取项目一生成的 json
    # 如果你的文件夹结构不同，请手动修改路径
    json_path = "../xiangmu1/scan_report.json"
    
    if not os.path.exists(json_path):
        return {"online": 0, "high_risk": 0}
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    online_count = len(data) # 数组长度就是在线设备数
    high_risk_count = 0
    
    # 遍历 JSON，统计标记为 High 的端口数量
    for host in data:
        for detail in host.get("details", []):
            if detail.get("risk_level") == "High":
                high_risk_count += 1
                
    return {"online": online_count, "high_risk": high_risk_count}

# --- 核心逻辑 2：读取项目二解析出的真实业务数据 ---
def get_real_hl7_stats():
    excel_path = "../xiangmu2/Clinical_Data_Export.xlsx"
    
    if not os.path.exists(excel_path):
        return {"depts": ["无数据"], "counts": [0]}
    
    # 使用 Pandas 自动统计科室分布
    df = pd.read_excel(excel_path)
    if "就诊科室" in df.columns:
        dept_counts = df["就诊科室"].value_counts().to_dict()
        return {
            "depts": list(dept_counts.keys()),
            "counts": list(dept_counts.values())
        }
    return {"depts": ["格式错误"], "counts": [0]}

# --- 页面 HTML 模板 (去标识化+排版优化) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>医疗资产安全态势监控</title>
    <style>
        body { background-color: #f0f2f5; font-family: sans-serif; margin: 0; }
        .header { background-color: #001529; color: white; padding: 15px 40px; text-align: center; }
        .main-box { padding: 25px; max-width: 1200px; margin: 0 auto; }
        .status-row { display: flex; gap: 20px; margin-bottom: 25px; }
        .card { background: white; padding: 20px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); flex: 1; }
        .stat-val { font-size: 28px; font-weight: bold; margin-top: 10px; }
        .chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    </style>
</head>
<body>
    <div class="header"><h1>医疗机构资产安全态势感知监控中心</h1></div>
    <div class="main-box">
        <div class="status-row">
            <div class="card">实时在线设备<div class="stat-val">{{ s.online }}</div></div>
            <div class="card">高危安全隐患<div class="stat-val" style="color: #ff4d4f">{{ s.high_risk }}</div></div>
            <div class="card">离线异常设备<div class="stat-val" style="color: #faad14">2</div></div>
        </div>
        <div class="chart-grid">
            <div class="card">{{ pie_html|safe }}</div>
            <div class="card">{{ bar_html|safe }}</div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    scan_s = get_real_scan_stats()
    hl7_s = get_real_hl7_stats()
    
    # 饼图：展示在线与风险占比
    pie = (Pie(init_opts=opts.InitOpts(width="100%", height="400px"))
           .add("", [("安全运行", scan_s['online']), ("高危风险", scan_s['high_risk'])])
           .set_colors(["#2ecc71", "#e74c3c"])
           .set_global_opts(title_opts=opts.TitleOpts(title="全网资产安全态势", pos_left="center")))
    
    # 柱状图：展示科室分布
    bar = (Bar(init_opts=opts.InitOpts(width="100%", height="400px"))
           .add_xaxis(hl7_s['depts'])
           .add_yaxis("资产数量", hl7_s['counts'], color="#3498db")
           .set_global_opts(title_opts=opts.TitleOpts(title="医疗资产科室分布", pos_left="center")))
    
    return render_template_string(HTML_TEMPLATE, s=scan_s, pie_html=pie.render_embed(), bar_html=bar.render_embed())

if __name__ == "__main__":
    # 关闭多余日志输出
    import logging
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    print("[*] 态势感知看板已启动，请访问 http://127.0.0.1:5000")
    app.run(debug=False, port=5000)