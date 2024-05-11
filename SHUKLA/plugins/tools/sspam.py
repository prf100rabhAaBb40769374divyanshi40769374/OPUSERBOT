import asyncio
from re import sub
from threading import Event
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from SHUKLA.modules.SHASHANK.data import GROUP
from ... import app, SUDO_USER
from ... import *
from SHUKLA.console import*

commands = ["spam", "statspam", "slowspam", "fastspam"]
SPAM_COUNT = [0]


def increment_spam_count():
    SPAM_COUNT[0] += 1
    return spam_allowed()


def spam_allowed():
    return SPAM_COUNT[0] < 4999

async def extract_args(message, markdown=True):
    if not (message.text or message.caption):
        return ""

    text = message.text or message.caption

    text = text.markdown if markdown else text
    if " " not in text:
        return ""

    text = sub(r"\s+", " ", text)
    text = text[text.find(" ") :].strip()
    return text

@app.on_message(cdz(["dspam"])  & (filters.me | filters.user(SUDO_USER)))
async def delayspam(client: Client, message: Message):
    if message.chat.id in GROUP:
        return await message.reply_text(
            "**This command is not allowed to be used in this group**"
        )
    delayspam = await extract_args(message)
    arr = delayspam.split()
    delay = float(arr[0])
    count = int(arr[1])
    spam_message = delayspam.replace(arr[0], "", 1)
    spam_message = spam_message.replace(arr[1], "", 1).strip()
    await message.delete()

    if not spam_allowed():
        return

    delaySpamEvent = Event()
    for i in range(0, count):
        if i != 0:
            delaySpamEvent.wait(delay)
        await client.send_message(message.chat.id, spam_message)
        limit = increment_spam_count()
        if not limit:
            break

    await client.send_message(
        LOG_GROUP, "**#DELAYSPAM**\nDelaySpam was executed successfully"
    )


@Client.on_message(filters.command(commands, ".") & (filters.me | filters.user(SUDO_USER)))
async def sspam(client: Client, message: Message):
    if message.chat.id in GROUP:
        return await message.reply_text(
            "**This command is not allowed to be used in this group**"
        )
    amount = int(message.command[1])
    text = " ".join(message.command[2:])

    cooldown = {"spam": 0.1, "statspam": 0.1, "slowspam": 0.9, "fastspam": 0}

    await message.delete()

    for msg in range(amount):
        if message.reply_to_message:
            sent = await message.reply_to_message.reply(text)
        else:
            sent = await client.send_message(message.chat.id, text)

        if message.command[0] == "statspam":
            await asyncio.sleep(0.1)
            await sent.delete()

        await asyncio.sleep(cooldown[message.command[0]])


@app.on_message(cdz(["sspam"])  & (filters.me | filters.user(SUDO_USER)))
async def spam_stick(client: Client, message: Message):
    if message.chat.id in GROUP:
        return await message.reply_text(
            "**This command is not allowed to be used in this group**"
        )
    if not message.reply_to_message:
        await message.reply_text(
            "**reply to a sticker with amount you want to spam**"
        )
        return
    if not message.reply_to_message.sticker:
        await message.reply_text(
            "**reply to a sticker with amount you want to spam**"
        )
        return
    else:
        i = 0
        times = message.command[1]
        
        if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            for i in range(int(times)):
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(
                    message.chat.id,
                    sticker,
                )
                await asyncio.sleep(0.10)

        if message.chat.type == enums.ChatType.PRIVATE:
            for i in range(int(times)):
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(message.chat.id, sticker)
                await asyncio.sleep(0.10)
      

__NAME__ = "Sᴘᴀᴍ"
__MENU__ = """
      `.spam` - .spam (count) (message)
      `.pspam` - .spam (count) (message)
`.sspam` - .sspam (count) (reply_media)
`.delayspam` - .delayspam (time in second) (count) (text)
   `.randi .randii` - .one word spam start
      `.stop` - . one word spam stop
"""
