import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
import os
from abc import ABC, abstractmethod
import seaborn as sns
from typing import List, Dict, Optional

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class DataStorage(ABC):
    """Abstract base class for data storage"""
    @abstractmethod
    def save_data(self, data: pd.DataFrame):
        pass
    
    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        pass

class JSONDataStorage(DataStorage):
    """JSON-based data storage implementation"""
    def __init__(self, filename: str = "expenses_data.json"):
        self.filename = filename
    
    def save_data(self, data: pd.DataFrame):
        """Save DataFrame to JSON file"""
        data.to_json(self.filename, orient='records', indent=2)
    
    def load_data(self) -> pd.DataFrame:
        """Load DataFrame from JSON file"""
        if os.path.exists(self.filename):
            return pd.read_json(self.filename, orient='records')
        return pd.DataFrame(columns=['date', 'category', 'amount', 'description'])

class ExpenseAnalyzer:
    """Class for analyzing expense data"""
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.data['date'] = pd.to_datetime(self.data['date'])
    
    def get_category_summary(self) -> pd.DataFrame:
        """Get summary of expenses by category"""
        return self.data.groupby('category')['amount'].agg(['sum', 'count', 'mean']).round(2)
    
    def get_monthly_summary(self) -> pd.DataFrame:
        """Get monthly expense summary"""
        monthly_data = self.data.copy()
        monthly_data['month'] = monthly_data['date'].dt.to_period('M')
        return monthly_data.groupby('month')['amount'].agg(['sum', 'count']).round(2)
    
    def get_spending_trend(self, window: int = 7) -> pd.DataFrame:
        """Calculate rolling spending trend"""
        daily_data = self.data.set_index('date').resample('D')['amount'].sum().fillna(0)
        return daily_data.rolling(window=window).mean()
    
    def detect_anomalies(self, threshold: float = 2.0) -> pd.DataFrame:
        """Detect anomalous spending patterns using Z-score"""
        category_means = self.data.groupby('category')['amount'].mean()
        category_stds = self.data.groupby('category')['amount'].std()
        
        anomalies = []
        for _, row in self.data.iterrows():
            category = row['category']
            amount = row['amount']
            if category in category_means and category in category_stds:
                z_score = (amount - category_means[category]) / category_stds[category]
                if abs(z_score) > threshold:
                    anomalies.append({**row.to_dict(), 'z_score': z_score})
        
        return pd.DataFrame(anomalies)

class BudgetManager:
    """Class for managing budgets and alerts"""
    def __init__(self):
        self.budgets = {}
    
    def set_budget(self, category: str, monthly_limit: float):
        """Set monthly budget for a category"""
        self.budgets[category] = monthly_limit
    
    def check_budget_violations(self, expenses: pd.DataFrame) -> Dict:
        """Check for budget violations"""
        current_month = datetime.now().strftime('%Y-%m')
        monthly_expenses = expenses[expenses['date'].dt.strftime('%Y-%m') == current_month]
        
        violations = {}
        for category, limit in self.budgets.items():
            category_expenses = monthly_expenses[monthly_expenses['category'] == category]
            total_spent = category_expenses['amount'].sum()
            
            if total_spent > limit:
                violations[category] = {
                    'limit': limit,
                    'spent': total_spent,
                    'overspend': total_spent - limit
                }
            elif total_spent > limit * 0.8:  # 80% threshold warning
                violations[category] = {
                    'limit': limit,
                    'spent': total_spent,
                    'warning': f"Approaching budget limit ({(total_spent/limit)*100:.1f}%)"
                }
        
        return violations

class ExpenseVisualizer:
    """Class for creating visualizations"""
    @staticmethod
    def plot_category_distribution(analyzer: ExpenseAnalyzer):
        """Plot pie chart of expenses by category"""
        category_summary = analyzer.get_category_summary()
        plt.figure(figsize=(10, 8))
        plt.pie(category_summary['sum'], labels=category_summary.index, autopct='%1.1f%%')
        plt.title('Expense Distribution by Category')
        plt.show()
    
    @staticmethod
    def plot_monthly_trends(analyzer: ExpenseAnalyzer):
        """Plot monthly spending trends"""
        monthly_data = analyzer.get_monthly_summary()
        plt.figure(figsize=(12, 6))
        monthly_data['sum'].plot(kind='bar')
        plt.title('Monthly Spending Trends')
        plt.xlabel('Month')
        plt.ylabel('Amount Spent')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_spending_trend(analyzer: ExpenseAnalyzer, window: int = 7):
        """Plot rolling spending trend"""
        trend_data = analyzer.get_spending_trend(window)
        plt.figure(figsize=(12, 6))
        trend_data.plot()
        plt.title(f'{window}-Day Rolling Average Spending')
        plt.xlabel('Date')
        plt.ylabel('Amount Spent')
        plt.grid(True)
        plt.show()

