import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from pdf_utils import extract_text_from_pdf, extract_invoices_from_zip
from prompts import invoice_analysis_prompt
import os

llm = ChatOpenAI(temperature=0)
embedding_model = OpenAIEmbeddings()

def analyze_invoices(policy_pdf, invoices_zip, employee_name, vector_store_path="faiss_index"):
    policy_text = extract_text_from_pdf(policy_pdf)
    invoice_paths = extract_invoices_from_zip(invoices_zip)
    
    texts = []
    metadatas = []

    for invoice_path in invoice_paths:
        invoice_text = extract_text_from_pdf(invoice_path)
        prompt = invoice_analysis_prompt(policy_text, invoice_text)
        response = llm.predict(prompt)

        status = "Unknown"
        reason = "Could not parse"
        for line in response.split("\n"):
            if line.lower().startswith("status:"):
                status = line.split(":")[1].strip()
            if line.lower().startswith("reason:"):
                reason = line.split(":")[1].strip()

        metadata = {
            "employee_name": employee_name,
            "invoice_file": os.path.basename(invoice_path),
            "status": status,
            "reason": reason
        }

        texts.append(invoice_text + " " + reason)
        metadatas.append(metadata)

    # Create FAISS vectorstore
    vectorstore = FAISS.from_texts(texts, embedding_model, metadatas=metadatas)
    vectorstore.save_local(vector_store_path)

    return metadatas
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import os
import shutil
from analyze import analyze_invoices
from chatbot import query_chatbot

app = FastAPI()

@app.post("/analyze-invoices/")
async def analyze_invoices_api(policy: UploadFile, invoices: UploadFile, employee_name: str = Form(...)):
    try:
        os.makedirs("uploads", exist_ok=True)

        policy_path = os.path.join("uploads", policy.filename)
        invoices_path = os.path.join("uploads", invoices.filename)

        with open(policy_path, "wb") as f:
            shutil.copyfileobj(policy.file, f)

        with open(invoices_path, "wb") as f:
            shutil.copyfileobj(invoices.file, f)

        # Call analysis
        results = analyze_invoices(policy_path, invoices_path, employee_name)
        return JSONResponse(content={"success": True, "results": results})
    
    except Exception as e:
        print("🔥 ERROR during invoice analysis:", str(e))  # Show error in terminal
        return JSONResponse(status_code=500, content={"error": str(e)})
