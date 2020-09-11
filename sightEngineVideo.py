# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import os


'''
 For calculating transcribtion time
'''
import timeit


'''
 1. Load the input file
'''
vidfile=str(input("Enter the video file to be moderated: "))
(name,ext)=os.path.splitext(vidfile)


base_url="https://github.com/NikhilBhargav/sightEngine/blob/master/input/"
url=base_url+vidfile+"?raw=true"
#print(url)
    
'''
 2. Call SightEngine's Video moderation API on input video for all models
''' 

# if you haven't already, install the SDK with "pip install sightengine"
from sightengine.client import SightengineClient

#Dilip's credential
#client = SightengineClient('1128730833', 'NUbdpQmTJZ8vimupHt4N')

#Nikhil's credential
#client = SightengineClient('87067536', 'XeJ4EhNkC9mYCsK8kWzn')

#Madhan's credentials
client = SightengineClient('1624310798', 'MyGgZE6DHjjD2C59ZtKo')

#DJ's credentials


#Time of execution of Videomoderation API
iterTime=0.0
starttime = timeit.default_timer()

#Checking only Nudity; weapons, alcohol and drugs; offensive and minors
output = client.check('nudity','wad','face-attributes','offensive').video_sync(url)
endtime=timeit.default_timer()
iterTime= endtime - starttime

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
#print("Starttime:",starttime,"Endtime:",endtime,"Exec Time:",endtime-starttime)
print("Time taken to moderate", vidfile,"is:",iterTime,"usec")

#Set Flags as True unless proved
nudityFlag= False
wepAlcoDrugFlag= False
offensiveFlag= False

thresholdProbability=0.75

#Process only if you get success of moderationAPI
if (output["status"]=="success"):
    data_dict=output["data"]
    mod_list=data_dict["frames"]
    for entry in mod_list:
        #1. Check for WepAlcoDrugFlag
        if(entry["weapon"]>=thresholdProbability or entry["alcohol"]>=thresholdProbability or entry["drugs"]>=thresholdProbability):
            wepAlcoDrugFlag=True
            
        #2. Check for NudityFlag
        if( (entry["nudity"]["raw"]>=thresholdProbability) or ((entry["nudity"]["partial"]>=thresholdProbability))): 
            nudityFlag=True
            
        #3. Check for OffensiveFlag
        if(entry["offensive"]["prob"]>=thresholdProbability):
            offensiveFlag=True
    
if(nudityFlag==False and wepAlcoDrugFlag==False and offensiveFlag==False):
    print("The given video is Approved")
else:
    reason=""
    if (nudityFlag):
        reason="Nudity"
    if (wepAlcoDrugFlag):
        if(len(reason)!=0):
            reason=reason+", Weapon, Alcohol and Drugs"
        else:
            reason="Weapon, Alcohol and Drugs"
    if (offensiveFlag):
        if(len(reason)!=0):
            reason=reason+" and Offensive content."
        else:
            reason="Offensive content."
        
    print("The given video is Rejected due to",reason)
