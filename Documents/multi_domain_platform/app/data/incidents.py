from pathlib import Path
import pandas as pd

def load_incidents_from_csv(conn):
    """Load incident data from CSV file into database"""
    csv_path = Path("DATA") / "cyber_incidents.csv"
    df = pd.read_csv(csv_path)
    df.to_sql('cyber_incidents', conn, if_exists='append', index=False)
    return len(df)

def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """
    Insert a new cyber incident into the database.

    Args:
        conn: Database connection
        date: Incident date (YYYY-MM-DD)
        incident_type: Type of incident
        severity: Severity level
        status: Current status
        description: Incident description
        reported_by: Username of reporter (optional)

    Returns:
        int: ID of the inserted incident
    """
    cursor = conn.cursor()
    query = "INSERT INTO cyber_incidents (date, incident_type, severity, status, description, reported_by) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    return cursor.lastrowid

def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.

    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table

    Returns:
        int: Number of rows loaded
    """
    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return 0

    df = pd.read_csv(csv_path)
    df.to_sql(name=table_name, con=conn, if_exists="append", index=False)

    row_count = len(df)
    print(f"Loaded {row_count} rows into {table_name}")
    return row_count

def load_all_csv_data(conn):
    """
    Load  CSV files into their respective tables.

    Args:
        conn: Database connection
    """
    cursor = conn.cursor()

    # Ensuring table is empty before loading
    for table in ("cyber_incidents", "datasets_metadata", "it_tickets"):
        cursor.execute(f"DELETE FROM {table};")
    conn.commit()

    total_rows = 0

    print("\nLoading cyber_incidents.csv...")
    total_rows += load_csv_to_table(conn, "DATA/cyber_incidents.csv", "cyber_incidents")

    print(f"\nTotal rows loaded: {total_rows}")
    return total_rows

def get_all_incidents(conn):
    """
    Retrieve all incidents from the database.

    Returns:
        pandas.DataFrame: All incidents
    """
    return pd.read_sql_query("SELECT * FROM cyber_incidents", conn)

def update_incident_status(conn, incident_id, new_status):
    """
    Update the status of an incident.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE cyber_incidents SET status = ? WHERE incident_id = ?", (new_status, incident_id))
    conn.commit()
    return cursor.rowcount

def delete_incident(conn, incident_id):
    """
    Delete an incident from the database.
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cyber_incidents WHERE incident_id = ?", (incident_id,))
    conn.commit()
    return cursor.rowcount

def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df