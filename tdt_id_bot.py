import telebot
from telebot import types
import datetime
import configparser
from utils.api_module import tdt_id_by_lot_size, tbtc_total_supply


config = configparser.ConfigParser()
config.read('config.ini')
bot = telebot.TeleBot(token=config["default"]["bot_token"])
buttons_per_string = 3
LOT_SIZE_LST = [0.001, 0.01, 0.1, 0.2, 0.5, 1]
COMMON_ERROR = 'error'


# MAIN MENU COMMANDS
GET_TDT_ID = '❇️ Get TDT ID'
TOTAL_SUPPLY = '💰Supply'
ABOUT      = 'ℹ️ About'
help_commands = ['start', 'help', ABOUT]
main_menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
main_menu.keyboard.clear()
main_menu.row(GET_TDT_ID, TOTAL_SUPPLY, ABOUT)


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text' and m.chat.id:
            print(f'{str(m.chat.username)} ({str(m.chat.id)}): {m.text}')


@bot.message_handler(content_types=['text'], regexp=ABOUT)
@bot.message_handler(commands=help_commands)
def to_main_menu(message):
    help_msg = '''This is simple Telegram bot to demonstrate one of the possibilities Keep Indexer (https://github.com/fedorov-m/KeepIndexer)
More information can be found on GitHub: https://github.com/c29r3/keep-tdt-id-bot
'''
    bot.send_message(message.chat.id, help_msg, disable_web_page_preview=True, reply_markup=main_menu)


def show_list_menu_generator(message: str, btn_names_list: list, command_: str):
    def divide_chunks(l, n):
        # subdivide n items in each list
        for d in range(0, len(l), n):
            yield l[d:d + n]

    kb = types.InlineKeyboardMarkup()
    buttons = []
    if len(btn_names_list) <= 0:
        return 'empty', 'empty'

    for i, value in enumerate(btn_names_list, start=1):
        message = f'Select lot size:'
        buttons.append({'text': str(value), 'callback_data': f'{command_};{value}'})

    kb.keyboard = list(divide_chunks(buttons, buttons_per_string))
    return message, kb


@bot.message_handler(content_types=['text'], regexp=GET_TDT_ID)
def select_lot_size(message):
    msg, keyboard = show_list_menu_generator(f'Select lot size:', LOT_SIZE_LST, GET_TDT_ID)
    bot.send_message(chat_id=message.chat.id, text=msg, reply_markup=keyboard)


@bot.message_handler(content_types=['text'], regexp=TOTAL_SUPPLY)
def get_total_supply(message):
    total_supply = tbtc_total_supply()
    if total_supply == "error":
        bot.send_message(chat_id=message.chat.id, text=f"Error: Can't get current total supply")
    else:
        bot.send_message(chat_id=message.chat.id, text=f'Total supply is: {total_supply}')


@bot.message_handler(func=lambda message: True)
def incorrect_command(message):
    if message.chat.id:
        bot.reply_to(message, "🙈 Command not recognized\n"
                              "Send /start to see the list of commands")


@bot.callback_query_handler(func=lambda call: True)
def callback_main(call):
    if GET_TDT_ID in str(call.data):
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"), call.from_user, call.message)
        lot_size = call.data.split(";")[1]
        tdt_id = tdt_id_by_lot_size(lot_size)
        if len(tdt_id) == 42:
            bot.send_message(chat_id=call.message.chat.id, text=f'Lot size: {lot_size}\nTDT ID: {tdt_id}')
        else:
            bot.send_message(chat_id=call.message.chat.id, text=f"❌ Can't find unused TDT ID for lot size {lot_size}")


bot.set_update_listener(listener)
bot.polling(timeout=30)
