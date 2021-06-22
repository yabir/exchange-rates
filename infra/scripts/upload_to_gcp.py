#from gcloud import storage
from google.cloud import storage
import os 
import sys

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/tmp/corded-keel-317515-5294400fe510.json"

#Check if credentials in argument, if not quit program
if len(sys.argv) > 1 and sys.argv[1]:
    credentialsFile = sys.argv[1]
else:
    print('No credentials were provided')
    quit()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentialsFile

toProcessDirectory = r'/opt/airflow/tmp/output'
processedDirectory = r'/opt/airflow/tmp/processedFiles'
gcsBucket = 'yca_datalake'

if not os.path.exists(toProcessDirectory):
    print('Input directory does not exists')
    quit()

if not os.path.exists(processedDirectory):
    os.makedirs(processedDirectory, mode=0o777, exist_ok=True)
    """ try:
        original_umask = os.umask(0)
        os.makedirs(processedDirectory, mode=0o777, exist_ok=True)
    finally:
        os.umask(original_umask) """

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

for filename in os.listdir(toProcessDirectory):
    fromFilePath = os.path.join(toProcessDirectory, filename)
    toFilePath = os.path.join(processedDirectory, filename)
    print('Starting process for file %s ...' % filename)
    try:
        #Upload file to GCS
        upload_blob(gcsBucket, str(fromFilePath), str(filename))
        #Move files to processed Directory
        os.rename(fromFilePath, toFilePath)
        print('File %s uploaded to bucket %s' % (filename, gcsBucket))
    except ValueError:
        print(ValueError)

