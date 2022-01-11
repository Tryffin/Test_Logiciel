
import requests, json

def send_message():
    """ TODO """
    print("Please enter the message")
    PORT = "90"
    SRVADR = "127.0.0.1"
    SUBURL = "/message"
    URL = "http://" + SRVADR + ":" + PORT + SUBURL
    mesg = input()
    data = mesg
    r = requests.post(URL, data=json.dumps(data))
    if r.status_code == 500:
        print("Can't send this message")
    else:
        return r

def add_user():
    """ TODO """
    print("Please enter the name and password in this form:<name> <password>")
    PORT = "90"
    SRVADR = "127.0.0.1"
    SUBURL = "/add_user"
    URL = "http://" + SRVADR + ":" + PORT + SUBURL
    userinfo = input()
    data = userinfo
    r = requests.post(URL, data=json.dumps(data))
    if r.status_code == 500:
        print("Can't add this person in the database")
    else:
        return r

def require_ip():
    """ TODO """
    print("Please enter the name for searching her/his IP adress")
    name = input()
    PORT = "90"
    SRVADR = "127.0.0.1"
    SUBURL = "/ip"
    FUNC = '?name=' + name
    URL = "http://" + SRVADR + ":" + PORT + SUBURL + FUNC
    r =  requests.get(URL)
    if r.status_code == 500:
        print("Can't find this person in the database")
    else:
        return print(r.text)
    

def disconnect():
    """ TODO """
    pass

if __name__ == '__main__':

    while True:
        
        print("Veuillez saisir la fonctionalite")
        print("1.Add user 2.Send Message 3.Get IP")

        cmd = input()

        if cmd == '1':
            add_user()
        elif cmd == '2':
            send_message()
        elif cmd == '3':
            require_ip()
            