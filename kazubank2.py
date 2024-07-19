import mysql.connector
from decimal import Decimal

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Afzal0510',
    'database': 'banks'
}

def initialize_database():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(50) PRIMARY KEY,
                password VARCHAR(20),
                balance DECIMAL(10, 2) DEFAULT 0.00
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transaction_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                transaction_description VARCHAR(255),
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        """)

        conn.commit()
        print("Database initialized successfully.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        print(f"Error initializing database: {e}")

initialize_database()

class User:
    def __init__(self, username, password, balance=0):
        self.username = username
        self.balance = Decimal(balance)
        self.password = password

    def deposit(self, amount):
        try:
            amount = Decimal(amount)
            if amount > 0:
                self.balance += amount
                print(f"Deposited: ₹{amount:.2f}")
                self.log_transaction(f"Deposited ₹{amount:.2f}")

                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                update_query = "UPDATE users SET balance = %s WHERE username = %s"
                cursor.execute(update_query, (self.balance, self.username))
                conn.commit()
                cursor.close()
                conn.close()
            else:
                print("Invalid amount. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

    def withdraw(self, amount):
        try:
            amount = Decimal(amount)
            if amount > 0:
                if amount <= self.balance:
                    self.balance -= amount
                    print(f"Withdrawn: ₹{amount:.2f}")
                    self.log_transaction(f"Withdrawn ₹{amount:.2f}")
                    conn = mysql.connector.connect(**db_config)
                    cursor = conn.cursor()
                    update_query = "UPDATE users SET balance = %s WHERE username = %s"
                    cursor.execute(update_query, (self.balance, self.username))
                    conn.commit()
                    cursor.close()
                    conn.close()
                else:
                    print("Insufficient balance.")
            else:
                print("Invalid amount. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

    def display_balance(self):
        print(f"Account balance for {self.username}: ₹{self.balance:.2f}")

    def log_transaction(self, transaction):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            query = "INSERT INTO transaction_logs (username, transaction_description) VALUES (%s, %s)"
            cursor.execute(query, (self.username, transaction))
            conn.commit()

            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            print(f"Error logging transaction: {e}")

    def view_transactions(self):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            query = "SELECT transaction_description, transaction_date FROM transaction_logs WHERE username = %s"
            cursor.execute(query, (self.username,))
            transactions = cursor.fetchall()

            cursor.close()
            conn.close()

            if transactions:
                print(f"Transaction history for {self.username}:")
                for transaction_description, transaction_date in transactions:
                    print(f"{transaction_date}: {transaction_description}")
            else:
                print("No transactions found.")
        except mysql.connector.Error as e:
            print(f"Error fetching transactions: {e}")

class BankSystem:
    def __init__(self):
        self.users = {}

    def create_user(self, username, password):
        if username in self.users:
            print("Username already exists. Please choose a different username.")
        else:
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()

                query = "INSERT INTO users (username, password, balance) VALUES (%s, %s, %s)"
                cursor.execute(query, (username, password, Decimal('0.00')))
                conn.commit()

                cursor.close()
                conn.close()

                self.users[username] = User(username, password)
                print(f"User {username} created successfully.")
            except mysql.connector.Error as e:
                print(f"Error creating user: {e}")

    def login(self, username, password):
        if username in self.users:
            if self.users[username].password == password:
                print(f"Welcome, {username}!")
                return self.users[username]
            else:
                print("Incorrect password. Please try again.")
                return None
        else:
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()

                query = "SELECT username, balance, password FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                user_record = cursor.fetchone()

                cursor.close()
                conn.close()

                if user_record:
                    stored_username, balance, stored_password = user_record
                    if stored_password == password:
                        self.users[username] = User(username, password, balance)
                        print(f"Welcome, {username}!")
                        return self.users[username]
                    else:
                        print("Incorrect password. Please try again.")
                        return None
                else:
                    print("User not found. Please create an account first.")
                    return None
            except mysql.connector.Error as e:
                print(f"Error logging in: {e}")
                return None

    def main_menu(self):
        while True:
            print("\nBank System Menu:")
            print("1. Create New User")
            print("2. Login")
            print("3. Quit")

            choice = input("Enter your choice: ")

            if choice == '1':
                username = input("Enter a username: ")
                password = input("Enter the password: ")
                self.create_user(username, password)
            elif choice == '2':
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                user = self.login(username, password)
                if user:
                    self.user_menu(user)
            elif choice == '3':
                print("\nThank you for using Kazu Bank.\nGoodbye!\nHave a nice day.")
                break
            else:
                print("Invalid choice. Please try again.")

    def user_menu(self, user):
        while True:
            print("\nBank Menu:")
            print("a. Deposit")
            print("b. Withdraw")
            print("c. View Transactions")
            print("d. Display balance")
            print("e. Logout")

            choice = input("Enter your choice: ")

            if choice == 'a':
                amount = input("Enter amount to deposit: ")
                user.deposit(amount)
            elif choice == 'b':
                amount = input("Enter amount to withdraw: ")
                user.withdraw(amount)
            elif choice == 'c':
                user.view_transactions()
            elif choice == 'd':
                user.display_balance()
            elif choice == 'e':
                print(f"Logging out {user.username}. Thank you and have a nice day!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    bank_system = BankSystem()
    bank_system.main_menu()
