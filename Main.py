from aiogram import Bot, Dispatcher, executor, types
from src.Game import Game
from src.Player import Player
import random
from src import Globals
import emoji
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from sys import argv

script, token  = argv
Globals.API_TOKEN = token

bot = Bot(token=Globals.API_TOKEN)
dp = Dispatcher(bot)

async def start_game(our_id, opp_id):
    await bot.send_message(our_id, "Начинаем!", 
                             reply_markup=ReplyKeyboardRemove())
    await bot.send_message(opp_id, "Начинаем!", 
                             reply_markup=ReplyKeyboardRemove())
    pl1 = Globals.all_ides[our_id]
    pl2 = Globals.all_ides[opp_id]
    tmp = random.randint(0, 100) % 2
    str1 = ""
    str2 = ""
    if tmp == 0:
        pl1.set_role('X')
        pl2.set_role('O')
        str1 = Globals.msg_you_are_cross
        str2 = Globals.msg_you_are_zero
    else:
        pl1.set_role('O')
        pl2.set_role('X')
        str2 = Globals.msg_you_are_cross
        str1 = Globals.msg_you_are_zero
    new_game = Game(bot, pl1, pl2, tmp + 1)
    pl1.set_game(new_game)
    pl2.set_game(new_game)
    pl1.set_status('game')
    pl2.set_status('game')
    inline_kb_full_pl1 = InlineKeyboardMarkup(row_width=3)
    inline_kb_full_pl2 = InlineKeyboardMarkup(row_width=3)
    for i in range(Globals.size):
        row = []
        row2 = []
        for j in range(Globals.size):
            row.append(InlineKeyboardButton(emoji.emojize("⬜"),
                    callback_data=('btn' + str(i) + str(j))))
            row2.append(InlineKeyboardButton(emoji.emojize("⬜"),
                    callback_data=('btn' + str(i) + str(j))))
        inline_kb_full_pl1.row(row[0], row[1], row[2])
        inline_kb_full_pl2.row(row2[0], row2[1], row2[2])
    pl1_last = await bot.send_message(our_id, str1, 
                                      reply_markup=inline_kb_full_pl1)
    pl2_last = await bot.send_message(opp_id, str2, 
                                      reply_markup=inline_kb_full_pl2)
    pl1.set_last(pl1_last.message_id)
    pl2.set_last(pl2_last.message_id)
    
async def set_buttons(id, message, msg):
    btn = KeyboardButton(text=message)
    btn2 = KeyboardButton(text=Globals.btn_exit)
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(btn)
    kb.add(btn2)
    await bot.send_message(id, msg, reply_markup=kb)
    
async def main_menu(id):
    await set_buttons(id, Globals.btn_new_game, "Начните новую игру!")
    
async def only_exit(id, msg):
    btn2 = KeyboardButton(text=Globals.btn_exit)
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(btn2)
    await bot.send_message(id, msg, reply_markup=kb)


async def ready(message: types.Message):
    our_id = message.from_user.id
    if Globals.all_ides[our_id].get_status() != 'connect':
        await message.reply("Непон")
    opp_id = Globals.all_ides[our_id].get_opponent()
    if Globals.all_ides[our_id].get_status() == 'connect' and \
       Globals.all_ides[opp_id].get_status() == 'connect':
        Globals.all_ides[our_id].set_status('ready')
        await only_exit(our_id, Globals.msg_wait_opponent)
    elif Globals.all_ides[our_id].get_status() == 'connect':
        Globals.all_ides[our_id].set_status('ready')
    if Globals.all_ides[our_id].get_status() == 'ready' and \
            Globals.all_ides[opp_id].get_status() == 'ready':
        await start_game(our_id, opp_id)


