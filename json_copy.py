import requests
import json
import sys
from requests_oauthlib import OAuth1



def check_type(curr):
    '''
    (dict/list) --> str
    Takse the data of some type and
    returns the string to represent the type
    '''
    if isinstance(curr, dict):
        return "dictionary"
    elif isinstance(curr, list):
        return "list"
    else:
        return "unknown"

def list_info():
    '''
    Prints the information about available commands in list
    '''
    print("COMMANDS:")
    print("len - to check the length of current level")
    print("index - to choose the index of next level to go")
    print("type - to check the data type of the current level")
    print("back - to go previous level")
    print("exit - to stop the program")

def dict_info():
    '''
    Prints the information about available commands in dict
    '''
    print("COMMANDS:")
    print("len - to check the length of current level")
    print("keys - to check the available keys")
    print("level - to chose the next level to go")
    print("type - to check the data type of the current level")
    print("back - to go previous level")
    print("exit - to stop the program")


def manager(data, current, level):
    val = ""
    if (isinstance(current, list)):
        if (len(current) > 0):
            list_info()
            while not val:
                command = input(">>>")
                if command == "len":
                    print(len(current))
                if command == "type":
                    print(check_type(current))
                if command == "exit":
                    sys.exit()
                if command == "back":
                    current = data
                    for curr_level in level[:-1]:
                        current = current[curr_level]
                    manager(data, current, level[:-1])
                if command == "index":
                    val = input("Write the index of next level: ")
                    if (not (val.isdigit() and (0 <= int(val) < int(len(current))))):
                        pass
                    else:
                        level.append(int(val))
                        manager(data, current[int(val)], level)

        else:
            print('You have reached the end')
            manager(data, current, level)

    elif (isinstance(current, dict)):
        dict_info()
        while not val:
            command = input(">>>")
            if command == "keys":
                for k in current.keys():
                    print(k)
            if command == "len":
                print(len(current.keys()))
            if command == "type":
                print(check_type(current))
            if command == "exit":
                sys.exit()
            if command == "back":
                current = data
                for curr_level in level[:-1]:
                    current = current[curr_level]
                manager(data, current, level[:-1])
            if command == "level":
                val = input("Write the next level: ")
                if not val in current.keys():
                    print("Missing value")
                else:
                    level.append(val)
                    manager(data, current[val], level)
    else:
        print("The final value: " + str(current))
        print("COMMANDS:")
        print("back - to go previous level")
        print("exit - to stop the program")
        command = input(">>>")
        if command == "back":
            current = data
            for curr_level in level[:-1]:
                current = current[curr_level]
            manager(data, current, level[:-1])
        if command == "exit":
            sys.exit()
        else:
            pass



if __name__ == "__main__":
    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    auth = OAuth1("API_KEY",
                  "API_SECRET",
                  "ACCESS_TOKEN",
                  "ACCESS_TOKEN_SECRET")
    requests.get(url, auth=auth)
    name = input("Write the name of twitter user: ")
    req = requests.get(
        'https://api.twitter.com/1.1/friends/list.json?screen_name=' + name, auth=auth)

    manager(req.json(), req.json(), [])

    # If some problems with API, you can check attached file:
    # json_data = open("user_friends.json").read()
    # data = json.loads(json_data)
    #
    # manager(data, data, [])