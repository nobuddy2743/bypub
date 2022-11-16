import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import bypasser
import os
import ddl
import requests
import threading
from texts import HELP_TEXT
from bypasser import ddllist

from configs import Config
import shutil
import psutil
from access_db import db
from add_user import AddUserToDatabase
from display_progress import progress_for_pyrogram, humanbytes


# bot
bot_token = os.environ.get("BOT_TOKEN")
api_hash = os.environ.get("API_HASH") 
api_id = os.environ.get("API_ID")
log_ch = os.environ.get("LOG_CHANNEL")
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)  


# loop thread
def loopthread(message):
    urls = []
    for ele in message.text.split():
        if "http://" in ele or "https://" in ele:
            urls.append(ele)
    if len(urls) == 0:
        return

    if bypasser.ispresent(ddllist,urls[0]):
        msg = app.send_message(message.chat.id, "⚡ __generating...__", reply_to_message_id=message.id)        
    else:
        if urls[0] in "https://olamovies" or urls[0] in "https://psa.pm/":
            msg = app.send_message(message.chat.id, "🔎 __this might take some time...__", reply_to_message_id=message.id)            
        else:
            msg = app.send_message(message.chat.id, "🔎 __bypassing...__", reply_to_message_id=message.id)            

    link = ""
    for ele in urls:
        if bypasser.ispresent(ddllist,ele):
            try: temp = ddl.direct_link_generator(ele)
            except Exception as e: temp = "**Error**: " + str(e)
        else:    
            try: temp = bypasser.shortners(ele)
            except Exception as e: temp = "**Error**: " + str(e)
        print("bypassed:",temp)
        link = link + temp + "\n\n"
        app.send_message(log_ch, f"**FIRST NAME**: [{message.from_user.first_name}](tg://user?id={message.from_user.id}) \n**LAST NAME** : {message.from_user.last_name} \n**USER ID** : {message.from_user.id} \n\n **Source Link** : {message.text} \n\n **Destination Link** : {link}")
        
    try: app.edit_message_text(message.chat.id, msg.id, f"**Source Link** : {message.text} \n\n **Destination Link** : {link}", disable_web_page_preview=True)
    #try: app.edit_message_text(message.chat.id, msg.id, f'__Your Link : {link}__', disable_web_page_preview=True)    
    except: app.edit_message_text(message.chat.id, msg.id, "__Failed to Bypass__")


# start command
@app.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, f"__**Hi** **{message.from_user.mention}** 👋, \n\n I am Link Bypasser Bot, **Just Send Me Any Valid Link and I Will Give you Results.**",
    reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton(" Share", url="https://t.me/link_bypass_kd_bot")]]), reply_to_message_id=message.id)


# status command    
@app.on_message(filters.private & filters.command("status") & filters.user(Config.BOT_OWNER))
async def status(_,m: pyrogram.types.messages_and_media.message.Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    await m.reply_text(
        text=f"**Total Disk Space:** {total} \n**Used Space:** {used}({disk_usage}%) \n**Free Space:** {free} \n**CPU Usage:** {cpu_usage}% \n**RAM Usage:** {ram_usage}%\n\n**Total Users in DB:** `{total_users}`",
        #parse_mode="Markdown",
        quote=True
    )


# help command
#@app.on_message(filters.command(["help"]))
#def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
#    app.send_message(message.chat.id, HELP_TEXT, reply_to_message_id=message.id, disable_web_page_preview=True)


# links
@app.on_message(filters.text)
def receive(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bypass = threading.Thread(target=lambda:loopthread(message),daemon=True)
    bypass.start()


# doc thread
def docthread(message):
    if message.document.file_name.endswith("dlc"):
        msg = app.send_message(message.chat.id, "🔎 __bypassing...__", reply_to_message_id=message.id)
        print("sent DLC file")
        sess = requests.session()
        file = app.download_media(message)
        dlccont = open(file,"r").read()
        link = bypasser.getlinks(dlccont,sess)
        app.edit_message_text(message.chat.id, msg.id, f'__{link}__')
        os.remove(file)

# doc
@app.on_message(filters.document)
def docfile(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bypass = threading.Thread(target=lambda:docthread(message),daemon=True)
    bypass.start()


# server loop
print("Bot Starting")
app.run()
