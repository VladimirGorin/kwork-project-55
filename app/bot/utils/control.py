from telebot import types

def generate_keyabord(ids):
    try:
        keyboard = types.InlineKeyboardMarkup()
        for id in ids:
            button = types.InlineKeyboardButton(text=f"({id[0]})", callback_data=f"control:{id[0]}")
            keyboard.add(button)
        return keyboard
    except Exception as e:
        raise Exception(f"не удалос создать клавиатуру для выбора объявления: {e}")


def generate_text(ids):
    try:
        # Создаем пустую строку для хранения результата
        generated_text = ""

        for ad in ids:
            generated_text += f"({ad[0]}) {ad[1]}\n\n"

        return generated_text
    except Exception as e:
        raise Exception(f"не удалось создать текст для выбора объявления: {e}")
