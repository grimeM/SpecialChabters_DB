import random
import sqlite3
from tkinter.ttk import Combobox
from tkinter import Label, scrolledtext
import tkinter as tk
from pymongo import MongoClient
from tkinter import messagebox, simpledialog, ttk
from tkcalendar import DateEntry
import pickle
from PIL import Image, ImageTk
from tkinter import simpledialog, messagebox, Toplevel, Scale, Label, Entry, Button
from datetime import datetime


cities = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Нижний Новгород",
    "Казань", "Челябинск", "Омск", "Самара", "Ростов-на-Дону", "Уфа", "Красноярск",
    "Пермь", "Воронеж", "Волгоград", "Краснодар", "Саратов", "Тюмень", "Тольятти",
    "Ижевск", "Ульяновск", "Барнаул", "Иркутск", "Хабаровск", "Ярославль", "Владивосток",
    "Махачкала", "Томск", "Оренбург", "Кемерово", "Новокузнецк", "Рязань", "Астрахань",
    "Набережные Челны", "Пенза", "Киров", "Липецк", "Чебоксары", "Тула", "Калининград",
    "Курск", "Брянск", "Архангельск", "Севастополь", "Сочи", "Белгород", "Владимир",
    "Смоленск", "Мурманск", "Калуга", "Чита", "Тверь", "Ставрополь", "Курган", "Саранск",
    "Стерлитамак", "Балашиха", "Химки", "Подольск", "Орёл", "Волгодонск", "Сыктывкар",
    "Магнитогорск", "Королёв", "Волжский", "Новочеркасск", "Энгельс", "Абакан", "Братск",
    "Рыбинск", "Нижнекамск", "Ангарск", "Дзержинск", "Октябрьский", "Березники", "Щёлково",
    "Салават", "Новомосковск", "Шахты", "Старый Оскол", "Мытищи", "Каменск-Уральский", "Мичуринск",
    "Новороссийск", "Прокопьевск", "Хасавюрт", "Елец", "Керчь", "Серпухов", "Электросталь",
    "Находка", "Рубцовск", "Альметьевск", "Копейск", "Петропавловск-Камчатский", "Майкоп",
    "Кисловодск", "Щёкино", "Ногинск", "Димитровград", "Нефтекамск", "Нефтеюганск", "Бугульма",
    "Дербент", "Ковров", "Глазов", "Кызыл", "Орск", "Каспийск", "Батайск", "Арзамас", "Новый Уренгой",
    "Домодедово", "Северодвинск", "Камышин", "Ступино", "Ессентуки", "Воткинск", "Сергиев Посад",
    "Жуковский", "Ачинск", "Киселёвск", "Новошахтинск", "Назрань", "Кыштым", "Кинешма", "Бузулук",
    "Егорьевск", "Армавир", "Серов", "Ливны", "Назарово", "Раменское", "Новотроицк", "Каменск-Шахтинский",
    "Тобольск", "Кропоткин", "Новоуральск", "Железногорск", "Кырнос", "Люберцы", "Артём", "Междуреченск",
    "Черкесск", "Сосновый Бор", "Борисоглебск", "Новочебоксарск", "Муром", "Курчатов", "Минеральные Воды",
    "Пушкино", "Реутов", "Северск", "Новокуйбышевск", "Сатка", "Бердск", "Долгопрудный", "Красногорск",
    "Балаково", "Зеленодольск", "Россошь", "Ковдор", "Краснокаменск", "Тихвин", "Ленинск-Кузнецкий",
    "Магадан", "Сертолово", "Саров", "Лобня", "Чапаевск", "Славянск-на-Кубани", "Одинцово", "Новоалтайск",
    "Североморск", "Белорецк", "Озёрск", "Краснотурьинск", "Тутаев", "Славгород", "Волоколамск", "Новоуральск",
    "Кольчугино", "Павловский Посад", "Лесосибирск", "Сарапул"]


def show_frame(frame):
    frame.tkraise()


# MOngoDB
def generate_unique_id():
    while True:
        new_id = random.randint(10000, 99999)
        # Проверяем, существует ли уже такой ID в базе данных
        if user_collection.count_documents({"id": new_id}) == 0:
            return new_id


def fetch_users():
    client = MongoClient()  # Укажите параметры подключения, если требуется
    db = client['user_database']  # Название вашей базы данных
    user_collection = db['users']  # Название коллекции с пользователями
    users = user_collection.find({}, {'login': 1, '_id': 0})  # Запрос всех логинов, исключая ID
    return [user["login"] for user in users]


def fetch_user_info(login):
    client = MongoClient('localhost', 27017)
    db = client['user_database']  # Название вашей базы данных
    users = db['users']  # Название вашей коллекции
    user_info = users.find_one({"login": login})
    if user_info:
        # Форматирование информации о пользователе для вывода
        info_text = f"ID: {user_info.get('id', 'N/A')}\n"
        info_text += f"Логин: {user_info.get('login', 'N/A')}\n"
        info_text += f"Имя пользователя: {user_info.get('name', 'N/A')}\n"
        info_text += f"Пароль: {user_info.get('password', 'N/A')}\n"
        info_text += f"Дата рождения: {user_info.get('birthdate', 'N/A')}\n"
        info_text += f"Город: {user_info.get('city', 'N/A')}\n"
        info_text += f"Роль: {user_info.get('role', 'N/A')}\n"
        return info_text


