from searchstrategy import SearchStrategy

class UriSequenceStrategy(SearchStrategy):

    def __init__(self, strategy, campaign, elasticSearch):
        SearchStrategy.__init__(self, strategy, campaign, elasticSearch)


    def execute(self):
        print("Executing UriSequenceStrategy")
        query = self.createQuery(self.strategy["sequence"]["entry"]["uri"], "now-10m")
        result = self.search(query)

        print("Found {} {}".format(len(result["hits"]["hits"]), self.strategy["sequence"]["entry"]["uri"]))
        for hit in result["hits"]["hits"]:

            gte = hit["_source"]["@timestamp"]
            lte = "{}||+{}".format(hit["_source"]["@timestamp"], self.strategy["sequence"]["next"]["timeSpan"])

            query = self.createQuery(self.strategy["sequence"]["next"]["uri"], gte, lte)

            result = result = self.search(query)

            print("Found {} {}".format(len(result["hits"]["hits"]), self.strategy["sequence"]["next"]["uri"]))
            if result["hits"]["hits"]:
                self.handleResult(result)

    def getTemplateQuery(self):
        return {
            "query": {
                "bool": {
                    "must": {
                        "term": {

                        }
                    },
                    "filter": {
                        "range": {
                            "@timestamp": {

                            }
                        }
                    }
                }
            }
        }

    def createQuery(self, uri, gte, lte=None):
        query = self.getTemplateQuery()
        query["query"]["bool"]["must"]["term"]["uri"] = uri

        if gte:
            query["query"]["bool"]["filter"]["range"]["@timestamp"]["gte"] = gte
        if lte:
            query["query"]["bool"]["filter"]["range"]["@timestamp"]["lte"] = lte

        return query
