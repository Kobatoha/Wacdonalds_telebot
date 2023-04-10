import telebot
import schedule
import time
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup as b


API_KEY = '5850863234:AAHtitqv5BpUC4eDtlGN1EmLpzakuDVsQpM'

# test chat_id

chat_id = '-1001965094555'
URL = 'http://kobatoha.beget.tech/respawn/'


def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    respawntimes = soup.find_all('p', class_='content')
    return [c.text for c in respawntimes]


def send_respawn_notification(name, chat_id):
    bot = telebot.TeleBot(API_KEY)
    message = f"{name} через 15 минут"
    bot.send_message(chat_id, message)


def update_time():
    list_of_times = parser(URL)
    print(list_of_times)
    return list_of_times


list_of_times = parser(URL)


# Отправляем сообщение со временем до респа каждого босса
def check_respawn():
    print(datetime.now().strftime('%H:%M'))
    list_of_times = update_time()
    for time_str in list_of_times:
        words = time_str.split()
        name = ' '.join(words[:words.index('появится')])
        time_boss = words[-1]
        hour_boss, minute_boss = map(int, time_boss.split(':'))
        boss_time = datetime.now().replace(hour=hour_boss, minute=minute_boss, second=0, microsecond=0)
        boss_time_minus_10 = boss_time - timedelta(minutes=15)
        schedule_time_str = boss_time_minus_10.strftime('%H:%M')

        if datetime.now() <= boss_time_minus_10:
            schedule.every().day.at(schedule_time_str).do(send_respawn_notification, name=name, chat_id=chat_id)


update_time()
check_respawn()


def solo_boss_and_kuka():
    now = datetime.now().strftime('%H:%M')
    solo_boss_time = ['08:45', '10:45', '12:45', '14:45', '16:45', '18:45', '20:45', '22:45', '00:45']
    if now in solo_boss_time:
        bot = telebot.TeleBot(API_KEY)
        message = f'Кука - 5 минут, брат, а соло РБ через 15 минут'
        bot.send_message(chat_id, message)


def solo_boss():
    now = datetime.now().strftime('%H:%M')
    solo_boss_time = ['08:55', '10:55', '12:55', '14:55', '16:55', '18:55', '20:55', '22:55', '00:55']
    if now in solo_boss_time:
        bot = telebot.TeleBot(API_KEY)
        message = f'Cоло РБ через 5 минут'
        bot.send_message(chat_id, message)


def zachistka():
    print(datetime.now().strftime('%H:%M'))
    message = f'Сегодня воскресенье, заберите зачистку'
    bot = telebot.TeleBot(API_KEY)
    bot.send_message(chat_id, message)


def olimpiada():
    print(datetime.now().strftime('%H:%M'))
    message = f'Олимп через 15 минут'
    bot = telebot.TeleBot(API_KEY)
    bot.send_message(chat_id, message)


def hellbound():
    print(datetime.now().strftime('%H:%M'))
    message = f'залетаем на ХБ через 10 минут'
    bot = telebot.TeleBot(API_KEY)
    bot.send_message(chat_id, message)

schedule.every(3).hours.do(update_time)
schedule.every(3).hours.do(check_respawn)
schedule.every().hour.at(':55').do(solo_boss)
schedule.every().sunday.at('23:45').do(zachistka)
schedule.every().monday.at('21:15').do(olimpiada)
schedule.every().tuesday.at('21:15').do(olimpiada)
schedule.every().wednesday.at('21:15').do(olimpiada)
schedule.every().thursday.at('21:15').do(olimpiada)
schedule.every().friday.at('21:15').do(olimpiada)
schedule.every().saturday.at('09:50').do(hellbound)


while True:
    schedule.run_pending()
    time.sleep(1)
