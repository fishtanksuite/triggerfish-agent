#!/bin/env python
import sys
from worker import Worker
from campaignloader import loadCampaigns
from elasticsearch import Elasticsearch

def main():
    workers = []
    campaigns = []

    #Load campaigns from directory: "campaigns"
    try:
        campaigns = loadCampaigns("campaigns")
    except Exception, e:
        print(str(e))

    #Check if at least one Campaign is loaded
    if(len(campaigns) == 0):
        print("No Campaigns loaded, exiting...")
        sys.exit()

    try:
        #Create Threads (For every Campaign one Thread)
        for i in range(len(campaigns)):
            workers.append(Worker(campaigns[i], name="Worker-{}".format(i)))

        #Instantiate ElasticSearch Client
        elasticSearch = Elasticsearch(
            [{'host': 'elasticsearch-host', 'port': 9200}]
        )

        #Inject ElasticSearch (ES Client doesn't work very well with fork; Injection after instatiation of ES Client)
        for worker in workers:
            worker.injectES(elasticSearch)

        #Start Threads
        for worker in workers:
            worker.start()

        #Join Threads
        for worker in workers:
            worker.join()

    except (KeyboardInterrupt, SystemExit):
        #Kill Threads
        for worker in workers:
            worker.running = False

        for worker in workers:
            worker.join()

        sys.exit()

if __name__ == "__main__":
    main()
