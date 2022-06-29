from abc import ABCMeta, abstractmethod

class MarketRetriever(metaclass=ABCMeta):
    ''' Abstract Class '''
    
    @classmethod
    def __subclasshook__(cls, subclass):
        return(hasattr(subclass, "fetch_trading_pairs") and callable(subclass.fetch_trading_pairs) 
        and hasattr(subclass,"_get_trading_pairs") and callable(subclass._get_trading_pairs) 
        and(hasattr(subclass,"fetch_tickers") and callable(subclass.fetch_tickers))
        or
        NotImplementedError)


    @abstractmethod
    def fetch_trading_pairs(self):
        pass

    @abstractmethod
    def _get_trading_pairs(self):
        pass
    
    @abstractmethod
    def fetch_tickers(self):
        pass