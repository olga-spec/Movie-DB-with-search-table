import mysql.connector

def connection_db(dbconfig):
    try:
        connection = mysql.connector.connect(**dbconfig)
        if connection.is_connected():
            cursor = connection.cursor()
            print( "Connection established")
            return connection, cursor        
    except Exception as a:
        return f"Error: {str(a)}"



def create_db(dbconfig):
    connection, cursor = connection_db(dbconfig)
    try:
        cursor.execute("drop database if exists final_project_Olga")
        print("Database dropped successfully")
        cursor.execute("create database final_project_Olga")
        print("Database created successfully")
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as a:
        return f"Error: {str(a)}"



def create_table(dbconfig):
    connection, cursor = connection_db(dbconfig)
    try:
        cursor.execute('''create table searched_info (
                        id int primary key auto_increment,
                        searched_key_word varchar(1000),
                        count int)''')
        connection.commit()
        cursor.close()
        connection.close()
        print("Table created successfully")
    except Exception as a:
        return f"Error: {str(a)}"



def drop_table(connection, cursor):
    cursor.execute('drop table searched_info')
    connection.commit()
    print("Table has been droped successfully")



def disconnect_connection(connection, cursor):
    cursor.close()
    connection.close()
    print('Disconnection complete')
