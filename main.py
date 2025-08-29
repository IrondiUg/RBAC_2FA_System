import os
import pyotp
import qrcode
import time
import hashlib
import datetime
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
    print(f"Scan this QR code with Google Authenticator: {img_file}")
    print(f"Or manually enter this URI in your Authenticator app:\n{uri}")
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
                    k, v = p.split(":", 1)  # split only at first colon
                    user_data[k.strip()] = v.strip()

            
            if user_data.get("Username") == username:
                if "2FA_Key" not in user_data:
                    print("\n2FA not set up for this user.")
                    return False
                        
                secret = user_data["2FA_Key"]
                totp = pyotp.TOTP(secret)
                if totp.verify(code):
                    print("\n✅ 2FA verified!")
                    return True
                else:
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

def work_hours():
    time = datetime.datetime.now().time()
    return 8 <= time.hour < 16

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def help_desk():
    """Function to display help desk information."""
    os.system("cls")
    print("\n==HELP DESK==")
    print("For assistance, please contact ...")
          

def Login():
    """Function to handle user login and redirect to dashboard."""
    while True:
        print("\n==HELLO THERE, LOGIN TO CONTINUE==")
        username = input("\nEnter Username:_")
        password = input("Enter password:_")
        #if not work_hours():
           # print("n\⚠⚠ UNAUTHORIZED LOGIN ATTEMPT OUTSIDE WORK HOURS.")
          #  logs(username, "FAILED LOGIN OUTSIDE WORK HOURS")
         #   time.sleep(2)
        #    break
        with open(os.path.join(BASE_DIR, "dataB.txt"), "r", encoding="utf-8") as pass_file:
            hashed_pass = hash_password(password)
            pass_found = False
            for line in pass_file:
                if not line.strip():
                    continue
                parts = line.strip().split(" || ")
                user_dict = {p.split(":")[0].strip(): p.split(":")[1].strip() for p in parts}

                if user_dict["Username"] == username and user_dict["Password"] == hashed_pass:
                    pass_found = True
                    code = input("\nEnter the 6-digit code from your Authenticator app: ")
                    if not verify_2fa(username, code):
                        logs(username, "⚠ FAILED LOGIN - INVALID 2FA")
                        time.sleep(1)
                        continue
                else:
                    pass_found = False
                    break
        if pass_found:
            print("✅ LOGIN SUCCESSFUL")
            logs(username, "SUCCESSFUL LOGIN")

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
        else:
            print("\nINVALID USERNAME OR PASSWORD")
            logs(username, "⚠ FAILED LOGIN")
            time.sleep(1)
            continue

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
                pass_file.write(f'Username: {username} || Password: {hashed_pass} || Department: {department} || Role: {role} || 2fa_Key:{key}' "\n")
                time.sleep(1)
                print(f"\nUser: {username} successfully added")
                logs(user_dict["Username"], "added New User:", username)
                time.sleep(3)
                it_admin_dashboard(user_dict)
                break

def menu():
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
            help_desk()
            break
        else:
            print("Invalid Option")
            time.sleep(1)
            continue
if __name__ == "__main__":
    menu()