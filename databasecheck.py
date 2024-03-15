import mysql.connector

# Connect to MySQL database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Subhasri',
    database='cheque'
)

# Initialize cursor
cursor = connection.cursor()

# Define a function to check if the account number and cheque number exist in the database
def check_cheque(account_number, cheque_number):

    # Define SQL queries to check if the account number and cheque number exist in the database
    cheque_query = "SELECT * FROM cheque WHERE account_number = %s AND cheque_number = %s"
    cursor.execute(cheque_query, (account_number, cheque_number))
    cheque_result = cursor.fetchone()  # Fetch one row from the result

    if cheque_result:
        stopcheques_query = "SELECT * FROM stopcheques WHERE account_number = %s AND cheque_number = %s"
        cursor.execute(stopcheques_query, (account_number, cheque_number))
        stopcheques_result = cursor.fetchone()  # Fetch one row from the result
        if not stopcheques_result:
            print("Cheque Accepted")
        else:
            print("Cheque Rejected")
            #break
    

    else:
        print("Cheque Rejected")

# Assuming you have extracted the account number and cheque number
account_number = "11010049001545"
cheque_number = "172471"

# Check if the account number and cheque number exist in the database
check_cheque(account_number, cheque_number)

# Close the cursor and connection
cursor.close()
connection.close()
