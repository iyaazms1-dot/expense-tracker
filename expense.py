class Expense:
    def __init__(self, amount, category, date, note=""):
        self.amount = amount
        self.category = category
        self.date = date
        self.note = note

    def __str__(self):
        return f"{self.date} | {self.category} | ₹{self.amount} | {self.note}"