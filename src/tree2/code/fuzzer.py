from fuzzywuzzy import fuzz

def fuzz_get(look_for, search_list):
    print("ooking for:", look_for)
    maxweight = 0
    result = list(search_list)[0]
    for i in search_list:
        weight = fuzz.ratio(look_for, i)
        #print(i, weight)
        if weight > maxweight and i != '':
            result = i
            maxweight = weight
    
    print("---"+result    , "==", look_for, "with weight", maxweight)
    return result, maxweight

def fuzz_get_variants(look_for_list, search_list):
    maxweight = -99
    result = list(search_list)[0]
    for i in search_list:
        for x in look_for_list:
            weight = fuzz.ratio(x, i)
            if weight > maxweight:
                result = i
                maxweight = weight
    return result, maxweight


