import word_classifier as worder
import address_storage as addr
import visualiser as vis
import fuzzer as f
import requests
import json

def parse_request(req_str):
    result = dict()  # Автоматически инициализирует новые ключи
    words = []
    
    try:
        # Правильное формирование JSON
        response = requests.post(
            "http://ai:5100/analyze",
            json={"line": req_str},  # requests сам сериализует в JSON
            timeout=5
        )
        response.raise_for_status()  # Проверка на ошибки HTTP
        
        print("Raw response:", response.text)
        
        # Парсинг ответа
        inter_result = response.json()  # Встроенный метод для парсинга JSON
        print(response.text)

        # Обработка данных
        for item in inter_result:
            try:
                wc = int(item["type"])
                w = item["value"]
                words.append(w)
                result[wc].append(w)  # defaultdict автоматически создаст список
            except (KeyError, ValueError) as e:
                result[wc] = []
                print(f"Error processing item {item}: {e}")
                
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise  # Или обработайте ошибку по-другому
        
    return result, words





def parse_request_old(req_str):
    result = {}

    req_str = req_str.lower()
    words = worder.parse_words(req_str)
    last_class = 0
    for w in words:
        word_class = worder.classify_word(w)
        #print(word_class)
        for wc in word_class:
            if wc in result.keys():
                if not w in result[wc]:
                    if wc >= last_class:
                        result[wc].append(w)
                        last_class = wc
                        break
            else:
                result[wc] = [w]
    return result, words

def cur_process(c):
    if type(c) != int:
        count = 10
        output = []
        for i in c:
            output.append(i)
            count -= 1
            if count <= 0:
                break
        return output
    else:
        return [c, addr.address_list[c]]

#Classified words have next format [{"type":1, "value":"пушистого"},{...},...]
def get_address_by_classified(list_classified_words, starting_node): 
    thresh = 45
    print("Looking for:", list_classified_words)
    last_weight = 100
    classified_words = dict()

    for i in list_classified_words:
        if i["type"] in classified_words.keys():
            classified_words[i["type"]].append(i["value"])
        else:
            classified_words[i["type"]] = [i["value"]]

    tokens = classified_words
    print("Tokens:", tokens)

    cur = starting_node#addr.address_tree.get_node("main","г Санкт-Петербург")
    # print(cur.name, "and it's connections", cur.connections)

    count = 0
    while type(cur) != int and count < 10 and last_weight > thresh:
        print(tokens)
        if count in tokens:
            token = tokens[count]
            w = token


            if len(token) != 0:
                #print(w, cur.keys())
                #w = " ".join(token)
                last_lr = ""
                
                print(cur.name,"connects to:", cur.connections)
                
                if cur.get_total_connections() == 0:
                    print("Reached value: ", cur.value)
                    return [cur.value]
                
                for con_lr in cur.connections:
                    # r = " ".join(raw_words)
                    thresh = 50 * 3 / len(" ".join(w))
                    name, weight = f.fuzz_get(" ".join(w), cur.connections[con_lr])    
                    last_weight = weight               
                    last_lr = con_lr
                
                if last_weight > thresh:
                    print("Next node is", name)
                    cur = addr.address_tree.get_node(last_lr, name)
        count += 1
    if len(list(cur.connections.keys())) > 0:
        return cur_process(cur.connections[list(cur.connections.keys())[0]])
    else:
        return [cur.value]

def get_address(req_str, starting_node):
    thresh = 45
    print("Looking for:", req_str)
    last_weight = 100
    tokens, raw_words = parse_request(req_str)



    cur = starting_node#addr.address_tree.get_node("main","г Санкт-Петербург")
    print(cur.name, "and it's connections", cur.connections)

    count = 0
    while type(cur) != int and count < 10 and last_weight > thresh:
        print(tokens)
        if count in tokens:
            token = tokens[count]
            w = token


            if len(token) != 0:
                #print(w, cur.keys())
                #w = " ".join(token)
                last_lr = ""
                
                print(cur.name,"connects to:", cur.connections)
                
                if cur.get_total_connections() == 0:
                    print("Reached value: ", cur.value)
                    return [cur.value]
                
                for con_lr in cur.connections:
                    r = " ".join(raw_words)
                    thresh = 50 * 3 / len(" ".join(w))
                    name, weight = f.fuzz_get(" ".join(w), cur.connections[con_lr])    
                    last_weight = weight               
                    last_lr = con_lr
                
                if last_weight > thresh:
                    print("Next node is", name)
                    cur = addr.address_tree.get_node(last_lr, name)
        count += 1
    if len(list(cur.connections.keys())) > 0:
        return cur_process(cur.connections[list(cur.connections.keys())[0]])
    else:
        return [cur.value]





