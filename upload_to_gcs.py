import random
import string
from google.cloud import storage

GOOGLE_CREDENTIALS_PATH = 'key.preprod.json'
BUCKET = 'terraform-helpyourshelf-test-private-uploads-92ui8d'

client = storage.Client.from_service_account_json(json_credentials_path='test.json')
bucket = client.get_bucket(BUCKET)

object_name_in_gcs_bucket = bucket.blob('video-test-' + (''.join(random.choice(string.digits) for i in range(10))) + '.mp4')
object_name_in_gcs_bucket.upload_from_filename('local_video.mp4')
