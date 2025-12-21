
## Core Functionalities
-  **Role-Based Authentication:** Every user is assigned a specific role (Admin, IT, HR, Finance, etc.), and access is granted strictly based on that role’s permissions.
-	**Two-Factor Authentication (2FA):** Adds an extra verification step after password login to strengthen account security.
-	**Admin-Only User Creation:** Only admins can add or manage users, ensuring centralized control and preventing unauthorized access.
-	**Account Lockout Policy:** After 3 failed login attempts, an account is automatically locked to prevent brute-force attacks.
-	**Timed Auto-Unlock:** Locked accounts unlock automatically after 5 minutes, reducing downtime while maintaining security.
-	**Admin/IT Unlock Override:** Admins or IT support can manually unlock accounts upon legitimate user requests.
-	**Session Tracking:** Logs user logins, logouts, and activities with timestamps for audit and accountability.
-	**Time-Based Access Restriction:** Users can log in only between 8 AM and 4 PM; admin authorization is required outside this window.

## Project Architecture
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
## Note
- For the time based access control, uncomment this section in main.py to be able to use it, it works with your machine time.
   ![Screenshot 2025-12-19 185617](https://github.com/user-attachments/assets/89951de2-72d9-482f-afa9-ee26bc77fdba)
- Some default logging credentials are in user.txt
- default users have 2fa appended already, to get the codes, scan the generated QRcodes in [User_QRcodes folder](User_QRcodes/) with an authenticator app or manually add the 2FA key in dataB.txt


- ⚠⚠ PLEASE ENSURE SYSTEM'S CLOCK IS IN SYNC WITH THE DEVICE WHERE YOUR AUTHENTICATION APP/CODES IS/ARE
- For any issues, please open an issue on the GitHub repository.

- Contributions are welcome! Feel free to fork the repository and submit pull requests.

## Video Demo
https://github.com/user-attachments/assets/5db24805-a55a-431d-ae65-55b0af0eb4fd







