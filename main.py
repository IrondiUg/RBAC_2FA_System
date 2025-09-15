import os
import pyotp
import qrcode
import time
import utils
import hashlib
import datetime
from datetime import timedelta
from dashboard import (
    it_admin_dashboard,
    it_engineer_dashboard,
    it_intern_dashboard,
    hr_manager_dashboard,
    hr_recruiter_dashboard,
    hr_clerk_dashboard,
    finance_dir_dashboard,
    finance_acct_dashboard,
    finance_clerk_dashboard,
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCK_FILE = os.path.join(BASE_DIR, "locked.txt")
login_attempt_limit = 3
lockout_duration = timedelta(minutes=2)

def load_login_attempts():
    attempts = {}
    if not os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "w", encoding="utf-8") as file:
            file.write("")
        return attempts

    with open(LOCK_FILE, "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            parts = line.strip().split(" || ")
            user = parts[0]
            data = {}
            for p in parts[1:]:
                if ":" in p:
                    k, v = p.split(":", 1)
                    k = k.strip()
                    v = v.strip()
                    if k == "failed_attempts":
                        data[k] = int(v)
                    elif k == "locked_until":
                        data[k] = int(v)
            attempts[user] = data
    return attempts

def save_login_attempts(attempts):
    with open(LOCK_FILE, "w", encoding="utf-8") as f:
        for user, data in attempts.items():
            line = f"{user}"
            if "failed_attempts" in data:
                line += f" || failed_attempts:{int(data['failed_attempts'])}"
            if "locked_until" in data:
                line += f" || locked_until:{int(data['locked_until'])}"
            f.write(line + "\n")

def unlock_accounts(user_dict):
    username = user_dict["Username"]
    login_attempts = load_login_attempts()
    now = time.time()
    
    if not login_attempts:
        print("\n No accounts are currently locked.")
        time.sleep(2)
        input("\nPress Enter to go back...")
        it_admin_dashboard(user_dict)
    
    print("\n==Locked Accounts==")
    lists_of_locked = []
    for idx, (user, attempts) in enumerate(login_attempts.items(), start=1):
        if "locked_until" in attempts:
            locked_until = attempts["locked_until"]
            if now < locked_until:
                remaining = int(locked_until - now)
                minute, sec = divmod(remaining, 60)
                print(f"{idx}. {user}:  {minute} minutes: {sec} seconds Remaining")
                lists_of_locked.append(user)
    if not lists_of_locked:
        print("\n✅ No accounts are currently locked.")
        time.sleep(2)
        return
    choice = input("\nEnter account ID to unlock:_").strip()
    if not choice:
        return
    if not choice.isdigit() or not 1 <= int(choice) <= len(lists_of_locked):
        print("Invalid choice.")
        time.sleep(1)
        return
    user_to_unlock = lists_of_locked[int(choice) - 1]
    pass_correct = False
    code_2fa_correct = False
    while True:
        password = input(f"\nEnter your password to confirm unlock for {user_to_unlock}:_ ").strip()
        with open(os.path.join(BASE_DIR, "dataB.txt"), "r", encoding="utf-8") as pass_file:
            hashed_pass = hash_password(password)
            for line in pass_file:
                if not line.strip():
                    continue
                parts = line.strip().split(" || ")
                user_data = {p.split(":")[0].strip(): p.split(":")[1].strip() for p in parts}
                if user_data["Username"] == username and user_data["Password"] == hashed_pass:
                    pass_correct = True
                    time.sleep(1)
                    code = input("\nEnter the 6-digit code from your Authenticator app:_ ")
                    if verify_2fa(username, code):
                        code_2fa_correct = True
                    break
        if not pass_correct:
            time.sleep(1)
            print("\nINCORRECT PASSWORD")
            logs(username, f"⚠ FAILED UNLOCK ATTEMPT - ({user_to_unlock}), INCORRECT PASSWORD")
            time.sleep(1)
            continue
        if not code_2fa_correct:
            print("\nINVALID 2FA CODE")
            logs(username, f"⚠ FAILED UNLOCK ATTEMPT - ({user_to_unlock}), INVALID 2FA CODE")
            time.sleep(1)
            continue
        if login_attempts.get(user_to_unlock, {}).get("locked_until", 0) < time.time():
            print(f"\n✅ Account <{user_to_unlock}> Already unlocked, Lock Expired.")
            del login_attempts[user_to_unlock]
            time.sleep(2)
            continue
        
        if pass_correct and code_2fa_correct:
            login_attempts = load_login_attempts()
            if user_to_unlock in login_attempts:
                login_attempts[user_to_unlock]["locked_until"] = 0
                login_attempts[user_to_unlock]["failed_attempts"] = 0
                del login_attempts[user_to_unlock]
                save_login_attempts(login_attempts)
            print(f"\n✅ Account '{user_to_unlock}' has been unlocked.")
            logs(username, "UNLOCKED ACCOUNT:", user_to_unlock)
            print("\n Press Enter to go back...")
            input("")
            it_admin_dashboard(user_dict)
            return

def create_ticket(username, issue):
    tickets = utils.load_tickets()
    ticket_id = len(tickets) + 1
    ticket = {
        "id":ticket_id,
        "username": username,
        "issue": issue,
        "status": "OPEN",
        "messages": [{"from": username, "msg": issue}]
    }
    utils.append_ticket(ticket)
    logs(username, "CREATED A SUPPORT TICKET -- ", f"Ticket ID: {ticket['id']}")
    print(f"\n🎫 Ticket Number ({ticket['id']}) created for {username}.")
    time.sleep(2)
    help_desk(username)
    return ticket["id"]

def account_locked(username):
    login_attempts = load_login_attempts()
    now = time.time()
    if username in login_attempts:
        locked_until = login_attempts[username].get("locked_until", 0)
        if locked_until > now:
            remaining = int(locked_until - now)
            minute, sec = divmod(remaining, 60)
            time.sleep(1)
            print(f"\nAccount is locked Due To Multiple Failed Attempts. Try again in {minute} minutes : {sec} seconds.")
            print("\nPress 'S' to contact support. Press any other key to return to main menu.")
            choice = input("\n").strip().lower()
            if choice == 's':
                help_desk(username)
            else:
                menu()
            return True
    return False

def record_failed_attempt(username):
    login_attempts = load_login_attempts()
    if username not in login_attempts:
        login_attempts[username] = {"failed_attempts": 0, "locked_until": 0}
    login_attempts[username]["failed_attempts"] += 1
    if login_attempts[username]["failed_attempts"] >= login_attempt_limit:
        lock_till = time.time() + lockout_duration.total_seconds()
        login_attempts[username]["locked_until"] = lock_till
        time.sleep(1)
        login_attempts[username]["failed_attempts"] = 0
        save_login_attempts(login_attempts)
        print(f"\nToo Many Failed Attempts!! Account Locked For {lockout_duration.total_seconds()//60} minutes.")
        logs(username, "ACCOUNT LOCKED DUE TO MULTIPLE FAILED LOGIN ATTEMPTS")
        time.sleep(2)
        input("\n\nPress Enter to return...")
    else:
        save_login_attempts(login_attempts)

def successful_login(username):
    now = time.time()
    login_attempts = load_login_attempts()
    if username in login_attempts:
        locked_until = login_attempts[username].get("locked_until")
        if locked_until > now:
            remaining = int(locked_until - now)
            minute, sec = divmod(remaining, 60)
            print(f"\nAccount is locked. Try again in {minute} minutes : {sec} seconds.")
            logs(username, "FAILED LOGIN ATTEMPT ON LOCKED ACCOUNT")
            return False
        del login_attempts[username]
        save_login_attempts(login_attempts)
    return True

def view_database(user_dict):
    with open(os.path.join(BASE_DIR, "dataB.txt"), "r", encoding="utf-8") as file:
        os.system("cls")
        logs(user_dict["Username"], "ACCESSED USER DATABASE:")
        print(f"{'ID':<5}{'Username':<15}{'Role':<12}{'Department':<12}{'Key':<40}{'Password (hashed)':<65}")
        print("-" * 120)
        id = 1
        for line in file:
            if not line.strip():
                continue
            parts = line.strip().split(" || ")
            user_data = {}
            for p in parts:
                if ":" in p:
                    k, v = p.split(":", 1)
                    user_data[k.strip()] = v.strip()
            username = user_data.get("Username")
            dept = user_data.get("Department")
            role = user_data.get("Role")
            password = user_data.get("Password")
            key = user_data.get("2FA_Key")
            print(f"{id:<5}{username:<15}{role:<12}{dept:<12}{key:<40}{password}")
            id += 1
        input("\n\nPress Enter to return to the dashboard...")
        it_admin_dashboard(user_dict)

def set_2fa(username):
    key = pyotp.random_base32()
    totp = pyotp.TOTP(key)
    uri = totp.provisioning_uri(name=username, issuer_name="python_RBAC")
    qr = qrcode.QRCode()
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qrcode_dir = os.path.join(BASE_DIR, "User_QRCodes")
    os.makedirs(qrcode_dir, exist_ok=True)
    img_file = os.path.join(qrcode_dir, f"{username}_2fa.png")
    img.save(img_file)

    print(f"\n2FA setup complete for {username}!")
    print(f"Please scan the QR code saved at {img_file} using your Authenticator app.")
    return key

def verify_2fa(username, code):
    with open(os.path.join(BASE_DIR, "dataB.txt"), "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            # Split by ' || ' first
            parts = line.strip().split(" || ")
            user_data = {}
            for p in parts:
                if ":" in p:
                    k, v = p.split(":", 1)
                    user_data[k.strip()] = v.strip()

            
            if user_data.get("Username") == username:
                if "2FA_Key" not in user_data:
                    print("\n2FA not set up for this user.")
                    return False
                        
                secret = user_data["2FA_Key"]
                totp = pyotp.TOTP(secret)
                if totp.verify(code):
                    time.sleep(1)
                    print("\n✅ 2FA verified!")
                    return True
                else:
                    time.sleep(1)
                    print("\nInvalid 2FA code!")
                    return False
    print("\nUser not found")
    return False


def logs(username: str, action: str, other: str=None ) -> None:
    log_filename = f"logs_{datetime.date.today()}.log"
    log_path = os.path.join(BASE_DIR, log_filename)

    if not os.path.exists(log_path):
        with open(log_path, "w", encoding="utf-8") as log_file:
            log_file.write("User Activity Logs\n")
    with open(log_path, "a", encoding="utf-8") as log_file:
        if other:
            log_file.write(f"{datetime.datetime.now()}: USER: {username} || ACTION: {action} -> {other}\n")
        else:
            log_file.write(f"{datetime.datetime.now()}: USER: {username} || STATUS: {action}\n")

def view_logs(user_dict):
    log_filename = f"logs_{datetime.date.today()}.log"
    log_path = os.path.join(BASE_DIR, log_filename)

    if not os.path.exists(log_path):
        print("No logs available for today.")
        return

    with open(log_path, "r", encoding="utf-8") as log_file:
        logs(user_dict["Username"], "VIEWED AUDIT LOGS:")
        print("\n==SYSTEM LOGS==\n")
        for line in log_file:
            print(line.strip())
    input("\nPress Enter to return to the dashboard...")
    it_admin_dashboard(user_dict)

def work_hours():
    time = datetime.datetime.now().time()
    return 8 <= time.hour < 16

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def help_desk(username = None):
    if not username:
        username = input("Enter your username: ").strip()
        db_file = os.path.join(BASE_DIR, "dataB.txt")
        found = False
        if os.path.exists(db_file):
            with open(db_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    parts = line.strip().split(" || ")
                    user_data = {}
                    for p in parts:
                        if ":" in p:
                            k, v = p.split(":", 1)
                            user_data[k.strip()] = v.strip()
                    if user_data.get("Username") == username:
                        found = True
                        break

        if not found:
            print("\n⚠ User not found. Returning to main menu.")
            time.sleep(1)
            return
    while True:
        os.system("cls")
        print("\n==HELP DESK==")
        print("1. Open a Ticket")
        print("2. View Opened Tickets")
        print("3. Back to Main Menu")
        choice = input("\n").strip()
        if choice == '1':
            create_ticket(username.strip(), issue=input("Describe your issue: ").strip())
            break
        elif choice == '2':
            view_my_tickets(username)

        elif choice == '3':
            return
        else:
            print("Invalid Option")
            time.sleep(1)

def view_my_tickets(username):
    tickets = utils.load_tickets()
    user_tickets = [t for t in tickets if t.get("username") == username and t.get("status") == "OPEN"]
    while True:
        if not user_tickets:
            print("\n✅ You have no active tickets.")
            time.sleep(2)
            return

        os.system("cls")
        print(f"\n📂 Active Tickets for {username}:")
        for t in user_tickets:
            print(f"\n=== Ticket Number - {t['id']} ===")
            print(f"Issue: {t['issue']}")
            print(f"Status: {t['status']}")
            print("\n💬 List:")
            with open(os.path.join(BASE_DIR, "tickets.log"), "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(f"ID: {t['id']} "):
                        print(line.strip())


        ticket_id = input("\nEnter Ticket ID to reply (or press Enter to go back): ").strip()
        
        if not ticket_id:
            break  

        if ticket_id.isdigit():
            ticket = next((t for t in user_tickets if t["id"] == ticket_id), None)
            if ticket:
                choice = input("'R' to reply, or press Enter to go back: ").strip().lower()
                if choice == 'r':
                    reply = input("Enter your reply: ")
                    ticket["messages"].append({"from": username, "msg": reply})
                    utils.save_tickets(tickets)
                    print("✅ Reply added.")
                    time.sleep(1)
            else:
                print("⚠ Invalid Ticket ID.")
                time.sleep(1)
        else:
            print("⚠ Please enter a valid number.")
            time.sleep(1)


def Login():
    """Function to handle user login and redirect to dashboard."""
    while True:
        os.system("cls")
        print("\n== HELLO THERE, LOGIN TO CONTINUE ==")
        username = input("\nEnter Username:_").strip()
        password = input("Enter password:_").strip()
        #if not work_hours():
           # print("n\⚠⚠ UNAUTHORIZED LOGIN ATTEMPT OUTSIDE WORK HOURS.")
          #  logs(username, "FAILED LOGIN OUTSIDE WORK HOURS")
         #   time.sleep(2)
        #    break
        if account_locked(username):
            time.sleep(2)
            return
        with open(os.path.join(BASE_DIR, "dataB.txt"), "r", encoding="utf-8") as pass_file:
            hashed_pass = hash_password(password)
            pass_found = False
            pass_2fa = False
            user = False
            pwd = False
            for line in pass_file:
                if not line.strip():
                    continue
                parts = line.strip().split(" || ")
                user_dict = {p.split(":")[0].strip(): p.split(":")[1].strip() for p in parts}

                if user_dict["Username"] == username:
                    user = True
                if  user_dict["Password"] == hashed_pass:
                    pwd = True
                if user and pwd:
                    pass_found = True
                    time.sleep(1)
                    code = input("\nEnter the 6-digit code from your Authenticator app: ")
                    if verify_2fa(username, code):
                        pass_2fa = True
                    break
        if not user:
            time.sleep(.8)
            print("\nUSERNAME DOESN'T EXIST")
            time.sleep(1)
            continue
        if not pwd:
            time.sleep(.8)
            print("\nINCORRECT PASSWORD")
            logs(username, "⚠ FAILED LOGIN, INCORRECT PASSWORD")
            time.sleep(1)
            record_failed_attempt(username)
            time.sleep(1)
            continue
        if not pass_2fa:
            logs(username, "⚠ FAILED LOGGING ATTEMPT, INVALID 2FA CODE")
            time.sleep(1)
            continue
        if pass_found and pass_2fa:
            if successful_login(username):
                print("✅ LOGIN SUCCESSFUL")
                logs(username, "SUCCESSFUL LOGIN")
                time.sleep(2)
                os.system("cls")
                if user_dict["Role"] == "ADMIN" and user_dict["Department"] == "IT":
                    it_admin_dashboard(user_dict)
                elif user_dict["Role"] == "ENGINEER" and user_dict["Department"] == "IT":
                    it_engineer_dashboard(user_dict)
                elif user_dict["Role"] == "INTERN" and user_dict["Department"] == "IT":
                    it_intern_dashboard(user_dict)
                elif user_dict["Role"] == "MANAGER" and user_dict["Department"] == "HR":
                    hr_manager_dashboard(user_dict)
                elif user_dict["Role"] == "RECRUITER" and user_dict["Department"] == "HR":
                    hr_recruiter_dashboard(user_dict)
                elif user_dict["Role"] == "CLERK" and user_dict["Department"] == "HR":
                    hr_clerk_dashboard(user_dict)
                elif user_dict["Role"] == "DIRECTOR" and user_dict["Department"] == "FINANCE":
                    finance_dir_dashboard(user_dict)
                elif user_dict["Role"] == "ACCOUNTANT" and user_dict["Department"] == "FINANCE":
                    finance_acct_dashboard(user_dict)
                elif user_dict["Role"] == "CLERK" and user_dict["Department"] == "FINANCE":
                    finance_clerk_dashboard(user_dict)

def addUser(user_dict):
    print("SELECT DEPARTMENT")
    print("1. IT")
    print("2. HR")
    print("3. FINANCE")
    print("4. GO BACK")
    dept_choice = input("\n")
    while True:
        if dept_choice == '1':
            department = 'IT'
            print("SELECT ROLE IN IT DEPARTMENT")
            print("1. ADMIN")
            print("2. ENGINEER")
            print("3. INTERN")
            rol_sel = input("\n")
            if rol_sel=='1':
                role = 'ADMIN'
                break
            elif rol_sel == '2':
                role = 'ENGINEER'
                break
            elif rol_sel == '3':
                role = 'INTERN'
                break
            else:
                print("INVALID OPTION")
                continue
        elif dept_choice=='2':
            department = 'HR'
            print("SELECT ROLE IN HR DEPARTMENT")
            print("1. MANAGER")
            print("2. RECRUITER")
            print("3. CLERK")
            rol_sel = input("\n")
            if rol_sel=='1':
                role = 'MANAGER'
                break
            elif rol_sel == '2':
                role = 'RECRUITER'
                break
            elif rol_sel == '3':
                role = 'CLERK'
                break
            else:
                print("INVALID OPTION")
                continue
        elif dept_choice=='3':
            department = 'FINANCE'
            print("SELECT ROLE IN FINANCE DEPARTMENT")
            print("1. DIRECTOR")
            print("2. ACCOUNTANT")
            print("3. CLERK")
            rol_sel = input("\n")
            if rol_sel=='1':
                role = 'DIRECTOR'
                break
            elif rol_sel == '2':
                role = 'ACCOUNTANT'
                break
            elif rol_sel == '3':
                role = 'CLERK'
                break
            else: 
                print("INVALID OPTION")
                continue
        elif dept_choice=='4':
            time.sleep(1)
            it_admin_dashboard(user_dict)
            break
        else:
            print("INVALID OPTION")
            continue

    while True:
        print(f"\n==REGISTER A NEW USER IN {department}==")
        username = input("\nEnter new Username:_ ")
        time.sleep(1)
        password = input("\nEnter password:_ ")
        confirm_password =  input("Please confirm password:_")
        with open(os.path.join(BASE_DIR, "dataB.txt"), "r", encoding="utf-8") as pass_file:
            existing_user = [line.strip().split(' || ')[0].replace("Username:", "") for line in pass_file]
            if username in existing_user:
                time.sleep(1)
                print("\nUsername taken, please enter another username")
                continue
            if password != confirm_password:
                print("Passwords do not match\n")
                time.sleep(1)
                continue
            
        if password == confirm_password:
            hashed_pass = hash_password(password)
            key = set_2fa(username)
            file_path = os.path.join(BASE_DIR, "dataB.txt")
            with open(file_path, "a", encoding="utf-8") as pass_file:
                pass_file.write(f'Username: {username} || Password: {hashed_pass} || Department: {department} || Role: {role} || 2FA_Key:{key}' "\n")
                pass_file.flush()
                os.fsync(pass_file.fileno())
                time.sleep(1)
                print(f"\nUser: {username} successfully added")
                logs(user_dict["Username"], "added New User:", username)
                time.sleep(3)
                it_admin_dashboard(user_dict)
                break

def menu(username=None):
    """Function to display the main menu and handle user choices."""
    while True:
        os.system("cls")
        print("==HELLO THERE!==")
        print("\n1. LOGIN\n")
        print("2. CONTACT SUPPORT")
        choice =  input("\n")
        if choice == '1':
            time.sleep(0.5)
            Login()
            break
        elif choice == '2':
            time.sleep(0.5)
            help_desk(username)
        else:
            print("Invalid Option")
            time.sleep(1)
            continue
if __name__ == "__main__":
    menu()