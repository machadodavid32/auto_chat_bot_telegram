# Importações
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# States(onde vem, o que fazer e para onde ir depois)
ESCOLHER_OPCAO, LOGIN, REGISTRAR_EMAIL, REGISTRAR_SENHA, REGISTRAR_CPF = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Logar","Registrar"]]

    await update.message.reply_text("Olá! Escolha uma opção:",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))

    return ESCOLHER_OPCAO

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Digite seu e-mail",reply_markup=ReplyKeyboardRemove())
    return LOGIN

async def registrar_email(update:Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Digite seu e-mail",reply_markup=ReplyKeyboardMarkup([["🚫Cancelar Cadastro"]],one_time_keyboard=False))

    return REGISTRAR_EMAIL

async def registrar_senha(update:Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print(context.user_data)
    context.user_data['email'] = update.message.text

    await update.message.reply_text("Digite sua senha:",reply_markup=ReplyKeyboardMarkup([["🚫Cancelar Cadastro"]],one_time_keyboard=False))

    return REGISTRAR_SENHA

async def registrar_cpf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print(context.user_data)
    context.user_data["senha"] = update.message.text
    await update.message.reply_text("Digite seu CPF:",reply_markup=ReplyKeyboardMarkup([["🚫Cancelar Cadastro"]],one_time_keyboard=False))

    return REGISTRAR_CPF

async def encerrar_cadastro(update: Update,context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Processo de cadastro/login foi cancelado.",reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def finalizar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if context.user_data.get('email'):
        await update.message.reply_text(f'Cadastro Concluído! E-mail {context.user_data["email"]}, Senha: {context.user_data["email"]}, CPF: {update.message.text}')
    else:
        await update.message.reply_text(f'Logado como {update.message.text}')

    return ConversationHandler.END



# ConversationHandler(Controlador de states- definir quais funções são responsáveis por o que)
def main() -> None:
    # Criar app
    application = Application.builder().token('6932406558:AAH7XN7IhCWH0NT6LqPZ8kMUET4EBK6IOx8').build()
    # Criar as rotas de conversa
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start',start),
            CommandHandler('iniciar',start)
        ],
        states={
            ESCOLHER_OPCAO:[
                MessageHandler(filters.Regex("^(Logar)$"),login),
                MessageHandler(filters.Regex("^(Registrar)$"),registrar_email)
        
            ],
            LOGIN:[
                MessageHandler(filters.TEXT & ~filters.COMMAND, finalizar),
            ],
            REGISTRAR_EMAIL: [
                MessageHandler(filters.Regex("^(🚫Cancelar Cadastro)$"),encerrar_cadastro),
                MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_senha)
        
            ],
            REGISTRAR_SENHA:[
                MessageHandler(filters.Regex("^(🚫Cancelar Cadastro)$"),encerrar_cadastro),
                MessageHandler(filters.TEXT & ~filters.COMMAND, registrar_cpf)
        
            ],
            REGISTRAR_CPF:[
                MessageHandler(filters.Regex("^(🚫Cancelar Cadastro)$"),encerrar_cadastro),
                MessageHandler(filters.TEXT & ~filters.COMMAND, finalizar)
        
            ]
        
        },
        fallbacks=[
            CommandHandler('start',start),
            CommandHandler('iniciar',start)
        ]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
