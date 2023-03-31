import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class BotDB:
    def __init__(self):
        """initialization of connection with db"""
        self.connection = psycopg2.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        self.create_table()

    def create_table(self):
        """create table"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS train_table (
                id serial PRIMARY KEY,
                phonenumber TEXT,
                name TEXT,
                surname TEXT,
                bonus INTEGER);"""
            )
        return "Таблиця готова до роботи"

    def if_client_exists(self, phonenumber1):
        """check if the client already in db"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT phonenumber FROM train_table WHERE phonenumber = %s;""",
                (phonenumber1,),
            )
            result = cursor.fetchall()
        return bool(len(result))

    def add_new_client(
        self, phonenumber1, name1, surname1, bonus1
    ):  # добавить пользователя в бд
        """add new client into db"""
        phonenumber1 = self.validate_phonenumber(phonenumber1)
        if phonenumber1 == "Error":
            return "Введіть номер телефону коректно"
        elif not bonus1.isdigit():
            return "Введіть кількість бонусів коректно"
        elif self.if_client_exists(phonenumber1):
            return "Такий клієнт вже існує"
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO train_table (phonenumber, name, surname, bonus) VALUES (%s, %s, %s, %s)""",
                    (
                        phonenumber1,
                        name1.capitalize(),
                        surname1.capitalize(),
                        int(bonus1),
                    ),
                )
                self.connection.commit()
            return "Інформацію додано"

    def minus_all_bonus_from_exist_client(self, phonenumber1):
        """minus bonuses by phonenumber"""
        phonenumber1 = self.validate_phonenumber(phonenumber1)
        if phonenumber1 == "Error":
            return "Введіть номер телефону коректно"
        if not self.if_client_exists(phonenumber1):
            return "Такого клієнту не існує"
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE train_table SET bonus = 0 WHERE phonenumber = %s;""",
                    (phonenumber1,),
                )
                self.connection.commit()
            return "Бонуси анульовані"

    def delete_exist_client(self, phonenumber1):
        """delete client from db"""
        phonenumber1 = self.validate_phonenumber(phonenumber1)
        if phonenumber1 == "Error":
            return "Введіть номер телефону коректно"
        if not self.if_client_exists(phonenumber1):
            return "Такого клієнту не існує"
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """DELETE FROM train_table WHERE phonenumber = %s;""",
                    (phonenumber1,),
                )
                self.connection.commit()
            return "Клієнт видален з бази"

    def plus_bonus_to_exist_client(self, phonenumber1, bonus1):
        """add bonus to client"""
        phonenumber1 = self.validate_phonenumber(phonenumber1)
        if phonenumber1 == "Error":
            return "Введіть номер телефону коректно"
        elif not bonus1.isdigit():
            return "Введіть кількість бонусів коректно"
        if not self.if_client_exists(phonenumber1):
            return "Такого клієнту не існує"
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE train_table SET bonus = bonus + %s WHERE phonenumber = %s;""",
                    (
                        int(bonus1),
                        phonenumber1,
                    ),
                )
                self.connection.commit()
            return "Бонуси успішно додані"

    def minus_bonus_from_exist_client(self, phonenumber1, bonus1):
        """minus bonuses"""
        phonenumber1 = self.validate_phonenumber(phonenumber1)
        if phonenumber1 == "Error":
            return "Введіть номер телефону коректно"
        elif not bonus1.isdigit():
            return "Введіть кількість бонусів коректно"
        if not self.if_client_exists(phonenumber1):
            return "Такого клієнту не існує"
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE train_table SET bonus = bonus - %s WHERE phonenumber = %s;""",
                    (
                        int(bonus1),
                        phonenumber1,
                    ),
                )
                self.connection.commit()
            return "Бонуси успішно списані"

    def edit_client_name(self, phonenumber1, new_name):
        """edit clients' name"""
        phonenumber1 = self.validate_phonenumber(phonenumber1)
        if phonenumber1 == "Error":
            return "Ведіть номер телефону коректно"
        elif not new_name.isalpha():
            return "Введіть нове ім'я коректно"
        elif not self.if_client_exists(phonenumber1):
            return "Такого клієнту не існує"
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE train_table SET name = %s WHERE phonenumber = %s;""",
                    (
                        new_name.capitalize(),
                        phonenumber1,
                    ),
                )
                self.connection.commit()
            return "Ім'я клієнту успішно змінено"

    def edit_client_surname(self, phonenumber1, new_surname):
        """edit clients' surname"""
        phonenumber1 = self.validate_phonenumber(phonenumber1)
        if phonenumber1 == "Error":
            return "Введіть номер телефону коректно"
        elif not new_surname.isalpha():
            return "Введіть нове прізвище коректно"
        elif not self.if_client_exists(phonenumber1):
            return "Такого клієнту не існує"
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE train_table SET surname = %s WHERE phonenumber = %s;""",
                    (
                        new_surname.capitalize(),
                        phonenumber1,
                    ),
                )
                self.connection.commit()
            return "Прізвище клієнту успішно змінено"

    def total_amount_of_clients(self):
        """return anount of clients in db"""
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT COUNT(id) as max_value FROM train_table;""")
            result = cursor.fetchall()
        return f"Загальна кількість клієнтів в базі: {result[0][0]}"

    def get_client_info(self, phonenumber1):
        """return clients' info"""
        phonenumber1 = self.validate_phonenumber(phonenumber1)
        if phonenumber1 == "Error":
            return "Введіть номер телефону коректно"
        elif not self.if_client_exists(phonenumber1):
            return "Такого клієнту не існує"
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """SELECT * FROM train_table WHERE phonenumber = %s;""",
                    (phonenumber1,),
                )
                result = cursor.fetchall()
            return (
                f"Прізвище та ім'я: {result[0][3]} {result[0][2]}\n"
                f"Номер телефону: {result[0][1]}\n"
                f"Кількість бонусів: {result[0][4]}"
            )

    def validate_phonenumber(self, phonenumber1):
        if phonenumber1.isdigit():
            if phonenumber1.startswith("0") and len(phonenumber1) == 10:
                phonenumber1 = "38" + phonenumber1
                return phonenumber1
            elif phonenumber1.startswith("38") and len(phonenumber1) == 12:
                return phonenumber1
            else:
                return "Error"
        else:
            return "Error"


