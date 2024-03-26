from functions.Requester import Requester
from bs4 import BeautifulSoup

class HtmlScraper:
    """
    A simple HTML scraper class using requests and BeautifulSoup.

    Attributes:
        url (str): The URL of the webpage to scrape.
        headers (dict): HTTP headers to be used in the requests.
        page_content (str): The HTML content of the webpage.

    Methods:
        _get_page_content(): Private method to fetch the HTML content of the webpage.
        scrape_element(selector, attribute=None): Scrapes elements based on the provided CSS selector.

    Example:
        url = 'https://example.com'
        scraper = HtmlScraper(url)

        # Scraping text content
        titles = scraper.scrape_element('h2.title')
        for title in titles:
            print(f'Title: {title}')

        # Scraping attribute (e.g., href) content
        links = scraper.scrape_element('a.link', attribute='href')
        for link in links:
            print(f'Link: {link}')
    """

    def __init__(self, url):
        """
        Initializes the HtmlScraper instance.

        Args:
            url (str): The URL of the webpage to scrape.
        """
        self.url, self.sessions = url, None
        self.requester = Requester()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.page_content = self._get_page_content()

    def _get_page_content(self,url=None, method:str='get', params=None, data=None, json=None, header=None, cookies=None, timeout=30, sessions=None, redirect=True, verify=True, proxy=None, ref=None, agent=None, pre_request=None):
        """
            Private method to fetch the HTML content of the webpage.

            Returns:
                str: The HTML content of the webpage.
            
            Raises:
                Exception: If the request to fetch the page content fails.
        """
        if url==None:
            url=self.url

        if header == None:
            header = self.headers

        if sessions!=None:
            response, self.sessions = self.requester.requestSessions(url, method, params, data, json, header, cookies, timeout, sessions, redirect, verify, proxy, ref, agent, pre_request)
        else:
            response = self.requester.request(url, method, params, data, json, header, cookies, timeout, redirect, verify, proxy, ref, agent)
        
        if response.status_code == 200: return response.text
        else: raise Exception(f"Failed to fetch page content. Status code: {response.status_code}")

    def scrape_element(self, selector, attribute=None):
        """
        Scrapes elements based on the provided CSS selector.

        Args:
            selector (str): The CSS selector to locate the desired elements.
            attribute (str, optional): The attribute to extract from the elements (e.g., 'href' for links). Defaults to None.

        Returns:
            list: A list of scraped content (either text or attribute values).
        """
        soup = BeautifulSoup(self.page_content, 'html.parser')
        elements = soup.select(selector)

        if attribute:
            return [element.get(attribute) for element in elements]
        else:
            return [element.text.strip() for element in elements]

    def scrape_elements_grouped(self, info_dict):
        """
            Scrapes elements based on the provided URL and element pathways, and groups the data.

            Args:
                info_dict (dict): A dictionary containing the URL and element pathways.

            Returns:
                dict: A dictionary with specified keys and values grouped in lists.
        """
        if isinstance(info_dict, dict):
            url = info_dict.get('url', '')
            paths = info_dict.get('path', {})

            if url:
                self._get_page_content(url)

            if not paths:
                raise ValueError("URL and element pathways must be specified in the info_dict.")

            grouped_data = {}
            for key, path in paths.items():
                if isinstance(path, str):
                    grouped_data[key] = self.scrape_element(path)
                elif isinstance(path, tuple):
                    grouped_data[key] = self.scrape_element(path[0], path[1])
                elif isinstance(path, dict):
                    grouped_data[key] = self.scrape_elements_grouped(key)
                elif isinstance(path, list):
                    for i in path:
                        if isinstance(i, str):
                            grouped_data[key] = self.scrape_element(i)
                        elif isinstance(i, dict):
                            grouped_data[key] = self.scrape_elements_grouped(i) 
                else: raise ValueError('The path is either needs to be string, dict or a listof those.')

            return grouped_data
        elif isinstance(info_dict, list):
            return [self.scrape_elements_grouped(i) for i in info_dict]
        else: return False


if __name__ == '__main__':
    # url = 'https://example.com'
    # scraper = HtmlScraper(url)
    # titles = scraper.scrape_element('body > div:nth-child(1) > p')
    # for title in titles:
    #     print(f'Title: {title}')
    # links = scraper.scrape_element('a', attribute='href')
    # for link in links:
    #     print(f'Link: {link}')


    scrape_data = {
        'url':'https://example.com',
        'params': {'continue':False},
        'path': {
            'title':{
                'element':'body > div:nth-child(1) > p',
                'attr': None,
                'path': {}
                     },
            'link' : {
                    'element':'a',
                    'attr': 'href',
                    'path':{}  
                    }
            }
    }