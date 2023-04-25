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
    if message.from_user.username not in db.all_admins():
        bot.send_message(message.from_user.id, "Вас не має в адміністраторах")
    else:
        bot.send_message(
            message.from_user.id, "Вас вітає бот!", reply_markup=main_menu()
        )


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Загальна кількість клієнтів")
    btn2 = types.KeyboardButton("Додати нового клієнта")
    btn3 = types.KeyboardButton("Вся інформація про клієнта")
    btn4 = types.KeyboardButton("Опрацювати старого клієнта")
    btn5 = types.KeyboardButton("Адмін")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup


def validation_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ValueError:
            bot.send_message(
                args[0].from_user.id, "Введіть номер телефону у числовому форматі"
            )
        except IndexError:
            bot.send_message(
                args[0].from_user.id, "Ви ввели недостатньо або забагато інформації"
            )
        except SyntaxError:
            bot.send_message(args[0].from_user.id, "Введіть бонуси у числовому форматі")
        except TypeError:
            bot.send_message(args[0].from_user.id, "Введіть ім'я або прізвище літерами")
        except KeyError:
            bot.send_message(args[0].from_user.id, "Введіть номер телефону коректно")

    return inner_function


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    match message.text:
        case "Загальна кількість клієнтів":
            bot.send_message(
                message.from_user.id,
                db.total_amount_of_clients(),
                reply_markup=main_menu(),
            )
        case "Вся інформація про клієнта":
            mesg = bot.send_message(
                message.chat.id,
                "Введіть номер телефону у такому форматі:\n" "380XXXXXXXXX",
            )
            bot.register_next_step_handler(mesg, parse_phonenumber)
        case "Додати нового клієнта":
            mesg = bot.send_message(
                message.chat.id,
                "Введіть дані клієнта у такому форматі:\n"
                "380XXXXXXXXX Ім'я Прізвище К-сть бонусів",
            )
            bot.register_next_step_handler(mesg, parse_add_new_client)
        case "Адмін":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Додати адміна")
            btn2 = types.KeyboardButton("Видалити адміна")
            btn3 = types.KeyboardButton("Список тегів всіх адмінів")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, "Оберіть дію", reply_markup=markup)
        case "Додати адміна":
            mesg = bot.send_message(
                message.chat.id,
                "Введіть тег адміну без @",
            )
            bot.register_next_step_handler(mesg, parse_add_new_admin)
        case "Видалити адміна":
            mesg = bot.send_message(
                message.chat.id,
                "Введіть тег адміну без @",
            )
            bot.register_next_step_handler(mesg, parse_del_admin)
        case "Список тегів всіх адмінів":
            mesg = ", ".join(db.all_admins())
            bot.send_message(
                message.from_user.id,
                mesg,
                reply_markup=main_menu(),
            )
        case "Опрацювати старого клієнта":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Додати бонуси")
            btn2 = types.KeyboardButton("Списати бонуси")
            btn3 = types.KeyboardButton("Анулювати бонуси")
            btn4 = types.KeyboardButton("Видалити клієнта")
            btn5 = types.KeyboardButton("Редагувати ім'я")
            btn6 = types.KeyboardButton("Редагувати прізвище")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
            bot.send_message(message.from_user.id, "Оберіть дію", reply_markup=markup)
        case "Додати бонуси":
            mesg = bot.send_message(
                message.chat.id,
                "Введіть дані у такому форматі:\n" "380XXXXXXXXX К-сть бонусів",
            )
            bot.register_next_step_handler(mesg, parse_add_bonus)
        case "Списати бонуси":
            mesg = bot.send_message(
                message.chat.id,
                "Введіть дані у такому форматі:\n" "380XXXXXXXXX К-сть бонусів",
            )
            bot.register_next_step_handler(mesg, parse_minus_bonus)
        case "Анулювати бонуси":
            mesg = bot.send_message(
                message.chat.id,
                "Введіть номер клієнта у такому форматі:\n" "380XXXXXXXXX",
            )
            bot.register_next_step_handler(mesg, parse_phone_minus_all)
        case "Видалити клієнта":
            mesg = bot.send_message(
                message.chat.id,
                "Введіть номер клієнта у такому форматі:\n" "380XXXXXXXXX",
            )
            bot.register_next_step_handler(mesg, parse_phone_for_del_client)
        case "Редагувати ім'я":
            mesg = bot.send_message(
                message.chat.id,
                "Введіть дані у такому форматі:\n" "380XXXXXXXXX Нове ім'я",
            )
            bot.register_next_step_handler(mesg, parse_phone_for_new_name)
        case "Редагувати прізвище":
            mesg = bot.send_message(
                message.chat.id,
                "Введіть дані у такому форматі:\n" "380XXXXXXXXX Нове прізвище",
            )
            bot.register_next_step_handler(mesg, parse_phone_for_new_surname)
        case _:
            bot.send_message(
                message.chat.id, "Потрібно щось обрати", reply_markup=main_menu()
            )


