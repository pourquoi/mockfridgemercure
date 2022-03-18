import json
import datetime
import time
import urllib
import threading
import requests
import sseclient

#API_ENDOINT = 'https://api-helpyourshelf.matters-test.tech'
API_ENDOINT = 'http://localhost:8080'
#MERCURE_ENDPOINT = 'https://mercure-helpyourshelf.matters-test.tech/.well-known/mercure'
MERCURE_ENDPOINT = 'http://localhost:83/.well-known/mercure'
FRIDGE_UUID = 'a5e27392-0088-4799-9b5d-8a76b7a75c45' # dev
#FRIDGE_UUID = 'ab3bcb6f-e1f6-43e0-8064-adc47e9849d8' # master
#FRIDGE_UUID = '9158815a-9b69-4f8b-8335-feb263aadf57' # demo
PING_FREQUENCY = 60


def ping():
    while True:
        try:
            # toujours la meme route pour le ping.. à voir plus tard pour ajouter une vraie route /ping
            get_door_status()
        except requests.exceptions.RequestException as e:
            print(e)
        except Exception as e:
            print(e)
        time.sleep(PING_FREQUENCY)


def open_door():
    print('opening door')
    try:
        # c'est bizarre comme logique mais c'est le comportement actuel
        get_door_status()
    except Exception as e:
        print(e)

    post_door_status(1)

    time.sleep(5)

    post_door_status(0)

    time.sleep(7)

#    headers = {'Accept': 'application/json'}
#    data = {'epc': "e28011700000020a7f69645b 0 0 0,e28011700000020a7f695abb 0 0 0,e28011700000020aa7bdf233 0 0 0,e28011700000020aa7bdd083 0 0 0,e28011700000020aa7bed472 0 0 0,e2801170000002ae3379b19d 0 0 0,e28011700000020aa7bf5002 0 0 0,e28011700000020aa7bd9223 0 0 0,e28011700000020cc487c80a 0 0 0,e28011700000020aa7bdd093 0 0 0"}
#    response = requests.post(API_ENDOINT + '/fridge_api/fridge/' + FRIDGE_UUID + '/rfid_report', headers=headers,
#                             json=data)


def get_door_status():
    headers = {'Accept': 'application/json'}
    response = requests.get(API_ENDOINT + '/fridge_api/fridge/' + FRIDGE_UUID + '/door_status', headers=headers)
    print('door_status ' + str(response.content))
    return json.loads(response.content)


def post_door_status(status):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    data = {'door_status': status}
    response = requests.post(API_ENDOINT + '/fridge_api/fridge/' + FRIDGE_UUID + '/change_door_status', headers=headers, json=data)
    print(response.content)


def main():
    #ping_thread = threading.Thread(target=ping)
    #ping_thread.start()

    while True:
        try:
            door_status = get_door_status()
        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep(10)
            continue
        except Exception as e:
            print(e)
            time.sleep(10)
            continue

        try:
            if door_status['opened']:
                open_door()
        except Exception as e:
            print(e)

        print('waiting for events')

        headers = {'Accept': 'text/event-stream'}
        try:
            with requests.get(MERCURE_ENDPOINT + '?' + urllib.parse.urlencode({'topic': 'https://example.com/fridge/' + FRIDGE_UUID + '/door_status'}, True), stream=True, timeout=(5,60), headers=headers) as response:
            #with requests.get(MERCURE_ENDPOINT + '?' + urllib.parse.urlencode({'topic': '*'}, True), stream=True, headers=headers) as response:
                client = sseclient.SSEClient(response)
                for event in client.events():
                    data = json.loads(event.data)
                    print(data)
                    if data['opened']:
                      open_door()
        except requests.exceptions.Timeout as e:
            print(e)
        except requests.exceptions.RequestException as e:
            print(e)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
