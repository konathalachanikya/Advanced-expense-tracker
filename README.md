# 💸 Advanced Expense Tracker
A comprehensive Python-based expense tracking system with advanced analytics, budgeting features, and beautiful visualizations. Get smart alerts when you approach your spending limits and gain insights into your financial habits.

https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/Pandas-1.5%252B-orange
https://img.shields.io/badge/Matplotlib-3.6%252B-green
https://img.shields.io/badge/Seaborn-0.12%252B-red
https://img.shields.io/badge/License-MIT-yellow

✨ Features
📊 Smart Expense Tracking: Log expenses with intuitive categories

💰 Budget Management: Set monthly budgets with 60% usage warnings

⚠️ Intelligent Alerts: Get early warnings before exceeding limits

📈 Data Visualization: Generate beautiful charts and graphs

🔍 Anomaly Detection: Identify unusual spending patterns automatically

📤 Data Export: Export to CSV for further analysis

💾 Persistent Storage: Automatic JSON data saving

🎯 Predefined Categories
Category	Icon	Description
Food	🍕	Groceries, restaurants, snacks
Cloth	👕	Clothing, accessories, shoes
Rent	🏠	Housing rent, mortgage
Bill	💡	Utilities, phone, internet bills
Medical	🏥	Healthcare, medicines, insurance
Fee	🎓	Education, subscriptions, fees
Other	📦	Miscellaneous expenses
🚀 Quick Start
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Installation
Clone the repository

bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
Install dependencies

bash
pip install -r requirements.txt
Run the application

bash
python expense_tracker.py
📋 Usage Guide
Adding Expenses
bash
Choose an option (1-7): 1
Enter category: food
Enter amount: 650
Enter description: Groceries for the week

Expense added successfully!
⚠️ Budget Alerts:
⚠️ Food: Budget used: 65.0% - Getting close to limit!
Setting Budgets
bash
Choose an option (1-7): 3
Available categories: Food, Cloth, Rent, Bill, Medical, Fee, Other
Enter category: rent
Enter monthly budget limit: 15000
Budget set for Rent: ₹15000.00
Viewing Reports
bash
Choose an option (1-7): 2
View by (month/category): category

📊 Category Summary:
          sum  count   mean
Category                   
Food    650.0      1  650.0
Rent   15000.0      1  15000.0

💰 Total Spent: ₹15650.00
📅 Average Daily: ₹15650.00
🛠️ Technical Architecture
text
expense-tracker/
├── expense_tracker.py    # Main application
├── requirements.txt      # Dependencies
├── README.md            # This file
├── expenses_data.json   # Auto-generated data
└── expense_report.csv   # Exported reports
Core Components
DataStorage: Abstract class for data persistence

JSONDataStorage: JSON file implementation

ExpenseAnalyzer: Data analysis and statistics

BudgetManager: Budget tracking with smart alerts

ExpenseVisualizer: Chart generation

ExpenseTracker: Main application logic

📊 Visualization Examples
The application generates three types of visualizations:

Category Distribution Pie Chart - See spending breakdown

Monthly Trends Bar Chart - Track spending over time

Rolling Average Trend Line - Identify spending patterns

⚙️ Configuration
Modifying Alert Thresholds
Edit the warning percentage in check_budget_violations method:

python
elif percentage_used >= 60:  # Change this value
Adding New Categories
Edit the categories list in the BudgetManager class:

python
self.categories = ['Food', 'Cloth', 'Rent', 'Bill', 'Medical', 'Fee', 'Other', 'YourNewCategory']
🤝 Contributing
We welcome contributions! Please feel free to:

Fork the project

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🆘 Support
If you encounter any issues:

Check the [ troubleshooting guide below]

Search existing issues on GitHub

Create a new issue with detailed information

🔧 Troubleshooting
Common Issues
Import errors:

bash
pip install -r requirements.txt
GitHub upload errors:

Ensure you have Git installed

Verify your GitHub repository URL

Use Personal Access Token instead of password

No graphs showing:

Ensure matplotlib is installed correctly

Check if you're using a GUI-supported environment

📞 Contact
For questions and support:

Create an issue on GitHub

Email: your-email@example.com

⭐ If you find this project useful, please give it a star on GitHub!

Happy Budgeting! 💰📊✨

