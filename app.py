from flask import Flask, render_template, request, redirect
import json
import os
from expense import Expense

app = Flask(__name__)
DATA_FILE = "data.json"


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    expenses = []
    for item in data:
        expenses.append(
            Expense(
                item["amount"],
                item["category"],
                item["date"],
                item.get("note", "")
            )
        )
    return expenses


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(
            [
                {
                    "amount": e.amount,
                    "category": e.category,
                    "date": e.date,
                    "note": e.note
                }
                for e in expenses
            ],
            f,
            indent=4
        )

@app.route("/")
def index():
    expenses = load_expenses()

    # get filter values from URL
    month = request.args.get("month")
    year = request.args.get("year")

    filtered_expenses = expenses

    if month and year:
        filtered_expenses = []
        for e in expenses:
            try:
                y,m,d = e.date.split("-")
                if m == month.zfill(2) and y == year:
                    filtered_expenses.append(e)
            except ValueError:
                pass  # ignore bad date formats

    # total
    total = sum(e.amount for e in filtered_expenses)

    # category summary
    category_summary = {}
    for e in filtered_expenses:
        category_summary[e.category] = category_summary.get(e.category, 0) + e.amount

    return render_template(
        "index.html",
        expenses=filtered_expenses,
        total=total,
        category_summary=category_summary,
        selected_month=month,
        selected_year=year
    )

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        expenses = load_expenses()
        expenses.append(
            Expense(
                float(request.form["amount"]),
                request.form["category"],
                request.form["date"],
                request.form["note"]
            )
        )
        save_expenses(expenses)
        return redirect("/")

    return render_template("add.html")


@app.route("/delete/<int:index>")
def delete(index):
    expenses = load_expenses()
    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_expenses(expenses)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)