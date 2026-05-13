# 医疗安全态势感知看板 (Medical Security Dashboard) 🖥️📈

本项目是医疗网络安全体系的展示终端，通过 Flask 框架实现了与底层探测工具的实时数据联动。

## 🌟 核心特性
- **多源数据融合**：实时解析项目一 (Scanner) 的 JSON 扫描报告与项目二 (Parser) 的 Excel 业务数据。
- **动态风险预警**：自动统计高危端口开放情况，实现安全状态的秒级感知。
- **可视化交互**：基于 `pyecharts` 构建资产分布图与安全态势饼图，直观展示科室安全画像。

## 🛠️ 技术栈
- **后端**：Python / Flask
- **前端**：HTML5 / CSS3 / Echarts
- **数据处理**：Pandas, JSON

## 📊 看板展示内容
1. **资产概览**：在线设备总数、高危隐患实时计数。
2. **安全分布**：基于 Nmap 扫描结果的风险比例分析。
3. **业务分布**：基于 HL7 协议解析的科室资产分布情况。
<img width="1724" height="904" alt="屏幕截图 2026-05-13 111342" src="https://github.com/user-attachments/assets/d048a506-9765-4f2e-9790-a1c6553c84fe" />
<img width="2559" height="979" alt="屏幕截图 2026-05-13 111402" src="https://github.com/user-attachments/assets/b43f2843-506c-47ad-98ea-7e6ec11107bb" />
