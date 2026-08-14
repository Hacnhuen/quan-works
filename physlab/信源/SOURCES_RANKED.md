# === 信源分级清单 (S>A>B, 溯源链 B→A→S) · 高中物理教学 ===
# 由 SOURCES_RANKED 技能生成（双轨获取 × 三级评级）
# 轨道A=本地(physlab/ phys_ladder_sources 等) / 轨道B=网上(课标/教材/高考/仿真/各国物理)
# 轨道B-联网实测：使用 agent-reach 技能 (Exa搜索 + B站bili-cli) 于 2026-08-07 获取，新增条目标 [exa]/[bili]
# topic: 高中物理教学  output_dir: physlab/信源/

## ---- S级：原始凭证（最高优先） ----

# —— 轨道A 本地一手（零噪声、已沉淀、可复现）——
local/phys_ladder_sources.md|高中物理/课标结构+常数公式|S|done  → 溯源: 普通高中物理课程标准2017版2025修订
local/junior_ladder_sources.md|初中物理/义务教育课标2022|S|done  → 溯源: 义务教育物理课程标准2022
local/physlab/L0-L4馆|高中物理/五层阶梯全站|S|done
local/AI备课/物理教学名家思想|教学方法/名家实证|S|done
local/AI备课/AI物理教练工作流|教学方法/AI教练|S|done

# —— 轨道B 网上：课程标准与教材一手（教学权威根）——
moe.gov.cn|课标/教育部官方|S|done  → 普通高中物理课程标准(2017版2025修订)
pep.com.cn|教材/人教版物理课本|S|done  → 人民教育出版社官方
gz.gzedu.gov.cn|高考/真题与考纲|S|done  → 各省教育考试院
ncpu.edu.cn|教研/课程教材研究所|S|done

# —— 轨道B 网上：国际教材与开放课件（一手）——
openstax.org/physics|教材/OpenStax Physics(英文开放)|S|done
phys.libretexts.org|教材/Physics LibreTexts|S|done
ocw.mit.edu/physics|教学/MIT开放课程物理|S|done
khanacademy.org/science/physics|教学/可汗学院物理|S|done
csrc.ac.cn|科研/中科院物理所|S|done

# —— 轨道B 网上：仿真与实验一手（教学可复现）——
phet.colorado.edu|仿真/PhET互动实验|S|done  → 科罗拉多大学(诺奖得主组)
physionet.org|数据/物理实验数据集|S|todo
arxiv.org/abs/physics-ed|教研/物理教育研究预印本|S|todo
# —— 轨道B-联网实测(agent-reach: Exa) 2026-08-07 ——
pmc.scnu.edu.cn|教材/华南师大国家教材基地·各版汇总[exa]|S|done  → 溯源: 国家智慧教育平台SmartEdu + 课标2017-2025修订
enjoyphysics.cn/Article3616|课标/高中物理课程标准2025修订[exa]|S|done  → 溯源: 普通高中物理课程标准(2017版2025修订)
smartedu.cn|教材/国家智慧教育平台数字教材[exa]|S|done

## ---- A级：权威认证（同行评议/正式出版） ----

# —— 轨道B 期刊与出版（物理教育/学科）——
aps.org/prper|教研/物理教育研究期刊(AIP)|A|done  → Physical Review PER
iop.org/physed|教研/Physics Education(IOP)|A|done
springer.com/physics|学科/物理教材丛书|A|done
science.org|综合/原始研究|A|done
nature.com|综合/原始研究|A|done
pnas.org|综合/院刊|A|done
cnki.net|中文学术/物理教育论文|A|done

# —— 轨道A 本地沉淀（经审结构）——
local/phys_ladder_sources/公式清单|高中物理/核心公式(可复算)|A|done  → 同源课标
local/AI备课/解题分析步骤|教学方法/解题步骤实证|A|done

## ---- B级：专业解读（须标注溯源） ----

# —— 轨道B 科普/教学解读（须溯源到 S/A）——
zhihu.com/physics|科普/物理问答|B|todo  → 溯源: S.pep.com.cn / A.cnki.net(须筛高赞溯源)
bilibili.com/物理科普|科普/视频解读|B|todo  → 溯源: S.pep.com.cn / S.phet.colorado.edu
物理之友/期刊|教研/中学物理教辅|B|todo  → 溯源: S.moe.gov.cn / A.cnki.net
3blue1brown.com|教学/直观推导(英语)|B|todo  → 溯源: S.arxiv.org / S.openstax.org
veritasium.com|科普/实验解读|B|todo  → 溯源: A.nature.com / S.phet.colorado.edu
scientificamerican.com/physics|科普/物理前沿|B|todo  → 溯源: A.science.org
leet物理/公众号|科普/中学物理|B|retry  → 溯源: 须补 S.moe.gov.cn 编号
# —— 轨道B-联网实测(agent-reach: B站 bili-cli) 2026-08-07 ——
bilibili.com/BV1yx4y1a7Wh|教学/高中物理实验系统课(北大学长跳跳,287万播)[bili]|B|done  → 溯源: S.pmc.scnu.edu.cn(必做实验)
bilibili.com/BV1664y1M7PZ|教学/高考物理实验篇(陈老师敲黑板,78万播)[bili]|B|done  → 溯源: S.enjoyphysics.cn(必做实验)
bilibili.com/BV1qf4y1b7G2|教学/高考物理题型剖析(阅优课,32万播)[bili]|B|todo  → 溯源: S.pep.com.cn(教材体系)
bilibili.com/BV1vY4y1F7cu|教学/初中物理实验操作(万唯,79万播)[bili]|B|todo  → 溯源: S.moe.gov.cn(义教课标2022)

# —— 轨道B 验证元源（校验教学信源）——
semanticscholar.org|验证/物理教育引用图|A|done
retractionwatch.com|验证/证伪撤稿|B|todo
archive.org|验证/失效页镜像|S|done
