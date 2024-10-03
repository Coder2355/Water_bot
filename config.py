import os

# Telegram API credentials
API_ID = int(os.getenv("API_ID", "21740783"))  # Replace YOUR_API_ID
API_HASH = os.getenv("API_HASH", "a5dc7fec8302615f5b441ec5e238cd46")  # Replace YOUR_API_HASH
BOT_TOKEN = os.getenv("BOT_TOKEN", "7116266807:AAFiuS4MxcubBiHRyzKEDnmYPCRiS0f3aGU")  # Replace YOUR_BOT_TOKEN

# Watermark settings
WATERMARK_TEXT = os.getenv("WATERMARK_TEXT", "Anime_warrior_tamil")
WATERMARK_PATH = os.getenv("WATERMARK_PATH", "default_watermark.png")

# FFmpeg settings (optional)
FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")
