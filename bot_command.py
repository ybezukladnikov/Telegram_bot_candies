from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
import logger


first_question, answer_yes, exit_play, choose_num_can, choose_max_num,start_play, happy_end = range(7)
temp_list = []

def start(update, _):
    logger.log(update, _)
    reply_keyboard = [['Да', 'Нет']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        f'Приветствую тебя уважаемый пользователь, {update.effective_user.first_name}!\n'
        'Хочешь ли ты поиграть в игру конфеты ',
        reply_markup=markup_key,)

    return first_question


def answer_fq(update, _):
    logger.log(update, _)
    if update.message.text == 'Нет':
        # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
        update.message.reply_text(
            'Очень жаль, приходи в следующий раз!'
            'И скажи мне хотя бы Пока)',
            reply_markup=ReplyKeyboardRemove(),
        )
        return exit_play
    else:
        # Список кнопок для ответа
        reply_keyboard = [['Бот', 'Человек']]
        # Создаем простую клавиатуру для ответа
        markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        # Начинаем разговор с вопроса

        update.message.reply_text(
            f'{update.effective_user.first_name}\n'
            'Выбери с кем ты будешь играть! '
            ,
            reply_markup=markup_key,)
        return answer_yes

def choose_mod(update, _):
    logger.log(update, _)
    if update.message.text == 'Бот':
        # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
        update.message.reply_text(
            'Отличный выбор!\n'
            'Приступаем к игре!\n'
            'Правила очень просты. Кто возмет последнюю конфету тот и проиграл!'
            'На первом этапе укажи сколько будет всего конфет!',
            reply_markup=ReplyKeyboardRemove(),
        )
    return choose_num_can

def check_num_can(update, _):
    logger.log(update, _)
    global temp_list
    try:
        num = int(update.message.text)
        if num <= 2:
            update.message.reply_text('Число конфет должно быть больше 2')
            return choose_num_can
        temp_list.append(num)

        update.message.reply_text('Все отлично. Продолжаем.\n'
                                  'Теперь напишите по сколько конфет будете брать')
        return choose_max_num

    except ValueError:
        update.message.reply_text('Вы ввели некорректное число, попробуйте снова!')
        return choose_num_can

def check_max_can(update, _):
    logger.log(update, _)
    global temp_list
    try:
        num = int(update.message.text)
        if num >temp_list[0] :
            update.message.reply_text(f'Число больше чем общее число конфет. Укажите меньшее {temp_list[0]}')
            return choose_max_num
        if num <= 2:
            update.message.reply_text('Число конефет не может быть меньше 3')
            return choose_max_num
        if not temp_list[0] % (num + 2):
            update.message.reply_text('По техническим причинам просим изменить максимальное кол. конфет, которые можно брать')
            return choose_max_num
        temp_list.append(num)
        update.message.reply_text('Все верно. Бот ходит первым.')
        if temp_list[0] < temp_list[1] + 2:
            num_cand_first_player = temp_list[0] - 1
        else:
            num_cand_first_player = temp_list[0] - (temp_list[1] + 2) * (temp_list[0] // (temp_list[1] + 2))
        update.message.reply_text(f'Bot взял {num_cand_first_player}')
        temp_list[0]-=num_cand_first_player
        update.message.reply_text(f'Осталось конфет => {temp_list[0]}, взять можно до {temp_list[1]} конфет. Сколько вы возьмете?')
        return start_play
    except ValueError:
        update.message.reply_text('Вы ввели некорректное число, попробуйте снова!')
        return choose_max_num

def main_func(update, _):
    logger.log(update, _)
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

    if temp_list[0]-num ==0:
        update.message.reply_text('К сожалению, вы проиграли.')
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
        if temp_list[0] < temp_list[1] + 2:
            num_cand_first_player = temp_list[0] - 1
        else:
            num_cand_first_player = temp_list[0] - (temp_list[1] + 2) * (temp_list[0] // (temp_list[1] + 2))

        update.message.reply_text(f'Осталось конфет => {temp_list[0]} Bot взял {num_cand_first_player}')
        temp_list[0] -= num_cand_first_player
        if temp_list[0]<temp_list[1]:
            update.message.reply_text(
                f'Осталось конфет => {temp_list[0]}, взять можно до {temp_list[0]} конфет. Сколько вы возьмете?')
        else:
            update.message.reply_text(
            f'Осталось конфет => {temp_list[0]}, взять можно до {temp_list[1]} конфет. Сколько вы возьмете?')
        return start_play




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


