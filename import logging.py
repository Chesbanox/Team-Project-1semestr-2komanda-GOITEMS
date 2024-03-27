import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = '6809237237:AAFPYLUIDTk6yKFQkiJq4oxIHUaGrQCo6do'

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

# Ініціалізуємо логування
logging.basicConfig(level=logging.INFO)

# Створюємо об'єкт бота та диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Створюємо словник для зберігання списку фільмів, які користувачі хочуть подивитися, та їхніх оцінок
user_data = {}

# Створюємо словник для зберігання оцінок користувачів
user_ratings = {}

# Створюємо словник для зберігання відгуків користувачів
user_reviews = {}

# Список людей
people = [
    "Кутузов Антон",
    "Конотоп Олексій",
    "Легкобит Марк",
    "Олександр Опалько",
    "Іван Аксьонов",
    "Джафаров Леван"
]

# Обробник команди /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Добрий день! Ви в сервісі фільмів|серіалів. Ось список доступних команд:\n\n"
                        "/movies - Переглянути список фільмів\n"
                        "/rate - Оцінити фільм. Використовуйте цю команду у форматі '/rate назва_фільму оцінка'\n"
                        "/review - Залишити відгук на фільм. Використовуйте цю команду у форматі '/review назва_фільму відгук'\n"
                        "/list - Переглянути список фільмів з оцінками та відгуками\n"
                        "/end - Завершити роботу з ботом")

# Обробник команди /movies
@dp.message_handler(commands=['movies'])
async def show_movies(message: types.Message):
    movie_list = "\n".join([f"{movie}: {link}" for movie, link in movies.items()])
    await message.reply(f"Фільми|серіали:\n\n{movie_list}", parse_mode=ParseMode.HTML)

# Обробник команди /rate
@dp.message_handler(commands=['rate'])
async def rate_movie(message: types.Message):
    command, movie, rating = message.text.split(' ', 2)
    if movie in movies and 1 <= int(rating) <= 10:
        user_ratings[message.from_user.id] = {movie: rating}
        await message.reply(f"Ви оцінили фільм {movie} на {rating} балів")
    else:
        await message.reply("Будь ласка, введіть назву фільму зі списку та оцінку від 1 до 10")

# Обробник команди /review
@dp.message_handler(commands=['review'])
async def review_movie(message: types.Message):
    command, movie, review = message.text.split(' ', 2)
    if movie in movies:
        user_reviews[message.from_user.id] = {movie: review}
        await message.reply(f"Ви залишили відгук на фільм {movie}: {review}")
    else:
        await message.reply("Будь ласка, введіть назву фільму зі списку та ваш відгук")

# Обробник команди /list
@dp.message_handler(commands=['list'])
async def list_ratings_reviews(message: types.Message):
    ratings_reviews_list = ""
    for movie in movies:
        ratings = [user_ratings[user][movie] for user in user_ratings if movie in user_ratings[user]]
        reviews = [user_reviews[user][movie] for user in user_reviews if movie in user_reviews[user]]
        average_rating = sum(ratings) / len(ratings) if ratings else "немає оцінки"
        reviews_text = "\n".join(reviews) if reviews else "немає відгуків"
        ratings_reviews_list += f"{movie}:\nОцінка: {average_rating}\nВідгуки:\n{reviews_text}\n\n"
    await message.reply(f"Оцінки та відгуки:\n\n{ratings_reviews_list}", parse_mode=ParseMode.HTML)

# Обробник команди /end
@dp.message_handler(commands=['end'])
async def end_interaction(message: types.Message):
    await message.reply("Спасибі за використання бота! Мирного рішення не буде. Ось список людей:\n\n" + "\n".join(people))

# Запускаємо бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
