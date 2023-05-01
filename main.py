from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext

from config import TOKEN
from parser import main


bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())


class Data(StatesGroup):
    youtuber = State()
    videos = State()


@dispatcher.message_handler(commands=['start'])
async def get_started(message: types.Message) -> None:
    name = message.from_user.username
    if name is None:
        name = "guest"

    await message.answer(parse_mode='HTML', text=f"Greetings, <em>{name}</em>! "
                                                "This telegram bot with help you automate your searching for new youtube videos!")
    await message.answer(text="Write /help to view more information.")


@dispatcher.message_handler(commands=['help'])
async def help_command(message: types.Message) -> None:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton('/get_new_videos'), KeyboardButton('/cancel'))

    await message.answer(text="You can choose any of these actions down below.\n/get_new_videos - by this command you can send request for youtuber's video\n/cancel - command which uses to revoke any action",
                        reply_markup=kb)


@dispatcher.message_handler(commands=['get_new_videos'])
async def get_new_videos(message: types.Message) -> None:
    await message.answer(text="Enter the name of necessary youtube channel:")
    await Data.youtuber.set()


@dispatcher.message_handler(commands=['cancel'])
async def cancel_command(message: types.Message, state: FSMContext):
    await message.answer(text='Your last action was revoked.')
    current_state = await state.get_state()
    if not current_state:
        return

    await state.finish()


@dispatcher.message_handler(state=Data.youtuber)
async def input_youtuber(message: types.Message, state: FSMContext):
    answer = message.text

    if type(answer) == str:
        if answer == '/cancel':
            return await cancel_command(message, state)

        async with state.proxy() as data:
            data['youtuber'] = answer

        await message.answer('Also enter quantity of videos you want to get. It will be any digit bettween 1 and 30.')
        return await Data.next()

    await message.answer("Please enter channel's name (text only).")
    await Data.youtuber.set()


@dispatcher.message_handler(state=Data.videos)
async def input_videos_quantity(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == '/cancel':
        return await cancel_command(message, state)

    elif answer.isdigit() or answer[1:].isdigit():
        if int(answer) < 1 or int(answer) > 30:
            return await message.answer("Inputed digit doesn't fit limits.")

        async with state.proxy() as data:
            data['videos'] = answer

        videos_list = main(data['youtuber'], int(data['videos']))
        if videos_list:
            for video in videos_list:
                await message.answer(video)
        else:
            await message.answer("Sorry, all links aren't valid.")

        return await state.finish()

    await message.answer('Input string must contains only digits. Try again.')
    await Data.videos.set()


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
