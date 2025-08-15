from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from PIL import Image, ImageDraw
import io

async def logo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Grab user text after /logo command
    description = ' '.join(context.args) if context.args else "default"

    # For demo: just change circle color based on description text length
    color = "#0088cc" if len(description) % 2 == 0 else "#00aaff"
    size = 256

    # Create a Telegram-style logo (circle + paper plane polygon)
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([(0, 0), (size, size)], fill=color)

    # Paper plane shape
    plane_points = [
        (size // 2, size // 4),
        (size // 4, size * 3 // 4),
        (size // 2, size // 2),
        (size * 3 // 4, size * 3 // 4)
    ]
    draw.polygon(plane_points, fill="white")

    # Save image to buffer
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # Send image with caption
    await update.message.reply_photo(photo=buf, caption=f"Logo generated for: {description}")

if __name__ == "__main__":
    # Replace "YOUR_BOT_TOKEN" with your real Telegram bot token from BotFather
    application = ApplicationBuilder().token("BOT_TOKEN").build()

    # Add command handler for /logo
    application.add_handler(CommandHandler("logo", logo_command))

    # Run bot
    application.run_polling()
    
