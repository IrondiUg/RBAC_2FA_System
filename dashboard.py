import time

def it_admin_dashboard(user_dict):
    print(f"\nWelcome {user_dict['Username'].upper()} to the IT Admin Dashboard")
    print("1. VIEW ALL USERS")
    print("2. MANAGE IT RESOURCES")
    print("3. REGISTER A NEW USER")
    print("4. CONTACT SUPPORT")
    print("5. LOGOUT")
    while True:
        choice = input("\n")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            from main import addUser, logs
            time.sleep(1)
            addUser(user_dict)
        elif choice == "4":
            from main import help_desk
            help_desk()
        elif choice == "5":
            print("\nExiting the program...")
            time.sleep(1)
            from main import menu, logs
            logs(user_dict["Username"], "LOGGED OUT")
            menu()
        else:
            print("\nInvalid choice, please try again.")
            time.sleep(1)
            continue
def it_engineer_dashboard(user_dict):
    print(f"\nWelcome {user_dict['Username'].upper()} to the IT Engineer Dashboard")
    print("1. VIEW ASSIGNED TASKS")
    print("2. REPORT ISSUES")
    print("3. CONTACT SUPPORT")
    print("4. LOGOUT")
    while True:
        choice = input("\n")
        if choice == "1":
                pass
        elif choice == "2":
            pass
        elif choice == "3":
            from main import help_desk
            help_desk()
        elif choice == "4":
            print("\nLogging out...")
            time.sleep(1)
            from main import menu, logs
            logs(user_dict["Username"], "LOGGED OUT")
            menu()
        else:
            print("\nInvalid choice, please try again.")
            time.sleep(1)
            continue
def it_intern_dashboard(user_dict):
    print(f"\nWelcome {user_dict['Username'].upper()} to the IT Intern Dashboard")
    print("1. VIEW LEARNING MATERIALS")
    print("2. SUBMIT INTERN REPORTS")
    print("3. CONTACT SUPPORT")
    print("4. LOGOUT")
    while True:
        choice = input("\n")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            from main import help_desk
            help_desk()
        elif choice == "4":
            print("\nExiting the program...")
            time.sleep(1)
            from main import menu, logs
            logs(user_dict["Username"], "LOGGED OUT")
            menu()
        else:
            print("\nInvalid choice, please try again.")
            time.sleep(1)
            continue
def hr_manager_dashboard(user_dict):
    print(f"\nWelcome {user_dict['Username'].upper()} to the HR Manager Dashboard")
    print("1. VIEW EMPLOYEE RECORDS")
    print("2. MANAGE HR POLICIES")
    print("3. CONTACT SUPPORT")
    print("4. LOGOUT")
    while True:
        choice = input("\n")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            from main import help_desk
            help_desk()
        elif choice == "4":
            print("\nLogging out...")
            time.sleep(1)
            from main import menu, logs
            logs(user_dict["Username"], "LOGGED OUT")
            menu()
        else:
            print("\nInvalid choice, please try again.")
            time.sleep(1)
            continue
def hr_recruiter_dashboard(user_dict):
    print(f"\nWelcome {user_dict['Username'].upper()} to the HR Recruiter Dashboard")
    print("1. VIEW JOB APPLICATIONS")
    print("2. SCHEDULE INTERVIEWS")
    print("3. CONTACT SUPPORT")
    print("4. LOGOUT")
    while True:
        choice = input("\n")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            from main import help_desk
            help_desk()
        elif choice == "4":
            print("\nLogging out...")
            time.sleep(1)
            from main import menu, logs
            logs(user_dict["Username"], "LOGGED OUT")
            menu()
        else:
            print("\nInvalid choice, please try again.")
            time.sleep(1)
            continue
def hr_clerk_dashboard(user_dict):
    print(f"\nWelcome {user_dict['Username'].upper()} to the HR Clerk Dashboard")
    print("1. MANAGE EMPLOYEE RECORDS")
    print("2. ASSIST IN RECRUITMENT")
    print("3. CONTACT SUPPORT")
    print("4. LOGOUT")
    while True:
        choice = input("\n")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            from main import help_desk
            help_desk()
        elif choice == "4":
            print("\nLogging out...")
            time.sleep(1)
            from main import menu, logs
            logs(user_dict["Username"], "LOGGED OUT")
            menu()
        else:
            print("\nInvalid choice, please try again.")
            time.sleep(1)
            continue
def finance_dir_dashboard(user_dict):
    print(f"\nWelcome {user_dict['Username'].upper()} to the Finance Director Dashboard")
    print("1. VIEW FINANCIAL REPORTS")
    print("2. APPROVE BUDGETS")
    print("3. MANAGE BUDGETS")
    print("4. CONTACT SUPPORT")
    print("5. LOGOUT")
    while True:
        choice = input("\n")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            from main import help_desk
            help_desk()
        elif choice == "5":
            print("\nLogging out...")
            time.sleep(1)
            from main import menu, logs
            logs(user_dict["Username"], "LOGGED OUT")
            menu()
        else:
            print("\nInvalid choice, please try again.")
            time.sleep(1)
            continue
def finance_acct_dashboard(user_dict):
    print(f"\nWelcome {user_dict['Username'].upper()} to the Finance Accountant Dashboard")
    print("1. MANAGE ACCOUNTS")
    print("2. PREPARE FINANCIAL STATEMENTS")
    print("3. CONTACT SUPPORT")
    print("4. LOGOUT")
    while True:
        choice = input("\n")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            from main import help_desk
            help_desk()
        elif choice == "4":
            print("\nLogging out...")
            time.sleep(1)
            from main import menu, logs
            logs(user_dict["Username"], "LOGGED OUT")
            menu()
        else:
            print("\nInvalid choice, please try again.")
            time.sleep(1)
            continue
def finance_clerk_dashboard(user_dict):
    print(f"\nWelcome {user_dict['Username'].upper()} to the Finance Clerk Dashboard")
    print("1. VIEW EMPLOYEE PAYROLL")
    print("2. MANAGE FINANCIAL DOCUMENTS")
    print("3. CONTACT SUPPORT")
    print("4. LOGOUT")
    while True:
        choice = input("\n")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            from main import help_desk
            help_desk()
        elif choice == "4":
            print("\nLogging out...")
            time.sleep(1)
            from main import menu, logs
            logs(user_dict["Username"], "LOGGED OUT")
            menu()
        else:
            print("\nInvalid choice, please try again.")
            time.sleep(1)
            continue
