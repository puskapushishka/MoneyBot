import telebot
import time
from TOKEN import TOKEN
from config import val
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


def polling():
    bot.polling()


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы начать введите команду в следующем формате:\n\
<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n\
Например:\n\
доллар евро 7.5\n\n\
Показать список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in val.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        us_input = message.text.split(' ')
        if len(us_input) > 3:
            raise ConvertionException('Слишком много параметров.')
        elif len(us_input) < 3:
            raise ConvertionException('Слишком мало параметров.')

        have, want, amount = us_input
        total = CryptoConverter.convert(have, want, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{amount} {val[have]} = {total} {val[want]}'
        bot.send_message(message.chat.id, text)


try:
    polling()
except Exception:
    print("Скорее всего разрыв соединения")
    time.sleep(60)
    polling()
