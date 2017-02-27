import threading
import socket, urlparse
from strategyfactory import StrategyFactory

class Worker(threading.Thread):

    def __init__(self, campaign, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        self.campaign = campaign
        self.running = False

        print("{} created".format(self.name))
        return

    def injectES(self, elasticSearch):
        self.elasticSearch = elasticSearch

    def run(self):
        self.running = True

        self.strategies = {}
        for strategy in self.campaign.data["SearchStrategies"]:
            self.strategies[strategy["name"]] = StrategyFactory.factory(strategy["type"], strategy, self.campaign, self.elasticSearch)

        print(self.strategies)

        if len(self.strategies) == 0:
            self.running = False
            print("No Strategies loaded. stop Thread...")
        else:
            print("{} started".format(self.name))

        while(self.running):
            for strategy in self.strategies:
                self.strategies[strategy].execute()


            #self.running = False

        print("{} stoped".format(self.name))
