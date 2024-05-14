
TOKEN = "7107513022:AAEGIY1qKvWmF0L_h9nsznRRAR9uavykb4Y"

import subprocess
import os
import sys

from flask import Flask, jsonify, render_template

# Import FastAPI and related dependencies
from fastapi import FastAPI
from flask import jsonify, render_template
from uvicorn import Config, Server

# Shared memory for process management
sys.SharedMemory = {}
sys.SharedMemory["process"] = None
sys.SharedMemory["is_process_running"] = False


# Specify the new working directory path
SERVER_working_directory = os.path.join(os.getcwd(), "MAIN")
os.chdir(SERVER_working_directory)
print(os.getcwd())

# Function to execute shell commands
def exe(cmd):
    subprocess.Popen(cmd, shell=True)

# Function to start the FastAPI server
def start_server():
    if sys.SharedMemory["is_process_running"]:
        print("Already a process is running")
        return False
    try:
        exe("uvicorn server:app --host 0.0.0.0 --port 5000 --ssl-keyfile /home/ubuntu/MAIN/privkey.pem --ssl-certfile /home/ubuntu/MAIN/fullchain.pem")
        sys.SharedMemory["is_process_running"] = True
        return True
    except Exception as e:
        print(f"Error starting FastAPI app: {e}")
        return False

# Function to stop the FastAPI server
def stop_server():
    try:
        exe("sudo pkill -f 'uvicorn.*server:app'")
    except:
        pass
    if sys.SharedMemory["is_process_running"]:
        try:
            sys.SharedMemory["is_process_running"] = False
            return True
        except Exception as e:
            print(f"Error stopping FastAPI app: {e}")
            return False
    else:
        return False


import time
import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ["Start Server", "Stop Server"],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    context.user_data["data"] = []
    await update.message.reply_text(
        "Welcome Jay!",
        reply_markup=markup,
    )

    return CHOOSING


async def start_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    # context.user_data["choice"] = text
    await update.message.reply_text(f"wait boss!")

    responce_text = ""
    if(text == "Start Server"):
        if sys.SharedMemory["process"] is None or sys.SharedMemory["process"].poll() is not None:
            if(start_server()):
                responce_text = "Done Boss!!"
            else:
                responce_text = "Failed Boss!!"
        else:
            responce_text = "Server is already running boss!"
    elif(text == "Stop Server"):
        if(stop_server()):
            responce_text = "Done Boss!!"
        else:
            responce_text = "Failed Boss!!"

    await update.message.reply_text(responce_text)

    return CHOOSING


async def normal_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    text = update.message.text
    context.user_data["data"].append(text)
    
    await update.message.reply_text("Stored")

    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    context.user_data

    await update.message.reply_text(
        "Here is the data : "+(','.join(context.user_data['data']))+"",
        reply_markup=ReplyKeyboardRemove(),
    )

    context.user_data.clear()
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(filters.Regex("^(Done|done)$"), done),
                MessageHandler(filters.Regex("^(Start Server|Stop Server)$"), start_stop),
                MessageHandler(filters.Regex("^.*$"), normal_messages)
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


main()