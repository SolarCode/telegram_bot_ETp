import requests
import datetime


class BotHandler:

    # Конструктор класса BotHandler, объект класса будет создан сразу с обязательным свойством token.
    # self – ссылка на сам только что созданный объект. self.token и self.api_url - это свойства объекта, мы можем
    # использовать их если укажем в методе ссылку на сам объект
    def __init__(self, token):
        self.token = token
        # здесь вставляем токен в url, это будет базой для дальнейших запросов к api бота
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    # метод отправляет запрос на сервер бота, а в ответ получает json файл со всеми обновлениям бота за последние 24
    # часа. Timeout - ограничение для количества запросов, offset - метка для уже просмотренных обновлений
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    # выделяем только последнее обновления из словаря всех обновлений
    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            # сюда попадаем если get_result вернул 0, значит обновлений не было и мы должы вренуть None, чтобы потом
            # пропустить итерацию в цикле, т.к обновлений не было и она не нужна. Происходит как бы работа программы в
            # ожидании обновления, как только обновление будет получено, цикл пройдет дальше.
            last_update = None

        return last_update


# создаем объект класса BotHandler, в момент создания автоматически происходит вызов функции __init__,
# в который мы должны передать токен, иначе объект не будет создан
greet_bot = BotHandler('your_token')
# список приветствий от человека, бот будет проверять обновления и если в месседже содержится приветствие из
# этого списка, то он отправит ответ
greetings = ('hello', 'hi', 'hey')
# фиксируем какая сейчас дата и время
now = datetime.datetime.now()


# метод с основным циклом программы, откуда будут запросы в другие методы
def main():
    # переменная для отметки уже просмотренных обновлений, см. ниже в конце цикла
    new_offset = None
    # для ответа в зависимости от времени, нам потребует выделить из now только день и час
    today = now.day
    hour = now.hour

    # основной цикл программы
    while True:
        # получаем обновления бота за последние 24 часа, вместе с вызовом функции мы передаем значение None в параметр
        # сдвига, это начальное значение для переменной, затем мы присвоем ей значение id обвновления + 1
        # благодарям этому мы как бы пометим уже просмотренные обновления и будем ждать следующее обновление с новым id
        # значение, которого было присвоено new_offset
        greet_bot.get_updates(new_offset)

        # из всех обновлений выделяем только последнее
        last_update = greet_bot.get_last_update()

        # Если обновлений не было оно вернет None, тогда пропускаем эту итерацию и цикл начинается заново
        if last_update is None:
            continue

        # получаем update_id он понадобится для отметки уже просмотренных обновлений и сдвига цикла
        last_update_id = last_update['update_id']
        # получаем text сообщения, далее мы проверим его со списком значений
        last_chat_text = last_update['message']['text']
        # получаем id чата, оно понадобиться для ответа бота
        last_chat_id = last_update['message']['chat']['id']
        # получаем имя отправителя, используем его в ответе бота
        last_chat_name = last_update['message']['chat']['first_name']

        # одинаковые проверки времени и сборка ответа бота в зависимости от времени суток
        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
            # прибавляем + 1 к дню после отправки сообщения, это говорит о том, что
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
            today += 1

        # прибавляем значение, в дальнейшем это будет означать отработку по этому обновлению и переход к ожиданию
        # следующего обновления
        new_offset = last_update_id + 1


# запуск основного цикла (программы) отсюда
if __name__ == '__main__':
    try:
        main()
    # Исключение KeyboardInterrupt вызывается при попытке остановить программу с помощью сочетания
    # Ctrl + C или Ctrl + Z в командной строке. Иногда это происходит неумышленно и подобная обработка поможет избежать
    # подобных ситуаций.
    except KeyboardInterrupt:
        exit()
