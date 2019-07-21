import pyowm
import telebot
import random

owm = pyowm.OWM('API', language='ru')
bot = telebot.TeleBot('Token')

@bot.message_handler(commands=['command1', 'command2'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Введите название города/страны на русском или английском, чтобы узнать погоду')

@bot.message_handler(content_types=['text'])
def send_echo(message):
    try:
        observation = owm.weather_at_place(message.text)
        w = observation.get_weather()
        temp = w.get_temperature('celsius')['temp']

        answer = 'В городе ' + str(message.text) + ' ' + w.get_detailed_status() + '\n'
        answer += 'Температура сейчас в районе ' + str(temp) + '\n'

        if temp <= 0:
            answer += random.choice(
                ['Одевайся тепло, на улице холодно, идиот',
                 'На улице меньше 0, лучше не выходи на улицу',
                 'Если ты решил прогуляться на улице, то оденься как будто на северный полюс',]
            )
        elif 0 < temp <= 10:
            answer += random.choice(
                ['Холодновато, оденься потеплее, мазафака',
                 'Срочно одевай штаны и куртку потеплей, если ты не дебил',
                 'Тепло - значит ты умный, будь умным и одень куртку']
            )
        elif 10 < temp <= 20:
            answer += random.choice(
                ['Тепло, но лучше подстраховаться, одень что-то с длинным рукавом',
                 'На улице тепло, но в шортах будет холодновато, оденься чуть теплее',
                 'Тепленько, но оденься, как мама говорит, то есть штаны и куртка']
            )
        else:
            answer += random.choice(
                ['Жара, можешь идти в шортах',
                 'Что-то жарко сегодня, одень что-то легкое',
                 'Раз на улице так тепло, то лучше пойти на улицу в футболке и шортах']
            )
    except pyowm.exceptions.api_response_error.NotFoundError:
        answer = 'такой страны/города нет, введите на другом языке или идите нахер'
    except:
        answer = 'Неизвестная ошибка'

    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
