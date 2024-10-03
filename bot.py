import os
import subprocess
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from config import WATERMARK_PATH, WATERMARK_TEXT, BOT_TOKEN, API_HASH, API_ID

# Default watermark settings
WATERMARK_TEXT = "Anime_warrior_tamil"  # Default watermark text
WATERMARK_PATH = "default_watermark.png"  # Path to default watermark image

# Initialize the bot
bot = Client("watermark_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Utility function for adding a watermark
async def add_watermark(input_file, output_file, watermark=WATERMARK_PATH, position="top-right"):
    positions = {
        "top-left": "(10, 10)",
        "top-right": "(main_w-overlay_w-10, 10)",
        "bottom-left": "(10, main_h-overlay_h-10)",
        "bottom-right": "(main_w-overlay_w-10, main_h-overlay_h-10)"
    }
    
    position_filter = positions.get(position, "(main_w-overlay_w-10, 10)")  # Default top-right

    command = [
        "ffmpeg", "-i", input_file, "-i", watermark, "-filter_complex",
        f"overlay={position_filter}", output_file
    ]

    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Utility function for removing watermark
async def remove_watermark(input_file, output_file):
    command = [
        "ffmpeg", "-i", input_file, "-vf", "delogo=x=10:y=10:w=100:h=100", output_file
    ]

    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Start command handler
@bot.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply_text(
        "Welcome to the Video Watermark Adder/Remover Bot!\n\n"
        "Send me a video to add or remove a watermark.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Add Watermark", callback_data="add_watermark"),
             InlineKeyboardButton("Remove Watermark", callback_data="remove_watermark")]
        ])
    )

# Video handler
@bot.on_message(filters.video)
async def video_handler(bot, message):
    video = await message.download()
    await message.reply_text(
        "What would you like to do with this video?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Add Watermark", callback_data=f"add_watermark|{video}"),
             InlineKeyboardButton("Remove Watermark", callback_data=f"remove_watermark|{video}")]
        ])
    )

# Callback query handler
@bot.on_callback_query()
async def callback_query_handler(bot, query):
    data = query.data.split("|")
    action = data[0]
    input_file = data[1]

    output_file = f"output_{os.path.basename(input_file)}"

    if action == "add_watermark":
        await query.message.reply_text("Adding watermark... Please wait.")
        success = await add_watermark(input_file, output_file)
        if success:
            await query.message.reply_video(output_file, caption="Here is your video with a watermark.")
        else:
            await query.message.reply_text("Failed to add watermark.")
    
    elif action == "remove_watermark":
        await query.message.reply_text("Removing watermark... Please wait.")
        success = await remove_watermark(input_file, output_file)
        if success:
            await query.message.reply_video(output_file, caption="Here is your video without a watermark.")
        else:
            await query.message.reply_text("Failed to remove watermark.")

    # Clean up
    os.remove(input_file)
    os.remove(output_file)

if __name__ == "__main__":
    bot.run()
