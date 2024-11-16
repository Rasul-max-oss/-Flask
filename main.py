from tkinter import *


# Функция для получения данных из полей и вывода в консоль
def send_message():
    name = entry_name.get()  # Получаем имя
    email = entry_email.get()  # Получаем email
    message = text_message.get("1.0", END)  # Получаем сообщение (включая символ новой строки)

    # Выводим данные в консоль
    print(f"Имя: {name}")
    print(f"Email: {email}")
    print(f"Сообщение: {message.strip()}")  # strip() удаляет лишние пробелы и новые строки


# Создание основного окна
root = Tk()
root.title("Форма обратной связи")  # Название окна
root.geometry("400x300")  # Размер окна

# Инструкция
label_instruction = Label(root, text="Заполните форму обратной связи", font=("Arial", 12))
label_instruction.pack(pady=10)

# Поле для ввода имени
label_name = Label(root, text="Имя:")
label_name.pack(pady=5)
entry_name = Entry(root, width=40)
entry_name.pack(pady=5)

# Поле для ввода email
label_email = Label(root, text="Email:")
label_email.pack(pady=5)
entry_email = Entry(root, width=40)
entry_email.pack(pady=5)

# Поле для ввода сообщения (многострочное)
label_message = Label(root, text="Сообщение:")
label_message.pack(pady=5)
text_message = Text(root, width=40, height=5)
text_message.pack(pady=5)

# Кнопка отправки
button_send = Button(root, text="Отправить", command=send_message)
button_send.pack(pady=20)

# Запуск основного цикла
root.mainloop()
