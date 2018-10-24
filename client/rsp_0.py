##############################
# PI 0 RESPONSIBILITIES:
#   1. Controls Speakers 
#   2. Controls TV
#############################

import os
import sys
import glog as log
import json
import subprocess 
sys.path.insert(0, "../")
import config
import boto3
import subprocess
import trigger

CLIENT_WAIT_TIME=20

# Create SQS client
client = boto3.client('sqs')

'''
def trigger_tv(video_static, static_sounds):
        thread.start_new_thread(os.system("omxplayer " + path)
'''      

while(True):
    response = client.receive_message(
        QueueUrl=config.sqs_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        WaitTimeSeconds=CLIENT_WAIT_TIME
    )
    print(response) 
    if 'Messages' in response:
        message = response['Messages'][0]
        body = message['Body']
        receipt_handle = message['ReceiptHandle']
        #print(body, end="\n\n")
         
        data = json.loads(body)
        #print(data)

        action = json.loads(data['Message'])
        if 'action' in action:
            if (action['action'] == 'turn_on_tv'):
                sound_path = "../media/static_sound.mp3"
                video = "../media/static_video.mp4"

                #Open subprocess to play static.mp4 at the same time as static_noise.mp3
                subprocess.Popen([trigger.TV, video])
                subprocess.Popen([trigger.audio, sound_path])
                
                #only delete if we have to
                client.delete_message(
                    QueueUrl=config.sqs_url,
                    ReceiptHandle=receipt_handle
                )
    else:
        #print(response, end="\n\n")
        pass
