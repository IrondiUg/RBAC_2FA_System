
## Core Functionality
- 👥 **Role-Based Access:** Each user’s permissions are determined by their department and role, ensuring proper access control.
- 📱 **Multi-Factor Authentication (MFA):** QR-code-based TOTP authentication with Google Authenticator or Authy.
- 🔏 **Failed Login Attempt Limit:** After 3 failed login attempts, account is locked, to be retreived throught IT support.
- 🎛️ **Custom Dashboards:** Personalized dashboards for each role provide relevant tools and information.  
- ⏰ **Time-Based Login Restrictions:** Users can only log in during working hours (8 AM–4 PM) unless granted admin authorization.  
- 📌 **Comprehensive Activity Tracking:** Every login, logout, and action is recorded for audit and accountability purposes.

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
├── locked.txt
├── tickets.log             
├── README.md                    
└── LICENSE                 
```
- Some default logging credentials are in user.txt
- default users have 2fa appended already, to get the codes, scan the generated QRcodes in [User_QRcodes folder](User_QRcodes/) with an authenticator app or manually add the 2FA key in dataB.txt


- ⚠⚠ PLEASE ENSURE SYSTEM'S CLOCK IS IN SYNC WITH THE DEVICE WHERE YOUR AUTHENTICATION APP/CODES IS/ARE
- For any issues, please open an issue on the GitHub repository.

- Contributions are welcome! Feel free to fork the repository and submit pull requests.



