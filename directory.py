# create dictionary for connection verb and it's description
def createDic():
    dictionary = {}
    with open('directory.txt', 'r', encoding='utf8') as file:
        for line in file:
            line_list = line.strip().replace('-', '\n').split(',')
            dictionary[line_list[0]] = line_list[1]
    return dictionary


# create verbs_list from keys then we will check input to this list
def mainDir():
    verbs_collection = createDic()
    verbs_list = list(verbs_collection.keys())
    return verbs_list
