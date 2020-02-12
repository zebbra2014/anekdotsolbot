import telebot
import requests
import bs4
import time
import sqlite3
import re

# Токен который выдает @botfather
token = 'ваштокен'
# Адрес телеграм канала, начинается с @
CHANNEL_NAME = '@имябота'

bot = telebot.TeleBot(token)
conn = sqlite3.connect('mydb.sqlite')
cursor = conn.cursor()

# Создаём файл базы данных, если его еще нет
try:
    cursor.execute('''CREATE TABLE IF NOT EXISTS anekdots (anekdot longtext)''')
except:
    pass

# Функция получающая с интернета список анекдотов
def getanekdot():
    z=[]
    s=requests.get('http://anekdotme.ru/random')
    b=bs4.BeautifulSoup(s.text, "html.parser")
    p=b.select('.anekdot_text')
    for x in p:        
        s=(x.getText().strip())
        reg = re.compile('[^0-9a-zA-Zа-яА-Я .:,!-—()_ ЁёьЬъЪ\n\r\t]')
        s=reg.sub('', s)
        z.append(s)
    return z
	
# Функция, которая принимает список сообщений, проверяет их наличие в БД
# и если их там нет, то постит их в телеграм канал, а потом записывает в БД
def postarticles(mas):
    global cursor
    global conn
    global bot
    for news in mas:
        cursor.execute('SELECT anekdot FROM anekdots WHERE anekdot = ?', (news,))
        row = cursor.fetchone()
        if row is None:
            cursor.execute('INSERT INTO anekdots (anekdot) VALUES (?)', (news,))
            conn.commit()
            print(news+'\n')
            bot.send_message(CHANNEL_NAME, news)
            time.sleep(2)
            
# Получаем список анекдотов
m=getanekdot()
# Постим ранее не встречавшиеся анекдоты в телеграм канал
postarticles(m)

# Закрываем соединение с БД
cursor.close()
conn.close()
