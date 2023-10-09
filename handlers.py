from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery, MediaGroup, InputMediaDocument
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from texts import *
from keyboards import * 
from database import *
import re
import asyncio
import datetime

async def cmdStart(message: types.Message):
    #print(message.from_user.id)
    await sql_add_scheduled_mailing(message.from_user.id)
    await bot.send_chat_action(chat_id=message.from_user.id, action=types.ChatActions.UPLOAD_VIDEO)
    with open("video0.mp4", "rb") as video_file:
        await bot.send_video_note(message.from_user.id, video_file)
    await message.answer(text=welcomeMessage)
    await message.answer(text="Планируешь посетить мастер-классы?", reply_markup=secondKeyboard)


async def yesAnswer(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id, text="Отлично, лови от нас полезное видео от солисток театра Аллы Духовой «Тодес» Юлии Филипповой-Бугаковой и Анны Ливинцевой.")
    await bot.send_chat_action(chat_id=callback_query.from_user.id, action=types.ChatActions.UPLOAD_VIDEO)
    with open("video1.mp4", "rb") as video_file:
        await bot.send_video_note(callback_query.from_user.id, video_file)
    await bot.send_message(chat_id=callback_query.from_user.id, text="Вам удобно оплатить мастер-классы сейчас онлайн или в день проведения?", reply_markup=paymentSelectionKeyboard)

async def noAnswer(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id, text="Очень жаль, надеемся с вами увидеться в следующий раз. А пока посмотрите полезное видео от солисток театра Аллы Духовой «Тодес» Юлии Филипповой-Бугаковой и Анны Ливинцевой.")
    await bot.send_chat_action(chat_id=callback_query.from_user.id, action=types.ChatActions.UPLOAD_VIDEO)
    with open("video1.mp4", "rb") as video_file:
        await bot.send_video_note(callback_query.from_user.id, video_file)
    
class FSMAdd(StatesGroup):
    a0 = State()
    a1 = State()
    a2 = State()
    a3 = State()
    a4 = State()
    a5 = State()

async def startSurvey(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id, text = "Перед оплатой, вам необходимо указать свои данные для допуска на мероприятие.")
    await bot.send_message(chat_id=callback_query.from_user.id, text = "Укажите ФИО")
    await FSMAdd.a0.set()

