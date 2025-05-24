import aioschedule
from aiogram.filters import Command
from aiogram import types, Bot, Dispatcher
import asyncio
import time
from aiogram import types
from data import *
from db import *
import pandas as pd
from io import BytesIO
from aiogram.types import BufferedInputFile
from datetime import datetime, timedelta
from aiogram import Bot
import asyncio


# ChannelName = "@test-sashabelov" 8004593517
# await bot.send_message(ChannelName, message_text)   # Kanalga xabar jonatish

TOKEN = ""

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}
user_data_superuser = {}
super_users = [921347523]





@dp.message()
async def handel_text(message: types.Message):
    try:
        total = get_super_admin()
        for i in total:
            if i:
                super_users.append(i[0])
        user_id = message.from_user.id
        if user_id not in super_users:
            if user_id not in user_data or message.text == "/start":
                await start(message)
            elif message.text in {"💵 To'lov", "💵 Payment", "💵 Оплата"}:
                await payment(message)
            elif message.text in aboutus:
                await about(message)
            elif message.text in loc:
                await location(message)
            elif message.text in courses:
                await course(message)
            elif message.text in back or message.text in language:
                await welcome(message)
            elif message.text in check:
                await confirm(message)
            elif "tolov" in user_data[user_id]:
                await process_payment_type(message)
            elif "fio" in user_data[user_id]:
                await check_phone(message)
            elif message.text in buttons:
                await register(message)
            elif "next_menu" in user_data[user_id]:
                await full_fio(message)
        else:
            if user_id not in user_data_superuser or message.text == "/start":
                await start_superuser(message)
            elif  message.text in superadmin_back:
                await menu_superuser(message)
            elif message.text in find_students:
                await find_student(message)
            elif message.text in add_admin:
                await add_admins(message)
            elif "delete" in user_data_superuser[user_id]:
                await del_student_check(message)
            elif message.text in admin_language:
                await menu_superuser(message)
            elif message.text in students_dict:
                await student_list_superuser(message)
            elif message.text in delete_st:
                await del_student(message)
            elif "find_student" in user_data_superuser[user_id]:
                await one_student(message)
            elif "admin" in user_data_superuser[user_id]:
                await add(message)


    except Exception as e:
        await message.answer(f"Unexpected error! Something went wrong.{e}")