class ExpenseTracker:
    """Main expense tracker class using OOP principles"""
    def __init__(self, storage: DataStorage = None):
        self.storage = storage or JSONDataStorage()
        self.data = self.storage.load_data()
        self.analyzer = ExpenseAnalyzer(self.data)
        self.budget_manager = BudgetManager()
        self.visualizer = ExpenseVisualizer()
    
    def add_expense(self, category: str, amount: float, description: str = ""):
        """Add a new expense"""
        new_expense = pd.DataFrame([{
            'date': datetime.now(),
            'category': category,
            'amount': amount,
            'description': description
        }])
        
        self.data = pd.concat([self.data, new_expense], ignore_index=True)
        self.storage.save_data(self.data)
        self.analyzer = ExpenseAnalyzer(self.data)  # Refresh analyzer
        
        print("Expense added successfully!")
        self.check_budgets()
    
    def check_budgets(self):
        """Check and display budget violations"""
        violations = self.budget_manager.check_budget_violations(self.data)
        if violations:
            print("\n⚠️  Budget Alerts:")
            for category, info in violations.items():
                if 'overspend' in info:
                    print(f"❌ {category}: Overspent by ₹{info['overspend']:.2f}")
                else:
                    print(f"⚠️  {category}: {info['warning']}")
    
    def view_summary(self, period: str = 'month'):
        """View expense summary"""
        if period == 'month':
            summary = self.analyzer.get_monthly_summary()
            print("\n📊 Monthly Summary:")
            print(summary)
        else:
            summary = self.analyzer.get_category_summary()
            print("\n📊 Category Summary:")
            print(summary)
        
        total_spent = self.data['amount'].sum()
        avg_daily = self.data.groupby(self.data['date'].dt.date)['amount'].sum().mean()
        print(f"\n💰 Total Spent: ₹{total_spent:.2f}")
        print(f"📅 Average Daily: ₹{avg_daily:.2f}")
    
    def view_anomalies(self):
        """View spending anomalies"""
        anomalies = self.analyzer.detect_anomalies()
        if not anomalies.empty:
            print("\n🔍 Spending Anomalies Detected:")
            print(anomalies[['date', 'category', 'amount', 'z_score']])
        else:
            print("\n✅ No unusual spending patterns detected.")
    
    def set_budget(self):
        """Set a budget for a category"""
        category = input("Enter category: ")
        try:
            limit = float(input("Enter monthly budget limit: "))
            self.budget_manager.set_budget(category, limit)
            print(f"Budget set for {category}: ₹{limit:.2f}")
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    def visualize_data(self):
        """Show data visualizations"""
        print("\n📈 Visualization Options:")
        print("1. Category Distribution")
        print("2. Monthly Trends")
        print("3. Spending Trend")
        
        choice = input("Choose option (1-3): ")
        if choice == "1":
            self.visualizer.plot_category_distribution(self.analyzer)
        elif choice == "2":
            self.visualizer.plot_monthly_trends(self.analyzer)
        elif choice == "3":
            window = int(input("Enter rolling window size (default 7): ") or "7")
            self.visualizer.plot_spending_trend(self.analyzer, window)
    
    def export_report(self, filename: str = "expense_report.csv"):
        """Export data to CSV"""
        self.data.to_csv(filename, index=False)
        print(f"Report exported to {filename}")

def main():
    """Main application function"""
    tracker = ExpenseTracker()
    
    while True:
        print("\n💸 Advanced Expense Tracker")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Set Budget")
        print("4. Check Anomalies")
        print("5. Visualize Data")
        print("6. Export Report")
        print("7. Exit")
        
        choice = input("Choose an option (1-7): ")
        
        if choice == "1":
            category = input("Enter category: ")
            try:
                amount = float(input("Enter amount: "))
                description = input("Enter description (optional): ")
                tracker.add_expense(category, amount, description)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        
        elif choice == "2":
            period = input("View by (month/category): ").lower()
            tracker.view_summary(period if period in ['month', 'category'] else 'month')
        
        elif choice == "3":
            tracker.set_budget()
        
        elif choice == "4":
            tracker.view_anomalies()
        
        elif choice == "5":
            tracker.visualize_data()
        
        elif choice == "6":
            filename = input("Enter filename (default: expense_report.csv): ") or "expense_report.csv"
            tracker.export_report(filename)
        
        elif choice == "7":
            print("Goodbye! 👋")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()