async def get_id(message: types.Message, id: int):
    str_id = str(id)
    if Globals.all_ides[message.from_user.id].get_status() != 'waitid':
        await message.answer(Globals.msg_bad_new_game)
        return
    if str_id.isdigit():
        opp_id = int(str_id)
        our_id = message.from_user.id
        if opp_id in Globals.all_ides.keys() and opp_id != our_id:
            print("Игрок " + str(our_id) + " ввел противника " + str(opp_id))
            if Globals.all_ides[opp_id].get_status() == 'init' or \
                    Globals.all_ides[opp_id].get_status() == 'waitid':
                Globals.all_ides[our_id].set_status('wait')
                Globals.all_ides[our_id].set_opponent(opp_id)
                await only_exit(our_id, Globals.msg_wait_connection)
            elif Globals.all_ides[opp_id].get_status() == 'wait' and \
                    Globals.all_ides[opp_id].get_opponent() == our_id:
                Globals.all_ides[our_id].set_status('connect')
                Globals.all_ides[opp_id].set_status('connect')
                Globals.all_ides[our_id].set_opponent(opp_id)
                await set_buttons(our_id, "Готов!", Globals.msg_wait_ready)
                await set_buttons(opp_id, "Готов!", Globals.msg_wait_ready)
                print('connect', our_id, opp_id)
            else:
                await message.answer(Globals.msg_busy_opponent)
                print("Игрок " + str(opp_id) + " уже занят")
                await main_menu(our_id)
        else:
            if opp_id != our_id:
                await message.answer(Globals.msg_bad_id)
                print(str(opp_id) + " такого id не существует")
                await main_menu(our_id)
            else:
                await message.answer(Globals.msg_self_id)
                print(str(opp_id) + " самоигра(")
                await main_menu(our_id)
    else:
        await message.answer(Globals.msg_not_id)
        await main_menu(our_id)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    curr_id = message.from_user.id
    curr_name = message.from_user.first_name
    for player in Globals.all_players:
        if curr_id == player.get_id():
            await set_buttons(curr_id, Globals.btn_new_game, Globals.cmd_welcome)
            return
    await set_buttons(curr_id, Globals.btn_new_game, Globals.cmd_welcome)
    print("Игрок " + str(curr_id) + " зарегистрировался")
    new_player = Player(curr_id, curr_name)
    with open('src/data.txt', 'a') as f:
        f.write(str(curr_id) + '^' + curr_name + '\n')
    Globals.all_players.append(new_player)
    Globals.all_ides.update([(curr_id, new_player)])
    
    
async def update_field(player, opponent, game):
    inline_kb_full_pl1 = InlineKeyboardMarkup(row_width=3)
    inline_kb_full_pl2 = InlineKeyboardMarkup(row_width=3)
    curr_id = player.get_id()
    await bot.delete_message(curr_id, player.get_last())
    await bot.delete_message(opponent.get_id(), opponent.get_last())
    for i in range(Globals.size):
        row = []
        row2 = []
        for j in range(Globals.size):
            row.append(InlineKeyboardButton(game.get_cell_image(i, j),
                    callback_data=('btn' + str(i) + str(j))))
            row2.append(InlineKeyboardButton(game.get_cell_image(i, j),
                    callback_data=('btn' + str(i) + str(j))))
        inline_kb_full_pl1.row(row[0], row[1], row[2])
        inline_kb_full_pl2.row(row2[0], row2[1], row2[2])
    opp_msg = ''
    if player.get_role() == 'O':
        opp_msg = Globals.msg_cross_turn
    else:
        opp_msg = Globals.msg_zero_turn
    pl1_last = await bot.send_message(curr_id, 
                                      Globals.msg_opponent_turn, 
                                      reply_markup=inline_kb_full_pl1)
    pl2_last = await bot.send_message(player.get_opponent(), opp_msg, 
                                      reply_markup=inline_kb_full_pl2)
    player.set_last(pl1_last.message_id)
    opponent.set_last(pl2_last.message_id)
    


async def win_game(win_id, lose_id):
    winner = Globals.all_ides[win_id]
    loser = Globals.all_ides[lose_id]
    await bot.delete_message(win_id, winner.get_last())
    await bot.delete_message(lose_id, loser.get_last())
    await bot.send_message(win_id, Globals.msg_win)
    await bot.send_message(lose_id, 
                           Globals.msg_lose.format(winner.get_name()))
    winner.destruct()
    loser.destruct()
    await main_menu(win_id)
    await main_menu(lose_id)
    
