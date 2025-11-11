# Week 7: Secure Authentication System

Student Name: [MARK KIHAGI KANARI]
Student ID: [M01059000]
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform

## Project Description

- A command-line authentication system implementing secure password hashing.
- This system allows users to register accounts and log in with proper password security through the use of bcrypt supports user login by verifying the entered password against the stored hash in users.txt.

## Features 

- During registration, the user provides a username and password.
- The password is then hashed and stored in a file named users.txt alongside the username.
- When logging in, the system checks whether the username exists, and if it does, bcrypt verifies that the password provided matches the stored hash.
- A simple menu is used to navigate between registration, login, and exit.

## Data storage format

- User credentials set in the users.txt file are in the format:
  username:hashed_password

## Running the program

- Ensure Python 3 is installed.
- Install bcrypt.
- Run the auth.py program.

## Testing results

The following tests were completed to verify that the system works as intended:
| Test | Action | Expected Result | Actual Result | Outcome |
| 1 | Register a new user | User is added to users.txt with a hashed password | User added successfully | Passed |
| 2 | Attempt to register same username again | System should not duplicate user | Registration blocked | Passed |
| 3 | Login with correct passsword | Access should be granted | Access granted | Passed |
| 4 | Login with incorrect password | Access should be denied | Access denied | Passed |
| 5 | Login with non-existent username | System should say user not found | User not found message | Passed | 

## Files included in this submission:
- auth.py - main authentication program.
- users.txt - stored usernames and hashed password.
- requirements.txt - python library bcrypt.
