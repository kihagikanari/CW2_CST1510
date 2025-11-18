import bcrypt
import os

#constant
USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
    #password encoding
    password_bytes = plain_text_password.encode("utf-8")
    #creating salt to hash password with
    salt = bcrypt.gensalt()
    #attaching the salt to the hash and decoding hash for storage
    hashed = bcrypt.hashpw(password_bytes, salt)
    #store as utf-8 string
    return hashed.decode("utf-8")

def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode("utf-8"),hashed_password.encode("utf-8"))

def user_exists(username):
    #case where file doesn't exist yet, no users exist
    if not os.path.exists(USER_DATA_FILE):
        return False

    #opening of file and checking each line
    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            stored_username = line.strip().split(":", 1)[0]
            if stored_username == username:
                return True
    return False

def register_user(username, password):
    #checking user already exists
    if user_exists(username):
        print("\nUser already exists.")
        return False

    #hashing password
    hashed_password = hash_password(password)

    #append the new user to the file
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username}:{hashed_password}\n")
        print(f"\nUser {username} registered successfully.")

def login_user(username, password):
    #checking if user is registered
    if not os.path.exists(USER_DATA_FILE):
        print("\nUser not found.")
        return False

    user_found = False

    #searching the file for the registered username and password
    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            stored_username, stored_hashed_password = line.strip().split(":", 1)

            if stored_username == username:
                user_found = True

                if verify_password(password, stored_hashed_password):
                    print(f"\nSuccess: Welcome, {username}!")
                    return True
                else:
                    print(f"\nError: incorrect password.")
                    return False

    if not user_found:
        print("\nError: User not found.")
    return False

def main():
    #main function
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
    #Displays the main menu options.
        print("\n" + "=" * 50)
        print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
        print(" Secure Authentication System")
        print("=" * 50)
        print("\n[1] Register a new user")
        print("[2] Login")
        print("[3] Exit")
        print("-" * 50)

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            confirm = input("Confirm password: ").strip()
            #adding password confirmation condition
            if password != confirm:
                print("\nPasswords do not match.")
                continue

            register_user(username, password)

        elif choice == "2":
            login_user(input("Username: "), input("Password: "))

        elif choice == "3":
            print("\nprogram exited...")
            break
        else:
            print("\nInvalid choice, Retry.")

if __name__ == "__main__":
    main()


