import sqlite3

def main():
    conn = sqlite3.connect('chainsaw_juggling.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            catches INTEGER NOT NULL
        );
    """)

    menu_text = """
    1. Display all records
    2. Search by name
    3. Add new record
    4. Edit existing record
    5. Delete record
    6. Quit
    """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_records(c)
        elif choice == '2':
            search_by_name(c)
        elif choice == '3':
            add_new_record(c, conn)
        elif choice == '4':
            edit_existing_record(c, conn)
        elif choice == '5':
            delete_record(c, conn)
        elif choice == '6':
            break
        else:
            print('Not a valid selection, please try again')

    conn.close()


def display_all_records(cursor):
    cursor.execute("SELECT * FROM records")
    records = cursor.fetchall()
    for record in records:
        print(record)


def search_by_name(cursor):
    name = input("Enter the name to search: ")
    cursor.execute("SELECT * FROM records WHERE name=?", (name,))
    record = cursor.fetchone()
    if record:
        print(record)
    else:
        print("No record found with the name:", name)


def add_new_record(cursor, connection):
    name = input("Enter the name: ")
    country = input("Enter the country: ")
    catches = int(input("Enter the number of catches: "))
    try:
        cursor.execute("""
            INSERT INTO records (name, country, catches)
            VALUES (?, ?, ?)
        """, (name, country, catches))
        connection.commit()
        print("Record added successfully.")
    except sqlite3.IntegrityError:
        print("Record already exists with the name:", name)


def edit_existing_record(cursor, connection):
    name = input("Enter the name of the record to edit: ")
    cursor.execute("SELECT * FROM records WHERE name=?", (name,))
    record = cursor.fetchone()
    if record:
        catches = int(input("Enter the new number of catches: "))
        cursor.execute("""
            UPDATE records
            SET catches=?
            WHERE name=?
        """, (catches, name))
        connection.commit()
        print("Record updated successfully.")
    else:
        print("No record found with the name:", name)


def delete_record(cursor, connection):
    name = input("Enter the name of the record to delete: ")
    connection = sqlite3.connect('chainsaw_juggling.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM records WHERE name=?", (name,))
   

if __name__ == '__main__':
    main()