#SQL
def connect_to_db():
    return sqlite3.connect('tests.db')


def fetch_tests():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT test_id, test_name FROM tests")
    tests = cursor.fetchall()
    conn.close()
    return tests


def fetch_questions(test_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT question_id, question_text, answer_id, answer_text, is_correct
        FROM questions
        JOIN answers ON questions.question_id = answers.question_id
        WHERE test_id = ?
    """, (test_id,))
    questions = cursor.fetchall()
    conn.close()
    return questions


def fetch_sections():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT section_name FROM sections")
    sections = [section[0] for section in cursor.fetchall()]
    conn.close()
    return sections


def fetch_tests(section_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
            SELECT t.test_id, t.test_name
            FROM tests t
            JOIN test_sections ts ON t.test_id = ts.test_id
            JOIN sections s ON ts.section_id = s.section_id
            WHERE s.section_name = ?
        """, (section_name,))
    tests = cursor.fetchall()
    conn.close()
    return tests


def fetch_questions_for_test(test_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT q.question_id, q.question_text, a.answer_id, a.answer_text
        FROM questions q
        JOIN test_answers ta ON q.question_id = ta.question_id
        JOIN answers a ON q.question_id = a.question_id
        WHERE ta.test_id = ?
    """, (test_id,))
    questions = []
    current_qid = None
    question_info = None
    for row in cursor.fetchall():
        if current_qid != row[0]:
            if question_info:
                random.shuffle(question_info['answers'])
                print("Перемешанные ответы:", question_info['answers'])  # Добавьте эту строку для отладки
                questions.append(question_info)
            question_info = {'question_id': row[0], 'question_text': row[1], 'answers': []}
            current_qid = row[0]
        question_info['answers'].append({'answer_id': row[2], 'answer_text': row[3]})
    if question_info:
        random.shuffle(question_info['answers'])
        questions.append(question_info)
    conn.close()
    return questions

def fetch_answers_for_question(question_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    # Присоединяем таблицу answers к test_answers, чтобы проверить, какой ответ является правильным
    cursor.execute("""
        SELECT a.answer_id, a.answer_text, 
               CASE WHEN ta.answer_id IS NOT NULL THEN 1 ELSE 0 END AS is_correct
        FROM answers a
        LEFT JOIN test_answers ta ON a.answer_id = ta.answer_id AND a.question_id = ta.question_id
        WHERE a.question_id = ?
    """, (question_id,))
    # Создаем список словарей для каждого ответа
    answers = [{'answer_id': row[0], 'answer_text': row[1], 'is_correct': bool(row[2])} for row in cursor.fetchall()]
    conn.close()
    return answers



def fetch_test_id(test_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT test_id FROM tests WHERE test_name = ?", (test_name,))
    # Получение результата
    test_id = cursor.fetchone()
    conn.close()
    return test_id

def fetch_name_test(test_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT test_name FROM tests WHERE test_id = ?"
    cursor.execute(query, (test_id,))
    result = cursor.fetchone()
    return result[0]

def get_average_scores():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
    SELECT test_id, AVG(score) as average_score
    FROM test_history
    GROUP BY test_id
    """
    try:
        cursor.execute(query)
        results = cursor.fetchall()  # Получение всех результатов
        result_str = ""  # Инициализация пустой строки для результата

        for test_id, average_score in results:
            test_name = fetch_name_test(test_id)  # Получение имени теста по ID
            result_str += f"{test_name} - Средний балл: {average_score:.2f}\n"  # Добавление результатов с новой строки

        return result_str.strip()  # Возвращаем результаты, удаляя последний перевод строки

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return "Ошибка при получении данных."

    finally:
        conn.close()

def get_average_rating(test_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
    SELECT AVG(rating) as average_rating
    FROM test_ratings
    WHERE test_id = ?
    GROUP BY test_id
    """
    try:
        cursor.execute(query, (test_id,))  # Передача test_id в запрос
        result = cursor.fetchone()  # Получение одного результата, так как запрос по одному test_id
        if result:
            return result[0]  # Возвращаем средний рейтинг, если он найден
        else:
            return "Нет данных"  # Возвращаем сообщение, если данных нет
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    finally:
        conn.close()

def fetch_comments(test_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT user_comment FROM test_comments WHERE test_id = 1"
    try:
        cursor.execute(query, (test_id,))
        comments = cursor.fetchall()  # Извлечение всех комментариев
        print(comments)
        return [comment[0] for comment in comments]  # Возвращаем список комментариев
    except Exception as e:
        print(f"Ошибка при извлечении данных: {e}")
        return []
    finally:
        conn.close()

#Pickle
# Функция для сохранения базы данных
def save_db(data, filename='results.pkl'):
    with open(filename, 'wb') as db_file:
        pickle.dump(data, db_file)


# Функция для загрузки базы данных
def load_db(filename='results.pkl'):
    try:
        with open(filename, 'rb') as db_file:
            return pickle.load(db_file)
    except FileNotFoundError:
        return {}


# Функция для добавления/обновления результата теста для пользователя
def update_test_result(user_id, test_name, result):
    db = load_db()
    if user_id not in db:
        db[user_id] = {}
    db[user_id][test_name] = result
    save_db(db)
    print("Результаты сохранены")


# Функция для получения всех результатов тестов пользователя
def get_user_results(user_id):
    db = load_db()
    user_results = db.get(user_id, {})  # Получаем результаты для данного пользователя

    # Создаем строку с результатами
    results_str = ''
    for test_name, scores in user_results.items():
        if scores:  # Проверяем, что список оценок не пустой
            score = scores[0]  # Предполагаем, что интересующая нас оценка - первая в списке
            results_str += f"Результат за {test_name} - {score} баллов\n"

    return results_str.strip()

# Функция для удаления результатов всех тестов пользователя
def delete_test_result(user_id):
    db = load_db()
    if user_id in db:
        del db[user_id]
        save_db(db)
        return True
    return False


def show_tests_frame(parent, user_data):
    profile_frame = tk.Frame(parent)
    def exit(event):
        profile_frame = create_profile_frame(parent, user_data)
        test_frame.place_forget()  # Скрываем фрейм регистрации
        profile_frame.place(x=0, y=0, width=720, height=720)
    test_frame = tk.Frame(parent)
    test_frame.place(x=0, y=0, width=720, height=720)

    tk.Label(test_frame, text="Выберите секцию:").pack(pady=(10, 0))
    section_var = tk.StringVar()
    section_combobox = ttk.Combobox(test_frame, textvariable=section_var, state="readonly")
    section_combobox['values'] = fetch_sections()
    section_combobox.pack()

    tk.Label(test_frame, text="Выберите тест:").pack(pady=(10, 0))
    test_var = tk.StringVar()
    test_combobox = ttk.Combobox(test_frame, textvariable=test_var, state="readonly")
    test_combobox.pack()

    average_lable = tk.Label(test_frame, text=f"Средняя оценка теста:")
    average_lable.pack(pady=(10, 0))
    # tk.Label(test_frame, text="Отзывы:").pack(pady=(10, 0))
    # text_area = scrolledtext.ScrolledText(test_frame, wrap=tk.WORD, width=40, height=10)
    # text_area.pack(padx=10, pady=10)
    # text_area.config(state=tk.DISABLED)


    def on_test_change(event):
        test_name = test_combobox.get()
        test_id_tuple = fetch_test_id(test_name)  # Эта функция возможно возвращает кортеж или None
        if test_id_tuple:
            test_id = test_id_tuple[0]  # Предполагаем, что ID теста это первый элемент кортежа
            # Убедитесь, что profile_frame доступен для передачи в эту функцию
            test_question_frame = show_test_questions_frame(parent, test_id, user_data)
            test_frame.place_forget()  # Скрываем фрейм регистрации
            test_question_frame.place(x=0, y=0, width=720, height=720)
        else:
            messagebox.showerror("Ошибка", "Тест не найден.")

    def on_combobox_select(event):
        test_name = test_combobox.get()
        test_id_tuple = fetch_test_id(test_name)  # Эта функция возможно возвращает кортеж или None
        if test_id_tuple:
            test_id = test_id_tuple[0]
            average_score = get_average_rating(test_id)
            average_lable.config(text=f"Средняя оценка теста: {average_score}")

            # comments = fetch_comments(test_id)
            # print(comments)
            # text_area.config(state=tk.NORMAL)
            # text_area.delete('1.0', tk.END)
            # text_area.insert(tk.END, "\n".join(comments))
            # text_area.config(state=tk.DISABLED)
    test_combobox.bind("<<ComboboxSelected>>", on_combobox_select)  # Подключаем функцию к событию выбора теста

    def on_section_change(event):
        selected_section = section_combobox.get()
        test_tuples = fetch_tests(selected_section)
        test_combobox['values'] = [test[1] for test in test_tuples]  # Список (имя теста, id теста)



    tk.Button(test_frame, text="Начать тест", command=lambda: on_test_change(None)).pack(pady=10)
    tk.Button(test_frame, text="Вернуться к профилю", command=lambda: exit(None)).pack(pady=10)
    section_combobox.bind("<<ComboboxSelected>>", on_section_change)
    return test_frame


def load_test(test_id, parent):
    for widget in parent.winfo_children():
        widget.destroy()
    questions = fetch_questions(test_id)
    for question in questions:
        tk.Label(parent, text=question[1]).pack(pady=(20, 2))
        for answer in question[2:]:
            btn = ttk.Button(parent, text=answer[3], command=lambda ans=answer: check_answer(ans, parent))
            btn.pack()


def check_answer(answer, parent):
    correct = answer[4]  # Assuming the `is_correct` field is a boolean
    if correct:
        messagebox.showinfo("Результат", "Правильный ответ!")
    else:
        messagebox.showinfo("Результат", "Неправильный ответ!")

def display_media(media_path, parent):
    # Загрузка изображения
    image = Image.open(media_path)
    #image = image.resize((200, 200), Image.ANTIALIAS)  # Изменение размера изображения
    photo = ImageTk.PhotoImage(image)

    # Проверка на наличие существующего Label, и его очистка, если он есть
    if hasattr(parent, 'image_label'):
        # Удаление старого изображения
        parent.image_label.destroy()

    # Создание нового Label для изображения
    parent.image_label = Label(parent, image=photo)
    parent.image_label.image = photo  # Сохраняем ссылку на изображение, чтобы предотвратить сбор мусора
    parent.image_label.pack(pady=20)


def show_test_questions_frame(parent, test_id, user_data):
    if not hasattr(parent, 'image_label'):
        parent.image_label = tk.Label(parent)
        parent.image_label.pack(side="bottom", pady=20)  # Position can be adjusted

    all_questions = fetch_questions_for_test(test_id)
    if not all_questions:
        messagebox.showerror("Ошибка", "Не найдено вопросов для этого теста.")
        return None

    questions_frame = tk.Frame(parent)

    questions = random.sample(all_questions, min(10, len(all_questions)))  # 10 случайных вопросов для теста
    question_index = [0]  # Индекс текущего вопроса в списке
    score = [0]  # Счетчик баллов
    current_question = [None]  # Текущий вопрос

    question_label = tk.Label(questions_frame, font=('Helvetica', 16))
    question_label.pack(pady=(10, 10))

    score_label = tk.Label(questions_frame, text=f"Ваш счет: {score[0]}", font=('Helvetica', 14))
    score_label.pack()

    hint_label = tk.Label(parent, font=('Helvetica', 10))  # Label for displaying hints
    hint_label.pack(pady=(5, 10), fill='x')

    question_counter_label = tk.Label(questions_frame, text=f"Вопрос {question_index[0]+1} из {len(questions)}", font=('Helvetica', 14))
    question_counter_label.pack()

    answers_frame = tk.Frame(questions_frame)
    answers_frame.pack(pady=(20, 20))

    def update_labels():
        score_label.config(text=f"Ваш счет: {score[0]}")
        question_counter_label.config(text=f"Вопрос {question_index[0]+1} из {len(questions)}")

    def display_question():
        hint_label.config(text="")
        for widget in answers_frame.winfo_children():
            widget.destroy()
        if question_index[0] < len(questions):
            current_question[0] = questions[question_index[0]]  # Убедитесь, что это словарь
            question_label.config(text=current_question[0]['question_text'],  wraplength=600, justify='center')

            # Загрузка медиа, если оно есть
            media_path = fetch_media_for_question(current_question[0]['question_id'])
            if media_path:
                print(media_path)
                # Предположим, что у вас есть функция для отображения изображения
                display_media(media_path, parent)

            update_media_display(media_path, parent)  # Обновление или скрытие изображения
            # Clear previous hint
            #answers = fetch_answers_for_question(current_question[0]['question_id'])
            for i, answer in enumerate(current_question[0]['answers']):
                btn = tk.Button(answers_frame, text=answer['answer_text'],
                                command=lambda a=answer: check_answer(a))
                btn.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            update_labels()
        else:
            show_results()
            rate_test_button = tk.Button(parent, text="Оценить тест", command=lambda: open_rating_form(parent, test_id))
            rate_test_button.pack(pady=(10, 0))


        if 'hint_button' not in globals():
            global hint_button
            hint_button = tk.Button(parent, text="Hint", command=show_hint)
            hint_button.pack(pady=(10, 0))
            hint_button.place(x=650, y=50)

    def show_hint():
        #Access the current question's ID correctly
        current_question = questions[question_index[0]]
        hint = fetch_hint_for_question(current_question['question_id'])
        hint_label.config(text=hint, wraplength=600, justify='center')

        hint_button.place(x=650, y=50)

    def update_media_display(media_path, parent):
        try:
            if media_path:
                img = Image.open(media_path)
                #img = img.resize((200, 200), Image.ANTIALIAS)  # Resize if necessary
                photo = ImageTk.PhotoImage(img)
                parent.image_label.config(image=photo)
                parent.image_label.image = photo  # Keep a reference!
            else:
                parent.image_label.config(image='')  # Remove image if no media path
        except Exception as e:
            print(f"Failed to load media: {e}")

    def check_answer(answer):
        correct_answer_id = fetch_correct_answer_id(current_question[0]['question_id'])
        if answer['answer_id'] == correct_answer_id:
            score[0] += 10
            question_index[0] += 1
            display_question()
        else:
            score[0] -= 1

    def show_results():
        for widget in questions_frame.winfo_children():
            widget.destroy()
        result_text = f"Тест завершен! Ваш результат: {score[0]} баллов."
        if score[0] > 70:
            result_text += "\nОтличный результат!"
        else:
            result_text += "\nПопробуйте еще раз для улучшения результатов."

        save_test_result(test_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), score[0])
        user_id = user_data["id"]
        test_name = fetch_name_test(test_id)
        update_test_result(user_id, test_name, score)

        tk.Label(questions_frame, text=result_text).pack(pady=(20, 10))

        # Уничтожаем или скрываем кнопку подсказки
        if 'hint_button' in globals() and hint_button.winfo_exists():
            hint_button.destroy()  # или hint_button.place_forget() если планируется повторное использование

        # Уничтожаем или скрываем изображение, если оно существует
        if hasattr(parent, 'image_label') and parent.image_label.winfo_exists():
            parent.image_label.destroy()  # или parent.image_label.pack_forget() если планируется повторное использование

        questions_frame.pack(fill="both", expand=True)  # Ensure the questions frame fills the parent container

    display_question()
    return questions_frame


def open_rating_form(parent, test_id):
    rating_window = Toplevel(parent)
    rating_window.title("Оценка теста")
    rating_window.geometry("300x200")

    # Star rating
    rating_label = Label(rating_window, text="Оцените тест:")
    rating_label.pack()

    rating_scale = Scale(rating_window, from_=1, to=5, orient='horizontal')
    rating_scale.pack()

    # Comment box
    comment_label = Label(rating_window, text="Комментарий:")
    comment_label.pack()

    comment_entry = Entry(rating_window, width=25)
    comment_entry.pack()

    # Submit button
    submit_button = Button(rating_window, text="OK", command=lambda: save_rating_and_close(rating_window, test_id, rating_scale.get(), comment_entry.get(), parent))
    submit_button.pack(pady=(10, 0))


def save_rating_and_close(rating_window, test_id, rating, comment, main_parent):
    # Connect to the database
    conn = connect_to_db()
    cursor = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp

    # Insert the rating into the test_ratings table
    cursor.execute("""
        INSERT INTO test_ratings (test_id, rating, rated_at)
        VALUES (?, ?, ?)
        RETURNING rating_id
    """, (test_id, rating, current_time))
    rating_id = cursor.fetchone()[0]

    # Check if there is a comment and if so, insert it into the test_comments table
    if comment.strip():  # This checks if comment is not just empty spaces
        cursor.execute("""
            INSERT INTO test_comments (rating_id, user_comment)
            VALUES (?, ?)
        """, (rating_id, comment))

    # Commit changes and close the database connection
    conn.commit()
    conn.close()

    # Close the rating window and show a message
    rating_window.destroy()
    messagebox.showinfo("Сохранено", "Ваша оценка и комментарий сохранены!")
    show_frame(main_parent)  # Assuming you have a function to show the main menu frame


def show_frame(frame):
    frame.tkraise()


def save_test_result(test_id, input_date, score):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO test_history (test_id, input_date, score)
        VALUES (?, ?, ?)
        RETURNING history_id
    """, (test_id, input_date, score))
    history_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return history_id

def fetch_media_for_question(question_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT media_link FROM question_media WHERE question_id = ?", (question_id,))
    media_path = cursor.fetchone()
    conn.close()
    return media_path[0] if media_path else None


def fetch_hint_for_question(question_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT hint_text FROM question_hints WHERE question_id = ?", (question_id,))
    hint = cursor.fetchone()
    conn.close()
    return hint[0] if hint else "No hint available for this question."


def fetch_correct_answer_id(question_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT answer_id FROM test_answers WHERE question_id = ?", (question_id,))
    answer_id = cursor.fetchone()[0]
    conn.close()
    return answer_id


def create_profile_frame(parent, user_data):
    profile_frame = tk.Frame(parent)
    tk.Label(profile_frame, text="Имя пользователя:").pack(pady=(20, 0))
    tk.Label(profile_frame, text=user_data["name"]).pack()
    tk.Label(profile_frame, text="Дата рождения:").pack(pady=(10, 0))
    tk.Label(profile_frame, text=user_data["birthdate"]).pack()
    tk.Label(profile_frame, text="Город:").pack(pady=(10, 0))
    tk.Label(profile_frame, text=user_data["city"]).pack()
    tk.Button(profile_frame, text="Перейти к тестам", command=lambda: show_tests_frame(profile_frame, user_data)).pack(
        pady=(20, 0))
    tk.Button(profile_frame, text="Выйти из профиля", command=lambda: show_frame(main_frame)).pack()
    profile_frame.place(x=0, y=0, width=720, height=720)
    return profile_frame


def create_admin_frame(parent, user_data):
    # Функция для фильтрации списка пользоателей
    def filters_users(event):
        search_text = users_combobox.get().lower()
        # Фильтрация и сортировка городов
        filtered_users = [user for user in list_users if search_text in user.lower()]
        filtered_users.sort(key=lambda user: (not user.lower().startswith(search_text), user))
        users_combobox['values'] = filtered_users
        users_combobox.focus()

    # Функция для обновления выпадающего списка с пользователями
    def update_combobox(combobox):
        user_logins = fetch_users()
        combobox['values'] = user_logins
        combobox.set('')

    # Функция для вывода информации о пользователе
    def show_user_data(event):
        user_login = users_combobox.get()
        list_users = fetch_users()
        if user_login not in list_users:
            messagebox.showerror("Ошибка", f"Указанный пользователь отсутсвует {user_login}")
            users_combobox.focus()
        else:
            user_info = fetch_user_info(user_login)
            messagebox.showinfo("Информация о пользователе", user_info)
        return

    # Функция для удаления пользователей
    def delete_user(event):
        user_login = users_combobox.get()
        if (user_data["role"] == 'admin'):
            messagebox.showerror("Ошибка", "У Вас отсутсвуют права на выполнение этого действия!")
        else:
            if user_login not in list_users:
                messagebox.showerror("Ошибка", f"Польлзователь {user_login} не существует")
                users_combobox.focus()
            else:
                response = messagebox.askyesno("Подтверждение",
                                               f"Вы уверены, что хотите удалить пользователя с логином {user_login}?")
                if response:
                    user_collection.delete_one({"login": user_login})
                    messagebox.showinfo("Успешно", f"Пользователь {user_login} удален!")
                    update_combobox(users_combobox)  # Обновляем список после удаления
                users_combobox.delete(0, 'end')
                update_combobox(None)
        return

    # Функция для смены пароля
    def change_password(event):
        user_login = users_combobox.get()
        if (user_data["role"] == 'admin'):
            messagebox.showerror("Ошибка", "У Вас отсутсвуют права на выполнение этого действия!")
        else:
            if user_login not in list_users:
                messagebox.showerror("Ошибка", f"Указанный пользователь отсутсвует {user_login}")
                users_combobox.focus()
            else:
                response = messagebox.askyesno("Подтверждение",
                                               f"Вы уверены, что хотите сменить пароль для пользователя {user_login}?")
                if response:
                    new_password = simpledialog.askstring("Новый пароль", "Введите новый пароль для пользователя:",show='*')
                    user_collection.update_one(
                        {"login": user_login},  # Условие для поиска пользователя по логину
                        {"$set": {"password": new_password}}  # Команда на обновление поля пароля
                    )
                    messagebox.showinfo("Успешно", f"Пароль успешно изменен!")

                    users_combobox.delete(0, 'end')
        return

    # Функция для вызова окна где можно создать нового пользователя
    def creat_new_user (event):
        new_user_frame = create_new_user_frame(parent, user_data)
        new_user_frame.place(x=0, y=0, width=720, height=720)  # Отображаем окно профиля

    profile_frame = tk.Frame(parent)
    profile_frame.grid(row=0, column=0, sticky="nsew")  # Установим фрейм так, чтобы он растягивался вместе с окном
    parent.columnconfigure(0, weight=1)  # Делаем колонку растягивающейся
    parent.rowconfigure(0, weight=1)  # Делаем строку растягивающейся
    tk.Label(profile_frame, text="Вы зашли в профиль для администрирования!", fg="red").grid(row=0, column=0, columnspan=3, pady=(20, 0), sticky="nsew")

    tk.Label(profile_frame, text=f"Логин: {user_data['login']}").grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky="nsew")

    list_frame = tk.Frame(profile_frame)
    list_frame.grid(row=2, column=0, columnspan=2, pady=(10,0), sticky="nsew")
    tk.Label(list_frame, text = "Выберите пользователя для редактирования").grid(row=0, column=0)
    list_users = fetch_users()
    users_combobox = Combobox(list_frame,values=list_users)
    users_combobox.grid(row=0, column=1)
    users_combobox.bind("<KeyRelease>", filters_users)

    button_frame = tk.Frame(profile_frame)
    button_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky="nsew")

    tk.Button(button_frame, text="Посмотреть информацию о пользователе", command=lambda: show_user_data(None)).grid(row=0, column=0,sticky="nsew")
    tk.Button(button_frame, text="Удалить пользователя", command=lambda: delete_user(None)).grid(row=0, column=1,sticky="nsew")
    tk.Button(button_frame, text="Изменить пароль для пользователя", command=lambda: change_password(None)).grid(row=0, column=2,sticky="nsew")

    def show_user_result(event):
        user_login = users_combobox.get()
        list_users = fetch_users()
        if user_login not in list_users:
            messagebox.showerror("Ошибка", f"Указанный пользователь отсутсвует {user_login}")
            users_combobox.focus()
        else:
            existing_user = user_collection.find_one({"login": user_login})
            user_id = existing_user['id']
            results_tests = get_user_results(user_id)
            messagebox.showinfo("Информация о пользователе", results_tests)
        return


    def delete_results(event):
        user_login = users_combobox.get()
        existing_user = user_collection.find_one({"login": user_login})
        user_id = existing_user['id']
        response = messagebox.askyesno("Подтверждение",
                                       f"Вы уверены, что хотите удалить результаты для пользователя {user_login}?")
        if response:
            delete_test_result(user_id)
            messagebox.showinfo("Успешно", f"Результаты всех тестов пользователя удалены!")
        return

    def show_average_score(event):
        avrg_score=get_average_scores()
        messagebox.showinfo("Средние баллы за тесты", avrg_score)

    button2_frame = tk.Frame(profile_frame)
    button2_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky="nsew")
    tk.Button(button2_frame, text="Посмотреть результаты тестов пользователя", command=lambda: show_user_result(None)).grid(row=0, column=0, sticky="nsew")
    tk.Button(button2_frame, text="Посмотреть средние баллы по тестам", command=lambda: show_average_score(None)).grid(row=0, column=1,sticky="nsew")
    tk.Button(button2_frame, text="Удалить историю тестов пользователя", command=lambda: delete_results(None)).grid(row=0, column=2,sticky="nsew")

    tk.Button(profile_frame, text="Добавить нового пользователя или администратора", command=lambda: creat_new_user(None)).grid(row=5, column=0, columnspan=3,pady=(40, 20),sticky="nsew")

    tk.Button(profile_frame, text="Выйти из профиля", command=lambda: show_frame(main_frame)).grid(row=6, column=0,columnspan=3,pady=(10, 0),sticky="nsew",)
    return profile_frame


# Функция для создания нового пользователя под администратором
def create_new_user_frame(parent, admin_data):
    register_frame = tk.Frame(parent)

    # Поле для ввода логина
    tk.Label(register_frame, text="Введите логин:").pack(pady=(20, 0))
    login_entry = tk.Entry(register_frame)
    login_entry.pack()

    # Поле для ввода пароля
    tk.Label(register_frame, text="Введите пароль:").pack(pady=(20, 0))
    password_entry = tk.Entry(register_frame, show='*')
    password_entry.pack()

    # Поле для ввода имени пользователя
    tk.Label(register_frame, text="Введите имя пользователя:").pack(pady=(20, 0))
    username_entry = tk.Entry(register_frame)
    username_entry.pack()

    # Поле для ввода даты рождения
    tk.Label(register_frame, text="Введите дату рождения (ДД.ММ.ГГГГ):").pack(pady=(20, 0))
    dob_entry = DateEntry(register_frame, date_pattern='dd.mm.yyyy')
    dob_entry.pack()

    def filter_cities(event):
        search_text = city_combobox.get().lower()
        # Фильтрация и сортировка городов
        filtered_cities = [city for city in cities if search_text in city.lower()]
        filtered_cities.sort(key=lambda city: (not city.lower().startswith(search_text), city))
        city_combobox['values'] = filtered_cities
        city_combobox.focus()

    def on_combobox_click(event):
        city_combobox.event_generate('<Down>')  # Открытие выпадающего списка

    # Поле для ввода города
    tk.Label(register_frame, text="Введите город:").pack(pady=(20, 0))
    city_combobox = Combobox(register_frame, values=cities)
    city_combobox.pack()
    city_combobox.bind("<KeyRelease>", filter_cities)

    tk.Label(register_frame, text="Выберите роль для пользователя").pack(pady=(20, 0))
    roles = ['user', 'admin', 'root']
    role_combobox = Combobox(register_frame, values=roles)
    role_combobox.pack()
    role = role_combobox.get()

    def submit_registration():
        # Сбор данных из формы
        login = login_entry.get()
        password = password_entry.get()
        user_name = username_entry.get()
        dob = dob_entry.get()
        city = city_combobox.get()

        existing_user = user_collection.find_one({"login": login})
        if existing_user:
            messagebox.showerror("Ошибка", f"Пользователь с логином {login} уже существует")
            return

        # Проверка длину пароля
        if len(password) < 5:
            messagebox.showerror("Ошибка", "Пароль слишком короткий, он должен содержать 5 или более символов!")
            return

        if city not in cities:
            messagebox.showerror("Ошибка", "Выбранный город отсутствует в списке допустимых городов!")
            city_combobox.focus()
            return

        # Проверка на заполненность всех полей
        if not (login and password and user_name and dob and city):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        user_data = {
                    "id": generate_unique_id(),
                    "login": login,
                    "password": password,
                    "name": user_name,
                    "birthdate": dob,
                    "city": city,
                    "role": role}

        user_collection.insert_one(user_data)
        print(f"Зарегистрирован новый пользователь: {login}, {user_name},{password}, {dob}, {city}")
        messagebox.showinfo("Успешно", "Пользователь зарегистрирован!")
        admin_frame = create_admin_frame(parent, admin_data)
        register_frame.place_forget()  # Скрываем фрейм регистрации
        admin_frame.place(x=0, y=0, width=720, height=720)

        #Очистка полей формы
        login_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        username_entry.delete(0, 'end')
        dob_entry.delete(0, 'end')
        city_combobox.delete(0, 'end')

    def exit():
        admin_frame = create_admin_frame(parent, admin_data)
        register_frame.place_forget()  # Скрываем фрейм регистрации
        admin_frame.place(x=0, y=0, width=720, height=720)

    # Кнопка для отправки формы
    tk.Button(register_frame, text="Зарегистрировать нового пользователя", command=submit_registration).pack(pady=(20, 0))

    # Кнопка "Назад"
    tk.Button(register_frame, text="Отмена", command=exit).pack()

    return register_frame


def create_login_frame(parent):
    login_frame = tk.Frame(parent)
    tk.Label(login_frame, text="Логин:").pack(pady=(20, 0))
    login_entry = tk.Entry(login_frame)
    login_entry.pack()

    tk.Label(login_frame, text="Пароль:").pack(pady=(20, 0))
    password_entry = tk.Entry(login_frame, show='*')
    password_entry.pack()

    def submit_login():
        login = login_entry.get()
        password = password_entry.get()

        user_data = user_collection.find_one({"login": login})
        if user_data:
            if user_data["password"] == password:
                if user_data["role"] == 'user':
                    print("Вход пользователя:", login_entry.get())
                    login_frame.pack_forget()  # Скрываем окно входа
                    profile_frame = create_profile_frame(parent, user_data)
                    profile_frame.place(x=0, y=0, width=720, height=720)  # Отображаем окно профиля
                else:
                    print("Вход пользователя с правами администратора:", login_entry.get())
                    login_frame.pack_forget()  # Скрываем окно входа
                    profile_frame = create_admin_frame(parent, user_data)
                    profile_frame.place(x=0, y=0, width=720, height=720)  # Отображаем окно профиля
            else:
                messagebox.showerror("Ошибка", f"Неправильный логин или пароль")
        else:
            messagebox.showerror("Ошибка", f"Неправильный логин или пароль")

        login_entry.delete(0, 'end')
        password_entry.delete(0, 'end')

    tk.Button(login_frame, text="Войти", command=submit_login).pack()
    tk.Button(login_frame, text="Назад", command=lambda: show_frame(main_frame)).pack()

    return login_frame


def create_register_frame(parent):
    register_frame = tk.Frame(parent)

    # Поле для ввода логина
    tk.Label(register_frame, text="Введите логин:").pack(pady=(20, 0))
    login_entry = tk.Entry(register_frame)
    login_entry.pack()

    # Поле для ввода пароля
    tk.Label(register_frame, text="Введите пароль:").pack(pady=(20, 0))
    password_entry = tk.Entry(register_frame, show='*')
    password_entry.pack()

    # Поле для ввода имени пользователя
    tk.Label(register_frame, text="Введите имя пользователя:").pack(pady=(20, 0))
    username_entry = tk.Entry(register_frame)
    username_entry.pack()

    # Поле для ввода даты рождения
    tk.Label(register_frame, text="Введите дату рождения (ДД.ММ.ГГГГ):").pack(pady=(20, 0))
    dob_entry = DateEntry(register_frame, date_pattern='dd.mm.yyyy')
    dob_entry.pack()

    def filter_cities(event):
        search_text = city_combobox.get().lower()
        # Фильтрация и сортировка городов
        filtered_cities = [city for city in cities if search_text in city.lower()]
        filtered_cities.sort(key=lambda city: (not city.lower().startswith(search_text), city))
        city_combobox['values'] = filtered_cities
        city_combobox.focus()

    def on_combobox_click(event):
        city_combobox.event_generate('<Down>')  # Открытие выпадающего списка

    # Поле для ввода города
    tk.Label(register_frame, text="Введите город:").pack(pady=(20, 0))
    city_combobox = Combobox(register_frame, values=cities)
    city_combobox.pack()
    city_combobox.bind("<KeyRelease>", filter_cities)

    def submit_registration():
        # Сбор данных из формы
        login = login_entry.get()
        password = password_entry.get()
        user_name = username_entry.get()
        dob = dob_entry.get()
        city = city_combobox.get()

        existing_user = user_collection.find_one({"login": login})

        if existing_user:
            messagebox.showerror("Ошибка", f"Пользователь с логином {login} уже существует")
            return

        # Проверка длину пароля
        if len(password) < 5:
            messagebox.showerror("Ошибка", "Пароль слишком короткий, он должен содержать 5 или более символов!")
            return

        if city not in cities:
            messagebox.showerror("Ошибка", "Выбранный город отсутствует в списке допустимых городов!")
            city_combobox.focus()
            return

        # Проверка на заполненность всех полей
        if not (login and password and user_name and dob and city):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        user_data = {
                    "id": generate_unique_id(),
                    "login": login,
                    "password": password,
                    "name": user_name,
                    "birthdate": dob,
                    "city": city,
                    "role": "user"
                }
        user_collection.insert_one(user_data)
        print(f"Зарегистрировался новый пользователь: {login}, {user_name},{password}, {dob}, {city}")
        messagebox.showinfo("Успешно", "Пользователь зарегистрирован!")
        login_frame = create_login_frame(parent)
        register_frame.place_forget()  # Скрываем фрейм регистрации
        login_frame.place(x=0, y=0, width=720, height=720)

        #Очистка полей формы
        login_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        username_entry.delete(0, 'end')
        dob_entry.delete(0, 'end')
        city_combobox.delete(0, 'end')

    # Кнопка для отправки формы
    tk.Button(register_frame, text="Зарегистрироваться", command=submit_registration).pack(pady=(20, 0))

    # Кнопка "Назад"
    tk.Button(register_frame, text="Назад", command=lambda: show_frame(main_frame)).pack()

    return register_frame


if __name__ == '__main__':
    print(fetch_users())
    client = MongoClient()
    # # Выбор базы данных (если база не существует, она будет автоматически создана)
    db = client['user_database']
    # # Создание коллекции пользователей
    user_collection = db['users']

    if  not user_collection.find_one({"login": "admin"}):
        user_data = {
            "id": generate_unique_id(),
            "login": 'admin',
            "password": '12345',
            "role": "admin"
        }
        user_collection.insert_one(user_data)

    if  not user_collection.find_one({"login": "root"}):
        user_data = {
            "id": generate_unique_id(),
            "login": 'root',
            "password": '12345',
            "role": "root"
        }
        user_collection.insert_one(user_data)

    root = tk.Tk()
    root.title("Главное меню")
    root.geometry('720x720')

    # Создание фреймов для логина, регистрации и главного меню
    main_frame = tk.Frame(root)
    login_frame = create_login_frame(root)
    register_frame = create_register_frame(root)

    for frame in (main_frame, login_frame, register_frame):
        frame.place(x=0, y=0, width=720, height=720)


        # Загрузка и отображение изображения
    image_path = 'images/begin.jpg'
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    image_label = Label(main_frame, image=photo)
    image_label.image = photo  # сохраняем ссылку на изображение
    image_label.place(x=0, y=0)  # Можно настроить положение, если нужно
    # Главное меню с кнопками переключения
    avto_button = tk.Button(main_frame, text="Авторизация", command=lambda: show_frame(login_frame))
    avto_button.place(x=200, y=550, width=100, height=50)

    reg_button = tk.Button(main_frame, text="Регистрация", command=lambda: show_frame(register_frame))
    reg_button.place(x=400, y=550, width=100, height=50)

    # Показываем главное меню
    show_frame(main_frame)

    root.mainloop()
