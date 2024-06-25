from Requester import Requester
from bs4 import BeautifulSoup
from FileHandler import write, read
from DataHandlers import get_unique

class HtmlScraper:

    def __init__(self, url:str, setSessions:bool=False, set_header:bool=True, set_agent:bool=True, set_proxy:bool=False)->None:
        """
            HtmlScraper
            ===========

            This is a class that is to be used to scrape a website.
        """
        self.url = url
        self.setSessions, self.sessions = setSessions, None
        self.req = Requester(set_header=set_header, set_agent=set_agent, set_proxy=set_proxy, agent_file='F:/Code Works/Python_works/storage/others/user-agent.txt') # proxy_file='F:/Code Works/Python_works/storage/others/proxies.txt')
        self.souped = None

    def _rectiftyPathway(self, pathway):

        if isinstance(pathway, list):
            pathway = [self._rectiftyPathway(p) for p in pathway]
        elif isinstance(pathway, dict):
            r = pathway.keys()
            if 'tag' in r:
                if 'attr' not in r:
                    pathway['attr'] = {}
                if 'type' not in r:
                    pathway['type'] = 'find'
            else:
                pathway = {k: self._rectiftyPathway(v) for k,v in pathway.items()}
        return pathway
                 
    def _request(self, method:str='get', params:dict={}, ref:str='', response_code:int=200):
        reqVals = {'url': self.url, 'method': method,'params': params, 'ref': ref, 'response_code': response_code}
        req = None
        if self.setSessions:
            req, self.sessions = self.req.requestSessions(sessions=self.sessions, **reqVals)
        else:
            req = self.req.request(**reqVals)
        return req

    def _souper(self, data, parser:str='html.parser'):
        """
            _souper()
            ---------

            Converts a html document data into BeautifulSoup class value.
        """
        self.souped = BeautifulSoup(data, parser)
        return self.souped
        
    def _getAtr(self, data, ty):
        if isinstance(data, list):
            return [self._getAtr(t, ty) for t in data if t is not None]
        else:
            r = None 
            if ty=='<text>' or ty=='<stext>':    
                r = data.getText(strip=(True if ty=='<stext>' else False))
            else:
                r = data.get(ty) 
            return r

    def _parser(self, selectorType:str='find', tagName='', attribute:dict={}, data=None)->(list|str|None):
        """
            _parser()
            ---------
            This method is responsible for fetching the target element in the document.

            Parameters:
            - `selectorType` str: The type of method that is to be used for fetching an element(s).Its values are
                - find: Finds a single element, the first element that matches the values (tagName & attribute). Also the default value.
                - find_all: Finds all the element of the same tag and atribute value.
                - select_one: Similar to find, the tagName used would be the JS query selector value. Selecting this value returns a single value.
                - select: Similar to find_all, the tagName used would be the JS query selector value. Selecting this value returns a list of value.
            - `tagName` str: This parameter determines where to lookand what to fetch. Depending of on the `selectorType`, the value can be a tagName(for `find` & `find_all`) or a JS querySelctor value (for `select` or  `select_one`)
            - `attribbute` dict: This acts as a supporter for finding the target tag value.
            - `data`: This parameter is to pass the html data where to look. Default is `None` which means, the page that will be parsed will be the page got during the requesting of the page.
        
            Returns:
            - NoneType|list|str: Depending on the value passsed in `selectorType` parameter, the data type passed can be a list, str or a None type value.
                - `select_one` or `find`: Return str 
                - `select` or `find_all`: Return list 
                - If no data found: Return None
        """
        if data==None:
            data=self.souped
        try:
            if selectorType == 'select':
                k = data.select(tagName, attr=attribute)
            elif selectorType == 'select_one':
                k = data.select_one(tagName, attr=attribute)
            elif selectorType == 'find':
                k = data.find(tagName, attr=attribute)
            elif selectorType == 'findall' or selectorType =='find_all':
                k = data.find_all(tagName, attr=attribute)
            return k
        except:
            return None   
        
    # basic purpose
    def storePage(self, fileName:str, data=None, seperator:str='\n', prevEmpty:bool=True)->None:
        """
            storePage()
            -----------
            This method is to store the page or the data in a file.

            Parameter:
            - fileName str: Name of the file.
            - data any: Takes the data that is to be inserted in the file. Default is `None`, which means the data stored will be the html data fetched during the request processes.
            - seperator str: THis paramerter specifies, how the data points will be seperated in the file. Default is `\n` (a line break).
            - prevEmpty bool: This parameter specifies if the existing data in the file should remain or be deleted. Default is `True`. Values:-
                - `True`: The file will be emptied before inserting new data.
                - `False`: The new data will be appended into the file with existing data.
        """
        write(file_name=fileName, data=(self.souped if data==None else data), separator=seperator, emptyPervious=prevEmpty)

    # User use functions
    def getAllUrls(self, data=None)->list[str]:
        """
            getAllUrls()
            ------------
            This method is fo getting all the urls in the parsed page
        """
        return get_unique([i.get('href') for i in self._parser(selectorType='find_all',tagName='a', data=data)])

    def getAllImages(self, data=None):
        """
            getAllImages()
            --------------
            Returns all the images in the page.
        """
        imgs = {'tag': 'img', 'attr': {}, 'type': 'select', 'inner':{'imgLnk': 'src', 'alt':'alt'}}
        return self.jsonParser(pathway=imgs, data=data)

    def getPageMeta(self, data=None):
        """
            getPageMeta()
            -------------
            Fetches the meta data of the page.
        """ 
        pathway = {'title': {'tag':'title', 'get': '<stext>'}}
        return self.jsonParser(pathway, data)

    def jsonParser(self, pathway:dict, data=None)->dict|None|list:
        """
            jsonParser()
            ------------
            This method is responsible for parsing the websitein the given structure.
        """
        if data==None:
            data = self._souper(self._request()) if self.souped==None else self.souped

        pathway = self._rectiftyPathway(pathway)
        try:
            if isinstance(pathway, str):
                return self._parser(selectorType='select', tag=pathway, data=data)
            elif isinstance(pathway, dict):
                ret:dict = {}
                if len(pathway) == 0: return None
                if 'tag' in pathway.keys():  
                    k = self._parser(selectorType=pathway['type'], tagName=pathway['tag'], attribute=pathway['attr'], data=data)
                    if k is not None:
                        if 'get' in pathway.keys() and pathway['get'] != '' and pathway['get'] is not None:
                            ret['get'] = self._getAtr(ty=pathway['get'], data=k)

                        if 'inner' in pathway.keys() and pathway['inner']!={}:
                            ret['inner'] = [self.jsonParser(data=n,pathway=pathway['inner']) for n in k] if isinstance(k, list) else self.jsonParser(data=k, pathway=pathway['inner'])
                        elif 'get' in ret.keys():
                            return ret['get']
                        else: return k
                else:
                    for k,v in pathway.items():
                        ret[k] = self._getAtr(ty=v, data=data) if isinstance(v, str) else self.jsonParser(pathway=v,data=data)

                return ret
            elif isinstance(pathway, list):
                return [self.jsonParser(pathway=i,data=data) for i in pathway]
        except:
            return None