async def cmdStop(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Регистрация прервана")

async def fio(message: types.Message, state: FSMContext):
    tmp = message.text
    async with state.proxy() as data:
        data['a0'] = tmp
    await FSMAdd.next()
    await bot.send_message(chat_id=message.from_user.id, text="Укажите возраст (полных лет)")
    

async def age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['a1'] = message.text
    await FSMAdd.next()
    await message.answer("Укажите студию")

async def studio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['a2'] = message.text
    await FSMAdd.next()
    await message.answer("Пожалуйста, введите ваш номер телефона в формате +7********** (например, +79123456789)")

phone_pattern = r'^\+7\d{10}$'

def is_valid_phone(phone):
    return re.match(phone_pattern, phone) is not None
async def numberPhone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        phone = message.text
        if is_valid_phone(phone):
            data['a3'] = phone
            await FSMAdd.next()
            await message.answer("Укажите ваш e-mail")
        else:
            await message.answer("Неправильный формат номера телефона. Пожалуйста, введите корректный номер в формате +7********** (например, +79123456789)")

email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

def is_valid_email(email):
    return re.match(email_pattern, email) is not None
async def eMail(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        email = message.text
        if is_valid_email(email):
            data['a4'] = email
            await FSMAdd.next()
            await message.answer("Отлично! Оплата производится по QR коду. После оплаты, для подтверждения регистрации <b>пришлите скриншот</b>.", parse_mode=types.ParseMode.HTML)
            with open("qr2.jpg", "rb") as qr_file:
                await bot.send_photo(message.from_user.id, qr_file, caption="Оплата одного мастер-класса")
            with open("qr1.jpg", "rb") as qr_file:
                await bot.send_photo(message.from_user.id, qr_file, caption= "Оплата всех мастер-классов")
        else:
            await message.answer("Неправильный формат email. Пожалуйста, введите корректный email.")



async def endPay(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['a5'] = message.photo[0].file_id
    await state.finish()
    await sql_write(list(data.values()), message.from_user.id)
    await message.answer("Ожидайте подтверждения оплаты администратором.")
    # await bot.send_message(chat_id=callback_query.from_user.id, text="Оплата производится по QR коду. После оплаты, для подтверждения регистрации пришлите скриншот")
    # with open("qr.png", "rb") as qr_file:
    #     await bot.send_photo(callback_query.from_user.id, qr_file)
    
async def afterPay(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id, text="Ждем вас в 11:00 по адресу п. Отрадное, ул. Пятницкая, 15. Центральная, танцевальная база Аллы Духовой «Тодес»")

ADMIN = [169163017, 1205977075, 853888293, 781374930, 1102558258, 1462359946, 280433503, 1313463136, 760026269, 158124398, 271757608]

async def admin(message: types.Message):
    if message.from_user.id in ADMIN:
        await message.answer("Вы администратор этого бота", reply_markup=adminKeyboard)

async def wait(message: types.Message):
    res = await sql_read()
    for i in res:
        tmpText = f"{i[2]}\n{i[3]}\n{i[4]}\n{i[5]}\n{i[6]}"
        await bot.send_photo(chat_id=message.from_user.id, photo = i[1], caption = tmpText, reply_markup=f(i[0],i[-1]))
async def payOK(callback_query: types.CallbackQuery):
    arr = callback_query.data.replace('good ', '').split("|")
    await sql_write_2(arr[0])
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.send_message(chat_id=arr[-1], text="Благодарим вас за оплату. Ждем с нетерпением с вами встречу на мастер-классах.")
    await bot.send_chat_action(chat_id=callback_query.from_user.id, action=types.ChatActions.UPLOAD_VIDEO)
    with open("video2.mp4", "rb") as video_file:
        await bot.send_video_note(callback_query.from_user.id, video_file)
async def sweets(message: types.Message):
    res = await sql_read_2()
    for i in res:
        tmpText = f"{i[2]}\n{i[3]}\n{i[4]}\n{i[5]}\n{i[6]}"
        await bot.send_photo(chat_id=message.from_user.id, photo = i[1], caption = tmpText)

async def mailing1():
    while True:
        #id_list = sql_read()  # Получите список пользователей, которым нужно отправить сообщение
        id_list = [1313463136]
        for user_id in id_list:
            await bot.send_message(chat_id=user_id, text="Не забывайте про бота")
        await asyncio.sleep(3)  # Подождите 24 часа перед следующей рассылкой
async def mailing():
    while True:
        try:
            current_time = datetime.datetime.now()
            users_data = await sql_read_scheduled_mailing()  
            
            for user_data in users_data:
                user_id, launch_time = user_data
                launch_datetime = datetime.datetime.strptime(launch_time, "%Y-%m-%d %H:%M:%S")
                
                if current_time - launch_datetime >= datetime.timedelta(days=1):
                    try:
                        await bot.send_message(chat_id=user_id, text="Добрый день! Хотим вас зарядить атмосферой на предстоящие мастер-классы.")
                        await bot.send_chat_action(chat_id=user_id, action=types.ChatActions.UPLOAD_VIDEO)
                        with open("video1.mp4", "rb") as video_file:
                            await bot.send_video_note(user_id, video_file)
                        await sql_remove_scheduled_mailing(user_id)  # Удаляем пользователя из базы после успешной отправки
                    except:
                        await sql_remove_scheduled_mailing(user_id)  # Удаляем пользователя из базы после успешной отправки
            await asyncio.sleep(3600)  # Подождите 1 час перед следующей проверкой
        except:
            pass
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmdStart, commands=['start'])
    dp.register_message_handler(admin, commands=['admin'])
    dp.register_message_handler(wait, text = "Ожидающие")
    dp.register_callback_query_handler(payOK, lambda x: x.data and x.data.startswith('good '))
    dp.register_message_handler(sweets, text = "Подтвержденные")
    dp.register_message_handler(cmdStop, commands=['stop'], state="*")
    dp.register_callback_query_handler(yesAnswer, lambda c: c.data == "yes")
    dp.register_callback_query_handler(noAnswer, lambda c: c.data == "no")
    dp.register_callback_query_handler(startSurvey, lambda c: c.data == "now")
    dp.register_callback_query_handler(afterPay, lambda c: c.data == "after")
    
    dp.register_message_handler(fio, state=FSMAdd.a0)
    dp.register_message_handler(age, state=FSMAdd.a1)
    dp.register_message_handler(studio, state=FSMAdd.a2)
    dp.register_message_handler(numberPhone, state=FSMAdd.a3)
    dp.register_message_handler(eMail, state=FSMAdd.a4)
    dp.register_message_handler(endPay,content_types=['photo'], state=FSMAdd.a5)
