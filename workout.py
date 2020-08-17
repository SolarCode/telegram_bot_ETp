import random
import main


# create dictionary for connection verb and it's translation
def createDic():
    dictionary = {}
    with open('workout.txt', 'r', encoding='utf8') as file:
        for line in file:
            line_list = line.strip().split(',')
            dictionary[line_list[0]] = line_list[1]
    return dictionary


# loop for exercises translation eng/ru
def mainWork(chat_id):
    verbs_collection = createDic()
    new_offset = None

    # get random verb from list and send it to user
    verb = random.choice(list(verbs_collection.keys()))
    main.greet_bot.send_message(chat_id, verb)

    # loop of workout program
    while True:

        # get update like in main loop
        main.greet_bot.get_updates(new_offset)
        last_update = main.greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']

        # if there were no updates - skip iteration
        if last_update is None:
            continue

        # skip first new update with text /workout otherwise it will be use in if/else and give wrong answer
        if last_chat_text == '/workout':
            new_offset = last_update_id + 1
            continue

        # if chat_text from user == value of verb(key in dict) send message = Correct
        if last_chat_text == verbs_collection[verb]:
            main.greet_bot.send_message(chat_id, 'Correct :)')
        # exit from workout program
        elif last_chat_text == '/exit':
            break
        else:
            # if chat_text from user != value of verb(key in dict) send message = Correct
            main.greet_bot.send_message(chat_id, 'Nope :(  /  ' + verbs_collection[verb])

        verb = random.choice(list(verbs_collection.keys()))
        main.greet_bot.send_message(chat_id, verb)

        # add + 1 to id update, until new update is coming the loop will be stop
        new_offset = last_update_id + 1
