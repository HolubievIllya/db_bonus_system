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

    def if_client_exists(self, phonenumber: str) -> bool:
        """check if the client already in db"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT phonenumber FROM train_table WHERE phonenumber = %s;""",
                (phonenumber,),
            )
            result = cursor.fetchall()
        return bool(len(result))

    def add_new_client(
        self, phonenumber: str, name: str, surname: str, bonus: str
    ) -> str:
        """add new client into db"""
        if self.if_client_exists(phonenumber):
            return "Такий клієнт вже існує"
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO train_table (phonenumber, name, surname, bonus) VALUES (%s, %s, %s, %s)""",
                    (
                        phonenumber,
                        name.capitalize(),
                        surname.capitalize(),
                        int(bonus),
                    ),
                )
                self.connection.commit()
            return "Інформацію додано"

    def minus_all_bonus_from_exist_client(self, phonenumber: str) -> str:
        """minus bonuses by phonenumber"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                """UPDATE train_table SET bonus = 0 WHERE phonenumber = %s;""",
                (phonenumber,),
            )
            self.connection.commit()
            if bool(cursor.rowcount):
                return "Бонуси анульовані"
        return "Такого клієнту не існує"

    def delete_exist_client(self, phonenumber: str) -> str:
        """delete client from db"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                """DELETE FROM train_table WHERE phonenumber = %s;""",
                (phonenumber,),
            )
            self.connection.commit()
            if bool(cursor.rowcount):
                return "Клієнт видален з бази"
        return "Такого клієнту не існує"

    def plus_bonus_to_exist_client(self, phonenumber: str, bonus: str) -> str:
        """add bonus to client"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                """UPDATE train_table SET bonus = bonus + %s WHERE phonenumber = %s;""",
                (
                    int(bonus),
                    phonenumber,
                ),
            )
            self.connection.commit()
            if bool(cursor.rowcount):
                return "Бонуси додані"
        return "Такого клієнту не існує"

    def minus_bonus_from_exist_client(self, phonenumber: str, bonus: str) -> str:
        """minus bonuses"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                """UPDATE train_table SET bonus = bonus - %s WHERE phonenumber = %s;""",
                (
                    int(bonus),
                    phonenumber,
                ),
            )
            self.connection.commit()
            if bool(cursor.rowcount):
                return "Бонуси списані"
        return "Такого клієнту не існує"

    def edit_client_name(self, phonenumber: str, new_name: str) -> str:
        """edit clients' name"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                """UPDATE train_table SET name = %s WHERE phonenumber = %s;""",
                (
                    new_name.capitalize(),
                    phonenumber,
                ),
            )
            self.connection.commit()
            if bool(cursor.rowcount):
                return "Ім'я клієнту успішно змінено"
        return "Такого клієнту не існує"

    def edit_client_surname(self, phonenumber: str, new_surname: str) -> str:
        """edit clients' surname"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                """UPDATE train_table SET surname = %s WHERE phonenumber = %s;""",
                (
                    new_surname.capitalize(),
                    phonenumber,
                ),
            )
            self.connection.commit()
            if bool(cursor.rowcount):
                return "Прізвище клієнту успішно змінено"
        return "Такого клієнту не існує"

    def total_amount_of_clients(self) -> str:
        """return anount of clients in db"""
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT COUNT(id) as max_value FROM train_table;""")
            result = cursor.fetchall()
        return f"Загальна кількість клієнтів в базі: {result[0][0]}"

    def get_client_info(self, phonenumber: str) -> str:
        """return clients' info"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM train_table WHERE phonenumber = %s;""",
                (phonenumber,),
            )
            result = cursor.fetchall()
        return (
            f"Прізвище та ім'я: {result[0][3]} {result[0][2]}\n"
            f"Номер телефону: {result[0][1]}\n"
            f"Кількість бонусів: {result[0][4]}"
        )
