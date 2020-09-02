# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import os

'''
 For exit()
'''
from sys import exit

'''
 For calculating transcribtion time
'''
import timeit

'''
 1. Load the input file
''' 
vidfile=str(input("Enter the video file to be moderated: "))
(name,ext)=os.path.splitext(vidfile)


cwd = os.getcwd()
folder_name="input"
vidpath=os.path.join(cwd,folder_name)
vidpath=os.path.join(vidpath,vidfile)        
    
#Check if the file exists else end the program
if (os.path.exists(vidpath)==False):
    print(vidfile,"doesnot exist")
    exit (1)

#print(vidpath)        

'''
 2. Call SightEngine's Video moderation API on input video for all models
''' 

# if you haven't already, install the SDK with "pip install sightengine"
from sightengine.client import SightengineClient
client = SightengineClient('1128730833', 'NUbdpQmTJZ8vimupHt4N')

#Time of execution of Videomoderation API
iterTime=0.0
starttime = timeit.default_timer()

output = client.check('nudity','wad','properties','face-attributes','text','offensive').video_sync("funfair.mp4")
endtime=timeit.default_timer()
iterTime+= endtime - starttime

json_object=json.dumps(output, indent = 2)
print(json_object)   

'''
 3. Store the output as json output file in separate output folder
''' 
cwd = os.getcwd()
folder_name="output"

vidpath=os.path.join(cwd,folder_name)

# create a directory to store the audio chunks
if not os.path.isdir(folder_name):
    os.mkdir(folder_name)

file=name+'.json'
out_file = os.path.join(vidpath, file)   
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
    
'''
 4. Use timeit to calculate moderation time
'''
print("Starttime:",starttime,"Endtime:",endtime,"Exec Time:",endtime-starttime)
print("Time taken to moderate", vidfile,"is:",iterTime,"usec")