import requests
import time

MERCURE_ENDPOINT = 'http://localhost:83/.well-known/mercure'
JWT = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXJjdXJlIjp7InB1Ymxpc2giOlsiKiJdfX0' \
      '.obDjwCgqtPuIvwBlTxUEmibbBf0zypKCNzNKP7Op2UM '

counter = 1

headers = {
    'Authorization': 'Bearer ' + JWT
}

while True:
    data = {'topic': 'test_counter', 'data': counter}
    try:
        print(counter)
        with requests.post(MERCURE_ENDPOINT, data=data, headers=headers) as response:
            pass
    except Exception as e:
        print(e)

    counter = counter + 1

    time.sleep(1)
