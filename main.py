import sqlite3

class Insured:
    def __init__(self, first_name, last_name, age, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.phone_number = phone_number

    def __str__(self):
        return f"Jméno: {self.first_name} {self.last_name}, Věk: {self.age}, Telefon: {self.phone_number}"

class InsuranceApp:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS insured
                          (first_name TEXT, last_name TEXT, age INTEGER, phone_number TEXT)''')
        self.conn.commit()

    def add_insured(self, insured):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO insured VALUES (?, ?, ?, ?)",
                       (insured.first_name, insured.last_name, insured.age, insured.phone_number))
        self.conn.commit()

    def display_all_insured(self):
        print("Seznam všech pojištěných:")
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM insured")
        insured_list = cursor.fetchall()
        for insured in insured_list:
            print(Insured(*insured))

    def search_insured(self, first_name, last_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM insured WHERE first_name = ? AND last_name = ?", (first_name, last_name))
        insured_list = cursor.fetchall()
        found_insured = [Insured(*insured) for insured in insured_list]
        return found_insured


def create_insured():
    first_name = input("Zadejte jméno pojištěného: ")
    last_name = input("Zadejte příjmení pojištěného: ")
    age = int(input("Zadejte věk pojištěného: "))
    phone_number = input("Zadejte telefonní číslo pojištěného: ")
    return Insured(first_name, last_name, age, phone_number)


def main():
    app = InsuranceApp("insurance.db")

    while True:
        print("---------------------------\nEvidence pojištěných\n---------------------------")
        print("1 - Přidat pojištěného")
        print("2 - Zobrazit seznam všech pojištěných")
        print("3 - Vyhledat pojištěného")
        print("4 - Konec")

        choice = input("Vyberte akci: \n")

        if choice == "1":
            insured = create_insured()
            app.add_insured(insured)
            print("Pojištěný byl úspěšně přidán.")

        elif choice == "2":
            app.display_all_insured()
            print("")

        elif choice == "3":
            first_name = input("Zadejte jméno pojištěného: ")
            last_name = input("Zadejte příjmení pojištěného: ")
            insured = app.search_insured(first_name, last_name)
            if insured:
                print("Nalezený pojištěný:")
                for person in insured:
                    print(person)
            else:
                print("Pojištěný nebyl nalezen.")

        elif choice == "4":
            app.conn.close()
            break

        else:
            print("Neplatná volba. Zadejte prosím znovu.")


if __name__ == "__main__":
    main()