async def draw_game(id_1, id_2):
    pl1 = Globals.all_ides[id_1]
    pl2 = Globals.all_ides[id_2]
    await bot.delete_message(id_1, pl1.get_last())
    await bot.delete_message(id_2, pl2.get_last())
    await bot.send_message(id_1, Globals.msg_draw)
    await bot.send_message(id_2, Globals.msg_draw)
    pl1.destruct()
    pl2.destruct()
    await main_menu(id_1)
    await main_menu(id_2)

@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    code = callback_query.data[3:]
    x = int(code[0])
    y = int(code[1])
    curr_id = callback_query.from_user.id
    msg_id = callback_query.message.message_id
    player = Globals.all_ides[curr_id]
    if msg_id != player.get_last():
        return
    if Globals.all_ides[curr_id].get_status() != 'game':
        await only_exit(callback_query.from_user.id, Globals.msg_what)
        return
    game = player.get_game()
    result = game.process_press(x, y, player)
    if result == 'ok':
        opponent = Globals.all_ides[player.get_opponent()]
        await update_field(player, opponent, game)
        return
    if result == 'Не твой ход':
        await only_exit(curr_id, Globals.msg_not_your_turn)
        return
    if result == 'Пчел тут занято':
        await only_exit(curr_id, Globals.msg_busy_cell)
        return
    if result == 'win':
        await win_game(curr_id, Globals.all_ides[curr_id].get_opponent())
        return
    if result == 'draw':
        await draw_game(curr_id, Globals.all_ides[curr_id].get_opponent())
        return
    
    await bot.send_message(curr_id, Globals.msg_what)
    return


@dp.message_handler(commands=['my_id'])
async def my_id(message: types.Message):
    await message.reply("Ваш id: " + str(message.from_user.id))


@dp.message_handler(commands=['exit'])
async def exit(message: types.Message):
    our_id = message.from_user.id
    if Globals.all_ides[our_id] == 'init' or Globals.all_ides[our_id] == 'wait' or \
            Globals.all_ides[our_id] == 'waitid':
        Globals.all_ides[our_id].destruct()
        await set_buttons(our_id, Globals.btn_new_game, "Начните новую игру!")
    else:
        opp_id = Globals.all_ides[our_id].get_opponent()
        if opp_id is not None:
            if Globals.all_ides[opp_id].get_status() == 'connect' or \
                    Globals.all_ides[opp_id].get_status() == 'game':
                Globals.all_ides[opp_id].destruct()
                await set_buttons(opp_id, Globals.btn_new_game, Globals.msg_interrupt_game)
        Globals.all_ides[our_id].destruct()
        await set_buttons(our_id, Globals.btn_new_game,  Globals.msg_end_game)


@dp.message_handler(commands=['help'])
async def help_msg(message: types.Message):
    await message.answer(Globals.cmd_help)
    
@dp.message_handler(commands=['info'])
async def help_msg(message: types.Message):
    await message.answer(Globals.cmd_info)
    
@dp.message_handler(commands=['commands'])
async def help_msg(message: types.Message):
    await message.answer(Globals.cmd_commands)
    

@dp.message_handler()
async def messages(message: types.Message):
    our_id = message.from_user.id
    player = Globals.all_ides[our_id]
    if message.text == Globals.btn_new_game and \
            (player.get_status() == 'init' or player.get_status() == 'wait'):
        await only_exit(our_id, "Введите id противника")
        print("Игрок " + str(our_id) + " начал новую игру")
        Globals.all_ides[our_id].set_status("waitid")
        return
    if message.text == 'Готов!':
        await ready(message)
        print("Игрок " + str(our_id) + " готов к началу игры")
        return
    if message.text == 'Выйти':
        print("Игрок " + str(our_id) + " вышел")
        await exit(message)
        return
    if message.text.isdigit():
        await get_id(message, int(message.text))
        return
    
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
