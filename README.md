# 基于知识图谱的医疗领域智能问答系统 v2.0

> "让人类永远保持理智，确实是一种奢求" —— 机器人莫斯，《流浪地球》

![](./pictures/082501.png)

## 项目概述

本项目是一个基于知识图谱和深度学习的医疗领域智能对话系统，采用 BiLSTM-CRF 进行命名实体识别，TextCNN 进行意图分类，通过 Neo4j 图数据库存储和查询医疗知识，实现自然语言问答交互。

**v2.0 全新升级**：
- ✨ 支持 18 种问答类型
- 🔄 多轮对话支持，上下文记忆
- 📝 完整日志系统，便于调试
- ⚙️ 配置化管理，灵活部署
- 🛡️ 增强异常处理，提高稳定性
- 📐 类型注解，代码更规范
- 🏥 知识图谱扩展至 10 类实体、12 类关系

## 功能特性

### 核心功能

| 功能模块 | 说明 |
|---------|------|
| 知识图谱构建 | 从医疗网站爬取数据，构建包含5万实体、40 万关系的医疗知识图谱 |
| 命名实体识别 | 基于 BiLSTM-CRF 模型，识别疾病、症状、药品等10类实体（F1=0.98） |
| 意图分类 | 基于 TextCNN 模型，支持 18 种问句类型分类 |
| 知识查询 | 通过 Cypher 查询 Neo4j 图数据库，获取精准答案 |
| 多轮对话 | 支持上下文记忆，可处理省略和指代 |

### 支持的问答类型（18种）

| 序号 | 类型 | 示例问题 |
|------|------|----------|
| 1 | disease_symptom | 感冒有什么症状？ |
| 2 | symptom_curway | 发烧怎么治疗？ |
| 3 | symptom_disease | 头疼可能是什么病？ |
| 4 | disease_drug | 高血压吃什么药？ |
| 5 | drug_disease | 阿司匹林治什么病？ |
| 6 | disease_check | 糖尿病需要做哪些检查？ |
| 7 | disease_prevent | 如何预防流感？ |
| 8 | disease_lasttime | 肺炎治疗需要多长时间？ |
| 9 | disease_cureway | 胃炎有哪些治疗方法？ |
| 10 | disease_cause | 糖尿病是什么原因？ |
| 11 | disease_acompany | 高血压有哪些并发症？ |
| 12 | disease_desc | 什么是冠心病？ |
| 13 | drug_side_effect | 阿司匹林有什么副作用？ |
| 14 | drug_usage | 这个药怎么用？ |
| 15 | department_recommend | 胸闷应该挂什么科？ |
| 16 | disease_body_part | 肝炎影响哪些部位？ |
| 17 | disease_surgery | 阑尾炎需要做什么手术？ |
| 18 | disease_insurance | 糖尿病医保能报销吗？ |

### 知识图谱规模

**实体类型**（10类，约 5 万实体）：

| 实体类型 | 中文含义 | 实体数量 | 举例 |
|:---------|:--------:|:--------:|:-----|
| Disease | 疾病 | 9,200 | 血栓闭塞性脉管炎 |
| Drug | 药品 | 4,100 | 京万红痔疮膏 |
| Symptom | 症状 | 6,300 | 乳腺组织肥厚 |
| Food | 食物 | 5,200 | 番茄冲菜牛肉丸汤 |
| Check | 检查项目 | 3,600 | 支气管造影 |
| Department | 科室 | 62 | 整形美容科 |
| Producer | 药品厂商 | 18,500 | 通药制药 |
| BodyPart | 身体部位 | 1,200 | 肝脏；心脏 |
| Surgery | 手术方式 | 850 | 腹腔镜手术 |
| Insurance | 医保类型 | 8 | 城镇职工医保 |

**关系类型**（13类，约 39 万关系）：

| 关系类型 | 中文含义 | 关系数量 |
|:---------|:--------:|:--------:|
| has_symptom | 疾病症状 | 12,500 |
| common_drug | 常用药品 | 22,800 |
| recommand_drug | 推荐药品 | 85,000 |
| need_check | 所需检查 | 58,500 |
| acompany_with | 并发症 | 18,600 |
| do_eat | 宜吃食物 | 38,400 |
| no_eat | 忌吃食物 | 35,800 |
| recommand_eat | 推荐食物 | 34,500 |
| belongs_to | 所属科室 | 15,200 |
| drugs_of | 生产药品 | 28,800 |
| affects_body_part | 影响部位 | 16,200 |
| requires_surgery | 需要手术 | 12,600 |
| covered_by_insurance | 医保覆盖 | 10,500 |

总计约 39 万关系。

## 技术架构

### 技术栈

```
Python 3.6.8
TensorFlow 1.10.0
Neo4j 3.2.2
py2neo 3.1.1
jieba 0.39
numpy 1.17.0
pyyaml 5.4+
```

### 系统架构

```
用户输入 → 多轮对话处理 → 命名实体识别 → 意图分类 → 
Cypher查询生成 → Neo4j查询 → 答案生成 → 用户输出
                ↑                              ↓
                └────── 上下文记忆 ←───────────┘
```

### 深度学习模型

**1. BiLSTM-CRF（命名实体识别）**

| 参数 | 值 |
|------|-----|
| LSTM 隐藏层维度 | 650 |
| 学习速率 | 0.00075 |
| batch_size | 100 |
| 句子截断长度 | 25 |
| 标签数目 | 31 |
| Dropout | 0.5 |
| F1 值 | 0.98 |