@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    button = [
        [types.KeyboardButton(text="🇺🇿 O'zbekcha"),types.KeyboardButton(text="🇺🇸 English"),types.KeyboardButton(text="🇷🇺 Русский")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
    await message.answer("Iltimos tilni tanlang.\n"
                         "Please choose language.\n"
                         "Пожалуйста выберите язык.", reply_markup=keyboard)
    print(message.chat.id)
    print(user_data)




async def welcome(message: types.Message):
    try:
        user_id = message.from_user.id
        for i in item:
            if i in user_data[user_id]:
                del user_data[user_id][i]
        try:
            if "language" in user_data[user_id]:
                til = user_data[user_id]["language"]
                user_data[user_id]["state"] = "welcome"
                lang = data[til] # [[]]
                button = [
                    [types.KeyboardButton(text=f"{lang[0][0]}"),types.KeyboardButton(text=f"{lang[0][1]}")],
                    [types.KeyboardButton(text=f"{lang[0][2]}"),types.KeyboardButton(text=f"{lang[0][3]}")],
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
                await message.answer(f"{lang[0][-1]}", reply_markup=keyboard)
                print(user_data)
            else:
                user_data[user_id]["language"] = message.text
                user_data[user_id]["state"] = "welcome"
                lang = data[message.text]  # [[]]
                button = [
                    [types.KeyboardButton(text=f"{lang[0][0]}"), types.KeyboardButton(text=f"{lang[0][1]}")],
                    [types.KeyboardButton(text=f"{lang[0][2]}"), types.KeyboardButton(text=f"{lang[0][3]}")],
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
                await message.answer(f"{lang[0][-1]}", reply_markup=keyboard)
                print(user_data)
        except Exception as e1:
            print(e1)
    except Exception as e:
        await message.answer(f"Unexpected error! Something went wrong.{e} 2")



async def register(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]["state"] = "register"
    lang = data[user_data[user_id]["language"]] # [[]]
    button = [
        [types.KeyboardButton(text=f"{lang[1][0]}")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
    await message.answer(f"{lang[1][-1]}", reply_markup=keyboard)
    user_data[user_id]["next_menu"] = "next_menu"
    print(user_data)



async def full_fio(message: types.Message):
    try:
        user_id = message.from_user.id
        lang = data[user_data[user_id]["language"]]  # [[]]
        user_data[user_id]["state"] = "check_course"
        ok = True
        matn = message.text
        text = message.text.split()
        for i in text:
            for j in i:
                if not j.isalpha():
                    await message.answer(f"{lang[2][-1]}")
                    ok = False
                    break

        if ok:
            user_data[user_id]["fio"] = matn
            button = [
                [types.KeyboardButton(text=f"{lang[2][0]}", request_contact=True), types.KeyboardButton(text=f"{lang[2][1]}")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
            await message.answer(f"{lang[2][2]}", reply_markup=keyboard)
            user_data[user_id]["fio"] = matn
    except Exception as e:
        await message.answer(f"Unexpected error! Something went wrong.{e}")
    print(user_data)



async def check_phone(message: types.Message):
    try:
        user_id = message.from_user.id
        user_data[user_id]["state"] = "ask_phone"
        lang = data[user_data[user_id]["language"]]
        phone_num = message.text
        state = True
        numbers = "+0123456789"
        fio = user_data[user_id]["fio"]
        course = lang[3][5]
        user_data[user_id]["course"] = course
        if message.contact is not None:
            phone_c = message.contact.phone_number
            user_data[user_id]['phone'] = phone_c
            button = [
                [types.KeyboardButton(text=f"{lang[3][0]}"),types.KeyboardButton(text=f"{lang[3][1]}")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
            await message.answer(f"{lang[3][2]}\n"
                                 f"👤 {lang[3][3]}: {fio}\n"
                                 f"📞 {lang[3][4]}: {phone_c}\n"
                                 f"📚 {lang[3][5]}", reply_markup=keyboard)
        else:
            if len(phone_num) == 13:
                if phone_num[:4] == "+998":
                    for i in phone_num:
                        if i not in numbers:
                            await message.answer(f"{lang[2][-1]}")
                            state = False
                            break
                    if state:
                        user_data[user_id]["phone"] = phone_num
                        button = [
                            [types.KeyboardButton(text=f"{lang[3][0]}"),types.KeyboardButton(text=f"{lang[3][1]}")]
                        ]
                        keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
                        await message.answer(f"{lang[3][2]}\n"
                                             f"👤 {lang[3][3]} {fio}\n"
                                             f"📞 {lang[3][4]} {phone_num}\n"
                                             f"📚 {lang[3][5]}", reply_markup=keyboard)
                else:
                    await message.answer(f"{lang[2][-2]}")
            else:
                await message.answer(f"{lang[2][-3]}")

    except Exception as e:
        await message.answer(f"Unexpected error! Something went wrong.{e}")
    print(user_data)



async def confirm(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]["state"] = "register"
    lang = data[user_data[user_id]["language"]] # [[]]
    button = [
        [types.KeyboardButton(text=f"{lang[4][0]}"), types.KeyboardButton(text=f"{lang[4][1]}")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
    await message.answer(f"{lang[4][-2]}", reply_markup=keyboard)
    await message.answer(f"{lang[4][-1]}", reply_markup=keyboard)
    print(user_data)




async def about(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]["state"] = "about"
    lang = data[user_data[user_id]["language"]] # [[]]

    button = [
        [types.KeyboardButton(text=f"{lang[5][0]}"), types.KeyboardButton(text=f"{lang[5][1]}")],
    ]
    but = [
        [types.InlineKeyboardButton(text="Youtube", url=f"{lang[5][2]}"), types.InlineKeyboardButton(text="Telegram", url=f"{lang[5][3]}")],
        [types.InlineKeyboardButton(text="Instagram", url=f"{lang[5][4]}")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
    key = types.InlineKeyboardMarkup(inline_keyboard=but, resize_keyboard=True)
    await message.answer(f"{lang[5][-2]}", reply_markup=keyboard)
    await message.answer(f"{lang[5][-1]}", reply_markup=key)
    print(user_data)



async def location(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]["state"] = "location"
    lang = data[user_data[user_id]["language"]] # [[]]

    button = [
        [types.KeyboardButton(text=f"{lang[6][-1]}")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
    await message.answer(f"{lang[6][2]}"
                         f"{lang[6][3]}"
                         f"{lang[6][4]}", reply_markup=keyboard)
    await bot.send_location(chat_id=message.from_user.id,
                                longitude=lang[6][0],
                                latitude=lang[6][1])
    print(user_data)


async def course(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]["state"] = "course"
    lang = data[user_data[user_id]["language"]] # [[]]
    button = [
        [types.KeyboardButton(text=f"{lang[7][0]}")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
    await message.answer(f"{lang[7][1]}\n"
                         f"{lang[7][-2]}", reply_markup=keyboard)
    await message.answer(f"{lang[7][-1]}")



async def payment(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]["state"] = "register"
    lang = data[user_data[user_id]["language"]]
    button = [
        [types.KeyboardButton(text=f"{lang[8][0]}")],
        [types.KeyboardButton(text=f"{lang[8][1]}"), types.KeyboardButton(text=f"{lang[8][2]}")],
        [types.KeyboardButton(text=f"{lang[8][3]}")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
    await message.answer(f"{lang[8][-1]}", reply_markup=keyboard)
    user_data[user_id]["tolov"] = "tolov"
    print(user_data)


@dp.message(lambda message: message.text in ["💳 Plastik karta", "Click", "Payme","💳 Bank card", "Click", "Payme","💳 Банковская карта", "Click", "Payme"])
async def process_payment_type(message: types.Message):
    user_id = message.from_user.id
    lang = data[user_data[user_id]["language"]]
    fio = user_data[user_id]["fio"]
    phone = user_data[user_id]["phone"]
    course = user_data[user_id]["course"]
    save_info(user_id, fio, phone, course)
    await message.answer(f'{lang[9][0]}')
    await message.answer(f'{lang[9][1]}')



# *************** ////////// ******************* #

# *************** A D M I N ******************** #


@dp.message(Command("start"))
async def start_superuser(message: types.Message):
    user_id = message.from_user.id
    user_data_superuser[user_id] = {}
    button = [
        [types.KeyboardButton(text="🇺🇿 O'zbekcha"),types.KeyboardButton(text="🇺🇸 English"),types.KeyboardButton(text="🇷🇺 Русский")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
    await message.answer("Iltimos tilni tanlang.\n"
                         "Please choose language.\n"
                         "Пожалуйста выберите язык.", reply_markup=keyboard)
    print("new",user_data_superuser)


async def menu_superuser(message: types.Message):
    user_id = message.from_user.id
    user_data_superuser[user_id]["state"] = "menu_superuser"
    if "language" not in user_data_superuser[user_id]:
        user_data_superuser[user_id]["language"] = message.text
        lang = admin[user_data_superuser[user_id]["language"]] # [[]]
        button = [
            [types.KeyboardButton(text=f"{lang[0][0]}"),types.KeyboardButton(text=f"{lang[0][1]}")],
            [types.KeyboardButton(text=f"{lang[0][2]}"),types.KeyboardButton(text=f"{lang[0][3]}")],
            [types.KeyboardButton(text=f"{lang[0][4]}"),types.KeyboardButton(text=f"{lang[0][5]}")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
        await message.answer(f"{lang[0][-1]}", reply_markup=keyboard)
    else:
        keys = {"delete", "find_student", "admin"}
        for key in keys:
            if key in user_data_superuser[user_id]:
                del user_data_superuser[user_id][key]
        lang = admin[user_data_superuser[user_id]["language"]]  # [[]]
        button = [
            [types.KeyboardButton(text=f"{lang[0][0]}"), types.KeyboardButton(text=f"{lang[0][1]}")],
            [types.KeyboardButton(text=f"{lang[0][2]}"), types.KeyboardButton(text=f"{lang[0][3]}")],
            [types.KeyboardButton(text=f"{lang[0][4]}"), types.KeyboardButton(text=f"{lang[0][5]}")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
        await message.answer(f"{lang[0][-1]}", reply_markup=keyboard)
    print(user_data_superuser)


# async def student_list_superuser(message: types.Message):
#     user_id = message.from_user.id
#     lang = admin[user_data_superuser[user_id]["language"]] # [[]]
#
#     def execl_file(info):
#         column = ["Tg_ID", "FIO", "Phone", "Course", "Created_At"]
#         df = pd.DataFrame(info, columns=column)
#         file = df.to_excel("students_info.xlsx", index=False)
#         print("✅ Excel faylga saqlandi: student_info.xlsx")
#         return file
#
#     students = get_all_students()
#
#     button = [
#         [types.KeyboardButton(text=f"{lang[1][0]}")],
#     ]
#     keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
#     for student in students:  # [()]
#         total = [] # [1212, fii, phone, course, time]
#         for i in student:
#             total.append(str(i) + "\n")
#         await message.answer(f"{lang[1][1]}\n"
#                              f"{lang[1][2]} {total[0]}"
#                              f"{lang[1][3]} {total[1]}"
#                              f"{lang[1][4]} {total[2]}"
#                              f"{lang[1][5]} {total[3]}"
#                              f"{lang[1][6]} {total[4]}", reply_markup=keyboard)
#     print(user_data_superuser)


# Excel faylni xotirada yaratish funksiyasi
def excel_file(info):
    from io import BytesIO

    columns = ["tg_id", "fio", "phone", "course", "payment_amount","balance","payment_date","created_at"]
    df = pd.DataFrame(info, columns=columns)
    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)
    return buffer



async def student_list_superuser(message: types.Message):
    user_id = message.from_user.id
    lang = admin[user_data_superuser[user_id]["language"]]

    try:
        students = get_all_students()

        if not students:
            await message.answer(lang[1][-1])
            return

        excel_buffer = excel_file(students)

        document = BufferedInputFile(
            file=excel_buffer.read(),  # Muhim: .read() qilish kerak!
            filename="students_info.xlsx"
        )

        button = [[types.KeyboardButton(text=f"{lang[1][0]}")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)

        await message.answer_document(document=document, caption=lang[1][1], reply_markup=keyboard)

    except Exception as e:
        print("❌ Xato:", e)




async def del_student(message: types.Message):
    user_id = message.from_user.id
    user_data_superuser[user_id]["delete"] = "student"
    lang = admin[user_data_superuser[user_id]["language"]]
    button = [
        [types.KeyboardButton(text=f"{lang[2][0]}")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
    await message.answer(f"{lang[2][1]}", reply_markup=keyboard)
    print(user_data_superuser)



async def del_student_check(message: types.Message):
    user_id = message.from_user.id
    lang = admin[user_data_superuser[user_id]["language"]]

    text = message.text.strip()
    res = None

    if text.isdigit():
        res = delete_student(tg_id=text)
    elif text.startswith('+') and text[1:].isdigit():
        res = delete_student(phone=text)
    else:
        res = delete_student(fio=text)

    button = [
        [types.KeyboardButton(text=f"{lang[2][0]}")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f"{res}", reply_markup=keyboard)



async def add_admins(message: types.Message):
    user_id = message.from_user.id
    user_data_superuser[user_id]["admin"] = "admin"
    lang = admin[user_data_superuser[user_id]["language"]]
    button = [
        [types.KeyboardButton(text=f"{lang[3][0]}")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
    await message.answer(f"{lang[3][1]}", reply_markup=keyboard)
    print(user_data_superuser)



async def add(message: types.Message):
    user_id = message.from_user.id
    lang = admin[user_data_superuser[user_id]["language"]]

    if message.text.isdigit():
        if len(message.text) == 9:
            tg_id = int(message.text)
            result = add_super_admin(tg_id)
            if result is True:
                await message.answer(f"{lang[4][2]}")
            else:
                await message.answer(f"{lang[4][1]}")
    else:
        await message.answer(f"{lang[4][0]}")



async def find_student(message: types.Message):
    user_id = message.from_user.id
    user_data_superuser[user_id]["find_student"] = "find_student"
    lang = admin[user_data_superuser[user_id]["language"]]
    button = [
        [types.KeyboardButton(text=f"{lang[5][0]}")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button,resize_keyboard=True)
    await message.answer(f"{lang[5][1]}", reply_markup=keyboard)
    print(user_data_superuser)


async def one_student(message: types.Message):
    user_id = message.from_user.id
    lang = admin[user_data_superuser[user_id]["language"]]
    text = message.text
    if text.isdigit() and len(text) >= 9:
        student = find_user(tg_id=text)
    elif text.isalpha():
        student = find_user(fio=text)
    else:
        student = find_user(phone=text)


    if student:
        student_info = ""
        for row in student:
            student_info += f"{lang[6][-3]} {lang[6][0]} {row[0]}\n{lang[6][1]} {row[1]}\n{lang[6][2]} {row[2]}\n{lang[6][3]} {row[3]}\n{lang[6][4]} {row[4]}"

        button = [[types.KeyboardButton(text=f"{lang[6][-1]}")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
        await message.answer(student_info, reply_markup=keyboard)
    else:
        await message.answer(f"{lang[6][-2]}")




async def daily_payment_check(bot: Bot):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT tg_id, fio, payment_date, payment_amount, balance FROM student_info")
    rows = cursor.fetchall()
    today = datetime.now().date()

    for row in rows:
        tg_id, fio, payment_date, amount, balance = row

        # Guruh ID lar odatda -100 bilan boshlanadi, shularni o'tkazib yuboramiz
        if str(tg_id).startswith('-100'):
            print(f"Guruh ID aniqlangan ({tg_id}), xabar yuborilmaydi.")
            continue

        if not payment_date or balance is None:
            print(f"Foydalanuvchi {tg_id} o‘tkazib yuborildi: to‘lov sanasi yoki balans yo‘q (None)")
            continue

        next_payment_date = payment_date + timedelta(days=30)
        days_left = (next_payment_date - today).days
        daily_cost = amount // 30
        passed_days = (today - payment_date).days
        used_payment = daily_cost * passed_days
        updated_balance = max(0, amount - used_payment)

        print(f"Foydalanuvchi {tg_id}: qolgan kunlar = {days_left}, yangilangan balans = {updated_balance}")

        cursor.execute(
            "UPDATE student_info SET balance = %s WHERE tg_id = %s",
            (updated_balance, tg_id)
        )
        conn.commit()

        # Faqat foydalanuvchilarga xabar yuboriladi
        try:
            if days_left in [5, 3]:
                await bot.send_message(
                    chat_id=tg_id,
                    text=f"📢 {fio}, {days_left} kun ichida to‘lov qilish kerak. Balansingiz: {updated_balance} so'm."
                )
            elif days_left <= 0 and updated_balance <= 0:
                await bot.send_message(
                    chat_id=tg_id,
                    text="⛔️ To‘lov muddati tugadi va balansingiz yo‘q. Siz guruhdan chiqarildingiz."
                )

                # Guruhdan chiqarish
                GROUP_ID = -1002631687688
                await bot.ban_chat_member(chat_id=GROUP_ID, user_id=tg_id)
                await bot.unban_chat_member(chat_id=GROUP_ID, user_id=tg_id)

                # Bazadan o'chirish
                cursor.execute("DELETE FROM student_info WHERE tg_id = %s AND balance = 0", (tg_id,))
                conn.commit()
                print(f"Foydalanuvchi {tg_id} ma'lumotlar bazasidan o‘chirildi.")
        except Exception as e:
            print(f"Xatolik yuz berdi (tg_id={tg_id}): {e}")

    cursor.close()
    conn.close()



async def scheduler(bot: Bot):
    print('Rejalar boshlandi...')

    def job():
        asyncio.create_task(daily_payment_check(bot))

    # aioschedule.every().minute.do(job)
    aioschedule.every().day.at("11:00").do(job)


    while True:
        print("Navbatdagi vazifalar bajarilmoqda...")
        await aioschedule.run_pending()
        await asyncio.sleep(60)


async def on_startup(dp):
    print("Bot ishga tushmoqda: Rejalar boshlanmoqda...")
    asyncio.create_task(scheduler(bot))


async def main():
    print("Bot ishlamoqda...")
    await daily_payment_check(bot)
    await dp.start_polling(bot, on_startup=on_startup)


asyncio.run(main())

