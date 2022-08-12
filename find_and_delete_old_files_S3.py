# script for search and delete old files with specific size in S3 bucket
import boto3

mybucket = 'yourbucket'
checkmonth = 5

s3_client = boto3.client('s3')
buckets = s3_client.list_buckets()
s3 = boto3.resource('s3')

def list_old_files(countcontrol, bucketname):
    my_bucket = s3.Bucket(bucketname)
    count = 0
    output = []
    for my_bucket_object in my_bucket.objects.filter(Prefix=""):
        month = int(my_bucket_object.last_modified.strftime("%m"))
        if month < checkmonth and my_bucket_object.size > 3072:
            count = count + 1
            currentoutput = (my_bucket_object.key)
            output.append(currentoutput)
            print(count, my_bucket_object.key, my_bucket_object.last_modified, my_bucket_object.size)
        if count >= countcontrol:
            break
    return (output, count)

def delete_old_files(bucketname, files):
    count = 0
    for my_bucket_object in files:
        count = count + 1
        print(count, 'Deleting in ', bucketname, ' - ', my_bucket_object)
        s3.Object(bucketname, my_bucket_object).delete()
    print('Finish. Deleted - ', count, 'objects')
    return (output, count)

#step for checkin - countinput
countinput = 100

output, count = list_old_files(countinput, mybucket)
print('Count of old files in this loop - ', count)
#print(output)
#delete_old_files(mybucket, output)
