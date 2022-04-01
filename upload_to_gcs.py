import random
import string
import requests
from google.cloud import storage
import datetime

GOOGLE_CREDENTIALS_PATH = 'key.preprod.json'
BUCKET = 'terraform-helpyourshelf-test-private-uploads-92ui8d'
LOCAL_FILE = 'local_video.mp4'
REMOTE_FILE = 'video-test-' + (''.join(random.choice(string.digits) for i in range(10))) + '.mp4'

client = storage.Client.from_service_account_json(json_credentials_path=GOOGLE_CREDENTIALS_PATH)

policy = client.generate_signed_post_policy_v4(BUCKET, REMOTE_FILE, expiration=datetime.datetime.now() + datetime.timedelta(days=1, hours=3),
    conditions=[
        ["content-length-range", 0, 50000000] # policy max 50mb, tu peux augmenter ou baisser
    ]
)

with open(LOCAL_FILE, "rb") as f:
    files = {"file": (LOCAL_FILE, f)}
    response = requests.post(policy["url"], data=policy["fields"], files=files)
    print(response.content)