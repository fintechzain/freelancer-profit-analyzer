import os
from openai import OpenAI
from dotenv import load_dotenv

# Load from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def generate_insights(income_data, expense_data):
    income_lines = "\n".join(
        f"- {entry['platform']}: ₨{entry['amount']}" for entry in income_data
    )
    expense_lines = "\n".join(
        f"- {entry['category']}: ₨{entry['amount']} ({entry['description']})" for entry in expense_data
    )

    prompt = f"""
You are a smart financial assistant for freelancers. Based on this data, provide:
1. Profitability summary (which platform earns more)
2. Expense analysis (what can be reduced)
3. Suggestions to increase profit

Income:
{income_lines}

Expenses:
{expense_lines}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ AI analysis failed: {str(e)}"
