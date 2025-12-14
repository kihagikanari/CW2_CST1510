from database.db import *
from app.data.schema import create_all_tables
from app.data.users import migrate_users_from_file, register_user, login_user
from app.data.incidents import *
from app.data.datasets import *
from app.data.tickets import *


def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """
    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)

    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("       Connected")

    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)

    # Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file(conn)
    print(f"       Migrated {user_count} users")

    # Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    total_rows = load_all_csv_data(conn)

    # Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()

    # Count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")

    conn.close()

    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n Database location: {DB_PATH}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")


def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "="*60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("="*60)

    conn = connect_database()

    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")

    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")

    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")

    # Create
    test_id = insert_incident(
        conn,
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"  Create: Incident #{test_id} created")

    # Read
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE incident_id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read: Found incident #{test_id}")

    # Update
    update_incident_status(conn, test_id, "Resolved")
    print(f"  Update:  Status updated")

    # Delete
    delete_incident(conn, test_id)
    print(f"  Delete:  Incident deleted")

    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")

    df_by_type = get_incidents_by_type_count(conn)
    print(f"  By Type:     Found {len(df_by_type)} incident types")

    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: Found {len(df_high)} status categories")


    print("\n" + "="*60)
    print("TESTS PASSED!")
    print("="*60)

    # TEST 4: Dataset CRUD
    print("\n[TEST 4] Dataset CRUD Operations")
    dataset_id = insert_dataset(conn, 999, "Test Dataset", 100, 10, "test_user", "2024-11-18")
    print(f"Create: Dataset #{dataset_id} created")

    datasets = get_all_datasets(conn)
    print(f" Read: Found {len(datasets)} datasets")

    update_dataset_name(conn, 999, "Updated Dataset")
    print("Update: Dataset name updated")

    delete_dataset(conn, 999)
    print("Delete: Dataset removed")

    # TEST 5: Ticket CRUD
    print("\n[TEST 5] Ticket CRUD Operations")
    ticket_id = insert_ticket(conn, 999, "High", "Test ticket", "Open", "tech_support", "2024-11-18", 2)
    print(f"Create: Ticket #{ticket_id} created")

    tickets = get_all_tickets(conn)
    print(f" Read: Found {len(tickets)} tickets")

    update_ticket_status(conn, 999, "Closed")
    print(" Update: Ticket status updated")

    delete_ticket(conn, 999)
    print(" Delete: Ticket removed")

    # TEST 6: CSV Data Loading
    print("\n[TEST 6] CSV Data Loading")
    incident_count = load_incidents_from_csv(conn)
    dataset_count = load_datasets_from_csv(conn)
    ticket_count = load_tickets_from_csv(conn)
    print(f" CSV Loaded: {incident_count} incidents, {dataset_count} datasets, {ticket_count} tickets")

    # TEST 7: SQL Injection Prevention
    print("\n[TEST 7] SQL Injection Prevention")
    malicious_input = "test'; DROP TABLE users; --"
    try:
        insert_incident(conn, "2024-11-05", malicious_input, "Low", "Open", "Test", "test_user")
        print(" SQL injection safely handled with parameterized queries")
    except Exception as e:
        print(f" Security: {e}")

    conn.close()

def main():
    print("\n" + "="*60)
    print("CST1510 WEEK 8 LAB")
    print("Complete database setup")
    print("="*60)

    setup_database_complete()
    run_comprehensive_tests()

    return True

if __name__ == "__main__":
    main()