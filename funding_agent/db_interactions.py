import sqlite3

# --- Load existing emails from spreadsheet ---

def coordinate_candidate_db(candidates, db_file_path):
    existing_orgs = set()

    # --- Set up db ---
    conn = sqlite3.connect(str(db_file_path))
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS funding_candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            org_name TEXT UNIQUE,
            funding_amount REAL,
            application_deadline TEXT,
            application_url TEXT,
            justification TEXT
        )
    """)

    # --- Load existing emails already in db ---

    cur.execute("SELECT org_name FROM funding_candidates")
    existing_orgs.update(
        row[0].strip().lower() for row in cur.fetchall() if row[0]
    )

    # --- Filter and insert ---

    inserted = 0
    skipped = 0
    for c in candidates:
        org_name = (c.get("org_name") or "").strip().lower()

        if not org_name or org_name in existing_orgs:
            skipped += 1
            continue

        cur.execute(
            "INSERT INTO funding_candidates (org_name, funding_amount, application_deadline, application_url, justification) VALUES (?, ?, ?, ?, ?)",
            (org_name, c.get('funding_amount'), c.get('application_deadline'), c.get('application_url'), c.get('justification'))
        )
        existing_orgs.add(org_name)
        inserted += 1

    conn.commit()
    conn.close()
    confirmation_message = f"Inserted: {inserted} into 'funding_candidates' table,\nSkipped (duplicate/missing email): {skipped}"
    return confirmation_message
