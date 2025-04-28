import pandas as pd
import word_classifier as worder
#data = pd.read_csv("fias_dict/fias_dict.csv")

data_parsed = []

def parse_data(value):
    row_data = []
    #for j in range(len(data.columns)):

    #if "к." in value:
    #  pos = value.find("к.")
    #  value = value[:pos-1] + "," + value[pos-1:]
#
    #if "литера" in value:
    #  pos = value.find("литера")
    #  value = value[:pos-1] + "," + value[pos-1:]

    # Разбиваем по запятым
    parts = value.split(",")


    # Убираем лишние пробелы и пустые строки
    parts = [worder.cleanup_words(part.strip()) for part in parts if part.strip() != "" and not part.strip() == "Санкт-Петербург г"]
    row_data.extend(parts)

    #print("==="+str(row_data))
    return row_data

# for i in range(len(data.iloc[0:10000])):
#     #for j in range(len(data.columns)):
#         value = str(data.iloc[i, 1])

#         row_data = parse_data(value)

#         data_parsed.append(row_data)

# # Преобразуем в DataFrame
# data_parsed_df = pd.DataFrame(data_parsed)