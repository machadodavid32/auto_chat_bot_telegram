from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

# Fluxo de criação para bot que responde a comandos:

# Criar uma função que faz algo quando um x comando é digitado
async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    horario_atual = datetime.now().strftime("%H:%M:%S")
    keyboard = [
        [
            InlineKeyboardButton("Vagas Restantes", callback_data="Restam 10 vagas"),
            InlineKeyboardButton("Horário Atual", callback_data=f"O horário atual é {horario_atual}")
        ],
        [
            InlineKeyboardButton("Sair", callback_data="Você escolheu sair")
        ],
        [
            InlineKeyboardButton("Exibir plano atual", callback_data=f"O ano atual é: {datetime.now().year}")
        ]
    ]
    
    replykeyboard = InlineKeyboardMarkup(keyboard)        
    await update.message.reply_text('Selecione uma opção:', reply_markup=replykeyboard )
    
    
async def monitorador_de_respostas(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query        
    await query.answer()
    await query.edit_message_text(text=f"Opção escolhida: {query.data}")

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Para iniciar o bot, digite /iniciar ou /start')

async def horas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    horario_atual = datetime.now().strftime('%H:%M:%S')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Horario de agora: {horario_atual}')

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() in ('olá', 'oi', 'bom dia', 'tudo bem?'):
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text='Seja bem vindo a este atendimento', reply_to_message_id=update.message.id)
        
    elif update.message.text.lower() in ('horários', 'horário', 'agendar', 'agendamento', 'agenda', 'marcar'):
        agenda = 'Horário de funcionamento é de segunda a sexta-feira'
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=agenda, reply_to_message_id=update.message.id)

async def nao_registrado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Este comando não é válido')        
    
if __name__ == '__main__':
    application = ApplicationBuilder().token('6932406558:AAH7XN7IhCWH0NT6LqPZ8kMUET4EBK6IOx8').build()
    # Registrar um handler de comandos(classe que observa que x comando foi digitado)
    application.add_handler(CommandHandler('iniciar', iniciar))
    application.add_handler(CommandHandler('start', iniciar))
    application.add_handler(CommandHandler('horas', horas))
    application.add_handler(CommandHandler('ajuda', ajuda))
    application.add_handler(CallbackQueryHandler(monitorador_de_respostas))
    # Reagir a palavras
    application.add_handler(MessageHandler(filters.COMMAND, nao_registrado))
    application.add_handler(MessageHandler(filters.TEXT, responder))
    # Ligar o monitoramento de comando
    application.run_polling()
