import telebot
import requests
from io import BytesIO

bot = telebot.TeleBot('6537004211:AAFrz9r8hd-vYMmwdhoOzsolA3ZeEcaE3j8')

@bot.message_handler(commands=['start'])
def handle_start(message):
    user = message.from_user
    bot.send_message(message.chat.id, f"Привет, {user.first_name}! Отправь мне фотографию полки с товарами.")

# Обработчик фотографии полки
@bot.message_handler(content_types=['photo'])
def handle_shelf_photo(message):
    user = message.from_user
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_path}'
    response = requests.get(file_url)

    if response.status_code == 200:
        image_data = BytesIO(response.content)
        response_from_server = send_shelf_image_to_server(image_data)

        bot.send_message(message.chat.id, text=format_shelf_info(response_from_server))

        bot.send_message(message.chat.id, "Отправьте фотографию ценника интересующего товара.")

        # Теперь ожидаем фотографию ценника
        bot.register_next_step_handler(message, handle_price_tag_photo)
    else:
        bot.send_message(message.chat.id, text="Произошла ошибка при загрузке фотографии. Попробуйте еще раз.")

# Обработчик фотографии ценника
def handle_price_tag_photo(message):
    user = message.from_user
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_path}'
    response = requests.get(file_url)

    if response.status_code == 200:
        image_data = BytesIO(response.content)
        response_from_server = send_price_tag_image_to_server(image_data)

        bot.send_message(message.chat.id, text=format_price_tag_info(response_from_server))
    else:
        bot.send_message(message.chat.id, text="Произошла ошибка при загрузке фотографии. Попробуйте еще раз.")

# Функция для отправки фотографии полки на сервер
def send_shelf_image_to_server(image_data):
    try:
        server_url = "http://127.0.0.1:8000/upload_shelf"
        files = {'file': ('shelf_photo.jpg', image_data)}

        response = requests.post(server_url, files=files)

        if response.status_code == 200:
            return response.json()
        else:
            return "Произошла ошибка на сервере обработки изображения."
    except Exception as e:
        return str(e)

# Функция для отправки фотографии ценника на сервер
def send_price_tag_image_to_server(image_data):
    try:
        server_url = "http://127.0.0.1:8000/upload_price_tag"
        files = {'file': ('price_tag.jpg', image_data)}

        response = requests.post(server_url, files=files)

        if response.status_code == 200:
            return response.json()
        else:
            return "Произошла ошибка на сервере обработки изображения."
    except Exception as e:
        return str(e)

# Функция для форматирования информации о полке
def format_shelf_info(shelf_info):
    formatted_info = f"Количество товаров: {shelf_info['goods']}\n"
    formatted_info += f"Количество пропусков: {shelf_info['passes']}\n"
    formatted_info += f"Размер полки: {shelf_info['size']}\n"
    return formatted_info

# Функция для форматирования информации о ценнике
def format_price_tag_info(price_tag_info):
    formatted_info =  f"Штрихкод: {price_tag_info['barcode']}\n"
    formatted_info += f"Наименование товара: {price_tag_info['name']}\n"
    formatted_info += f"Цена: {price_tag_info['price']} руб.\n"
    formatted_info += f"Акция: {price_tag_info['promo']}\n"
    return formatted_info


# Запуск бота
bot.polling(none_stop=True)
