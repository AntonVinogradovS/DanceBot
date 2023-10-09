from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

firstKeyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="Каталог")).add(KeyboardButton(text="Связаться с нами"))
secondKeyboard = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="Да", callback_data="yes")).add(InlineKeyboardButton(text="Нет", callback_data="no"))
paymentSelectionKeyboard = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="Сейчас онлайн", callback_data="now")).add(InlineKeyboardButton(text="В день проведения", callback_data="after"))
adminKeyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="Ожидающие")).add(KeyboardButton(text="Подтвержденные"))

def f(count, id):
    kb = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="Подтвердить", callback_data=f"good {count}|{id}"))
    return kb