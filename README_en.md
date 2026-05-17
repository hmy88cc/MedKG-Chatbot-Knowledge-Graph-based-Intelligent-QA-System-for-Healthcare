# Medical Knowledge Graph-based Intelligent Q&A System v2.0

> "Keeping humans always rational is indeed a luxury." —— MOSS, The Wandering Earth

![](./pictures/082501.png)

## Overview

This project is an intelligent medical dialogue system based on knowledge graphs and deep learning. It employs BiLSTM-CRF for Named Entity Recognition (NER), TextCNN for intent classification, and Neo4j graph database for storing and querying medical knowledge, enabling natural language question-and-answer interactions.

**v2.0 New Features**:
- Supports 18 question types
- Multi-turn dialogue with context memory
- Complete logging system for debugging
- Configuration-driven deployment
- Enhanced exception handling for stability
- Type annotations for better code quality
- Knowledge graph expanded to 10 entity types and 13 relation types

## Features

### Core Capabilities

| Module | Description |
|---------|------|
| Knowledge Graph Construction | Crawls medical websites to build a graph with ~50K entities and ~390K relations |
| Named Entity Recognition | BiLSTM-CRF model recognizing 10 entity types (F1=0.98) |
| Intent Classification | TextCNN model supporting 18 question type classifications |
| Knowledge Query | Cypher queries against Neo4j graph database for precise answers |
| Multi-turn Dialogue | Context-aware, handles ellipsis and coreference |

### Supported Question Types (18 Types)

| # | Type | Example Question |
|------|------|----------|
| 1 | disease_symptom | What are the symptoms of a cold? |
| 2 | symptom_curway | How to treat a fever? |
| 3 | symptom_disease | What disease might cause a headache? |
| 4 | disease_drug | What medicine should I take for hypertension? |
| 5 | drug_disease | What does aspirin treat? |
| 6 | disease_check | What tests are needed for diabetes? |
| 7 | disease_prevent | How to prevent influenza? |
| 8 | disease_lasttime | How long does pneumonia treatment take? |
| 9 | disease_cureway | What are the treatment methods for gastritis? |
| 10 | disease_cause | What causes diabetes? |
| 11 | disease_acompany | What are the complications of hypertension? |
| 12 | disease_desc | What is coronary heart disease? |
| 13 | drug_side_effect | What are the side effects of aspirin? |
| 14 | drug_usage | How to use this medicine? |
| 15 | department_recommend | Which department should I visit for chest tightness? |
| 16 | disease_body_part | Which body parts does hepatitis affect? |
| 17 | disease_surgery | What surgery is needed for appendicitis? |
| 18 | disease_insurance | Is diabetes covered by insurance? |

### Knowledge Graph Scale

**Entity Types** (10 types, ~50K entities):

| Entity Type | Meaning | Count | Example |
|:---------|:--------:|:--------:|:-----|
| Disease | Disease | 9,200 | Thromboangiitis obliterans |
| Drug | Medicine | 4,100 | Jingwanhong Hemorrhoid Ointment |
| Symptom | Symptom | 6,300 | Breast tissue hypertrophy |
| Food | Food | 5,200 | Tomato beef ball soup |
| Check | Examination | 3,600 | Bronchography |
| Department | Department | 62 | Plastic Surgery |
| Producer | Manufacturer | 18,500 | Tongyao Pharmaceutical |
| BodyPart | Body Part | 1,200 | Liver; Heart |
| Surgery | Surgery | 850 | Laparoscopic surgery |
| Insurance | Insurance Type | 8 | Urban employee insurance |

**Relation Types** (13 types, ~390K relations):

| Relation Type | Meaning | Count |
|:---------|:--------:|:--------:|
| has_symptom | Disease-Symptom | 12,500 |
| common_drug | Common Drug | 22,800 |
| recommand_drug | Recommended Drug | 85,000 |
| need_check | Required Check | 58,500 |
| acompany_with | Complication | 18,600 |
| do_eat | Recommended Food | 38,400 |
| no_eat | Avoid Food | 35,800 |
| recommand_eat | Suggested Food | 34,500 |
| belongs_to | Belongs to Department | 15,200 |
| drugs_of | Manufacturer-Drug | 28,800 |
| affects_body_part | Affected Body Part | 16,200 |
| requires_surgery | Required Surgery | 12,600 |
| covered_by_insurance | Insurance Coverage | 10,500 |

Total: ~390K relations.

## Technical Architecture

### Tech Stack

```
Python 3.6.8
TensorFlow 1.10.0
Neo4j 3.2.2
py2neo 3.1.1
jieba 0.39
numpy 1.17.0
pyyaml 5.4+
```

### System Architecture

```
User Input → Dialogue Processing → NER → Intent Classification → 
Cypher Generation → Neo4j Query → Answer Generation → User Output
                     ↑                                      ↓
                     └────── Context Memory ←───────────────┘
```

### Deep Learning Models

**1. BiLSTM-CRF (Named Entity Recognition)**

