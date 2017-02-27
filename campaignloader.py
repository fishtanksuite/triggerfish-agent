import os
import json
from campaign import Campaign

def loadCampaigns(directory):
    campaigns = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            try:
                campaigns.append(loadCampaignFromFile("{}/{}".format(directory, file)))
            except Exception, e:
                print("Error loading File: {}/{}".format(directory, file))
                print(str(e))
    return campaigns

def loadCampaignFromFile(path):
    with open(path) as file:
        data = json.load(file)
        return createCampaign(data)

def createCampaign(data):
    return Campaign(name=data["name"], data=data)
