import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TICKETS_FILE = os.path.join(BASE_DIR, "tickets.log")

def append_ticket(ticket):
    messages_str = "; ".join([f"{m['from']}: {m['msg']}" for m in ticket["messages"]])
    with open(TICKETS_FILE, "a", encoding= "utf-8") as f:
        f.write(
            f"ID: {ticket['id']} | User: {ticket['username']} | Issue: {ticket['issue']} | "
            f"Status: {ticket['status']} | "
            f"Messages: {messages_str}\n"
        )
def load_tickets():
    tickets = []
    if not os.path.exists(TICKETS_FILE):
        return tickets

    with open(TICKETS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(" | ")
            data = {}
            for p in parts:
                if ":" in p:
                    k, v = p.split(":", 1)
                    data[k.strip().lower()] = v.strip()
            if data:
                messages = []
                if "messages" in data and data["messages"]:
                    for m in data["messages"].split("; "):
                        if ": " in m:
                            sender, msg = m.split(": ", 1)
                            messages.append({"from": sender, "msg": msg})
                tickets.append({
                    "id": int(data.get("id", 0)),
                    "username": data.get("user", ""),
                    "issue": data.get("issue", ""),
                    "status": data.get("status", "OPEN"),
                    "messages": messages
                })
    return tickets

def save_tickets(tickets):
    with open(TICKETS_FILE, "w", encoding="utf-8") as f:
        for t in tickets:
            messages_str = "; ".join([f"{m['from']}: {m['msg']}" for m in t["messages"]])
            f.write(
                f"ID: {t['id']} | User: {t['username']} | "
                f"Issue: {t['issue']} | Status: {t['status']} | "
                f"Messages: {messages_str}\n"
            )
