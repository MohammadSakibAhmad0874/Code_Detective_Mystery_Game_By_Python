import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import random
from datetime import datetime, timedelta
import re

class DetectiveGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Code Detective Mystery")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Game state
        self.current_case = 0
        self.solved_cases = []
        self.hints_used = 0
        
        # Sample data for mysteries
        self.cases = [
            {
                "title": "The Missing Database Records",
                "description": "A company's employee database has been tampered with. Some records are missing and others contain suspicious data. Use your Python skills to find the pattern!",
                "concept": "Lists and Data Analysis",
                "data": [
                    {"id": 1, "name": "Alice Johnson", "department": "IT", "salary": 75000, "hire_date": "2020-01-15"},
                    {"id": 2, "name": "Bob Smith", "department": "HR", "salary": 65000, "hire_date": "2019-03-22"},
                    {"id": 3, "name": "Charlie Brown", "department": "IT", "salary": 95000, "hire_date": "2021-07-10"},
                    {"id": 5, "name": "Diana Prince", "department": "Finance", "salary": 80000, "hire_date": "2020-11-05"},
                    {"id": 6, "name": "Eve Wilson", "department": "IT", "salary": 120000, "hire_date": "2018-09-14"},
                    {"id": 8, "name": "Frank Miller", "department": "HR", "salary": 55000, "hire_date": "2022-02-28"},
                ],
                "clues": [
                    "Employee IDs should be consecutive starting from 1",
                    "IT department salaries seem unusually high",
                    "Check for missing employee records"
                ],
                "solution_code": """# Find missing employee IDs
ids = [emp['id'] for emp in data]
missing_ids = []
for i in range(1, max(ids) + 1):
    if i not in ids:
        missing_ids.append(i)

# Find suspicious salaries
it_salaries = [emp['salary'] for emp in data if emp['department'] == 'IT']
avg_salary = sum(it_salaries) / len(it_salaries)

print(f"Missing employee IDs: {missing_ids}")
print(f"Average IT salary: ${avg_salary:,.2f}")
print("Suspicious: IT salaries are unusually high!")""",
                "hint": "Look for gaps in employee IDs and compare department salaries"
            },
            {
                "title": "The Encrypted Message",
                "description": "A suspicious message was intercepted. It appears to be encoded using a simple cipher. Decode it to reveal the criminal's plan!",
                "concept": "String Manipulation and Algorithms",
                "data": "Wkh#phhwlqj#lv#dw#plgqljkw#lq#wkh#zduhkrxvh",
                "clues": [
                    "This looks like a Caesar cipher",
                    "Each letter is shifted by a fixed number",
                    "Try different shift values"
                ],
                "solution_code": """# Caesar cipher decoder
message = "Wkh#phhwlqj#lv#dw#plgqljkw#lq#wkh#zduhkrxvh"

def caesar_decode(text, shift):
    decoded = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            decoded += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
        else:
            decoded += char
    return decoded

# Try different shifts
for shift in range(1, 26):
    decoded = caesar_decode(message, shift)
    if 'the' in decoded.lower():
        print(f"Shift {shift}: {decoded}")
        break""",
                "hint": "A Caesar cipher shifts each letter by the same amount. Try shift = 3"
            },
            {
                "title": "The Fraudulent Transactions",
                "description": "A bank noticed unusual patterns in their transaction logs. Some transactions appear to be fraudulent. Find the suspicious activities!",
                "concept": "Data Filtering and Pattern Recognition",
                "data": [
                    {"id": "T001", "amount": 1500, "time": "14:23", "account": "A123", "location": "NYC"},
                    {"id": "T002", "amount": 50, "time": "14:25", "account": "A123", "location": "LA"},
                    {"id": "T003", "amount": 2000, "time": "14:27", "account": "A123", "location": "Chicago"},
                    {"id": "T004", "amount": 75, "time": "15:45", "account": "B456", "location": "NYC"},
                    {"id": "T005", "amount": 3000, "time": "14:30", "account": "A123", "location": "Miami"},
                    {"id": "T006", "amount": 200, "time": "16:15", "account": "C789", "location": "Boston"},
                ],
                "clues": [
                    "Look for transactions in different cities within short time periods",
                    "High amounts in quick succession might be suspicious",
                    "One account has multiple rapid transactions"
                ],
                "solution_code": """# Find suspicious transaction patterns
from datetime import datetime

def time_to_minutes(time_str):
    h, m = map(int, time_str.split(':'))
    return h * 60 + m

# Group by account
accounts = {}
for transaction in data:
    acc = transaction['account']
    if acc not in accounts:
        accounts[acc] = []
    accounts[acc].append(transaction)

# Find rapid transactions in different locations
for account, transactions in accounts.items():
    if len(transactions) > 2:
        transactions.sort(key=lambda x: time_to_minutes(x['time']))
        locations = set()
        for t in transactions:
            locations.add(t['location'])
        if len(locations) > 2:
            print(f"FRAUD ALERT: Account {account} has transactions in {len(locations)} different cities!")
            for t in transactions:
                print(f"  {t['time']} - ${t['amount']} in {t['location']}")""",
                "hint": "Focus on account A123 and check time intervals between transactions in different cities"
            }
        ]
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="🕵️ CODE DETECTIVE MYSTERY", 
                              font=("Arial", 20, "bold"), 
                              bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Case Selection Tab
        self.create_case_tab()
        
        # Investigation Tab
        self.create_investigation_tab()
        
        # Code Editor Tab
        self.create_code_tab()
        
        # Results Tab
        self.create_results_tab()
        
        # Progress tracking
        self.create_progress_bar()
        
    def create_case_tab(self):
        self.case_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.case_frame, text="📁 Case Files")
        
        # Case selection
        tk.Label(self.case_frame, text="Select a Case to Investigate:", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        self.case_listbox = tk.Listbox(self.case_frame, height=8, font=("Arial", 11))
        for i, case in enumerate(self.cases):
            status = "✅ SOLVED" if i in self.solved_cases else "🔍 OPEN"
            self.case_listbox.insert(tk.END, f"{status} - {case['title']}")
        self.case_listbox.pack(pady=10, padx=20, fill=tk.X)
        
        # Case details
        self.case_details = scrolledtext.ScrolledText(self.case_frame, height=10, width=80)
        self.case_details.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = tk.Frame(self.case_frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="View Case Details", 
                 command=self.show_case_details, bg='#3498db', fg='white',
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Start Investigation", 
                 command=self.start_investigation, bg='#e74c3c', fg='white',
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
    def create_investigation_tab(self):
        self.investigation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.investigation_frame, text="🔍 Investigation")
        
        # Case info display
        self.case_info = tk.Text(self.investigation_frame, height=6, wrap=tk.WORD)
        self.case_info.pack(pady=10, padx=20, fill=tk.X)
        
        # Evidence section
        tk.Label(self.investigation_frame, text="📋 Evidence & Data:", 
                font=("Arial", 12, "bold")).pack(pady=(10,5))
        
        self.evidence_text = scrolledtext.ScrolledText(self.investigation_frame, height=12)
        self.evidence_text.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)
        
        # Clues section
        tk.Label(self.investigation_frame, text="💡 Clues:", 
                font=("Arial", 12, "bold")).pack(pady=(10,5))
        
        self.clues_text = tk.Text(self.investigation_frame, height=4, wrap=tk.WORD)
        self.clues_text.pack(pady=5, padx=20, fill=tk.X)
        
        # Hint button
        tk.Button(self.investigation_frame, text="Get Hint", 
                 command=self.show_hint, bg='#f39c12', fg='white',
                 font=("Arial", 10, "bold")).pack(pady=10)
        
    def create_code_tab(self):
        self.code_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.code_frame, text="💻 Code Editor")
        
        tk.Label(self.code_frame, text="Write your detective code here:", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        # Code editor
        self.code_editor = scrolledtext.ScrolledText(self.code_frame, height=20, 
                                                    font=("Courier", 11))
        self.code_editor.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = tk.Frame(self.code_frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Run Code", 
                 command=self.run_code, bg='#27ae60', fg='white',
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Clear Code", 
                 command=lambda: self.code_editor.delete(1.0, tk.END),
                 bg='#e67e22', fg='white',
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Show Solution", 
                 command=self.show_solution, bg='#9b59b6', fg='white',
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
    def create_results_tab(self):
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="📊 Results")
        
        tk.Label(self.results_frame, text="Code Output:", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        self.output_text = scrolledtext.ScrolledText(self.results_frame, height=15,
                                                    font=("Courier", 10))
        self.output_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Verdict section
        tk.Label(self.results_frame, text="Detective's Verdict:", 
                font=("Arial", 12, "bold")).pack(pady=(10,5))
        
        self.verdict_text = tk.Text(self.results_frame, height=5, wrap=tk.WORD)
        self.verdict_text.pack(pady=5, padx=20, fill=tk.X)
        
        tk.Button(self.results_frame, text="Submit Solution", 
                 command=self.submit_solution, bg='#e74c3c', fg='white',
                 font=("Arial", 12, "bold")).pack(pady=10)
        
    def create_progress_bar(self):
        progress_frame = tk.Frame(self.root, bg='#2c3e50')
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(progress_frame, text="Progress:", bg='#2c3e50', fg='#ecf0f1',
                font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.progress_var = tk.StringVar()
        self.update_progress()
        tk.Label(progress_frame, textvariable=self.progress_var, 
                bg='#2c3e50', fg='#ecf0f1', font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        
    def update_progress(self):
        solved = len(self.solved_cases)
        total = len(self.cases)
        self.progress_var.set(f"{solved}/{total} cases solved | Hints used: {self.hints_used}")
        
    def show_case_details(self):
        selection = self.case_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a case first!")
            return
            
        case_index = selection[0]
        case = self.cases[case_index]
        
        details = f"Case: {case['title']}\n"
        details += f"Programming Concept: {case['concept']}\n"
        details += f"Status: {'SOLVED' if case_index in self.solved_cases else 'UNSOLVED'}\n\n"
        details += f"Description:\n{case['description']}\n\n"
        
        self.case_details.delete(1.0, tk.END)
        self.case_details.insert(1.0, details)
        
    def start_investigation(self):
        selection = self.case_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a case first!")
            return
            
        self.current_case = selection[0]
        case = self.cases[self.current_case]
        
        # Update investigation tab
        case_info = f"🔍 INVESTIGATING: {case['title']}\n"
        case_info += f"📚 Concept: {case['concept']}\n"
        case_info += f"📝 Description: {case['description']}\n"
        
        self.case_info.delete(1.0, tk.END)
        self.case_info.insert(1.0, case_info)
        
        # Show evidence
        evidence = "# Available data variable: 'data'\n"
        if isinstance(case['data'], list):
            evidence += f"data = {json.dumps(case['data'], indent=2)}"
        else:
            evidence += f'data = "{case["data"]}"'
            
        self.evidence_text.delete(1.0, tk.END)
        self.evidence_text.insert(1.0, evidence)
        
        # Show clues
        clues = "\n".join([f"• {clue}" for clue in case['clues']])
        self.clues_text.delete(1.0, tk.END)
        self.clues_text.insert(1.0, clues)
        
        # Switch to investigation tab
        self.notebook.select(1)
        
        # Add starter code
        starter_code = f"# {case['title']} - Investigation Code\n"
        starter_code += f"# Concept: {case['concept']}\n\n"
        starter_code += "# The evidence is stored in the 'data' variable\n"
        starter_code += "# Write your code below to analyze the data and solve the mystery!\n\n"
        
        self.code_editor.delete(1.0, tk.END)
        self.code_editor.insert(1.0, starter_code)
        
    def show_hint(self):
        if self.current_case >= 0:
            case = self.cases[self.current_case]
            messagebox.showinfo("💡 Hint", case['hint'])
            self.hints_used += 1
            self.update_progress()
        else:
            messagebox.showwarning("No Case", "Please start investigating a case first!")
            
    def run_code(self):
        code = self.code_editor.get(1.0, tk.END)
        
        # Clear previous output
        self.output_text.delete(1.0, tk.END)
        
        if self.current_case < 0:
            self.output_text.insert(tk.END, "Please start investigating a case first!")
            return
            
        case = self.cases[self.current_case]
        
        # Create execution environment
        exec_globals = {
            'data': case['data'],
            'print': lambda *args, **kwargs: self.custom_print(*args, **kwargs),
            'datetime': datetime,
            'timedelta': timedelta,
            're': re,
            'json': json
        }
        
        try:
            exec(code, exec_globals)
            self.notebook.select(3)  # Switch to results tab
        except Exception as e:
            self.output_text.insert(tk.END, f"❌ Error: {str(e)}\n")
            self.output_text.insert(tk.END, "Check your code and try again!")
            
    def custom_print(self, *args, **kwargs):
        output = " ".join(str(arg) for arg in args) + "\n"
        self.output_text.insert(tk.END, output)
        self.output_text.see(tk.END)
        
    def show_solution(self):
        if self.current_case >= 0:
            case = self.cases[self.current_case]
            self.code_editor.delete(1.0, tk.END)
            self.code_editor.insert(1.0, case['solution_code'])
            messagebox.showinfo("Solution Revealed", "The solution code has been loaded. Study it carefully!")
        else:
            messagebox.showwarning("No Case", "Please start investigating a case first!")
            
    def submit_solution(self):
        verdict = self.verdict_text.get(1.0, tk.END).strip()
        if not verdict:
            messagebox.showwarning("No Verdict", "Please write your detective's verdict!")
            return
            
        if self.current_case >= 0 and self.current_case not in self.solved_cases:
            self.solved_cases.append(self.current_case)
            messagebox.showinfo("Case Closed!", 
                              f"Excellent detective work! Case {self.current_case + 1} has been marked as solved.\n\n"
                              f"Your verdict: {verdict[:100]}...")
            self.update_progress()
            
            # Update case list
            self.case_listbox.delete(0, tk.END)
            for i, case in enumerate(self.cases):
                status = "✅ SOLVED" if i in self.solved_cases else "🔍 OPEN"
                self.case_listbox.insert(tk.END, f"{status} - {case['title']}")
                
            if len(self.solved_cases) == len(self.cases):
                messagebox.showinfo("Congratulations!", 
                                  "🎉 You've solved all the cases! You're a true Code Detective!")
        else:
            messagebox.showinfo("Case Status", "This case has already been solved!")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = DetectiveGame()
    game.run()