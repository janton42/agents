import sqlite3
import csv
from pathlib import Path

# --- Load existing emails from spreadsheet ---

def coordinate_candidate_db(candidates, sp_file_path, db_file_path):
    existing_emails = set()

    csv_path = Path(sp_file_path)
    if csv_path.exists():
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = row.get("EMAIL")
                if email:
                    existing_emails.add(email.strip().lower())

    # --- Set up db ---
    conn = sqlite3.connect(str(db_file_path))
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            org_name TEXT,
            contact_email TEXT UNIQUE,
            justification TEXT
        )
    """)

    # --- Load existing emails already in db ---

    cur.execute("SELECT contact_email FROM candidates")
    existing_emails.update(
        row[0].strip().lower() for row in cur.fetchall() if row[0]
    )

    # --- Filter and insert ---

    inserted = 0
    skipped = 0
    for c in candidates:
        email = (c.get("contact_email") or "").strip().lower()

        if not email or email in existing_emails:
            skipped += 1
            continue

        cur.execute(
            "INSERT INTO candidates (org_name, contact_email, justification) VALUES (?, ?, ?)",
            (c.get("org_name"), email, c.get("justification"))
        )
        existing_emails.add(email)
        inserted += 1

    conn.commit()
    conn.close()
    confirmation_message = f"Inserted: {inserted}, Skipped (duplicate/missing email): {skipped}"
    return confirmation_message
