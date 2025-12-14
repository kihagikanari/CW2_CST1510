from pathlib import Path
import pandas as pd


def load_tickets_from_csv(conn):
    """Load ticket data from CSV file into database"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM it_tickets")  # Clear existing data first
    conn.commit()

    csv_path = Path("DATA") / "it_tickets.csv"
    df = pd.read_csv(csv_path)
    df.to_sql('it_tickets', conn, if_exists='append', index=False)
    return len(df)

def insert_ticket(conn, ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours):
    """Creating new It ticket"""
    cursor = conn.cursor()
    cursor.execute("""
         INSERT INTO it_tickets (
            ticket_id,
            priority,
            description,
            status,
            assigned_to,
            created_at,
            resolution_time_hours
        )
        VALUES ( ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ticket_id,
            priority,
            description,
            status,
            assigned_to,
            created_at,
            resolution_time_hours,
        ),
    )
    conn.commit()
    return cursor.lastrowid

def get_all_tickets(conn):
    """Getting all tickets"""
    query = "SELECT * FROM it_tickets"
    return pd.read_sql(query, conn)

def get_ticket_by_id(conn, ticket_id):
    """Getting ticket by ID"""
    query = "SELECT * FROM it_tickets WHERE ticket_id = ?"
    return pd.read_sql(query, conn, params=(ticket_id,))

def get_ticket_by_status(conn, new_status):
    """Getting ticket by status"""
    query = "SELECT * FROM it_tickets WHERE status = ?"
    return pd.read_sql(query, conn, params=(new_status,))

def update_ticket_status(conn, ticket_id, new_status):
    """Updating ticket status"""
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE it_tickets SET status = ? WHERE ticket_id = ?""",
        (new_status, ticket_id),
    )
    conn.commit()
    return cursor.rowcount

def delete_ticket(conn, ticket_id):
    """Deleting ticket"""
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM it_tickets WHERE ticket_id = ?""",
        (ticket_id,),
    )
    conn.commit()
    return cursor.rowcount

def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.

    TODO: Implement this function.

    Args:
        conn: Database connection
        csv_path: Path to CSV file
        table_name: Name of the target table

    Returns:
        int: Number of rows loaded
    """
    # TODO: Check if CSV file exists
    csv_path = Path(csv_path)
    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return 0

    # TODO: Read CSV using pandas.read_csv()
    df = pd.read_csv(csv_path)

    # TODO: Use df.to_sql() to insert data
    # Parameters: name=table_name, con=conn, if_exists='append', index=False
    df.to_sql(name=table_name, con=conn, if_exists="append", index=False)

    # TODO: Print success message and return row count
    row_count = len(df)
    print(f"Loaded {row_count} rows into {table_name}")
    return row_count

def load_all_csv_data(conn):
    """
    Load  CSV files into their respective tables.

    TODO: Implement this function.

    Args:
        conn: Database connection
    """

    cursor = conn.cursor()

    # Ensuring table is empty before loading
    for tables in ("cyber_incidents", "datasets_metadata","it_tickets"):
        cursor.execute(f"DELETE FROM {tables};")
    conn.commit()

    total_rows = 0

    print("\nloading it_tickets.csv...")
    total_rows += load_csv_to_table(conn, "DATA/it_tickets.csv", "it_tickets")

    print(f"\n Total rows loaded: {total_rows}")
    return total_rows

