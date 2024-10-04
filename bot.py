import os
import random

from telebot import TeleBot
from commands import commands
from config import TOKEN

TOKEN = os.getenv('TOKEN') or TOKEN
bot = TeleBot(TOKEN)

tribes = ["Xin-xi", "Imperius", "Bardur", "Oumaji", "Kickoo", "Hoodrick", "Luxidoor", "Vengir", "Zebasi", "ΑΜi-Mο",
          "Quetzali", "Yadakk", "Aquarion", "Elyrion", "Polaris", "Cymanti"]
map_type = ["Суша", "Озёра", "Пангея", "Континенты", "Архипелаг", "Водный мир"]
map_type_weights = [3, 4, 5, 7, 2, 1]
map_size = ["Крошечная", "Малая", "Средняя", "Большая", "Огромный", "Гигантский"]


def map_size_weights_generator(count_of_players):
    match count_of_players:
        case 2:
            map_size_weights = [3, 4, 1, 0, 0, 0]
        case 3:
            map_size_weights = [3, 4, 2, 0, 0, 0]
        case 4:
            map_size_weights = [3, 4, 3, 1, 0, 0]
        case 5:
            map_size_weights = [3, 5, 4, 2, 0, 0]
        case 6:
            map_size_weights = [3, 5, 4, 2, 1, 0]
        case _:
            map_size_weights = [3, 4, 7, 3, 2, 1]
    return map_size_weights


@bot.message_handler(commands=['play'])
def config_game(message):
    bot.send_message(message.chat.id, "Введите количество игроков")
    bot.register_next_step_handler(message, get_player_count)


def get_player_count(message):
    try:
        count_of_players = int(message.text)
        if count_of_players > 16:
            bot.send_message(message.chat.id, "Максимум игроков 16")
            bot.register_next_step_handler(message, get_player_count)
        map_size_weights = map_size_weights_generator(count_of_players)
        config = ((random.choices(map_type, weights=map_type_weights)[0]) + ", "
                  + (random.choices(map_size, weights=map_size_weights)[0]))
        bot.send_message(message.chat.id, config)
        players = random.choices(tribes, k=count_of_players)
        list_of_players = ""
        for i in range(count_of_players):
            list_of_players += str(i + 1) + ": " + f"{players[i]}\n"
        bot.send_message(message.chat.id, list_of_players)
    except ValueError:
        bot.send_message(message.chat.id, "Введите число")
        bot.register_next_step_handler(message, get_player_count)


if __name__ == "__main__":
    bot.set_my_commands(commands)
    bot.infinity_polling(
        skip_pending=True,
        allowed_updates=[],
    )
