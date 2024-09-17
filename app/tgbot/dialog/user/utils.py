import re

def phone_check(text: str) -> str:
    # Удаляем пробелы и лишние символы
    phone_number = text.strip()
    
    # Проверяем, что номер состоит только из цифр
    if not re.match(r"^\d+$", phone_number):
        raise ValueError("Номер телефона должен содержать только цифры.")
    
    # Проверяем длину номера телефона (опционально, например, не менее 10 цифр)
    if len(phone_number) < 10:
        raise ValueError("Номер телефона должен содержать как минимум 10 цифр.")
    
    return phone_number