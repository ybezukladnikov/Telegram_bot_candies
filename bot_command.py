from random import randint

from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler, CallbackContext
import logger


first_question, answer_yes, exit_play, choose_num_can, choose_max_num,start_play,\
    create_name, step_first_pl, step_second_pl = range(9)
temp_list = []
list_name = []

def start(update, _):
    logger.my_log(update, CallbackContext, 'Начал игру')
    reply_keyboard = [['Да', 'Нет']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        f'Приветствую тебя уважаемый пользователь, {update.effective_user.first_name}!\n'
        'Хочешь ли ты поиграть в игру конфеты?\n'
        'Ты можешь завершить игру на любом этапе просто, нужно просто ввести команду:\n'
        '/cancel',
        reply_markup=markup_key,)

    return first_question


def answer_fq(update, _):
    if update.message.text == 'Нет':
        logger.my_log(update, CallbackContext, 'Не захотел играть.')
        # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
        update.message.reply_text(
            'Очень жаль, приходи в следующий раз!'
            'И скажи мне хотя бы Пока)',
            reply_markup=ReplyKeyboardRemove(),
        )
        return exit_play
    else:
        logger.my_log(update, CallbackContext, 'Захотел поиграть.')
        reply_keyboard = [['Бот', 'Человек']]
        # Создаем простую клавиатуру для ответа
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


        update.message.reply_text(
            f'{update.effective_user.first_name}\n'
            'Выбери с кем ты будешь играть! '
            ,
            reply_markup=markup_key,)
        return answer_yes

def choose_mod(update, _):
    if update.message.text == 'Бот':
        logger.my_log(update, CallbackContext, 'Выбрал игру с ботом.')
        # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
        update.message.reply_text(
            'Отличный выбор!\n'
            'Приступаем к игре!\n'
            'Правила очень просты. Кто возмет последнюю конфету тот и выиграл!'
            'На первом этапе укажи сколько будет всего конфет!',
            reply_markup=ReplyKeyboardRemove(),
        )
        return choose_num_can
    else:
        logger.my_log(update, CallbackContext, 'Выбрал игру с человеком.')
        update.message.reply_text(
            "Хорошо. Теперь введи через пробел имена двух игроков",
            reply_markup=ReplyKeyboardRemove(),
        )
        return create_name


def check_name(update, _):
    global list_name
    text_m = update.message.text
    try:
        name_first, name_second = text_m.split()
        if name_first == name_second:
            update.message.reply_text('Хитрый) Но я хитрее)) мы добавим первому имени 1, а второму 2))')
            name_first+='-1'
            name_second+='-2'

    except:
        update.message.reply_text('Вы ввели имена некорректно, попробуйте еще!')
        return create_name

    random_num = randint(0, 1)
    if random_num:
        list_name.append(name_first)
        list_name.append(name_second)
    else:
        list_name.append(name_second)
        list_name.append(name_first)
    logger.my_log(update, CallbackContext, f'Пользователь задал два имени {list_name[0]} и {list_name[1]} ')
    update.message.reply_text(f'Отличные имена!\n'
        f'Первым будет ходить {list_name[0]}'
        f'Приступаем к игре!\n'
        f'Правила очень просты. Кто возьмет последнюю конфету тот и выиграл!'
        f'На первом этапе укажи сколько будет всего конфет!')

    return  choose_num_can


def check_num_can(update, _):

    global temp_list
    temp_list = []
    try:
        num = int(update.message.text)
        if num <= 2:
            update.message.reply_text('Число конфет должно быть больше 2')
            return choose_num_can
        temp_list.append(num)

        update.message.reply_text('Все отлично. Продолжаем.\n'
                                  'Теперь напишите по сколько конфет будете брать')
        logger.my_log(update, CallbackContext, f'Для игры было выбрано {num} конфет')
        return choose_max_num

    except ValueError:
        update.message.reply_text('Вы ввели некорректное число, попробуйте снова!')
        return choose_num_can

