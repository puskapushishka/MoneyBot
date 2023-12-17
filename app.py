import telebot
import time
from TOKEN import TOKEN
from config import val
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)  # create bot


def polling():  # the bot launch function
    bot.polling()


# command processing
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


# processing messages and sending a response + error handling
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        us_input = message.text.split(' ')
        if len(us_input) > 3:
            raise ConvertionException('Слишком много параметров.')
        elif len(us_input) < 3:
            raise ConvertionException('Слишком мало параметров.')

        base, quote, amount = us_input
        total = CryptoConverter.get_price(base, quote, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{amount} {val[base]} = {total} {val[quote]}'
        bot.send_message(message.chat.id, text)


try:
    polling()
except Exception:
    print("an error in the bot's operation")
    time.sleep(60)
    print("re-launch")
    polling()
