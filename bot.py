import os
import telebot
from google import genai

# Initialisation du client GenAI
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Token Telegram
bot = telebot.TeleBot(os.environ["TELEGRAM_BOT_TOKEN"])

PROMPT_BARISTA = """You are an expert Barista specializing in high-extraction espresso and the Gaggia Classic. 
Always answer in English. 
Analyze the extraction parameters given by the user (dose, yield, brew time, taste, equipment/mods) 
and provide precise, actionable advice regarding grind size, temperature surfing, pressure, or ratio adjustments."""

# Dictionnaire pour maintenir une session de chat par utilisateur
user_chats = {}

@bot.message_handler(commands=['start', 'reset'])
def send_welcome(message):
    user_id = message.from_user.id
    # Réinitialise la session de chat
    user_chats[user_id] = client.chats.create(
        model='gemini-3.6-flash',
        config={'system_instruction': PROMPT_BARISTA}
    )
    bot.reply_to(
        message, 
        "☕ *Welcome to your Gaggia Classic Barista Assistant!*\n\n"
        "Send me your extraction details (dose, yield, time, taste profile, machine mods) "
        "and I'll help you dial in your shot.\n\n"
        "*(Type /reset anytime to start a fresh discussion)*",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    
    try:
        # Création du fil de chat en anglais s'il n'existe pas
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
        bot.reply_to(message, f"Error: {str(e)}")

print("Bot en cours d'exécution...")
bot.infinity_polling()
