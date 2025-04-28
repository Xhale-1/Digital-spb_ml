import word_classifier as worder
from word_classifier import cleanup_words
from data_classifier import parse_data
from tree import Graph
import json


def calc_layer_name(ownedby, owner_of_owner):
    return str(owner_of_owner) + "-" + str(ownedby)

address_graph = dict()
address_list = dict()
address_tree = Graph("address_tree")
address_list_buffer = dict()
address_buffer_number = 0
address_list_buffers = dict()

address_tree.add_node("г Санкт-Петербург", "main", "г Санкт-Петербург")
part_size = 300000

def buffer_by_id(searchnum):
    global part_size
    file_id = searchnum//part_size
    return file_id


def change_address_buffer(bufferid):
    global address_buffer_number
    global address_buffer_number
    if bufferid != address_buffer_number:
        save_address_buffer()
        load_address_buffer(bufferid)

def add_entry(address, new_id):
    global address_buffer_number
    global address_buffer_number
    bid = buffer_by_id(new_id)

    if bid not in address_list_buffers:
        if load_address_buffer(bid):
            address_list_buffers = address_list_buffer
        else:
            address_list_buffers[bid] = {}

def load_address_buffer(bufferid):
    return
    global address_list_buffer
    global address_buffer_number
    address_buffer_number = bufferid

    try:
        f = open("search_vocab/"+str(address_buffer_number)+".json", "r")
        jsdump = f.read()
        f.close()
        address_list_buffer = json.loads(jsdump, ensure_ascii=False)
    except:
        return False
    finally:
        return True

def save_address_buffer():
    return
    global address_list_buffer
    jsdump = json.dumps(address_list_buffer, ensure_ascii=False)
    f = open("search_vocab/"+str(address_buffer_number)+".json", "w")
    f.write(jsdump)
    f.close()

def add_search_entry(address, new_id):
    bid = buffer_by_id(new_id)
    change_address_buffer(bid)
    address_list_buffer[str(new_id)] = address

def get_search_entry(search_id):
    bid = buffer_by_id(search_id)
    change_address_buffer(bid)
    return  address_list_buffer[str(search_id)]

# def save_address_vocab():
#     global address_list
#     for i in address_list:
#         addrnum = int(i)

# def add_to_address_list():


# def get_address_by_id(search_id):


def learn_address(address, new_id):
    global address_graph
    global address_tree

    current = address_tree.get_node("main","г Санкт-Петербург")
    prevname = "main"
    #address_list[new_id] = address
    add_search_entry(address, new_id)
    #l = address.split(", ")
    l = parse_data(address)
    for x in range(len(l)):
        i = l[x]
        w = cleanup_words(i)

        new_layer = calc_layer_name(current.name, prevname)
        new_value = i

        if x >= len(l)-1:
            new_value = new_id


        #con_to = current.connections[new_layer]

        if not address_tree.node_exists(new_layer, i):
            next_node = address_tree.add_node(i, new_layer, new_value)
        else:
            next_node = address_tree.get_node(new_layer, i)
        current.add_connection(next_node.name, new_layer)
        
        prevname = calc_layer_name(current.name, prevname)
        current = next_node