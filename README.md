## RBAC-2FA_System – Python Role-Based Access Control 
RBAC-System is a robust Python Role-Based Access Control (RBAC) system designed for organizations with multiple departments and ranks. It ensures secure, structured, and auditable access for all users.

---

## Core Functionality
- 👥 **Role-Based Access:** Each user’s permissions are determined by their department and role, ensuring proper access control.
- 📱 **Multi-Factor Authentication (MFA):** QR-code-based TOTP authentication with Google Authenticator or Authy.
- 🔏 **Failed Login Attempt Limit:** After 3 failed login attempts, account is locked, to be retreived throught IT support.
- 🎛️ **Custom Dashboards:** Personalized dashboards for each role provide relevant tools and information.  
- ⏰ **Time-Based Login Restrictions:** Users can only log in during working hours (8 AM–4 PM) unless granted admin authorization.  
- 📌 **Comprehensive Activity Tracking:** Every login, logout, and action is recorded for audit and accountability purposes.  

---
### Quick Features
```
| 🔒 Secure Login Authentication ✅    
| 📊 Department-Specific Dashboards ✅    
| 🛡️ Rank-Based Permissions ✅    
| 📝 Activity Logging  ✅   
| ⏰ Time-Based Login Restrictions ✅     
| 📱 Multi-Factor Authentication ✅     
| 📌 Comprehensive Session Tracking ✅     
| 🗂️ Logs Export and Auditing  ✅     
```

## Requirements
- Python 3.8 or later  
- pip (Python package installer)  

### Python Libraries
- **pyotp** → Generate & validate OTP tokens  
- **qrcode** → Generate QR codes for MFA setup  
- **pillow** → Image handling for QR codes  

---

## Setup & Run
### 1. Clone the repository
```bash
git clone https:https://github.com/IrondiUg/RBAC_2FA_System.git
cd RBAC_2FA-System
```
### 2. Install dependencies
```
pip install -r requirements.txt
```
### 3. Run the system
```
python main.py
```

## Project Structure
```
RBAC-System/
│
├── logs/                        
│   └── .gitkeep
│
├── User_QRcodes/               
│   └── .gitkeep
│
├── dashboards.py               
├── main.py                      
├── requirements.txt
├── users.txt             
├── README.md                    
└── LICENSE                     
```

## Note
- For the time based access control, uncomment this section in main.py to be able to use it, it works with your machine time.
   ![see image](https://img001.prntscr.com/file/img001/UDt7TrxGTEmGFvul7NR_mw.png)


- Some default logging credentials are in user.txt
- default users have 2fa appended already, to get the codes, scan the generated QRcodes in [User_QRcodes folder](User_QRcodes/) with an authenticator app.


- ⚠⚠ PLEASE ENSURE SYSTEM'S CLOCK IS IN SYNC WITH THE DEVICE WHERE YOUR AUTHENTICATION APP/CODES IS/ARE
- For any issues, please open an issue on the GitHub repository.

- Contributions are welcome! Feel free to fork the repository and submit pull requests.

