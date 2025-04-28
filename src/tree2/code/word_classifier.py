import sys
import json

#print(sys.getdefaultencoding())

word_classes = dict()

replacements = {}

def read_replacements():
    global replacements
    try:
        f = open("word_cleanup/replacements.json")
        jsdump = f.read()
        replacements = json.loads(jsdump)
        f.close()
    finally:
        return

def cleanup_words(pos):
    global replacements
    new_pos = pos
        
    for i in replacements:
        new_pos = new_pos.replace(i, replacements[i])

    return new_pos


def parse_words(pos):
    pos = cleanup_words(pos)
    words = pos.split()
    return words

def learn_word(word, new_class):
    global word_classes
    current = word_classes
    l = word[:3]
    if not l in word_classes:
        word_classes[l] = [new_class]
    else:
        word_classes[l].append(new_class)


def classify_word(word):
    result = [-1]
    global word_classes
    w = word[:3].lower()

    if w in word_classes:
        #print("classifyin:", word, word_classes[w])
        return word_classes[w]
    else:
        return [-1]

def learn_line(line):
    line = line.lower()
    positions = line.split(", ")
    for i in range(len(positions)):
        words = parse_words(positions[i])
        for w in words:
            learn_word(w, i)