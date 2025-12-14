from pathlib import Path
import pandas as pd


def load_datasets_from_csv(conn):
    """Load dataset metadata from CSV file into database"""
    csv_path = Path("DATA") / "datasets_metadata.csv"
    df = pd.read_csv(csv_path)
    df.to_sql('datasets_metadata', conn, if_exists='append', index=False)
    return len(df)


def insert_dataset(conn, dataset_id, name, rows, columns, uploaded_by, upload_date):
    """Adding new dataset to database"""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO datasets_metadata (dataset_id, name, rows, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (dataset_id, name, rows, columns, uploaded_by, upload_date)
    )
    conn.commit()
    return cursor.lastrowid

def get_all_datasets(conn):
    """Retrieving all datasets"""
    query = "SELECT * FROM datasets_metadata"
    return pd.read_sql(query, conn)

def get_dataset_by_id(conn, dataset_id):
    """Retrieving dataset by ID"""
    query = "SELECT * FROM datasets_metadata WHERE dataset_id = ?"
    return pd.read_sql(query, conn, params=(dataset_id,))

def update_dataset_name(conn, dataset_id, new_name):
    """updating dataset name"""
    cursor = conn.cursor()
    cursor.execute(
    """ UPDATE datasets_metadata SET name = ? WHERE dataset_id = ? """, (new_name,dataset_id,),
    )
    conn.commit()
    return cursor.rowcount

def delete_dataset(conn, dataset_id):
    """deleting dataset by ID"""
    cursor = conn.cursor()
    cursor.execute(
        """ DELETE FROM datasets_metadata WHERE dataset_id = ? """, (dataset_id,)
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
    Load CSV files into their respective tables.

    TODO: Implement this function.

    Args:
        conn: Database connection
    """

    cursor = conn.cursor()

    # Ensuring table is empty before loading
    for tables in ("cyber_incidents", "datasets_metadata", "it_tickets"):
        cursor.execute(f"DELETE FROM {tables};")
    conn.commit()

    total_rows = 0

    print("\nloading datasets_metadata.csv...")
    total_rows += load_csv_to_table(conn, "DATA/datasets_metadata.csv", "datasets_metadata")


    print(f"\n Total rows loaded: {total_rows}")
    return total_rows





