from searchstrategy import SearchStrategy

class KeywordStrategy(SearchStrategy):

    def __init__(self, strategy, campaign, elasticSearch):
        SearchStrategy.__init__(self, strategy, campaign, elasticSearch)
        self.query = self.createQuery(strategy["keywords"])

    def execute(self):
        print("Executing KeywordStrategy")
        result = self.search(self.query)

        if result["hits"]["hits"]:
            print("Got {} Results".format(len(result["hits"]["hits"])))
            self.handleResult(result)
        else:
            print("No Results")

    def createQuery(self, keywords):
        query = {
             "query" : {
                "constant_score" : {
                    "filter" : {
                        "bool" : {
                          "must" : [
                            {"range": { "@timestamp": { "gte": "now-10m" }}},
                            { "match" : {"message" : "REQMOD"}}],
                         "should" : [
                         { "terms" : { "decrypted" : keywords}}]
                        }
                   }
               }
            }
        }

        return query
