import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = 'токен'

movies = {
    "Fight club": "https://docs.google.com/document/d/13VL92vH0LI8nDqv4oDpw3NWX8g6RSrE_y1V4zfRJV1w/edit",
    "The Matrix": "https://docs.google.com/document/d/1Z7Ugj-aHCB6SAept53X05U0-w59cWlLE_GSd66sXsw8/edit#heading=h.gby1tm1gf07k",
    "how to train your dragon": "https://docs.google.com/document/d/1XxuQ2A8fLarFGuSkPdJYF0gVAPv6LUYFwrcWNRrvQCc/edit",
    "Gran Turismo":"https://docs.google.com/document/d/1TT8ZG8fKD_vVVQZBSWhvpzv9fxClmUDnB90ebSi5Tc8/edit",
    "Lord of the Rings":"https://docs.google.com/document/d/1aOvPOEFHNFVv34k_TmeEt2bujWFG5P1WrG9cQT9L21k/edit",
    "Breaking Bad":"https://docs.google.com/document/d/1SUJqQb-M93Ff1_VBiIMSJA2tsx7NLMRsVQDP8E1pglc/edit",
    "The big bang theory":"https://docs.google.com/document/d/1U1vlHZKXes4cKv1Zy1Yn824ebI6O7fnm84geuSKHuT8/edit",
    "The Hobbit trilogy":"https://docs.google.com/document/d/1psgp1aTLg9R9YFC9Dk2hB2Dv7BwyLvXOoUzMhrDKcts/edit",
    "game of thrones":"https://docs.google.com/document/d/13oOAk9vUVmTCpCoBn1Gx6FXMcRA1VMn8aruxpIYoKko/edit",
    "Diuna":"https://docs.google.com/document/d/1usPjLSNzEiWhOanJpDtDQsyRLi_RH6WIO-eHYkF897w/edit"
}

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

user_data = {}
user_ratings = {}
user_reviews = {}

people = [
    "",
    "",
    "",
    "",
    "",
    ""
]

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Добрий день! Ви в сервісі фільмів|серіалів. Ось список доступних команд:\n\n"
                        "/movies - Переглянути список фільмів\n"
                        "/rate - Оцінити фільм. Використовуйте цю команду у форматі '/rate назва_фільму оцінка'\n"
                        "/review - Залишити відгук на фільм. Використовуйте цю команду у форматі '/review назва_фільму відгук'\n"
                        "/list - Переглянути список фільмів з оцінками та відгуками\n"
                        "/end - Завершити роботу з ботом")

@dp.message_handler(commands=['movies'])
async def show_movies(message: types.Message):
    movie_list = "\n".join([f"{movie}: {link}" for movie, link in movies.items()])
    await message.reply(f"Фільми|серіали:\n\n{movie_list}", parse_mode=ParseMode.HTML)

@dp.message_handler(commands=['rate'])
async def rate_movie(message: types.Message):
    command, movie, rating = message.text.split(' ', 2)
    if movie in movies and 1 <= int(rating) <= 10:
        user_ratings[message.from_user.id] = {movie: int(rating)}  # зберігаємо оцінку як число
        await message.reply(f"Ви оцінили фільм {movie} на {rating} балів")
    else:
        await message.reply("Будь ласка, введіть назву фільму зі списку та оцінку від 1 до 10")


@dp.message_handler(commands=['review'])
async def review_movie(message: types.Message):
    command, movie, review = message.text.split(' ', 2)
    if movie in movies:
        user_reviews[message.from_user.id] = {movie: review}
        await message.reply(f"Ви залишили відгук на фільм {movie}: {review}")
    else:
        await message.reply("Будь ласка, введіть назву фільму зі списку та ваш відгук")

@dp.message_handler(commands=['list'])
async def list_ratings_reviews(message: types.Message):
    ratings_reviews_list = ""
    for movie in movies:
        ratings = [user_ratings[user][movie] for user in user_ratings if movie in user_ratings[user]]
        reviews = [user_reviews[user][movie] for user in user_reviews if movie in user_reviews[user]]
        average_rating = sum(ratings) / len(ratings) if ratings else 0
        average_rating_text = str(average_rating) if ratings else "немає оцінки"
        reviews_text = "\n".join(reviews) if reviews else "немає відгуків"
        ratings_reviews_list += f"{movie}:\nОцінка: {average_rating_text}\nВідгуки:\n{reviews_text}\n\n"
    await message.reply(f"Оцінки та відгуки:\n\n{ratings_reviews_list}", parse_mode=ParseMode.HTML)

@dp.message_handler(commands=['end'])
async def end_interaction(message: types.Message):
    await message.reply("Спасибі за використання бота від команди 'Мирного рішення не буде' Ось список людей:\n\n" + "\n".join(people))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

    executor.start_polling(dp, skip_updates=True)
