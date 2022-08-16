from bot_comands import *


def start_button():
    bot = Bot(token=TOKEN)
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    help_handler = CommandHandler('help', help)
    start_handler = CommandHandler('start', start)
    cl_start_handler = CommandHandler('close', cl_start)

    conv_handler_pvsbot = ConversationHandler(
        entry_points=[CommandHandler('play', p_vs_bot)],
        states={
            FIRST_P: [MessageHandler(Filters.text & ~Filters.command, first_p)],
            WORD_LEN: [MessageHandler(Filters.text & ~Filters.command, word_len)],
            PLAYER_TURN: [MessageHandler(Filters.text & ~Filters.command, player_turn)],
            PLAYER_GUESS: [MessageHandler(Filters.text & ~Filters.command, player_guess)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # message_handler = MessageHandler(Filters.text, message)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(cl_start_handler)

    dispatcher.add_handler(conv_handler_pvsbot)


    # dispatcher.add_handler(message_handler)
    dispatcher.add_handler(unknown_handler)

    print('server started')
    updater.start_polling()
    updater.idle()
