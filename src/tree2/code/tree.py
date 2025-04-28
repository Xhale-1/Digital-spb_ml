import os
from flask import jsonify
import json

class Node:
    def __init__(self, name, value):
        self.name = str(name)
        self.value = value
        self.connections = dict()

    def add_connection(self, b, layer):
        if not layer in list(self.connections.keys()):
            self.connections[layer] = []

        if type(b) == str:
            if not b in self.connections[layer]:
                self.connections[layer].append(b)
        if type(b) == Node:
            if not b.name in self.connections[layer]:
                self.connections[layer].append(b.name)

    def get_total_connections(self):
        s = 0
        for i in self.connections:
            s += len(self.connections[i])
        return s
    
    def get_connections(self):
        return self.connections
    
    def get_nodes_at_layer(self, layer):
        return self.connections[layer]

class Graph:
    def __init__(self, name):
        self.name = name
        self.node_layers = dict()
        self.pathbase = "data_graph/"
        self.last_changed = "main"

    def layer_exists(self, layer):
        result = layer in self.node_layers

        if result:
            if len(self.node_layers[layer]) == 0:
                result = False
        return result

    def layer_file_exists(self, layer):
        result = True
        try:
            f = open(self.pathbase+layer+".json", "r")
            f.close()
        except:
            result = False
        finally:
            return result

    def add_node(self, name, layer = "main", value = None, do_load_layer = True):
        new_node = Node(name, value)

        should_add_layer = not layer in self.node_layers

        if not should_add_layer:
            if len(self.node_layers[layer]) == 0:
                should_add_layer = True

        if should_add_layer:
            if self.layer_file_exists(layer) and do_load_layer:
                self.load_layer(layer)
            else:
                self.node_layers[layer] = dict()

        self.node_layers[layer][name] = new_node
        return new_node

    def node_exists(self, layer, name):
        if self.layer_exists(layer):
            return name in self.node_layers[layer]
        else:
            return False

    def get_node(self, layer, name):
        if not self.layer_exists(layer):
            if self.layer_file_exists(layer):
                print("Loading layer ", layer)
                self.load_layer(layer)
            else:
                print("Layer does not exist and it's file can not be opened!")

        if self.layer_exists(layer):
            if self.node_exists(layer, name):
                return self.node_layers[layer][name]
            else:
                return None
        else:
            return None
    
    def forget_layer(self, layer):
        if layer == self.last_changed:
            return
        
        self.save_layer(layer)
        del self.node_layers[layer]

    def forget_graph(self):
        self.save_graph()

        self.node_layers = dict()

    def node_to_dict(self, node):
        result = dict()
        result["name"] = node.name
        result["value"] = str(node.value)
        result["connections"] = dict()
        for i in node.connections:
            result["connections"][i] = []
            for x in node.connections[i]:
                result["connections"][i].append(x)
        return result
    
    def node_from_dict(self, data, layer):
        name = data["name"]
        value = data["value"] #I aint expecting anything in value field yet but strings

        node = self.add_node(name, layer, value, False)
        #node = 

        for i in data["connections"]:
            for n in data["connections"][i]:
                self.get_node(layer, name).add_connection(n, i)
    
    def save_layer(self, layer_name):
        to_save = dict()
        for i in self.node_layers[layer_name]:
            current_node = self.node_layers[layer_name][i]

            to_save[i] = self.node_to_dict(current_node)
        save_string = json.dumps(to_save, ensure_ascii=True)

        try:
            f = open(self.pathbase + layer_name + ".json", "w")
            f.write(save_string)
            f.close()
        finally:
            return
    
    def load_layer(self, layer_name):
        datastr = ""
        print("Reading layer", layer_name, "from file", self.pathbase+layer_name+".json")
        try:
            f = open(self.pathbase+layer_name+".json", "r")
        except:
            print("Layerfile for", layer_name, "does not exist!")
        finally:
            datastr = f.read()
            f.close()
            data = json.loads(datastr)#, ensure_ascii=False)
            #print(data)

            for i in data.keys():
                d = data[i]
                self.node_from_dict(d, layer_name)
        return

    def save_graph(self):
        for i in self.node_layers:
            self.save_layer(i)
        return
    

