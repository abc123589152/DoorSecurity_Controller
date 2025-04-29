import time
openLimit = 15
def limittime(openLimit):
    status = ""
    while openLimit >0:
        with open("/Users/yangfuen/codingtest/door_status","r") as readline:
            if (readline.read().strip() == "open"):
                openLimit-=1
                print(openLimit)
                status = "1"
            else:
                status = "0"
                break;
        time.sleep(1)
    if status == "1":
        print("開門過久")
    else:
        print("關門")
limittime(openLimit)
#time.sleep(openLimit)
    