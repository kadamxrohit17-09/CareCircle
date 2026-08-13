import os
import json
import google.generativeai as genai
from django.conf import settings

# Configure Gemini
genai.configure(api_key=os.environ.get("AI_API_KEY"))

PROMPT = """
You are a medical report extraction AI. Your ONLY job is to extract explicit data from the provided document.

CRITICAL SAFETY RULES:
- Do NOT diagnose diseases.
- Do NOT recommend medicines.
- Do NOT generate treatment plans.
- Do NOT invent test values.
- Do NOT invent reference ranges.
- Do NOT invent follow-up dates.
- If a follow-up date/instruction is not present in the document, return null for follow_up.
- If information cannot be confidently extracted, mark the status as "unknown".

Use the reference range stated in the uploaded report to determine the status (normal, borderline, low, high, unknown).

Return the data STRICTLY as a JSON object matching this schema, without any markdown formatting or extra text:
{
    "patient_name": "string or null",
    "report_type": "string",
    "report_date": "YYYY-MM-DD or null",
    "results": [
        {
            "test_name": "string",
            "value": "string",
            "unit": "string",
            "reference_range": "string",
            "status": "normal|borderline|low|high|unknown"
        }
    ],
    "follow_up": {
        "date": "YYYY-MM-DD or null",
        "instruction": "string or null",
        "source": "doctor_instruction|report_instruction|manual"
    }
}
"""

def analyze_report(file_path, mime_type):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        with open(file_path, 'rb') as f:
            file_data = f.read()

        response = model.generate_content([
            {'mime_type': mime_type, 'data': file_data},
            PROMPT
        ])
        
        text = response.text
        # Strip markdown json block if present
        if text.startswith('```json'):
            text = text[7:]
        if text.endswith('```'):
            text = text[:-3]
            
        data = json.loads(text.strip())
        return True, data
    except Exception as e:
        print(f"AI Analysis Error: {str(e)}")
        return False, str(e)
