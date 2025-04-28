import word_classifier as worder
import address_storage as addr
import visualiser as vis
import fuzzer as f
import pandas
import searcher as ser

worder.learn_word("100-я", 0)
worder.learn_word("100кв", 1)
worder.learn_word("100стр", 2)

print(worder.word_classes)
print(ser.parse_request("100"))