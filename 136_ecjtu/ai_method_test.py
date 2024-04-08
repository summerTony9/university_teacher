from transformers import AutoModelForQuestionAnswering,AutoTokenizer,pipeline
model = AutoModelForQuestionAnswering.from_pretrained('uer/roberta-base-chinese-extractive-qa')
tokenizer = AutoTokenizer.from_pretrained('uer/roberta-base-chinese-extractive-qa')
QA = pipeline('question-answering', model=model, tokenizer=tokenizer)
QA_input = {
    'question': "肖乾的研究方向是什么？",
    'context': "肖乾，男，博士，博士生导师，二级教授，华东交通大学党委委员、副校长，享受国务院特殊津贴专家。"
               "近五年来，主持国家自然科学基金面向项目等3项、江西省自然科学基金重点项目等省部级项目近10项。"
               "企业横向课题等近20项，项目经费1500余万元。"
               "在Wear、AppliedSurfaceScience、铁道学报、中国铁道科学、西南交通大学学报等国内外刊物发表学术论文60余篇，"
               "其中SCI/EI检索近40篇。相关科研成果获江西省科技进步一等奖、二等奖、全国詹天佑铁道科学技术奖、茅以升铁道科技奖、"
               "江西省青年科技创新项目奖、第五届江西省高校科技成果二等奖。获批专利近20余项，其中3项在企业成功实现转化。"
               "目前主要研究方向为轨道车辆运行品质分析与评价；轨道车辆运维装备研究与开发；"
               "CAX/VR/AR。交通运输部交通青年科技英才茅以升铁道科学技术奖江西省科技进步一等奖"
               "江西省教学成果一等奖江西省虚拟现实产业创新团队负责人江西省高水平本科教学团队负责人"
               "江西省“井冈学者”特聘教授江西省百千万人才工程省级人选詹天佑铁道科学技术奖青年奖江西省杰出青年基金资助人选江西省青年科技创新项目一等奖、优胜奖江西省第五届高等学校科技成果奖江西省高校优秀共产党员江西省首届专业学位研究生在职业能力竞赛优秀指导教师江西省第五届三维数字建模大赛优秀指导教师江西省第三届三维数字建模大赛优秀指导教师华东交通大学天佑优秀人才华东交通大学首届优秀硕士生导师华东交通大学优秀共产党员、最美共产党员"}
print(QA(QA_input))
