import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import openai

# Устанавливаем API-ключ OpenAI
openai.api_key = "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"
def find_answer():
    urll = url_entry.get()
    prompt = question_entry.get()
    # Загрузите текст с веб-сайта (здесь предполагается, что вы используете библиотеку requests)
    response = requests.get(urll)
    if response.status_code == 200:
        webpage_text = response.text
    else:
        result_label.config(text="Ошибка при загрузке веб-страницы.")
        return
    # Соедините вопрос и текст с веб-сайта, чтобы сформулировать запрос к GPT-3
    input_text = f"Веб-страница: {webpage_text}\nВопрос: {prompt}"

    try:
        # Запросите ответ с помощью GPT-3
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1000  # Максимальное количество токенов в ответе
        )
        answer=response.choices[0].text
        print (answer)
        result_label.config(text=answer)
    except Exception as e:
        result_label.config(text="Произошла ошибка при запросе к GPT-3.")
        print(e)

def check_age():
    # Получаем URL из текстового поля
    url = entry.get()
    response = requests.get(url)
    if response.status_code == 200:
        # Используем BeautifulSoup для парсинга HTML-кода страницы
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все заголовки <h1> на странице
        headers = soup.find_all(['h1'])

        stop_words = ['Оценка', 'Комментарии', 'Популярное', 'Ещё почитать', 'Опросы', 'Кто здесь?', 'О проекте',
                      'Ещё в разделе', 'т.д.']

        # Очищаем текстовое поле с результатами
        result_text.delete(1.0, tk.END)

        # Выводим текст каждого заголовка, исключая заголовки с запрещенными словами
        for header in headers:
            header_text = header.text.strip()
            if all(word not in header_text for word in stop_words):
                result_text.insert(tk.END, header_text + '\n')

    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f'Ошибка при выполнении запроса. Код состояния: {response.status_code}')
# Создаем главное окно
window = tk.Tk()
window.title("VanDam Work")
window.geometry("400x400")



# Создаем контроллер вкладок
tab_control = ttk.Notebook(window)






# Создаем панели для вкладок
panel1 = tk.Frame(tab_control)
panel2 = tk.Frame(tab_control)

style = ttk.Style()
style.configure("TNotebook", background="#000000")
# Устанавливаем черный фон для окна
panel1.configure(bg="#A658E3")
panel2.configure(bg="#A658E3")

tab_control.add(panel1, text="Поиск заголовков")
tab_control.add(panel2, text="Вопрос-Ответ")
tab_control.pack(fill="both", expand=True)

# Стилизация виджетов в первой вкладке
label = tk.Label(panel1, text="Введите ссылку на источник:", bg="#A658E3")
label.config(font=("Franklin Gothic Medium", 20))  # Установка шрифта для метки
label.pack()

entry = tk.Entry(panel1)
entry.config(font=("Franklin Gothic Medium", 12), bg="#A658E3", width="30", border="3")  # Установка шрифта для текстового поля
entry.pack()

button = tk.Button(panel1, text="Подтвердить", foreground="black", command=check_age)
button.config(font=("Franklin Gothic Medium", 12), bg="#FF2187", width="20", foreground="black")  # Цвет фона и текста для кнопки
button.pack()

result_text = tk.Text(panel1, wrap=tk.WORD, width=40, height=15)
result_text.config(font=("Arial", 12), bg="#A658E3", borderwidth="0",foreground="black")  # Цвет фона для текстового поля
result_text.pack()





#https://qaa-engineer.ru/kak-izmenit-stil-okna-v-pyqt5/
#что такое pyqt5













url_label = tk.Label(panel2, text="URL веб-сайта:", bg="#A658E3")
url_label.config(font=("Franklin Gothic Medium", 20))
url_label.pack()

url_entry = tk.Entry(panel2, width=70, bg="#A658E3")
url_entry.config(font=("Franklin Gothic Medium", 12), bg="#A658E3", width="30", border="3")
url_entry.pack()

question_label = tk.Label(panel2, text="Ваш вопрос:", bg="#A658E3")
question_label.config(font=("Franklin Gothic Medium", 20))
question_label.pack()

question_entry = tk.Entry(panel2, width=70, bg="#A658E3")
question_entry.config(font=("Franklin Gothic Medium", 12), bg="#A658E3", width="30", border="3")
question_entry.pack()

find_button = tk.Button(panel2, text="Найти ответ", command=find_answer, bg="#A658E3")
find_button.config(font=("Franklin Gothic Medium", 12), bg="#FF2187", width="20", foreground="black")
find_button.pack()

result_label = tk.Label(panel2, text="\n ", width=100,wraplength=300, bg="#A658E3")
result_label.config(font=("Franklin Gothic Medium", 12), foreground="black")
result_label.pack()


















# Запускаем цикл событий для главного окна
window.mainloop()
