from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

# Fluxo de criação para bot que responde a comandos:

# Criar uma função que faz algo quando um x comando é digitado
async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Bem vindo ao Bot do David')

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
    application.add_handler(CommandHandler('horas', horas))
    # Reagir a palavras
    application.add_handler(MessageHandler(filters.COMMAND, nao_registrado))
    application.add_handler(MessageHandler(filters.TEXT, responder))
    # Ligar o monitoramento de comando
    application.run_polling()
