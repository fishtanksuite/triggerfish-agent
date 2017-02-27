from redirect import requestRedirect
import socket, urlparse

class SearchStrategy(object):

    def __init__(self, strategy, campaign, elasticSearch):
        self.strategy = strategy
        self.campaign = campaign
        self.elasticSearch = elasticSearch

    def execute(self):
        raise NotImplementedError('execute')

    def search(self, query, index='logstash-*', doc_type='logstash'):
        return self.elasticSearch.search(
            index = index,
            doc_type = doc_type,
            body = query
        )

    def handleResult(self, results):
        for hit in results['hits']['hits']:
            host = hit['_source']['headers']['host'][0].split(':')[0]
            if host:
                ip = socket.getaddrinfo(host,80)[0][4][0]
                for portRedirect in self.campaign.data["portRedirects"]:
                    requestRedirect(ip, self.campaign.data["redirectIp"], portRedirect["originalPort"], portRedirect["redirectPort"])
