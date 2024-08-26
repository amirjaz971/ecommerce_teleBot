import logging
import telebot

API_TOKEN = '7041414535:AAE46lwqg81SBPNxg6BsOO-jhQScP9BmUWQ'
Channel_cid = 'your_channel_id_here'
admins = [245324256]  

logging.basicConfig(filename='project.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

bot = telebot.TeleBot(API_TOKEN, num_threads=10)
# Define commands and message IDs

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'aseman10',
    'database': 'ecommercebotdb'
}