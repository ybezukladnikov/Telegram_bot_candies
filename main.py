import logging
import bot_command as bt
from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
from config import TOKEN
import logger

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# logger = logging.getLogger(__name__)
def cancel(update, _):
    # определяем пользователя
    # user = update.message.from_user
    # # Пишем в журнал о том, что пользователь не разговорчивый
    # logger.info("Пользователь %s отменил разговор.", user.first_name)
    # # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Как будет грустно, пиши',
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END


bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


conv_handler = ConversationHandler( # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[MessageHandler(Filters.text, bt.start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            bt.first_question: [MessageHandler(Filters.regex('^(Да|Нет)$'), bt.answer_fq)],
            bt.answer_yes:[MessageHandler(Filters.regex('^(Бот|Человек)$'), bt.choose_mod)],
            bt.choose_num_can:[MessageHandler(Filters.text, bt.check_num_can)],
            bt.choose_max_num:[MessageHandler(Filters.text, bt.check_max_can)],
            bt.start_play:[MessageHandler(Filters.text, bt.main_func)],
            bt.create_name:[MessageHandler(Filters.text, bt.check_name)],
            bt.step_first_pl:[MessageHandler(Filters.text, bt.main_step_first)],
            bt.step_second_pl:[MessageHandler(Filters.text, bt.main_step_second)],

            # PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            # LOCATION: [
            #     MessageHandler(Filters.location, location),
            #     CommandHandler('skip', skip_location),
            # ],
            bt.exit_play: [MessageHandler(Filters.text, cancel)]
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )


# del_abv_handler = CommandHandler('del_abv', bt.del_abv)
# start_handler = CommandHandler('start', bt.start)
# info_handler = CommandHandler('info', bt.info)
# message_handler = MessageHandler(Filters.text, bt.give_word)
# unknown_handler = MessageHandler(Filters.command, bt.unknown)  # /game

# dispatcher.add_handler(del_abv_handler)
# dispatcher.add_handler(start_handler)
# dispatcher.add_handler(info_handler)
dispatcher.add_handler(conv_handler)
# dispatcher.add_handler(unknown_handler)
# dispatcher.add_handler(message_handler)


print('server started')
updater.start_polling()
updater.idle()


# bt.first_question: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), bt.give_word)]

# bt.exit_play: [MessageHandler(Filters.text & ~Filters.command, bt.give_word)],