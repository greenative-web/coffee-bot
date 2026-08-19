import os
import telebot
from google import genai

# Initialisation du client GenAI
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Token Telegram
bot = telebot.TeleBot(os.environ["TELEGRAM_BOT_TOKEN"])

PROMPT_BARISTA = """Tu es un expert Barista spécialisé en espresso haute extraction et Gaggia Classic. 
Analyse les paramètres d'extraction donnés par l'utilisateur (dose, rendement, temps, goût) 
et donne des conseils précis sur la mouture, la température ou la pression."""

# Dictionnaire pour maintenir une session de chat par utilisateur
user_chats = {}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    
    try:
        # Création du fil de chat s'il n'existe pas encore pour cet utilisateur
        if user_id not in user_chats:
            user_chats[user_id] = client.chats.create(
                model='gemini-3.6-flash',
                config={'system_instruction': PROMPT_BARISTA}
            )
        
        # Envoi du message dans la conversation
        chat = user_chats[user_id]
        response = chat.send_message(message.text)
        
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Erreur : {str(e)}")

print("Bot en cours d'exécution...")
bot.infinity_polling()