@validation_handler
def parse_phonenumber(message: types.Message):
    mes = validate_input(message.text, 1)
    bot.send_message(message.chat.id, db.get_client_info(mes[0]))


@validation_handler
def parse_add_new_admin(message: types.Message):
    bot.send_message(message.chat.id, db.add_new_admin(message.text))


@validation_handler
def parse_add_new_client(message: types.Message):
    mes = validate_input(message.text, 4)
    bot.send_message(message.chat.id, db.add_new_client(mes[0], mes[1], mes[2], mes[3]))


@validation_handler
def parse_add_bonus(message: types.Message):
    mes = validate_input(message.text, 2)
    bot.send_message(
        message.chat.id,
        db.plus_bonus_to_exist_client(mes[0], mes[1]),
        reply_markup=main_menu(),
    )


@validation_handler
def parse_minus_bonus(message: types.Message):
    mes = validate_input(message.text, 2)
    bot.send_message(
        message.chat.id,
        db.minus_bonus_from_exist_client(mes[0], mes[1]),
        reply_markup=main_menu(),
    )


@validation_handler
def parse_phone_minus_all(message: types.Message):
    mes = validate_input(message.text, 1)
    bot.send_message(
        message.chat.id,
        db.minus_all_bonus_from_exist_client(mes[0]),
        reply_markup=main_menu(),
    )


@validation_handler
def parse_del_admin(message: types.Message):
    bot.send_message(
        message.chat.id, db.delete_exist_admin(message.text), reply_markup=main_menu()
    )


@validation_handler
def parse_phone_for_del_client(message: types.Message):
    mes = validate_input(message.text, 1)
    bot.send_message(
        message.chat.id, db.delete_exist_client(mes[0]), reply_markup=main_menu()
    )


@validation_handler
def parse_phone_for_new_name(message: types.Message):
    mes = validate_input(message.text, 2)
    bot.send_message(
        message.chat.id,
        db.edit_client_name(mes[0], mes[1]),
        reply_markup=main_menu(),
    )


@validation_handler
def parse_phone_for_new_surname(message: types.Message):
    mes = validate_input(message.text, 2)
    bot.send_message(
        message.chat.id,
        db.edit_client_surname(mes[0], mes[1]),
        reply_markup=main_menu(),
    )


def validate_input(message, items_num: int) -> list:
    if "." in message:
        mes = message.split(".")
    elif "," in message:
        mes = message.split(",")
    else:
        mes = message.split(" ")
    if len(mes) != items_num:
        raise IndexError("Ви ввели недостатньо або забагато інформації")
    if not mes[0].isdigit():
        raise ValueError("Введіть номер телефону у числовому форматі")
    if len(mes[0]) != 12:
        raise KeyError("Введіть номер телефону коректно")
    if len(mes) == 4:
        if not mes[3].isdigit():
            raise SyntaxError("Введіть бонуси у числовому форматі")
        elif not mes[1].isalpha() or not mes[2].isalpha():
            raise TypeError("Введіть ім'я або прізвище у літерами")
    return mes


bot.polling(none_stop=True, interval=0)
