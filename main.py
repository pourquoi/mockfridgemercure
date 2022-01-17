import json
import datetime
import time
import urllib
import threading
import requests
import sseclient

API_ENDOINT = 'http://localhost:8080'
MERCURE_ENDPOINT = 'http://localhost:83/.well-known/mercure'
FRIDGE_UUID = 'a5e27392-0088-4799-9b5d-8a76b7a75c45'
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
    time.sleep(1)


def get_door_status():
    headers = {'Accept': 'application/json'}
    response = requests.get(API_ENDOINT + '/fridge_api/fridge/' + FRIDGE_UUID + '/door_status', headers=headers)
    print(response.content)
    return json.loads(response.content)


def main():
    ping_thread = threading.Thread(target=ping)
    ping_thread.start()

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

        if door_status['opened']:
            open_door()

        print('waiting for events')

        headers = {'Accept': 'text/event-stream'}
        try:
            with requests.get(MERCURE_ENDPOINT + '?' + urllib.parse.urlencode({'topic': 'https://example.com/fridge/' + FRIDGE_UUID + '/door_status'}, True), stream=True, headers=headers) as response:
            #with requests.get(MERCURE_ENDPOINT + '?' + urllib.parse.urlencode({'topic': '*'}, True), stream=True, headers=headers) as response:
                client = sseclient.SSEClient(response)
                for event in client.events():
                    data = json.loads(event.data)
                    if data['opened']:
                      open_door()
        except requests.exceptions.Timeout as e:
            print(e)
            time.sleep(10)
        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep(10)
        except Exception as e:
            print(e)
            time.sleep(10)


if __name__ == '__main__':
    main()
