import pickle

def load_pickle_data(filename):
    """ Загружаем данные из файла pickle. """
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        print("Файл не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return None


def print_structure(data, indent=0):
    """ Рекурсивно печатаем структуру данных. """
    if isinstance(data, dict):
        for key, value in data.items():
            print('  ' * indent + str(key) + ':')
            print_structure(value, indent+1)
    elif isinstance(data, list):
        print('  ' * indent + 'List of ' + str(len(data)) + ' items')
        if data:
            print_structure(data[0], indent+1)
    elif isinstance(data, set):
        print('  ' * indent + 'Set of ' + str(len(data)) + ' items')
    else:
        print('  ' * indent + str(type(data)))

filename = 'results.pkl'  # Измените на имя вашего файла pickle
data = load_pickle_data(filename)
if data is not None:
    print("Структура загруженных данных:")
    print_structure(data)
else:
    print("Данные не загружены.")
