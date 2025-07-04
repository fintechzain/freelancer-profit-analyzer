from collections import defaultdict
import pandas as pd
import io
from openpyxl import Workbook

def calculate_profit_summary(income_data, expense_data, tax_rate=15):
    total_income = 0
    total_fees = 0
    income_by_platform = defaultdict(float)

    for entry in income_data:
        amount = entry['amount']
        platform = entry['platform']

        fee_percent = 0.20 if platform == "Fiverr" else 0.10 if platform == "Upwork" else 0
        fee = amount * fee_percent
        total_fees += fee
        total_income += amount
        income_by_platform[platform] += amount

    total_expenses = sum(e['amount'] for e in expense_data)
    expense_by_category = defaultdict(float)
    for e in expense_data:
        expense_by_category[e['category']] += e['amount']

    taxable_income = total_income - total_fees
    estimated_tax = (taxable_income * tax_rate) / 100
    net_profit = taxable_income - estimated_tax - total_expenses

    return {
        'total_income': round(total_income, 2),
        'total_fees': round(total_fees, 2),
        'estimated_tax': round(estimated_tax, 2),
        'total_expenses': round(total_expenses, 2),
        'net_profit': round(net_profit, 2),
        'tax_rate': tax_rate,
        'income_chart_data': dict(income_by_platform),
        'expense_chart_data': dict(expense_by_category)
    }


def calculate_project_profit(price, hours_worked):
    hourly_rate = price / hours_worked if hours_worked else 0
    return {
        'price': round(price, 2),
        'hours_worked': hours_worked,
        'hourly_rate': round(hourly_rate, 2)
    }


def export_to_excel(income_data, expense_data):
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Summary"

    ws1.append(["Platform", "Amount", "Note"])
    for i in income_data:
        ws1.append([i['platform'], i['amount'], i['note']])

    ws2 = wb.create_sheet("Expenses")
    ws2.append(["Category", "Amount", "Description"])
    for e in expense_data:
        ws2.append([e['category'], e['amount'], e['description']])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output
