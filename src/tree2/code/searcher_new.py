import pandas as pd
from fuzzywuzzy import process

def fuzzy_search_address(query, csv_file, threshold=70):
    """
    Выполняет нечёткий поиск адреса в CSV-файле и возвращает соответствующий id.

    :param query: Строка запроса для поиска адреса.
    :param csv_file: Путь к CSV-файлу с данными.
    :param threshold: Минимальный порог схожести (по умолчанию 70).
    :return: Список кортежей с найденными id и их схожестью.
    """
    # Чтение CSV-файла
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Файл {csv_file} не найден.")
        return []

    if 'id' not in df.columns or 'address' not in df.columns:
        print("CSV-файл должен содержать столбцы 'id' и 'address'.")
        return []

    print("started reading csv file")

    # Извлечение списка адресов
    addresses = df['address'].tolist()
    ids = df['id'].tolist()

    print(len(addresses))

    # Нечёткий поиск
    print("Running search")
    result = process.extract(query, addresses, limit=min(threshold, len(addresses)))

    # Фильтрация результатов по порогу схожести
    filtered_results = [
        (ids[addresses.index(match)], match, score)
        for match, score in result
        if score >= threshold
    ]

    return filtered_results



#if __name__ == "__main__":
    # Пример использования
    #csv_file = "fias_dict/fias_dict.csv"  # Путь к вашему CSV-файлу
    

    #if results:
    #    print("Результаты поиска:")
    #    for address_id, address, score in results:
    #        print(f"ID: {address_id}, Адрес: {address}, Схожесть: {score}%")
    #else:
        #print("Адрес не найден.")