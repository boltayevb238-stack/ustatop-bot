import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# 1. SOZLAMALAR
API_TOKEN = '8643267988:AAEagHn5yWtylv1M6vdy6ljtFy81OTqySVg'
GROUP_ID = -1003962798702 # 

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# 2. HOLATLAR
class OrderProcess(StatesGroup):
    choosing_service = State()
    choosing_district = State()
    getting_info = State()

# 3. KNOPKALAR (5 ta xizmat + tumanlar)
service_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🛠 Santexnik"), KeyboardButton(text="⚡️ Elektrik")],
    [KeyboardButton(text="❄️ Maishiy texnika"), KeyboardButton(text="🪑 Mebel ustasi"), KeyboardButton(text="🧱 Qurilish")],
], resize_keyboard=True)

district_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Chilonzor"), KeyboardButton(text="Yunusobod")],
    [KeyboardButton(text="Mirobod"), KeyboardButton(text="Yakkasaroy"), KeyboardButton(text="Shayxontohur")],
    [KeyboardButton(text="Bektemir"), KeyboardButton(text="Sergeli"), KeyboardButton(text="Olmazor")],
    [KeyboardButton(text="Uchtepa"), KeyboardButton(text="Mirzo Ulug'bek")]
], resize_keyboard=True)

# 4. FUNKSIYALAR
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("UstaTop-ga xush kelibsiz! Qaysi xizmat turini tanlaysiz?", reply_markup=service_kb)

@dp.message(OrderProcess.choosing_service) # Xizmat tanlash
async def get_district(message: types.Message, state: FSMContext):
    await state.update_data(service=message.text)
    await message.answer("Tumaningizni tanlang:", reply_markup=district_kb)
    await state.set_state(OrderProcess.choosing_district)

@dp.message(OrderProcess.choosing_district) # Tuman tanlash
async def get_info(message: types.Message, state: FSMContext):
    await state.update_data(district=message.text)
    await message.answer("Oxirgi qadam: Ism va telefon raqamingizni yozing:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(OrderProcess.getting_info)

@dp.message(OrderProcess.getting_info)
async def finalize_order(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = (f"🔔 YANGI BUYURTMA!\n"
            f"🛠 Xizmat: {data['service']}\n"
            f"📍 Tuman: {data['district']}\n"
            f"👤 Mijoz: {message.from_user.full_name}\n"
            f"📞 Ma'lumot: {message.text}")
    
    await bot.send_message(GROUP_ID, text)
    await message.answer("✅ Arizangiz qabul qilindi! Ustalarimiz tez orada siz bilan bog'lanishadi.")
    await state.clear()
