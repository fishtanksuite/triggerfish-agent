from keywordstrategy import KeywordStrategy
from urisequencestrategy import UriSequenceStrategy

class StrategyFactory(object):

    def factory(type, strategy, campaign, elasticSearch):
        if type == 'KeywordStrategy': return KeywordStrategy(strategy, campaign, elasticSearch)
        if type == 'UriSequenceStrategy': return UriSequenceStrategy(strategy, campaign, elasticSearch)
    factory = staticmethod(factory)
