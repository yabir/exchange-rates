#from gcloud import storage
from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os 

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/tmp/corded-keel-317515-5294400fe510.json"

toProcessDirectory = r'/tmp/blablacar/output'
processedDirectory = r'/tmp/blablacar/processedFiles'
gcsBucket = 'blabladwh'

if not os.path.exists(processedDirectory):
    os.makedirs(processedDirectory)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

for filename in os.listdir(toProcessDirectory):
    fromFilePath = os.path.join(toProcessDirectory, filename)
    toFilePath = os.path.join(processedDirectory, filename)
    print('fromFilePath %s' % fromFilePath)
    print('toFilePath %s' % toFilePath)
    print('Starting process for file %s ...' % filename)
    #Upload file to GCS
    upload_blob(gcsBucket, str(fromFilePath), str(filename))
    #Move files to processed Directory
    os.rename(fromFilePath, toFilePath)
    print('File %s uploaded to bucket %s' % (filename, gcsBucket))

