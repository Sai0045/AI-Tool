# 🧠 AI Exam Question Generator

### LLM-Based Intelligent Question Paper Generation System

---

## 📌 Overview

AI Exam Question Generator is an intelligent system that automatically generates exam question papers from a given syllabus using Large Language Models (LLMs).

The system uses structured pipelines, Bloom’s Taxonomy, and prompt engineering to generate high-quality, exam-oriented questions along with marking schemes and formatted outputs.

---

## 🚀 Key Features

* 📚 Generates question papers from syllabus input
* 🧠 Uses LLM (Gemini API) for intelligent question generation
* 🎯 Assigns Bloom’s Taxonomy levels to questions
* 📝 Automatically creates marking schemes
* 📄 Exports outputs in Markdown and JSON formats
* ⚙️ Modular pipeline-based architecture
* ✅ Validation of generated content

---

## 🏗️ System Workflow

```
Syllabus Input
      ↓
Syllabus Parser
      ↓
Prompt Builder
      ↓
LLM Pipeline (Gemini API)
      ↓
Question Generator
      ↓
Bloom’s Level Assignment
      ↓
Validation
      ↓
Export (Question Paper + Marking Scheme)
```

---

## 📂 Project Structure

```
ai-exam-question-generator/
│
├── app.py                         # Main application entry point  
├── list_models.py                 # Lists available LLM models  
├── requirements.txt               # Dependencies  
│
├── data/  
│   ├── sample_syllabus.txt        # Input syllabus  
│   └── sample_pattern.json        # Question pattern  
│
├── outputs/  
│   ├── question_paper.md          # Generated question paper  
│   ├── marking_scheme.md          # Generated marking scheme  
│   └── generated_paper.json       # Structured output  
│
├── src/  
│   ├── generator.py               # Core question generation logic  
│   ├── llm_pipeline.py            # LLM workflow handling  
│   ├── gemini_client.py           # Gemini API integration  
│   ├── prompt_builder.py          # Prompt construction  
│   ├── syllabus_parser.py         # Parses syllabus input  
│   ├── bloom.py                   # Bloom’s taxonomy definitions  
│   ├── bloom_assigner.py          # Assigns Bloom levels  
│   ├── validators.py              # Output validation  
│   ├── exporters.py               # Export logic  
│   ├── pdf_utils.py               # PDF utilities  
│   └── paper_schema.py            # Data structure definitions  
```

---

## 🛠️ Technologies Used

* **Python** 🐍
* **LLM (Gemini API)**
* **Prompt Engineering**
* **Bloom’s Taxonomy**
* **JSON / Markdown Processing**

---

## ⚙️ Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/Sai0045/AI-Tool.git
cd AI-Tool
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
python app.py
```

---

## 📊 Input & Output

### Input:

* Syllabus (`.txt`)
* Question pattern (`.json`)

### Output:

* 📄 Question Paper (`.md`)
* 📝 Marking Scheme (`.md`)
* 📊 Structured JSON Output

---

## 🎯 Use Cases

* Automated exam paper generation
* Academic institutions
* Practice test creation
* AI-based education tools

---

## 📈 Future Enhancements

* 🌐 Web interface using Streamlit
* 📄 Direct PDF export
* 🌍 Multi-language support
* 📊 Difficulty control and customization

---

## 👨‍💻 Author

**Sairaj Abhale**
AI & ML Student | AI Developer

---

## 📜 License

This project is open-source and available for educational use.
