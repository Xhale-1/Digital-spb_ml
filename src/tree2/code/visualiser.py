def print_tree(tree, maxlevel = -1, level = 0):
    for i in tree:
        print(("-"*level) +str(i))
        if level != maxlevel:
            if type(tree[i]) == dict:
                print_tree(tree[i], maxlevel, level + 1)
            else:
                print(("-"*level) + str(tree[i]))