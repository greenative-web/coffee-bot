import os
import telebot
from google import genai

# Configuration du SDK Google GenAI
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Configuration du Bot Telegram
bot = telebot.TeleBot(os.environ["TELEGRAM_BOT_TOKEN"])

PROMPT_BARISTA = """Tu es un expert Barista spécialisé en espresso haute extraction et Gaggia Classic. 
Analyse les paramètres d'extraction donnés par l'utilisateur (dose, rendement, temps, goût) 
et donne des conseils précis sur la mouture, la température ou la pression."""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Modèle mis à jour vers gemini-3.6-flash
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=f"{PROMPT_BARISTA}\n\nUtilisateur: {message.text}"
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Erreur : {str(e)}")

print("Bot en cours d'exécution...")
bot.infinity_polling()
