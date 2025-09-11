from main import login_attempts
import time
import os
import utils

def view_locked_accounts():
    print("\n==Locked Accounts:==")
    for username, attempts in login_attempts.items():
        if "locked_until" in attempts:
            locked_until = attempts["locked_until"]
            if time.time() < locked_until:
                remaining = int(locked_until - time.time())
                minute, sec = divmod(remaining, 60)
                print(f"- {username}: Locked for another {minute} minutes and {sec} seconds")
    input("\nPress Enter to return to the main menu...")

def view_tickets():
    tickets = utils.load_tickets()
    if not tickets:
        print("\n✅ No tickets available.")
        time.sleep(2)
        return
    
    print("\n📂 Active Tickets:")
    for t in tickets:
        print(f"ID: {t['id']} | User: {t['username']} | Issue: {t['issue']} | Status: {t['status']}")

    choice = input("\nEnter Ticket ID to open (or press Enter to go back): ").strip()
    if choice.isdigit():
        open_ticket(int(choice))

def open_ticket(ticket_id):
    tickets = utils.load_tickets()
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        print("\n⚠ Invalid Ticket ID.")
        return
    
    print(f"\n=== Ticket #{ticket['id']} ===")
    print(f"User: {ticket['username']}")
    print(f"Issue: {ticket['issue']}")
    print(f"Status: {ticket['status']}")
    print("\n💬 Conversation:")
    for m in ticket["messages"]:
        print(f"{m['from']}: {m['msg']}")

    while True:
        print("\nOptions: ")
        print("1. Add Reply")
        print("2. Mark as Resolved")
        print("3. Go Back")
        action = input("Select option: ").strip()

        if action == "1":
            reply = input("Enter your reply: ")
            ticket["messages"].append({"from": "support", "msg": reply})
            utils.save_tickets(tickets)
            print("✅ Reply added.")
        elif action == "2":
            ticket["status"] = "CLOSED"
            utils.save_tickets(tickets)
            print("✅ Ticket closed.")
            break
        elif action == "3":
            break
        else:
            print("⚠ Invalid choice.")

def help_desk():
    while True:
        os.system("cls")
        print("1. View Locked Accounts")
        print("2. View Opened Tickets")
        print("3. Go Back")
        choice = input("\nSelect an option: ").strip()
        if choice == '1':
            view_locked_accounts()
        elif choice == '2':
            view_tickets()
        elif choice == '3':
            break
        else:
            print("⚠ Invalid Option")
            time.sleep(1)
        continue
if __name__ == "__main__":
    help_desk()