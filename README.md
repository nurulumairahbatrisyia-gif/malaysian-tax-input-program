import os
import pandas as pd
from function import verify_user, calculate_tax, save_to_csv, read_from_csv

USERS_FILENAME = "users.csv"      # to store registered users (id,ic)
RECORDS_FILENAME = "tax_records.csv"  # to store tax results

def load_users():
    """Return users as a dict: {user_id: ic_number}"""
    if not os.path.isfile(USERS_FILENAME):
        return {}
    df = pd.read_csv(USERS_FILENAME)
    # Convert to dict safely
    return {str(row['user_id']): str(row['ic_number']) for _, row in df.iterrows()}

def save_user(user_id: str, ic_number: str):
    """Append a new user to users.csv or create the file."""
    df = pd.DataFrame([{"user_id": user_id, "ic_number": ic_number}])
    if not os.path.isfile(USERS_FILENAME):
        df.to_csv(USERS_FILENAME, index=False)
    else:
        df.to_csv(USERS_FILENAME, mode="a", header=False, index=False)

def prompt_register(users: dict):
    print("---- Registration ----")
    while True:
        user_id = input("Enter a user id (alphanumeric): ").strip()
        if not user_id:
            print("User id cannot be empty.")
            continue
        if user_id in users:
            print("This user id is already registered. Try a different id.")
            continue
        ic_number = input("Enter your IC number (12 digits): ").strip()
        if not ic_number.isdigit() or len(ic_number) != 12:
            print("IC number must be 12 digits. Please try again.")
            continue
        # Save
        save_user(user_id, ic_number)
        users[user_id] = ic_number
        print("Registration successful. Use your ID and the last 4 digits of your IC as password to log in.")
        break

def prompt_login(users: dict) -> str:
    print("---- Login ----")
    for attempt in range(3):
        user_id = input("User ID: ").strip()
        password = input("Password (last 4 digits of IC): ").strip()

        if user_id not in users:
            print("User ID not found. If you haven't registered, choose option 1 to register.")
            continue
        ic = users[user_id]
        if verify_user(ic, password):
            print("Login successful.")
            return user_id
        else:
            print("Invalid password.")
    raise SystemExit("Too many failed login attempts. Exiting.")

def get_numeric_input(prompt_text: str, min_value: float = 0.0) -> float:
    while True:
        val = input(prompt_text).strip()
        try:
            f = float(val)
            if f < min_value:
                print(f"Value must be at least {min_value}.")
                continue
            return f
        except ValueError:
            print("Please enter a valid numeric value.")

def display_records():
    df = read_from_csv(RECORDS_FILENAME)
    if df is None or df.empty:
        print("No records found.")
        return
    print("\n--- Tax Records ---")
    print(df.to_string(index=False))
    print("-------------------\n")

def main_menu():
    users = load_users()
    while True:
        print("\n==== Malaysian Tax Input Program ====")
        print("1. Register")
        print("2. Login and calculate tax")
        print("3. View tax records")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            prompt_register(users)
        elif choice == "2":
            if not users:
                print("No registered users found. Please register first.")
                continue
            try:
                user_id = prompt_login(users)
            except SystemExit as e:
                print(e)
                continue

            ic = users[user_id]

            # List of major Malaysian tax reliefs
            relief_options = [
                "1. Individual: RM9,000",
                "2. Spouse (no income = RM4,000): Up to RM4,000",
                "3. Child: RM8,000 each up to a maximum of 12 children",
                "4. Medical expenses (self/spouse/child): Up to RM8,000",
                "5. Lifestyle (books, sports, computer, phone, internet): Up to RM2,500",
                "6. Education fees (self): Up to RM7,000",
                "7. Parental care: Up to RM5,000",
                "8. Disabled individual: RM6,000",
                "9. Supporting equipment for disabled (self/spouse/child/parent): Up to RM6,000",
                "10. Breastfeeding equipment (child under 2 years old): Up to RM1,000",
                "11. Child care fees (child aged 6 and below): Up to RM3,000",
                "12. Disabled spouse: Up to RM5,000",
                "13. Disabled child (additional deduction): RM6,000 per child",
                "14. Unmarried child under 18 years old: RM2,000"
            ]
            relief_set = set(relief_options)
            
            # Display the list to the user
            print("\nBelow are the common Malaysian tax reliefs you may claim:")
            for relief in relief_options:
                print("   - " + relief)

            input("\n(Press Enter to continue...)")
                
            print("\nEnter income and the total tax relief amount you are claiming.")
            
            income = get_numeric_input("Annual income (RM): ", min_value=0.0)
            tax_relief = get_numeric_input("Total tax relief claimed (RM): ", min_value=0.0)
            
            tax_payable = calculate_tax(income, tax_relief)
            print(f"\nChargeable income: RM{max(0.0, income - tax_relief):,.2f}")
            print(f"Tax payable: RM{tax_payable:,.2f}")
            
            data = {
                "ic_number": ic,
                "income": income,
                "tax_relief": tax_relief,
                "tax_payable": tax_payable
            }
            save_to_csv(data, RECORDS_FILENAME)
            print("Record saved to CSV.")
        elif choice == "3":
            display_records()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main_menu()