| Parameter | Value |
|------|-----|
| LSTM Hidden Size | 650 |
| Learning Rate | 0.00075 |
| Batch Size | 100 |
| Sentence Length | 25 |
| Tag Numbers | 31 |
| Dropout | 0.5 |
| F1 Score | 0.98 |

**2. TextCNN (Intent Classification)**

| Parameter | Value |
|------|-----|
| Embedding Dimension | 200 |
| Filter Sizes | 2, 3, 4 |
| Number of Filters | 128 |
| Max Sentence Length | 20 |
| Number of Classes | 18 |

## Quick Start

### 1. Environment Setup

```bash
pip install -r requirements.txt
```

### 2. Configure Neo4j

Edit `config.yaml` to configure Neo4j connection:

```yaml
neo4j:
  host: "your_neo4j_host"
  http_port: 7474
  user: "neo4j"
  password: "your_password"
```

### 3. Build Knowledge Graph (Optional)

Skip this step if Neo4j data already exists:

```bash
python build_medicalgraph.py
```

### 4. Start the Q&A System

```bash
python chatbot_graph.py
```

### 5. Interactive Usage

```
============================================================
Hello, I'm the medical chatbot Li Wen φ(゜▽゜*)♪
What would you like to know? I hope my answers can help you!
Type "quit" or "exit" to exit, "clear" to clear context
============================================================
User: What are the symptoms of a cold?
Li Wen: Symptoms of a cold include: fever; headache; nasal congestion...

User: How to treat it?
Li Wen: Treatment for a cold may include: medication; supportive therapy
```

## Project Structure

```
medical_chatbot/
├── config.yaml                    # System configuration file
├── config_loader.py               # Configuration loader
├── logger_utils.py                # Logging utility
├── dialogue_manager.py            # Multi-turn dialogue manager
├── chatbot_graph.py               # Main Q&A system program
├── question_analysis.py           # Question analyzer (NER + intent classification)
├── question_parser.py             # Question parser (generates Cypher queries)
├── answer_search.py               # Answer search and generation
├── BiLSTM_CRF.py                  # BiLSTM-CRF network model
├── text_cnn.py                    # TextCNN network model
├── nerApp.py                      # NER application script
├── nerUtils.py                    # NER utility functions
├── classifyApp.py                 # Classification application script
├── classifyUtils.py               # Classification utility functions
├── build_medicalgraph.py          # Knowledge graph construction script
├── data/
│   └── medical.json               # Medical knowledge data
├── data_ai/
│   ├── cbowData/                  # Word embedding data
│   ├── nerModel/                  # NER model
│   └── classifyModel/             # Classification model
├── dict/                          # Entity dictionaries
└── prepare_data/                  # Data preparation tools
    ├── data_spider.py             # Web scraper
    ├── build_data.py              # Data processing
    └── max_cut.py                 # Tokenization tool
```

## Configuration

### config.yaml Key Settings

```yaml
# Neo4j Database Configuration
neo4j:
  host: "172.24.30.243"
  http_port: 7474
  user: "neo4j"
  password: "12345"

# Model Configuration
model:
  gpu_memory_fraction: 0.3
  ner:
    model_path: "./data_ai/nerModel/"
    hidden_size: 650
  classifier:
    model_path: "./data_ai/classifyModel"
    num_classes: 18

# Dialogue Configuration
chatbot:
  answer_limit: 20
  dialogue:
    enable_context: true
    max_context_turns: 5
    context_timeout: 300

# Logging Configuration
logging:
  level: "INFO"
  file: "logs/chatbot.log"
```

## Multi-turn Dialogue

The system supports simple multi-turn dialogue, handling ellipsis and coreference:

```
User: What medicine should I take for a cold?
Li Wen: Common medications for a cold include: Amoxicillin; Ganmaoling...

User: What are the side effects?  # System understands this refers to cold medicine
Li Wen: Side effects of Amoxicillin include: ...
```

**Dialogue Commands**:
- `clear` - Clear dialogue context
- `summary` - View dialogue history summary
- `quit` / `exit` - Exit the system

## Logging System

The system uses Python logging module, supporting:
- Console output
- File logging (auto-rotation, max 10MB)
- Log levels (DEBUG/INFO/WARNING/ERROR)

Log file location: `logs/chatbot.log`

## Development Guide

### Adding New Question Types

1. Add label mapping in `config.yaml`
2. Add processing logic in `question_parser.py` `parser_main()`
3. Add Cypher template in `question_parser.py` `sql_transfer()`
4. Add response template in `answer_search.py` `answer_prettify()`

### Extending Entity Recognition Types

1. Update `entity_types` in `config.yaml`
2. Update `state2entityType` mapping in `question_analysis.py`
3. Prepare new training data and retrain the model

## FAQ

**Q: Model loading fails?**
A: Check if TensorFlow version is 1.10.0 and model files are complete.

**Q: Neo4j connection fails?**
A: Verify connection settings in `config.yaml` and ensure Neo4j service is running.

**Q: Inaccurate answers?**
A: May need to expand training data or adjust model parameters.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Data sourced from xywy.com (寻医问药网站)
- Thanks to the open-source community for contributions

## Contact

For questions or suggestions, feel free to submit an Issue or Pull Request.
