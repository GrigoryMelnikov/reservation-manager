import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.ext.filters import CONTACT
import csv
import asyncio
from config import bot_token
from DB_connector import postgres_exe
from functions import phone_validation

async def verify_user_token(token) -> bool:
    if len(postgres_exe("select * from inv_payed_customers where telegram_token='{}'".format(token))) > 0:
        return True
    else:
        return False


async def add_user(token, user_id):
    postgres_exe("insert into inv_telegram_users(telegram_user_id, telegram_token) values( '{}','{}')".format(user_id, token), True)


async def verify_user_telegram(user_id):
    if len(postgres_exe("select * from inv_telegram_users where telegram_user_id='{}'".format(user_id))) > 0:
        return True
    else:
        return False


# Define a function to handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    args = context.args
    user_id = update.effective_user.id
    if args:
        token = args[0]
        if await verify_user_token(token):
            await add_user(token, user_id)
            await update.message.reply_text('Welcome! Please send your contacts.')
    else:
        await update.message.reply_text('Welcome! Please provide your authentication token or buy our service.')


async def group_change(update: Update, context: CallbackContext) -> None:
    group_name = context.args
    user_id = update.effective_user.id
    if await verify_user_telegram(user_id):
        postgres_exe('inset into inv_active_group(telegram_user_id, group_name) values({1},{2});'.format(user_id, group_name))
        await update.message.reply_text('Active group set to {}.'.format(group_name))
    else:
        await update.message.reply_text("You are not authorized!")


# Define a function to handle received contact files
async def receive_contact(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    contact = update.message.contact
    if str(contact.last_name) != 'None':
        full_name = str(contact.first_name) + ' ' + str(contact.last_name)
    else:
        full_name = str(contact.first_name)
    if await verify_user_telegram(user_id):
        phone_data = phone_validation(contact.phone_number)
        if phone_data[1]:
            if postgres_exe("insert into inv_contacts(telegram_user_id, tel_number, full_name) values('{}','{}','{}');"
                                    .format(user_id, phone_data[0], full_name), True):
                await update.message.reply_text('Contact {} added.'.format(full_name))
            else:
                await update.message.reply_text('Operation failed, please try again later.')
        else:
            await update.message.reply_text('Phone number of contact {}, is invalid'.format(full_name))
    else:
        await update.message.reply_text("You are not authorized!")


# Run the Bot
async def run_application():
    await application.run_polling()


nest_asyncio.apply()
# Create the Application and pass it your bot's token
application = Application.builder().token(bot_token).build()

# Register the command handler and the contact handler
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('group', group_change))
application.add_handler(MessageHandler(CONTACT, receive_contact))


# Run the Bot using asyncio.run()
if __name__ == '__main__':
    asyncio.run(run_application())
