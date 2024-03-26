from bs4 import BeautifulSoup
from functions.DataHandlers import DataHandler
from functions.Requester import Requester


class HTMLScraper:
    def __init__(self, url='', sessions:bool=True):
        self.requester = Requester()
        self.url = url
        self.content = ''
        
    def _getPages(self, url:str='', method:str='get', params=None, data=None, json=None, header=None, cookies=None, timeout:int=60, redirect:bool=True, verify:bool=True, proxy=None, ref=None, agent=None, sessions=None, pre_request:bool=False):
        """
            _getPages()
            -----------

            This method is for fetching webpages.

            Args:
                - url (str, optional): _description_. Defaults to ''.
                - method (str, optional): _description_. Defaults to 'get'.
                - params (_type_, optional): _description_. Defaults to None.
                - data (_type_, optional): _description_. Defaults to None.
                - json (_type_, optional): _description_. Defaults to None.
                - header (_type_, optional): _description_. Defaults to None.
                - cookies (_type_, optional): _description_. Defaults to None.
                - timeout (int, optional): _description_. Defaults to 60.
                - redirect (bool, optional): _description_. Defaults to True.
                - verify (bool, optional): _description_. Defaults to True.
                - proxy (_type_, optional): _description_. Defaults to None.
                - ref (_type_, optional): _description_. Defaults to None.
                - agent (_type_, optional): _description_. Defaults to None.
                - sessions (_type_, optional): _description_. Defaults to None.
                - pre_request (bool, optional): _description_. Defaults to False.

            Returns:
                _type_: _description_
        """
        if url == '':
            url = self.url

        if sessions!=None:
            response, self.sessions = self.requester.requestSessions(url, method, params, data, json, header, cookies, timeout, sessions, redirect, verify, proxy, ref, agent, pre_request)
        else:
            response = self.requester.request(url, method, params, data, json, header, cookies, timeout, redirect, verify, proxy, ref, agent)
        return response

    def pageParser(self, content,  element:str, attribute:str=''):
        """ 
            This method is responsible for parsing the data given.   

        Args:
            content (_type_): _description_
            element (str): _description_
            attribute (str, optional): _description_. Defaults to ''.

        Returns:
            _type_: _description_
        """
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.select(element)

        if attribute:
            return [element.get(attribute) for element in elements]
        else:
            return [element.text.strip() for element in elements]

if __name__ == '__main__':
    pass


