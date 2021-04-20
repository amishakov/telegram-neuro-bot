import logging
from aiogram import Bot, Dispatcher, executor, types
import os
import random
import mc


API_TOKEN = '123' # токен бота

# Логи в консоль
logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

dir_to_txt = "Dialogs/"

@dp.message_handler(content_types=["new_chat_members"])
async def new_chat(message: types.Message):
	dialog_filename = f"{dir_to_txt}{message.chat.id}.txt"

	if not os.path.exists(dialog_filename):
		open(dialog_filename, "w").close()
	for user in message.new_chat_members:
		if user.id == bot.id:
			await message.answer(f"Вы добавили меня в чат, мои команды /help\nНе забудьте выдать мне права администратора!")


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	await message.answer(f'Привет, {message.from_user.first_name}, я работаю только в чатах.')


@dp.message_handler(commands=['help'])
async def react(message: types.Message):
	await message.answer('Мои команды:\n/gen - сгенерировать фразу\n/info - данные о базе')

@dp.message_handler(commands=['gen'])
async def gen(message: types.Message):
	text_length = len(message.text)
	chat_path = f"{dir_to_txt}{message.chat.id}.txt"

	with open(chat_path, encoding="utf8") as f:
		text_lines = len(f.readlines())

	if text_lines >= 4:
		with open(chat_path, encoding="utf8") as file:
			texts = file.read().splitlines()
		# Выбираем рандомный текст
		generator = mc.StringGenerator(samples=texts)
		random_text = generator.generate_string(attempts=100, validator=mc.util.combine_validators(mc.validators.words_count(minimal=1, maximal=100)))
		await message.answer(random_text.lower())

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
	chat_path = f"{dir_to_txt}{message.chat.id}.txt"
	with open(chat_path, encoding="utf8") as f:
		text_count = len(f.readlines())

	await message.answer(
		f"ID чата: {message.chat.id}\nсохранено {text_count} строк")

@dp.message_handler(content_types=['text'])
async def sov(message: types.Message):
	text_length = len(message.text)
	chat_path = f"{dir_to_txt}{message.chat.id}.txt"
	if message.text in [
		"/gen",
		"/start",
		"/help",
		"/info"

	]:
		return
	if (
		message.text.startswith("http://")
		or message.text.startswith("https://")
		or message.text.startswith("vk.com")
		or message.text.startswith("https://vk.com/")
		or message.text.startswith("/")
	):
		return
		
	if 0 < text_length <= 1000:
		with open(chat_path, "a", encoding="utf8") as f:
			f.write(message.text + "\n")

	with open(chat_path, encoding="utf8") as f:
		text_lines = len(f.readlines())
	demorpic = random.randint(0,5)
	if demorpic in [1,2,3,4]:
		if text_lines >= 4:
			with open(chat_path, encoding="utf8") as file:
				texts = file.read().splitlines()
			# Выбираем рандомный текст
			generator = mc.StringGenerator(samples=texts)
			random_text = generator.generate_string(attempts=100, validator=mc.util.combine_validators(mc.validators.words_count(minimal=1, maximal=100)))
			await message.answer(random_text.lower())










if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)
	if not os.path.exists("Dialogs/"):
		os.mkdir("Dialogs/")