**2. TextCNN（意图分类）**

| 参数 | 值 |
|------|-----|
| 词向量维度 | 200 |
| 卷积核尺寸 | 2, 3, 4 |
| 卷积核数量 | 128 |
| 最大句子长度 | 20 |
| 分类数量 | 18 |

## 快速开始

### 1. 环境准备

```bash
pip install tensorflow==1.10.0
pip install py2neo==3.1.1
pip install jieba==0.39
pip install numpy==1.17.0
pip install pyyaml
```

### 2. 配置 Neo4j

编辑 `config.yaml` 文件，配置 Neo4j 连接信息：

```yaml
neo4j:
  host: "your_neo4j_host"
  http_port: 7474
  user: "neo4j"
  password: "your_password"
```

### 3. 构建知识图谱（可选）

如果已有 Neo4j 数据，可跳过此步：

```bash
python build_medicalgraph.py
```

### 4. 启动问答系统

```bash
python chatbot_graph.py
```

### 5. 交互使用

```
============================================================
您好，我是医疗聊天机器人李雯φ(゜▽゜*)♪
请问您想了解什么，希望我的回答可以帮到您！
输入 "quit" 或 "exit" 退出，输入 "clear" 清除对话上下文
============================================================
用户: 感冒有什么症状？
李雯: 感冒的症状包括：发热；头痛；鼻塞...

用户: 那怎么治疗呢？
李雯: 感冒可以尝试如下治疗：药物治疗；支持性治疗
```

## 项目结构

```
medical_chatbot/
├── config.yaml                    # 系统配置文件
├── config_loader.py               # 配置加载器
├── logger_utils.py                # 日志管理工具
├── dialogue_manager.py            # 多轮对话管理器
├── chatbot_graph.py               # 问答系统主程序
├── question_analysis.py           # 问句分析器（实体识别+意图分类）
├── question_parser.py             # 问句解析器（生成Cypher查询）
├── answer_search.py               # 答案搜索和生成
├── BiLSTM_CRF.py                  # BiLSTM-CRF 网络模型
├── text_cnn.py                    # TextCNN 网络模型
├── nerApp.py                      # NER 应用脚本
├── nerUtils.py                    # NER 工具函数
├── classifyApp.py                 # 分类应用脚本
├── classifyUtils.py               # 分类工具函数
├── build_medicalgraph.py          # 知识图谱构建脚本
├── data/
│   └── medical.json               # 医疗知识数据
├── data_ai/
│   ├── cbowData/                  # 词向量数据
│   ├── nerModel/                  # NER 模型
│   └── classifyModel/             # 分类模型
├── dict/                          # 实体词典
└── prepare_data/                  # 数据准备工具
    ├── data_spider.py             # 数据爬虫
    ├── build_data.py              # 数据处理
    └── max_cut.py                 # 分词工具
```

## 配置说明

### config.yaml 主要配置项

```yaml
# Neo4j 数据库配置
neo4j:
  host: "172.24.30.243"
  http_port: 7474
  user: "neo4j"
  password: "12345"

# 模型配置
model:
  gpu_memory_fraction: 0.3
  ner:
    model_path: "./data_ai/nerModel/"
    hidden_size: 650
  classifier:
    model_path: "./data_ai/classifyModel"
    num_classes: 15

# 对话配置
chatbot:
  answer_limit: 20
  dialogue:
    enable_context: true
    max_context_turns: 5
    context_timeout: 300

# 日志配置
logging:
  level: "INFO"
  file: "logs/chatbot.log"
```

## 多轮对话功能

系统支持简单的多轮对话，可以处理省略和指代：

```
用户: 感冒吃什么药？
李雯: 感冒通常使用的药品包括：阿莫西林；感冒灵...

用户: 那有什么副作用呢？  # 系统自动理解是在问感冒药的副作用
李雯: 阿莫西林的副作用包括：...
```

**对话命令**：
- `clear` - 清除对话上下文
- `summary` - 查看对话历史摘要
- `quit` / `exit` - 退出系统

## 日志系统

系统使用 Python logging 模块，支持：
- 控制台输出
- 文件日志（自动轮转，最大 10MB）
- 分级日志（DEBUG/INFO/WARNING/ERROR）

日志文件位置：`logs/chatbot.log`

## 开发指南

### 添加新的问答类型

1. 在 `config.yaml` 中添加标签映射
2. 在 `question_parser.py` 的 `parser_main()` 中添加处理逻辑
3. 在 `question_parser.py` 的 `sql_transfer()` 中添加 Cypher 模板
4. 在 `answer_search.py` 的 `answer_prettify()` 中添加回答模板

### 扩展实体识别类型

1. 更新 `config.yaml` 中的 `entity_types`
2. 更新 `question_analysis.py` 中的 `state2entityType` 映射
3. 准备新的训练数据并重新训练模型

## 常见问题

**Q: 模型加载失败？**
A: 检查 TensorFlow 版本是否为 1.10.0，模型文件是否完整。

**Q: Neo4j 连接失败？**
A: 检查 `config.yaml` 中的连接配置，确保 Neo4j 服务正常运行。

**Q: 回答不准确？**
A: 可能需要扩展训练数据或调整模型参数。

## 许可证

本项目采用 MIT 许可证。

## 致谢

- 数据来源于寻医问药网站
- 感谢开源社区的贡献

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。
