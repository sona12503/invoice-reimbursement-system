# invoice-reimbursement-system
# Invoice Reimbursement System

An AI-powered system to analyze employee invoice reimbursements using LLMs, FastAPI, and vector search.

## 🔧 Features
- Uploads HR policy and ZIP of invoices
- Uses OpenAI LLMs to determine:
  - Fully Reimbursed
  - Partially Reimbursed
  - Declined
- Stores analysis in vector DB (e.g., FAISS)
- RAG-based chatbot for querying invoices

## 📦 Tech Stack
- Python, FastAPI
- LangChain, OpenAI API
- FAISS Vector Store
- PyMuPDF for PDF parsing

## 🚀 Endpoints
### `/analyze-invoices/`
- Input: HR policy PDF + ZIP of invoices
- Output: JSON analysis of each invoice

### `/chat/`
- Input: Natural language query
- Output: Relevant invoice info using RAG

## ⚙️ How to Run

```bash
git clone https://github.com/sona12503/invoice-reimbursement-system.git
cd invoice-reimbursement-system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
