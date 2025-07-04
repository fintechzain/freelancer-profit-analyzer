from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import csv
import os
import io
from utils.profit_utils import calculate_profit_summary, calculate_project_profit, export_to_excel
from utils.ai_utils import generate_insights

app = Flask(__name__)

# Global in-memory data
income_data = []
expense_data = []
profit_goal = {"amount": 0}


# Load sample data from CSV files
def load_sample_data():
    income_file = os.path.join("data", "income.csv")
    expense_file = os.path.join("data", "expenses.csv")

    try:
        with open(income_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                income_data.append({
                    'platform': row['platform'],
                    'amount': float(row['amount']),
                    'note': row.get('note', '')
                })

        with open(expense_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                expense_data.append({
                    'category': row['category'],
                    'amount': float(row['amount']),
                    'description': row.get('description', '')
                })

        print("✅ Sample data loaded successfully!")

    except Exception as e:
        print("❌ Sample data load failed:", e)


# Call the sample data loader
load_sample_data()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_income', methods=['POST'])
def add_income():
    platform = request.form['platform']
    amount = float(request.form['amount'])
    note = request.form.get('note', '')
    income_data.append({'platform': platform, 'amount': amount, 'note': note})
    return redirect(url_for('index'))


@app.route('/add_expense', methods=['POST'])
def add_expense():
    category = request.form['category']
    description = request.form['description']
    amount = float(request.form['amount'])
    expense_data.append({'category': category, 'description': description, 'amount': amount})
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    summary = calculate_profit_summary(income_data, expense_data)
    return render_template('dashboard.html', summary=summary, income_data=income_data, expense_data=expense_data)


@app.route('/insights')
def insights():
    summary = calculate_profit_summary(income_data, expense_data)
    ai_suggestions = generate_insights(income_data, expense_data)
    return render_template('insights.html', insights=ai_suggestions, summary=summary)


@app.route('/goal', methods=['GET', 'POST'])
def goal():
    if request.method == 'POST':
        try:
            goal_value = float(request.form['goal'])
            profit_goal['amount'] = goal_value
        except:
            profit_goal['amount'] = 0
        return redirect(url_for('goal'))

    summary = calculate_profit_summary(income_data, expense_data)
    net_profit = summary['net_profit']
    goal_amount = profit_goal['amount']
    progress = (net_profit / goal_amount) * 100 if goal_amount else 0

    return render_template(
        'goal.html',
        goal=goal_amount,
        profit=net_profit,
        progress=round(progress, 2)
    )


@app.route('/project-profit', methods=['GET', 'POST'])
def project_profit():
    if request.method == 'POST':
        try:
            price = float(request.form['price'])
            hours = float(request.form['hours'])
            result = calculate_project_profit(price, hours)
            return render_template('project_profit.html', result=result, price=price, hours=hours)
        except:
            return render_template('project_profit.html', result=None)
    return render_template('project_profit.html', result=None)


@app.route('/export')
def export():
    output = export_to_excel(income_data, expense_data)
    return send_file(output, as_attachment=True, download_name="freelancer_report.xlsx")


if __name__ == '__main__':
    app.run(debug=True)
