import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from flask import Flask
from threading import Thread
import asyncio

API_TOKEN = '8643267988:AAEagHn5yWtylv1M6vdy6ljtFy81OTqySVg'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# 24/7 ishlashi uchun
app = Flask('')
@app.route('/')
def home(): return "Bot ishlayapti!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# Holatlar
class ClientOrder(StatesGroup):
    choosing_service = State()
    getting_info = State()

# Guruh ID
GROUP_ID = -1002166649867 

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="👤 Mijoz"), KeyboardButton(text="🛠️ Usta")]], resize_keyboard=True)
    await message.answer("UstaTop-ga xush kelibsiz! Kim sifatida davom etasiz?", reply_markup=kb)

@dp.message(F.text == "👤 Mijoz")
async def client_start(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🚰 Santexnik"), KeyboardButton(text="⚡ Elektrik")]], resize_keyboard=True)
    await state.set_state(ClientOrder.choosing_service)
    await message.answer("Xizmat turini tanlang:", reply_markup=kb)

@dp.message(ClientOrder.choosing_service)
async def get_client_info(message: types.Message, state: FSMContext):
    await state.update_data(service=message.text)
    await state.set_state(ClientOrder.getting_info)
    await message.answer("Ism, telefon raqam va manzilingizni yozing:", reply_markup=ReplyKeyboardRemove())

@dp.message(ClientOrder.getting_info)
async def finish_order(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = f"🔔 **YANGI BUYURTMA!**\n🛠 Xizmat: {data['service']}\n👤 Mijoz: {message.from_user.full_name}\n📞 Ma'lumot: {message.text}"
    await bot.send_message(GROUP_ID, text, parse_mode="Markdown")
    await message.answer("✅ Arizangiz qabul qilindi, ustalarimiz tez orada bog'lanishadi!")
    await state.clear()

async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