def check_max_can(update, _):
    global temp_list
    global list_name
    try:
        num = int(update.message.text)
        if num >temp_list[0] :
            update.message.reply_text(f'Число больше чем общее число конфет. Укажите меньшее {temp_list[0]}')
            return choose_max_num
        if num <= 1:
            update.message.reply_text('Число конефет не может быть меньше 2')
            return choose_max_num
        if not temp_list[0] % (num + 1) and len(list_name)==0:
            update.message.reply_text('По техническим причинам просим изменить максимальное кол. конфет, которые можно брать')
            return choose_max_num
        logger.my_log(update, CallbackContext, f'Установлено максимальное кол. конфет = {num}')
        temp_list.append(num)
        if len(list_name)==0:
            update.message.reply_text('Все верно. Бот ходит первым.')
            if temp_list[0] <= temp_list[1]:
                num_cand_first_player = temp_list[0]
                logger.my_log(update, CallbackContext, f'Бот взял {num_cand_first_player} конфет')
            else:
                num_cand_first_player = temp_list[0] - (temp_list[1] + 1) * (temp_list[0] // (temp_list[1] + 1))
                logger.my_log(update, CallbackContext, f'Бот взял {num_cand_first_player} конфет')
            update.message.reply_text(f'Bot взял {num_cand_first_player}')
            temp_list[0]-=num_cand_first_player
            update.message.reply_text(f'Осталось конфет => {temp_list[0]}, взять можно до {temp_list[1]} конфет. Сколько вы возьмете?')
            return start_play
        else:
            update.message.reply_text(f'Отлично! Начинаем игру!\n'
                                      f'Сейчас конфет осталось => {temp_list[0]},\n'
                                      f'взять можно до {temp_list[1]} конфет.\n'
                                      f'{list_name[0]}, Сколько вы возьмете?')
            return step_first_pl
    except ValueError:
        update.message.reply_text('Вы ввели некорректное число, попробуйте снова!')
        return choose_max_num

def main_func(update, _):
    global temp_list
    try:
        num = int(update.message.text)
        if num > temp_list[1]:
            update.message.reply_text('Число конфет больше разрешонного. Попробуйте еще. ')
            return start_play
        if num < 1:
            update.message.reply_text('Число конфет меньше 1 попробуйте еще. ')
            return start_play
        if temp_list[0]-num <0:
            update.message.reply_text('Конфет осталось меньше, попробуйте еще. ')
            return start_play

    except ValueError:
        update.message.reply_text('Вы ввели некорректное число. Пробуйте еще.  ')
        return start_play
    logger.my_log(update, CallbackContext, f'Пользователь взял {num} конфет')
    if temp_list[0]-num <=temp_list[1]:
        update.message.reply_text(f'Осталось конфет => {temp_list[0]-num} Bot забирает последние {temp_list[0]-num}')
        update.message.reply_text('К сожалению, вы проиграли.')
        logger.my_log(update, CallbackContext, f'Пользователь проиграл')
        temp_list = []
        reply_keyboard = [['Да', 'Нет']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            f'{update.effective_user.first_name}, Хотите ли еще раз\n'
            'попытать свое счастье?)',
            reply_markup=markup_key, )


        return first_question

    else:
        temp_list[0]-=num


        num_cand_first_player = temp_list[0] - (temp_list[1] + 1) * (temp_list[0] // (temp_list[1] + 1))

        update.message.reply_text(f'Осталось конфет => {temp_list[0]} Bot взял {num_cand_first_player}')
        logger.my_log(update, CallbackContext, f'Бот взял {num_cand_first_player} конфет')
        temp_list[0] -= num_cand_first_player

        update.message.reply_text(
            f'Осталось конфет => {temp_list[0]}, взять можно до {temp_list[1]} конфет. Сколько вы возьмете?')
        return start_play

def main_step_first(update, _):
    global temp_list
    global list_name
    try:
        num = int(update.message.text)
        if num > temp_list[1]:
            update.message.reply_text('Число конфет больше разрешонного. Попробуйте еще. ')
            return step_first_pl
        if num < 1:
            update.message.reply_text('Число конфет меньше 1 попробуйте еще. ')
            return step_first_pl
        if temp_list[0]-num <0:
            update.message.reply_text('Конфет осталось меньше, попробуйте еще. ')
            return step_first_pl

    except ValueError:
        update.message.reply_text('Вы ввели некорректное число. Пробуйте еще. ')
        return step_first_pl
    logger.my_log(update, CallbackContext, f'Первый игрок взял {num} конфет')
    if temp_list[0] - num ==0:
        update.message.reply_text(f'Ура! Поздравляем {list_name[0]}, вы забрали последние конфеты\n'
                                  f'А это значит, что вы выиграли!!!')
        temp_list = []
        list_name = []
        reply_keyboard = [['Да', 'Нет']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            f'{update.effective_user.first_name}, Хотите ли еще раз\n'
            'сыграть в нашу игру?)',
            reply_markup=markup_key, )
        logger.my_log(update, CallbackContext, f'Выиграл первый игрок')
        return first_question

    temp_list[0]-=num
    update.message.reply_text(f'{list_name[0]} взял {num}')
    update.message.reply_text(
        f'Осталось конфет => {temp_list[0]}, взять можно до {temp_list[1]} конфет. {list_name[1]}, Cколько вы возьмете?')
    return step_second_pl

def main_step_second(update, _):
    global temp_list
    global list_name
    try:
        num = int(update.message.text)
        if num > temp_list[1]:
            update.message.reply_text('Число конфет больше разрешонного. Попробуйте еще. ')
            return step_first_pl
        if num < 1:
            update.message.reply_text('Число конфет меньше 1 попробуйте еще. ')
            return step_first_pl
        if temp_list[0] - num < 0:
            update.message.reply_text('Конфет осталось меньше, попробуйте еще. ')
            return step_first_pl

    except ValueError:
        update.message.reply_text('Вы ввели некорректное число. Пробуйте еще. ')
        return step_first_pl
    logger.my_log(update, CallbackContext, f'Второй игрок взял {num} конфет')
    if temp_list[0] - num == 0:
        update.message.reply_text(f'Ура! Поздравляем {list_name[1]}, вы забрали последние конфеты\n'
                                  f'А это значит, что вы выиграли!!!')
        logger.my_log(update, CallbackContext, f'Выиграл второй игрок')
        temp_list = []
        list_name = []
        reply_keyboard = [['Да', 'Нет']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            f'{update.effective_user.first_name}, Хотите ли еще раз\n'
            'сыграть в нашу игру?)',
            reply_markup=markup_key, )
        return first_question

    temp_list[0] -= num
    update.message.reply_text(f'{list_name[1]} взял {num}')
    update.message.reply_text(
        f'Осталось конфет => {temp_list[0]}, взять можно до {temp_list[1]} конфет. {list_name[0]}, Cколько вы возьмете?')
    return step_first_pl








    # while temp_list[0] > 0:
    #     print(f'Осталось конфет => {num_sweet}, взять можно до {max_sweet} конфет')
    #     if num_sweet < max_sweet + 2:
    #         num_cand_first_player = num_sweet - 1
    #     else:
    #         num_cand_first_player = num_sweet - (max_sweet + 2) * (num_sweet // (max_sweet + 2))
    #     print(f'Bot взял {num_cand_first_player}')
    #
    #     num_sweet -= num_cand_first_player
    #     if num_sweet <= 0:
    #         print(f'Поздравляем! {name_player}, вы выиграли!')
    #         break
    #     print(f'Осталось конфет => {num_sweet}, взять можно до {max_sweet}')
    #     num_cand_second_player = check_step(name_player, max_sweet)
    #     num_sweet -= num_cand_second_player
    #     if num_sweet <= 0:
    #         print(f'Поздравляем! {first_player} , вы выиграли!')
    #         break


    # Пишем в журнал пол пользователя
    # logger.info("Пол %s: %s", user.first_name, update.message.text)
    # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`

    # переходим к этапу `PHOTO`



# def start(update, context):
#     logger.log(update, context)
#     update.message.reply_text(f'Привет, {update.effective_user.first_name}!')
#     # arg = context.args
#     # if not arg:
#     #     context.bot.send_message(update.effective_chat.id, "Привет")
#     # else:
#     #     context.bot.send_message(update.effective_chat.id, f"{' '.join(arg)}")

# def del_abv(update, context):
#     arg = context.args
#     sub_string = 'абв'
#     text_new = ' '.join(filter(lambda x: sub_string not in x, arg))
#     if not arg:
#         context.bot.send_message(update.effective_chat.id, "Введите текст через пробел")
#     else:
#         context.bot.send_message(update.effective_chat.id, f"{text_new}")

# def info(update, context):
#     context.bot.send_message(update.effective_chat.id,
#                              """Доступны следующие команды:
#                              /start - эхобот, повторяет всё сказанное через пробел,
#                              /info - информация,
#                              /add - добавить задачу""")

# def first_question1(update, context):
#     text = update.message.text
#     if text.lower() == 'привет':
#         context.bot.send_message(update.effective_chat.id, 'Привет..')
#     else:
#         context.bot.send_message(update.effective_chat.id, 'я тебя не понимаю')





# def unknown(update, context):
#     comand = update.message.text
#     joke='Нет такой команды'
#     if comand == '/modern': joke = anecAPI.modern_joke()
#     elif comand == '/sovet': joke = anecAPI.soviet_joke()
#     elif comand == '/random':joke = anecAPI.random_joke()
#     context.bot.send_message(update.effective_chat.id, joke)

# def give_word(update, context):
#     word = update.message.text
#     if "бар" in word:
#         joke = '''Белый медведь заходит в паб и говорит бармену:
#                 - Дайте мне виски и... кока-колу.
#                 - А почему такая пауза? - спрашивает бармен.
#                 - Это всё, что вас удивляет? - с обидой говорит медведь.'''
#         context.bot.send_message(update.effective_chat.id, joke)
#         return joke
#     elif "пика" in word:
#         context.bot.send_message(update.effective_chat.id, 'Твой пика тебе очень сильно любит и скучает!')
#         return word
#     context.bot.send_message(update.effective_chat.id, 'Вы, как всегда, правы, милорд')


