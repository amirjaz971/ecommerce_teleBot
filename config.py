import logging
import telebot

API_TOKEN = '7041414535:AAGj_6rSBT0UnzYGmycTF3IYRfLy8abczLM'

admins = [245324256]  

def setup_logging_config():
    logging.basicConfig(filename='project.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

bot = telebot.TeleBot(API_TOKEN, num_threads=10)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'aseman10',
    'database': 'ecommercebotdb'
}