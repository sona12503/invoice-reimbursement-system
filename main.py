from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import os
import shutil
from analyze import analyze_invoices
from chatbot import query_chatbot

app = FastAPI()

@app.post("/analyze-invoices/")
async def analyze_invoices_api(policy: UploadFile, invoices: UploadFile, employee_name: str = Form(...)):
    os.makedirs("uploads", exist_ok=True)
    
    policy_path = f"uploads/{policy.filename}"
    invoices_path = f"uploads/{invoices.filename}"
    
    with open(policy_path, "wb") as f:
        shutil.copyfileobj(policy.file, f)
    with open(invoices_path, "wb") as f:
        shutil.copyfileobj(invoices.file, f)
    
    results = analyze_invoices(policy_path, invoices_path, employee_name)
    return JSONResponse(content={"success": True, "results": results})

@app.post("/chat/")
async def chat(query: str = Form(...)):
    answer = query_chatbot(query)
    return JSONResponse(content={"response": answer})
@app.post("/analyze-invoices/")
async def analyze_invoices_api(policy: UploadFile, invoices: UploadFile, employee_name: str = Form(...)):
    try:
        os.makedirs("uploads", exist_ok=True)
        
        policy_path = f"uploads/{policy.filename}"
        invoices_path = f"uploads/{invoices.filename}"
        
        with open(policy_path, "wb") as f:
            shutil.copyfileobj(policy.file, f)
        with open(invoices_path, "wb") as f:
            shutil.copyfileobj(invoices.file, f)
        
        results = analyze_invoices(policy_path, invoices_path, employee_name)
        return JSONResponse(content={"success": True, "results": results})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})