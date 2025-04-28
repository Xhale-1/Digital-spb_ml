import word_classifier as worder
import address_storage as addr
import request_receiver as req
import visualiser as vis
import fuzzer as f
import pandas


print("============APPLICATION TESTING START============")
CHUNK_SIZE = 1

worder.read_replacements()
a = pandas.read_csv("fias_dict/fias_dict.csv", delimiter=',', quotechar='"', chunksize=CHUNK_SIZE, iterator=True)

chunk_count = 0
chunks_to_read = 1
print("Chunk size:", CHUNK_SIZE)

global tree_start
tree_start = None

if addr.address_tree.layer_file_exists("main"):
    print("Loading addresses...")
    #addr.address_tree.load_layer("main")
    addr.address_tree.load_layer("main")

    first_node = list(addr.address_tree.node_layers["main"].keys())[0]

    tree_start = addr.address_tree.get_node("main", first_node)
    print(tree_start.connections)
    for chunk in a:
        print(chunk_count*CHUNK_SIZE, " - ", (chunk_count+1)*CHUNK_SIZE)
        for i in chunk["address"]:
            line = i
            worder.learn_line(line)
            #print(i)
        for i in range(len(chunk["address"])):
            cur_addr = chunk["address"][i+chunk_count*CHUNK_SIZE]
            cur_id = int(chunk["id"][i+chunk_count*CHUNK_SIZE])

            #addr.add_search_entry(cur_addr, cur_id)
        chunk_count += 1
        if chunk_count >= chunks_to_read:#20:
            
            break
else:
    print("Learning addresses...")
    for chunk in a:
        print(chunk_count*CHUNK_SIZE, " - ", (chunk_count+1)*CHUNK_SIZE)
        for i in chunk["address"]:
            line = i
            worder.learn_line(line)
            #print(i)

        for i in range(len(chunk["id"])):
            addr.learn_address(chunk["address"][i+chunk_count*CHUNK_SIZE], int(chunk["id"][i+chunk_count*CHUNK_SIZE]))
        chunk_count += 1
        addr.address_tree.forget_graph();
        if chunk_count >= chunks_to_read:#20:
            tree_start = addr.address_tree.get_node("main", "г Санкт-Петербург")
            break

for i in addr.address_list:
    print(i, addr.address_list[i])

print("Finished learning addresses")
