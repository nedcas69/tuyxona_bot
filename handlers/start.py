from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsPrivate, IsAdm
from keyboards import lang_btn, kb_admin  # Импортируем нашу клавиатуру
from loader import dp


@dp.message_handler(Command("start"), IsAdm())  # Создаём message handler который ловит команду /menu
async def menu(message: types.Message):  # Создаём асинхронную функцию
    await message.answer("Admin!", reply_markup=kb_admin)


@dp.message_handler(Command("start"), IsPrivate())  # Создаём message handler который ловит команду /menu
async def menu(message: types.Message):  # Создаём асинхронную функцию
    await message.answer("Выберите язык!", reply_markup=lang_btn)
    doc_uz = 'BQACAgIAAxkBAAIIImS1CvOg3e7fdNRur3l-BLrJOWhrAAJcLwAC1HqoSWCzyuemdKr6LwQ'
    doc_ru = 'BQACAgIAAxkBAAIIJGS1EfF-nuHoulbWnUV73YahvvhkAAJ-LwAC1HqoSX4JqSozaw58LwQ'
    await message.answer_document(doc_uz)
    await message.answer_document(doc_ru)
