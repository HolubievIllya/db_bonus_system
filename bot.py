import telebot
from telebot import types
from db_funcs import BotDB
import os
from dotenv import load_dotenv

load_dotenv()


bot = telebot.TeleBot(os.getenv("TG_TOKEN"))
db = BotDB()


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.from_user.id, "Вас вітає бот!", reply_markup=main_menu())


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Загальна кількість клієнтів")
    btn2 = types.KeyboardButton("Додати нового клієнта")
    btn3 = types.KeyboardButton("Вся інформація про клієнта")
    btn4 = types.KeyboardButton("Опрацювати старого клієнта")
    markup.add(btn1, btn2, btn3, btn4)
    return markup


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text == "Загальна кількість клієнтів":
        res = db.total_amount_of_clients()
        bot.send_message(message.from_user.id, res, reply_markup=main_menu())
    elif message.text == "Вся інформація про клієнта":
        mesg = bot.send_message(
            message.chat.id, "Введіть номер телефону у такому форматі:\n" "380XXXXXXXXX"
        )
        bot.register_next_step_handler(mesg, parse_phonenumber)
    elif message.text == "Додати нового клієнта":
        mesg = bot.send_message(
            message.chat.id,
            "Введіть дані клієнта у такому форматі:\n"
            "380XXXXXXXXX Ім'я Прізвище К-сть бонусів",
        )
        bot.register_next_step_handler(mesg, parse_add_new_client)
    elif message.text == "Опрацювати старого клієнта":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Додати бонуси")
        btn2 = types.KeyboardButton("Списати бонуси")
        btn3 = types.KeyboardButton("Анулювати бонуси")
        btn4 = types.KeyboardButton("Видалити клієнта")
        btn5 = types.KeyboardButton("Редагувати ім'я")
        btn6 = types.KeyboardButton("Редагувати прізвище")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.from_user.id, "Оберіть дію", reply_markup=markup)
    elif message.text == "Додати бонуси":
        mesg = bot.send_message(
            message.chat.id,
            "Введіть дані у такому форматі:\n" "380XXXXXXXXX К-сть бонусів",
        )
        bot.register_next_step_handler(mesg, parse_add_bonus)
    elif message.text == "Списати бонуси":
        mesg = bot.send_message(
            message.chat.id,
            "Введіть дані у такому форматі:\n" "380XXXXXXXXX К-сть бонусів",
        )
        bot.register_next_step_handler(mesg, parse_minus_bonus)
    elif message.text == "Анулювати бонуси":
        mesg = bot.send_message(
            message.chat.id, "Введіть номер клієнта у такому форматі:\n" "380XXXXXXXXX"
        )
        bot.register_next_step_handler(mesg, parse_phone_minus_all)
    elif message.text == "Видалити клієнта":
        mesg = bot.send_message(
            message.chat.id, "Введіть номер клієнта у такому форматі:\n" "380XXXXXXXXX"
        )
        bot.register_next_step_handler(mesg, parse_phone_for_del_client)
    elif message.text == "Редагувати ім'я":
        mesg = bot.send_message(
            message.chat.id, "Введіть дані у такому форматі:\n" "380XXXXXXXXX Нове ім'я"
        )
        bot.register_next_step_handler(mesg, parse_phone_for_new_name)
    elif message.text == "Редагувати прізвище":
        mesg = bot.send_message(
            message.chat.id,
            "Введіть дані у такому форматі:\n" "380XXXXXXXXX Нове прізвище",
        )
        bot.register_next_step_handler(mesg, parse_phone_for_new_surname)
    else:
        bot.send_message(
            message.chat.id, "Потрібно щось обрати", reply_markup=main_menu()
        )


def parse_phonenumber(message: types.Message):
    bot.send_message(message.chat.id, db.get_client_info(message.text))


def parse_add_new_client(message: types.Message):
    mes = validate_input(message.text)
    if len(mes) != 4:
        bot.send_message(message.chat.id, "Введіть інформацію коректно")
    else:
        bot.send_message(
            message.chat.id, db.add_new_client(mes[0], mes[1], mes[2], mes[3])
        )


def parse_add_bonus(message: types.Message):
    mes = validate_input(message.text)
    if len(mes) != 2:
        bot.send_message(message.chat.id, "Введіть інформацію коректно")
    else:
        bot.send_message(
            message.chat.id,
            db.plus_bonus_to_exist_client(mes[0], mes[1]),
            reply_markup=main_menu(),
        )


def parse_minus_bonus(message: types.Message):
    mes = validate_input(message.text)
    if len(mes) != 2:
        bot.send_message(message.chat.id, "Введіть інформацію коректно")
    else:
        bot.send_message(
            message.chat.id,
            db.minus_bonus_from_exist_client(mes[0], mes[1]),
            reply_markup=main_menu(),
        )


def parse_phone_minus_all(message: types.Message):
    bot.send_message(
        message.chat.id,
        db.minus_all_bonus_from_exist_client(message.text),
        reply_markup=main_menu(),
    )


def parse_phone_for_del_client(message: types.Message):
    bot.send_message(
        message.chat.id, db.delete_exist_client(message.text), reply_markup=main_menu()
    )


def parse_phone_for_new_name(message: types.Message):
    mes = validate_input(message.text)
    if len(mes) != 2:
        bot.send_message(message.chat.id, "Введіть інформацію коректно")
    else:
        bot.send_message(
            message.chat.id,
            db.edit_client_name(mes[0], mes[1]),
            reply_markup=main_menu(),
        )


def parse_phone_for_new_surname(message: types.Message):
    mes = validate_input(message.text)
    if len(mes) != 2:
        bot.send_message(message.chat.id, "Введіть інформацію коректно")
    else:
        bot.send_message(
            message.chat.id,
            db.edit_client_surname(mes[0], mes[1]),
            reply_markup=main_menu(),
        )


def validate_input(message):
    if "." in message:
        mes = message.split(".")
    elif "," in message:
        mes = message.split(",")
    else:
        mes = message.split(" ")
    return mes


bot.polling(none_stop=True, interval=0)
