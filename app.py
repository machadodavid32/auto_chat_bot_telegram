from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from telegram import Update
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

# Fluxo de criação para bot que responde a comandos:

# Criar uma função que faz algo quando um x comando é digitado
async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Bem vindo ao Bot do David')

if __name__ == '__main__':
    application = ApplicationBuilder().token('6932406558:AAH7XN7IhCWH0NT6LqPZ8kMUET4EBK6IOx8').build()
    # Registrar um handler de comandos(classe que observa que x comando foi digitado)
    application.add_handler(CommandHandler('iniciar', iniciar))
    
    # Ligar o monitoramento de comando
    application.run_polling()
