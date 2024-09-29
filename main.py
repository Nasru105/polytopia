import random

from telebot import TeleBot

from commands import commands
from config import BOT_TOKEN

bot = TeleBot(BOT_TOKEN)

tribes = ["Xin-xi", "Imperius", "Bardur", "Oumaji", "Kickoo", "Hoodrick", "Luxidoor", "Vengir", "Zebasi", "ΑΜi-Mο",
          "Quetzali", "Yadakk",
          "Aquarion", "Elyrion", "Polaris", "Cymanti"]
map_type = ["Суша", "Озёра", "Пангея", "Континенты", "Архипелаг", "Водный мир"]
map_type_weights = [2, 3, 4, 6, 2, 1]
map_size = ["Крошечная", "Малая", "Средняя", "Большая", "Огромный", "Гигантский"]
map_size_weights = [2, 3, 6, 3, 2, 1]


@bot.message_handler(commands=['play'])
def config_game(message):
    bot.send_message(message.chat.id, "Введите количество игроков")
    bot.register_next_step_handler(message, get_player_count)

def get_player_count(message):
    try:
        count_of_players = int(message.text)
        config = ((random.choices(map_type, weights=map_type_weights)[0]) + ", "
                  + (random.choices(map_size, weights=map_size_weights)[0]))
        bot.send_message(message.chat.id, config)
        players = random.choices(tribes, k=count_of_players)
        list_of_players = ""
        for player in range(count_of_players):
            list_of_players += str(player + 1) + ": " + f"{players[player]}\n"
        bot.send_message(message.chat.id, list_of_players)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")
        bot.register_next_step_handler(message, get_player_count)  # Повторная попытка

if __name__ == "__main__":
    bot.set_my_commands(commands)
    bot.infinity_polling(
        skip_pending=True,
        allowed_updates=[],
    )