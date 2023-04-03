import os

import telebot

import mongodb
import poll_parser

bot = telebot.TeleBot(os.getenv("POLL_CHECKER_BOT_TOKEN"))


@bot.message_handler(commands=['start', 'help'])
def command_start_and_help(message):
    bot.send_message(message.chat.id,
                     "Willkommen beim Poll Checker Bot 📋\n\nDer Bot ermöglicht dir das Anlegen einer Liste von Strings (also Zeichenketten, beispielsweise einem Wort) und anschließend beliebige Textnachrichten nach diesen Strings zu durchsuchen 🔎\n\nFolgende Befehle sind erlaubt ✅\n/start - erklärt den Bot\n/help - erklärt den Bot\n/setlist - erlaubt das festlegen einer Liste von Strings\n/list zeigt die aktuelle Liste an\n/cancel - bricht die aktuelle Aktion ab\n\nUm den Bot nutzen zu können, muss zuerst mit /setlist eine Liste angelegt werden. Anschließend können Textnachrichten an den Bot geschrieben/weitergeleitet werden, welche er durchsuchen wird 💯")
    mongodb.set_setting_list(message.chat.id, False)


@bot.message_handler(commands=['cancel'])
def command_cancel(message):
    mongodb.set_setting_list(message.chat.id, False)
    bot.send_message(message.chat.id,
                     "Alle laufenden Aktionen wurden abgebrochen.\n\nFür Hilfe können Sie /help tippen.")


@bot.message_handler(commands=["list", "names"])
def show_list(message):
    if mongodb.has_list(message.chat.id):
        bot.send_message(message.chat.id,
                         poll_parser.list_to_message(mongodb.get_list(message.chat.id)))
    else:
        inform_user_about_missing_list(message.chat.id)
    mongodb.set_setting_list(message.chat.id, False)


@bot.message_handler(commands=["set", "setstrings", "setlist", "setnames"])
def set_list(message):
    mongodb.set_setting_list(message.chat.id, True)
    bot.send_message(message.chat.id,
                     "Sie sind dabei, eine Liste mit Strings anzulegen. Bitte geben Sie jetzt in einer Nachricht alle "
                     "Strings an (pro Zeile ein String).\n\nMit /cancel können Sie die Erstellung der Liste "
                     "abbrechen.")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if mongodb.is_setting_list(message.chat.id):
        string_list = poll_parser.message_to_list(message.text)
        mongodb.set_list(message.chat.id, string_list)
        bot.send_message(message.chat.id,
                         "Die Liste wurde erfolgreich gespeichert. Sie können mit /list ihre aktuelle Liste anschauen "
                         "oder mit /setlist diese ersetzen.")
    elif mongodb.has_list(message.chat.id):
        bot.send_message(message.chat.id, search_missing_strings(message.chat.id, message.text))
    else:
        inform_user_about_missing_list(message.chat.id)


def inform_user_about_missing_list(id: str) -> None:
    bot.send_message(id,
                     "Sie müssen erst eine Liste anlegen, um den Bot nutzen zu können.\n\nTippen Sie /setlist um eine "
                     "Liste anzulegen oder tippen Sie /help für mehr Informationen.")


def search_missing_strings(id: str, message: str) -> str:
    missing_strings = "Es fehlen folgende Strings:\n\n"
    all_found = True
    for string in mongodb.get_list(id):
        if string not in message:
            missing_strings = missing_strings + string + "\n"
            all_found = False
    if all_found:
        return "Es sind alle Strings in der Nachricht vorhanden!"
    return missing_strings


if __name__ == "__main__":
    try:
        bot.polling(skip_pending=True, timeout=60, non_stop=True)
    except Exception as e:
        print(e)
