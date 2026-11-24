import os

from dotenv import load_dotenv
from telebot import TeleBot, types

from questions import questions

load_dotenv()

tg_token = os.environ.get("TG_TOKEN")

bot = TeleBot(tg_token)

# Тут храним состояние прохождения квиза каждого пользователя
quiz_state = {}

@bot.message_handler(commands=["quiz"])
def start_quiz(message):
    # при старте квиза ставим значения по умолчанию для пользователя
    quiz_state[message.from_user.id] = {
        "score": 0,
        "quest_idx": 0,
        "answer": None,
    }

    # создаем кнопки, в callback_data записываем quiz:НОМЕРВОПРОСА:ВАРИАНТОТВЕТА
    buttons = [
        types.InlineKeyboardButton(
            option,
            callback_data=f"quiz:0:{option}"
        ) for option in questions[0]["options"]
    ]

    kbd = types.InlineKeyboardMarkup()
    kbd.add(*buttons)

    # отправляем вопрос и кнопки
    bot.send_message(
        message.chat.id,
        questions[0]["text"],
        reply_markup=kbd,
    )

# обрабатываем только те кнопки, у которых в callback_data строка начинается с quiz:
@bot.callback_query_handler(
    func=lambda call: call.data.startswith("quiz:")
)
def answer_question(call):
    # подтверждаем телеграмму, что колбек отрабатываем
    bot.answer_callback_query(call.id)

    # Получаем номер вопроса и ответ от кнопки которую нажал пользователь
    _, quest_idx, answer = call.data.split(":")
    quest_idx = int(quest_idx)

    # если ответ правильный увеличиваем счетчик очков
    if answer in questions[quest_idx]["answers"]:
        quiz_state[call.from_user.id]["score"] += 1

    # увеличиваем счетчик номера вопроса
    quiz_state[call.from_user.id]["quest_idx"] += 1

    # если вопросы кончились(счетчик больше или равен количеству вопросов)
    if quiz_state[call.from_user.id]["quest_idx"] >= len(questions):
        # выводим общее количество баллов
        bot.send_message(
            call.message.chat.id,
            f"Ваши баллы: {quiz_state[call.from_user.id]['score']}"
        )
    # если вопросы еще есть
    else:
        # собираем кнопки для нового вопроса
        buttons = [
            types.InlineKeyboardButton(
                option,
                callback_data=f"quiz:{quiz_state[call.from_user.id]['quest_idx']}:{option}"
            ) for option in questions[quiz_state[call.from_user.id]["quest_idx"]]["options"]
        ]
        
        kbd = types.InlineKeyboardMarkup()
        kbd.add(*buttons)

        # отправляем пользователю новый вопрос с вариантами ответов
        bot.send_message(
            call.message.chat.id,
            questions[quiz_state[call.from_user.id]["quest_idx"]]["text"],
            reply_markup=kbd,
        )

# @bot.message_handler(
#     commands=["menu"]
# )
# def show_menu(message):

#     profile_btn = types.InlineKeyboardButton(
#         "Профиль",
#         callback_data="profile_action"
#     )
#     settings_btn = types.InlineKeyboardButton(
#         "Настройки",
#         callback_data="settings_action"
#     )
    
#     kbd = types.InlineKeyboardMarkup()
#     kbd.add(profile_btn, settings_btn)

#     bot.send_message(
#         message.chat.id,
#         "Вы в меню, выберите действие",
#         reply_markup=kbd,
#     )

# @bot.callback_query_handler(
#     func=lambda c: c.data.endswith("_action")
# )
# def menu_button_handler(call):
#     bot.answer_callback_query(call.id)
#     if call.data == "profile_action":
#         bot.send_message(
#             call.message.chat.id,
#             "Имя: Вадим, баланс - 100р"
#         )
#     elif call.data == "settings_action":
#         bot.send_message(
#             call.message.chat.id,
#             "Уведомления: выключены"
#         )

# @bot.message_handler(
#     commands=["quiz"]
# )
# def start_quiz(message):
#     keyboard = types.ReplyKeyboardMarkup()
#     keyboard.add("Раз", "Два")
#     bot.send_message(
#         message.chat.id,
#         "Выберите вариант",
#         reply_markup=keyboard,               
#     )

# @bot.message_handler(
#     func=lambda m: m.text == "Раз"
# )
# def raz(message):
#     bot.send_message(
#         message.chat.id, 
#         "Вы нажали раз",
#         reply_markup=types.ReplyKeyboardRemove()
#     )

# @bot.message_handler(
#     func=lambda m: m.text == "Два"
# )
# def dva(message):
#     bot.send_message(
#         message.chat.id, 
#         "Вы нажали два",
#         reply_markup=types.ReplyKeyboardRemove()    
#     )

# @bot.message_handler(
#     func=lambda m: True
# )
# def echo(mess):
#     bot.reply_to(mess, mess.text)

# запускаем бесконченый поллинг для связи бота и телеграмма
bot.infinity_polling()
