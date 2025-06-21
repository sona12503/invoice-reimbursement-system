def invoice_analysis_prompt(policy_text, invoice_text):
    return f"""
You are a smart assistant helping with invoice reimbursements.

Your job is to read both the reimbursement policy and an employee invoice and decide:

1. Should the invoice be Fully Reimbursed, Partially Reimbursed, or Declined?
2. Explain your reasoning in 2–3 lines based on the policy.

---
Reimbursement Policy:
{policy_text}

---
Invoice:
{invoice_text}

---
Respond in this format:
Status: <Fully/Partially/Declined>
Reason: <your reason here>
"""
