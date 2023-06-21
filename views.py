from dotenv import load_dotenv
from datetime import datetime
from db import mysql

load_dotenv()


#create new user.
def register_user_to_db(
    first_name: str,
    last_name: str,
    username: str,
    birth_date: datetime,
    address: str,
    email_address: str,
    password: str,
):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """INSERT INTO customers(first_name, last_name, username, birth_date, address, email_address, password)
VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        (
            first_name,
            last_name,
            username,
            birth_date,
            address,
            email_address,
            password,
        ),
    )
    mysql.connection.commit()
    cursor.close()

#crete new ticket.
def create_ticket_to_db(
    username: str,
    ticket_title: str,
    ticket_type: str,
    status_name: str,
    description: str,
):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """INSERT INTO tickets(username, ticket_title, ticket_type, status_name, description)
VALUES (%s,%s,%s,%s,%s)""",
        (username, ticket_title, ticket_type, status_name, description),
    )
    mysql.connection.commit()
    cursor.close()

#update current ticket.
def update_ticket_to_db(
    ticket_number: int,
    ticket_title: str,
    ticket_type: str,
    status_name: str,
    description: str,
):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """UPDATE tickets
SET ticket_title = %s,
    ticket_type = %s,
    status_name = %s,
    description = %s
WHERE ticket_number = %s""",
        (ticket_title, ticket_type, status_name, description, ticket_number),
    )
    mysql.connection.commit()
    cursor.close()

#delete a ticket.
def delete_ticket_from_db(ticket_number: int):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """DELETE
FROM tickets
WHERE ticket_number = %s""",
        (ticket_number,),
    )
    mysql.connection.commit()
    cursor.close()

#view all ticket if user is root o.w show only for particular user.
def view_tickets_from_db(username: str):
    cursor = mysql.connection.cursor()
    if username == "root":
        cursor.execute(
            """SELECT *
FROM tickets"""
        )
    else:
        cursor.execute(
            """SELECT *
FROM tickets
WHERE username = %s""",
            (username,),
        )
    data = cursor.fetchall()
    results = []
    for row in data:
        result = {
            "id": row[0],
            "name": row[1],
            "issue": row[2],
            "priority": row[3],
            "status": row[4],
            "description": row[5],
        }
        results.append(result)

    cursor.close()
    # print("view_ticket_from_db",results)
    return results

#show ticket by ticket number.
def view_ticket_by_id_from_db(ticket_number: int):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT *
FROM tickets
WHERE ticket_number = %s""",
        (ticket_number,),
    )
    data = cursor.fetchone()
    # print("view_ticket_by_id_from_db",data)
    result = {
        "id": data[0],
        "name": data[1],
        "issue": data[2],
        "priority": data[3],
        "status": data[4],
        "description": data[5],
    }
    cursor.close()
    return result

# fetch data for a particular user. 
def view_user_from_db(username: str):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT *
FROM customers
WHERE username = %s""",
        (username,),
    )

    result = cursor.fetchone()
    cursor.close()
    result = {
        "firstName": result[1],
        "lastName": result[2],
        "userName": result[3],
        "dob": result[4],
        "address": result[5],
        "email": result[6],
        "password": result[7],
    }
    return result

# edit record for a existing user.
def edit_user_from_db(
    first_name: str,
    last_name: str,
    username: str,
    birth_date: datetime,
    address: str,
    email_address: str,
    password: str,
):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """UPDATE customers
SET first_name = %s,
    last_name = %s,
    birth_date = %s,
    address= %s,
    email_address = %s,
    password=%s
WHERE username = %s""",
        (first_name, last_name, birth_date, address, email_address, password, username),
    )
    mysql.connection.commit()
    cursor.close()

# check if user exists in database.
def check_user(username: str, password: str):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT username,
       password
FROM customers
WHERE username=%s
  AND password=%s""",
        (username, password),
    )

    result = cursor.fetchone()
    if result:
        return True
    else:
        return False
