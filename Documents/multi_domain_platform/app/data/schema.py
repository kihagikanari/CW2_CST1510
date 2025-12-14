from database.db import conn

def create_users_table(conn):
    """
    Create the users table if it doesn't exist.

    This is a COMPLETE IMPLEMENTATION as an example.
    Study this carefully before implementing the other tables!

    Args:
        conn: Database connection object
    """
    cursor = conn.cursor()

    # SQL statement to create users table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print("✅Users table created successfully!")


def create_cyber_incidents_table(conn):
    """
    Create the cyber_incidents table.

    TODO: Implement this function following the users table example above.

    Required columns:
    - incident_id: INTEGER PRIMARY KEY AUTOINCREMENT
    - date: TEXT (format: YYYY-MM-DD)
    - incident_type: TEXT (e.g., 'Phishing', 'Malware', 'DDoS')
    - severity: TEXT (e.g., 'Critical', 'High', 'Medium', 'Low')
    - status: TEXT (e.g., 'Open', 'Investigating', 'Resolved', 'Closed')
    - description: TEXT
    - reported_by: TEXT (username of reporter)
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
    # TODO: Get a cursor from the connection
    cursor = conn.cursor()
    # TODO: Write CREATE TABLE IF NOT EXISTS SQL statement
    # Follow the pattern from create_users_table()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        incident_type TEXT,
        severity TEXT,
        category TEXT,
        status TEXT,
        description TEXT,
        reported_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        timestamp TEXT,
        FOREIGN KEY (reported_by) REFERENCES users(username)
    )
    """
    # TODO: Execute the SQL statement
    cursor.execute(create_table_sql)
    # TODO: Commit the changes
    conn.commit()
    # TODO: Print success message
    print("cyber incidents table created successfully!")
    pass


def create_datasets_metadata_table(conn):
    """
    Create the datasets_metadata table.

    TODO: Implement this function following the users table example.

    Required columns:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - dataset_name: TEXT NOT NULL
    - category: TEXT (e.g., 'Threat Intelligence', 'Network Logs')
    - source: TEXT (origin of the dataset)
    - last_updated: TEXT (format: YYYY-MM-DD)
    - record_count: INTEGER
    - file_size_mb: REAL
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
    # TODO: Implement following the users table pattern
    cursor = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        dataset_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        rows INTEGER,
        columns INTEGER, 
        uploaded_by TEXT,
        upload_date TEXT
    )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print("datasets table created successfully!")
    pass


def create_it_tickets_table(conn):
    """
    Create the it_tickets table.

    TODO: Implement this function following the users table example.

    Required columns:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT
    - ticket_id: TEXT UNIQUE NOT NULL
    - priority: TEXT (e.g., 'Critical', 'High', 'Medium', 'Low')
    - status: TEXT (e.g., 'Open', 'In Progress', 'Resolved', 'Closed')
    - category: TEXT (e.g., 'Hardware', 'Software', 'Network')
    - subject: TEXT NOT NULL
    - description: TEXT
    - created_date: TEXT (format: YYYY-MM-DD)
    - resolved_date: TEXT
    - assigned_to: TEXT
    - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
    # TODO: Implement following the users table pattern=
    cursor = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS it_tickets (
        ticket_id INTEGER PRIMARY KEY,
        priority TEXT,
        description TEXT,
        status TEXT,
        assigned_to TEXT,
        created_at TEXT,
        resolution_time_hours INTEGER
    )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print("IT tickets table created successfully!")
    pass

def create_all_tables(conn):
    """
    Create all tables in the database.
    """
    cursor = conn.cursor()
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    conn.commit()
    print("\nAll tables created successfully!")

create_all_tables(conn)
