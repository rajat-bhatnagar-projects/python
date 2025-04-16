import csv
import os
from datetime import datetime

FILENAME = "expenses.csv"

def add_expense():
    while True:
        date_input = input("Enter date (YYYY-MM-DD) or type 'exit' to cancel: ").strip()
        if date_input.lower() == "exit":
            print("Returning to main menu...\n")
            return
        
        try:
            # This will raise ValueError if the date format or values are invalid
            date_obj = datetime.strptime(date_input, "%Y-%m-%d")
            break
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD\n")
    
    day_of_week = date_obj.strftime('%A')  # e.g., Monday, Tuesday, etc.
    category = input("Enter category (e.g. Food, Rent, Utilities): ").strip()
    amount = input("Enter amount: ").strip()

    # Append new expense data to CSV. Create header if file is empty.
    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        if os.path.getsize(FILENAME) == 0:
            writer.writerow(["Date", "Day", "Category", "Amount"])
        writer.writerow([date_input, day_of_week, category, amount])
    
    print("✅ Expense added successfully!\n")

def view_expenses(show_index=False):
    if not os.path.exists(FILENAME) or os.path.getsize(FILENAME) == 0:
        print("No expenses recorded yet.\n")
        return []
    
    expenses = []
    with open(FILENAME, mode='r', newline='') as file:
        reader = csv.reader(file)
        try:
            headers = next(reader)
        except StopIteration:
            print("The CSV file is empty.\n")
            return []
        
        # Validate header columns count
        if len(headers) < 4:
            print("CSV file header is missing or incomplete. Displaying raw data:\n")
            for row in reader:
                print(row)
            return []
        
        print("\nExpenses:")
        # If show_index is True, print an index beside each expense
        if show_index:
            print(f"{'No.':<4} {headers[0]:<12} {headers[1]:<10} {headers[2]:<20} {headers[3]:<10}")
        else:
            print(f"{headers[0]:<12} {headers[1]:<10} {headers[2]:<20} {headers[3]:<10}")
        
        index = 1
        for row in reader:
            if len(row) >= 4:
                if show_index:
                    print(f"{index:<4} {row[0]:<12} {row[1]:<10} {row[2]:<20} ${row[3]:<10}")
                else:
                    print(f"{row[0]:<12} {row[1]:<10} {row[2]:<20} ${row[3]:<10}")
                expenses.append(row)
                index += 1
            else:
                print("Row data incomplete:", row)
    print()
    return expenses

def edit_expense():
    # Load existing expenses and display them with indices
    expenses = view_expenses(show_index=True)
    if not expenses:
        print("No expenses to edit.\n")
        return

    try:
        choice = int(input("Enter the expense number to edit (or 0 to cancel): "))
    except ValueError:
        print("Invalid input. Returning to main menu.\n")
        return

    if choice == 0:
        print("Edit cancelled. Returning to main menu.\n")
        return

    if choice < 1 or choice > len(expenses):
        print("Invalid expense number. Returning to main menu.\n")
        return

    # Adjust for zero-based index
    index_to_edit = choice - 1

    # Get original expense data
    orig_expense = expenses[index_to_edit]
    print("\nEditing Expense:")
    print(f"Original Date: {orig_expense[0]}, Day: {orig_expense[1]}, Category: {orig_expense[2]}, Amount: {orig_expense[3]}")

    # Get new date with validation (cancellable)
    while True:
        new_date = input("Enter new date (YYYY-MM-DD) or type 'exit' to cancel edit: ").strip()
        if new_date.lower() == "exit":
            print("Edit cancelled. Returning to main menu.\n")
            return
        try:
            date_obj = datetime.strptime(new_date, "%Y-%m-%d")
            break
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD\n")
    
    new_day = date_obj.strftime('%A')
    new_category = input("Enter new category: ").strip()
    new_amount = input("Enter new amount: ").strip()

    # Read all file content: header + rows
    all_rows = []
    with open(FILENAME, mode='r', newline='') as file:
        reader = list(csv.reader(file))
        if reader:
            header = reader[0]
            data = reader[1:]
        else:
            print("No data found.")
            return
        all_rows = [header] + data

    # Update the selected row with new data
    data[index_to_edit] = [new_date, new_day, new_category, new_amount]
    # Update the file: combine header and updated data
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
    
    print("✅ Expense updated successfully!\n")

def delete_individual_expense():
    # Load and display expenses with indices
    expenses = view_expenses(show_index=True)
    if not expenses:
        print("No expenses to delete.\n")
        return

    try:
        choice = int(input("Enter the expense number to delete (or 0 to cancel): "))
    except ValueError:
        print("Invalid input. Returning to main menu.\n")
        return

    if choice == 0:
        print("Deletion cancelled. Returning to main menu.\n")
        return

    if choice < 1 or choice > len(expenses):
        print("Invalid expense number. Returning to main menu.\n")
        return

    confirm = input("Are you sure you want to delete the selected expense? (y/n): ")
    if confirm.lower() != 'y':
        print("Deletion cancelled. Returning to main menu.\n")
        return

    # Adjust for zero-based indexing
    index_to_delete = choice - 1

    # Read full CSV data
    with open(FILENAME, mode='r', newline='') as file:
        reader = list(csv.reader(file))
        if reader:
            header = reader[0]
            data = reader[1:]
        else:
            print("No data found.")
            return

    # Remove the chosen expense
    if index_to_delete < len(data):
        del data[index_to_delete]
    else:
        print("Expense not found. Returning to main menu.\n")
        return

    # Write updated data back to the file
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
    
    print("✅ Expense deleted successfully!\n")

def delete_all_expenses():
    confirm = input("Are you sure you want to delete all expenses? (y/n): ")
    if confirm.lower() == 'y':
        open(FILENAME, 'w').close()
        print("All expenses deleted.\n")
    else:
        print("Deletion cancelled.\n")

def main():
    while True:
        print("---- Personal Expense Tracker ----")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Edit Expense")
        print("4. Delete Individual Expense")
        print("5. Delete All Expenses")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()
        print()

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            edit_expense()
        elif choice == '4':
            delete_individual_expense()
        elif choice == '5':
            delete_all_expenses()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
