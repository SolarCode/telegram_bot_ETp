import requests
import workout
import directory


class BotHandler:

    # Constructor of BotHandler class, object will be create at once with the required property token.
    # self – link to that object, self.token and self.api_url - it's property of object, we can use them if indicate
    # link to object
    def __init__(self, token):
        self.token = token
        # put token in url, it will be base for request to bot api
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    # method send request to bot server. response json-file with all updates in 24 hours. Timeout - limit for count of
    # requests, offset - mark of watched updates
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        # once this error appear, for now i think it disappeared :) it's code for catching and check her
        try:
            print(resp.json(), 'try')
            result_json = resp.json()['result']
        except KeyError:
            print(resp.json(), 'except')
            resp.json()['result'] = []
            print(resp.json(), 'except')
            result_json = resp.json()['result']

        return result_json

    # method of sending messages
    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    # get only last update from dictionary of all updates
    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            # if we are here get_result return 0, it means update wasn't there we must return None
            last_update = None

        return last_update


# create object of class BotHandler, in moment of creation happens start method __init__, where we must send token
# otherwise object won't be create
greet_bot = BotHandler('token')


def main():
    # variable for mark of watched updates
    new_offset = None

    # main loop of program
    while True:
        # get update of bot in 24 hour, with calling of method we give None in shift parameter it start value
        # for variable after we set value id + 1 thereby we mark already watched updates and will wait new update with
        # this id of variable new_offset
        greet_bot.get_updates(new_offset)

        # save last update for opportunity to stop loop
        last_update = greet_bot.get_last_update()

        # if update wasn't there it returns None, then will skip this iteration.
        # the program is waiting for a new update
        if last_update is None:
            continue

        # get update_id it need for mark already watched updates
        last_update_id = last_update['update_id']
        # get text of message, after we will compare with a list of values
        last_chat_text = last_update['message']['text']
        # get id of a chat, it needs for answer of the bot
        last_chat_id = last_update['message']['chat']['id']

        if last_chat_text.lower() == '/workout':
            greet_bot.send_message(last_chat_id, 'Great idea! For return send /exit. '
                                                 'Now translate this verb into russian:')
            workout.mainWork(last_chat_id)
        elif last_chat_text.lower() == '/start':
            greet_bot.send_message(last_chat_id, 'Hey, dude! Send an irregular verb for information about it '
                                                 '(available 50 frequently used) or use '
                                                 '/help to get a list of commands.')
        elif last_chat_text.lower() == '/help':
            greet_bot.send_message(last_chat_id, 'I can accept only these commands:\n'
                                                 '/workout - begin translation training (eng/ru)\n'
                                                 '/start - intro\n'
                                                 '/about - info about the bot\n')
        elif last_chat_text.lower() == '/about':
            greet_bot.send_message(last_chat_id, 'Hey, this is Viktor, creator of this bot. He can do two things:\n'
                                                 'First: give info about an irregular verb which you send him '
                                                 '(available 50 frequently used).\n'
                                                 'Second: train you by sending a verb, in response you must send its '
                                                 'translation.\n'
                                                 'Our goal is to help you learn irregular verbs a little.\n'
                                                 'We hope we can do it. Good luck and have a nice day :)')

        elif last_chat_text.lower() in directory.mainDir():
            dictionary = directory.createDic()
            greet_bot.send_message(last_chat_id, dictionary[last_chat_text.lower()])

        # add + 1 to id update, until new update is coming the loop will be stop
        new_offset = last_update_id + 1


# start program (main) here
if __name__ == '__main__':
    try:
        main()
    # Except KeyboardInterrupt calling when is attempt stop program by Ctrl + C or Ctrl + Z
    except KeyboardInterrupt:
        exit()
