import requests, random, time, websockets, aiohttp, asyncio
from urllib.parse import urlparse, parse_qsl, urlencode
from functions.FileHandler import read

class Requester:
    """
        Requester()
        ===========

        Requester is a class for making HTTP & HTTPS requests easier speciall dureing the time of development. 

    """

    def __init__(self, agent:list=[], header:dict={}, proxy:list=[], ref:list=[], ref_file:str='', proxy_file:str='', agent_file:str='', set_agent:bool=True, set_header:bool=True, set_ref:bool=False, set_proxy:bool=False, break_pt:list=[]):
        self.agent, self.ref, self.proxy, self.header = 0, '', 0, 0
        self.break_pt = break_pt
        self.ws = None

        if agent_file != '':
            self.agent = read(agent_file, '\n')
        elif agent != []:
            self.agent = agent
        else:
            self.agent = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3']

        if ref_file != '':
            self.ref = read(ref_file,'\n')
        elif ref is not None:
            self.ref = ref

        if proxy_file  != '':
            self.proxy = read(proxy_file,'\n')
        elif proxy != []:
            self.proxy = proxy
        else:
            self.proxy= []

        if set_header:
            self.header = header

        # if self._check_connection()==False:
        #     raise ConnectionRefusedError('There is some issues with the internet Connection. Please the internet connection before performing any requests.')
    
    def get_proxy(self):
        """
            This method gives a proxy url randomly.     
        """
        if self.proxy != []: return random.choice(self.proxy) 

    def headers(self, agent:str='', ref:str='', header:dict={}, change:bool=False):
        """
            headers()
            --------
            The header method of the class gives out the headers necessay for the requests
            Args:
                agent (str, optional): _description_. Defaults to None.
                ref (str, optional): _description_. Defaults to None.
                header (dict, optional): _description_. Defaults to None.
                change (bool, optional): This parameter takes in True or False which determines whether the headers will change or remain the same based on the data passed respectively. Defaults to False.

            Returns:
                _type_: _description_
        """
        headers = {'connection': 'keep-alive','accept-Encoding': 'gzip, deflate, br','cache-Control': 'max-age=0','dnt': '1','upgrade-insecure-requests': '1','user-agent': '','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','sec-fetch-site': 'same-origin','sec-fetch-mode': 'navigate','sec-fetch-user': '?1', 'referer': '','accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}

        if (self.header!=0) and (header=={}) and (change==False):
            header = self.header
        elif (header!={}):
            headers = {**headers, **{k:v for k,v in header.items()}}
            if change:
                self.header = headers
        
        if agent=='' and isinstance(self.agent, list):
            agent = random.choice(self.agent)
        elif agent!='':
            agent = agent

        if ref=='' and self.ref!=[]:
            if isinstance(self.ref, list):
                ref=random.choice(self.ref)
            elif isinstance(self.ref, str):
                ref = self.ref

        headers['user-agent'] = str(agent)
        headers['referer'] = str(ref)

        return headers

    def set_url_params(self, url, params:dict={}):
        """Set the parameters in a URL.

        Parameters:
            url (str): The base URL.
            params (dict): A dictionary of parameters to set in the URL.

        Returns:
            str: The URL with the parameters set.
        """
        if params!={}:
            params = {k: v for k, v in params.items() if v!=None or v!=''}
            encoded_params = urlencode(params)
            url = f"{url}?{encoded_params}"
        return url

    def get_urlinfo(self, url):
        """
            This method returns the info of the url.
        """
        ino = urlparse(url)
        return {'scheme':ino.scheme, 'hostname':ino.hostname, 'path':ino.path,'params':dict(parse_qsl(ino.params)), 'query':ino.query, 'fragment':ino.fragment}

    def parse_url_parameters(self, url:str):
        """
            This method gets parameters from the url. 
        """
        return self.get_urlinfo(url)['params']

    def request(self, url, method='get', params=None, data=None, json:dict={}, header:dict={}, cookies=None, timeout=5, redirect=True, verify=True, proxy=None, ref:str='', agent:str='', break_pt:list=[], setHeader:bool=False):

        break_pt = self.break_pt if break_pt is [] else break_pt
        if break_pt != []: time.sleep(random.uniform(break_pt[0], break_pt[1]))
        proxy = self.get_proxy() if proxy is None else proxy
        header = None if header=={} else self.headers(agent, ref, header, setHeader)

        if method.lower() == 'get':
            ret = requests.get(url, params=params, headers=header, cookies=cookies, timeout=timeout, allow_redirects=redirect, verify=verify, proxies=proxy) #type:ignore
        elif method.lower() == 'post':
            ret = requests.post(url, params=params, data=data, json=json, headers=header, cookies=cookies, timeout=timeout, allow_redirects=redirect, verify=verify, proxies=proxy) #type:ignore
        elif method.lower() == 'put':
            ret = requests.put(url, params=params, data=data, json=json, headers=header, cookies=cookies, timeout=timeout, allow_redirects=redirect, verify=verify, proxies=proxy) #type:ignore
        elif method.lower() == 'patch':
            ret = requests.patch(url, params=params, data=data, json=json, headers=header, cookies=cookies, timeout=timeout, allow_redirects=redirect, verify=verify, proxies=proxy) #type:ignore
        elif method.lower() == 'delete':
            ret = requests.delete(url,params=params,data=data, json=json, headers=header, cookies=cookies, timeout=timeout, allow_redirects=redirect, verify=verify, proxies=proxy) #type:ignore
        return ret #type:ignore

    def requestSessions(self, url:str, method:str='get', params=None, data=None, json=None, header=None, cookies=None, timeout:int=5, sessions=None, redirect=True, verify=True, proxy=None, ref:str='', agent:str='', pre_request:bool=False, break_pt:list=[]):
        """
            This method (requestSessions) is do make request based on the sessions.

            Args:
                url (str): Take the url that is to be requested.
                method (str, optional): Takes the method in which the url is requested. Defaults to 'get'.
                params (dict, optional): Takes the parameters of the url in a dict format. Defaults to None.
                data (_type_, optional): _description_. Defaults to None.
                json (_type_, optional): _description_. Defaults to None.
                header (_type_, optional): _description_. Defaults to None.
                cookies (_type_, optional): _description_. Defaults to None.
                timeout (int, optional): This takes the time in seconds how much time will the systems wait for the respose . Defaults is 5 (5 sec).
                sessions (_type_, optional): Takes the sessions data. Defaults to None.
                redirect (bool, optional): _description_. Defaults to True.
                verify (bool, optional): _description_. Defaults to True.
                proxy (_type_, optional): _description_. Defaults to None.
                ref (_type_, optional): Takes the reffered url or the url that will display where its requested froms. Defaults to None.
                agent (_type_, optional): Takes the user-agent detials. Defaults to None.
                pre_request (bool, optional): This parameter is responsible for adding sessions to the requsted url if given `True`. Defaults to False.
                break_pt (_type_, optional): _description_. Defaults to None.

            Returns:
                resonse: Returns the response of the requested url.
                sessions: Returns the sessions created in the requseting process.  
        """
        break_pt = self.break_pt if break_pt == [] else break_pt
        if break_pt != []: time.sleep(random.uniform(break_pt[0], break_pt[1]))
        proxy = self.get_proxy() if proxy is None else proxy
        header = self.headers(agent, ref) if header is None else header 

        s = sessions if sessions!=None else requests.sessions.Session()
        if header != None: s.headers.update(header)
        if cookies!=None: s.cookies.update(cookies)
        if proxy != None: s.proxies.update(proxy)
        s.verify = verify
        s.timeout = timeout 
        s.allow_redirects = redirect

        if pre_request and sessions==None:
           if isinstance(pre_request, bool):
               info = self.get_urlinfo(url)
               prevon = info['scheme'] + '://'+ info['hostname']
               s.get(prevon)
           else: s.get(pre_request)

        if method.lower() == 'get':
            ret = s.get(url, params=params)
        elif method.lower() == 'post':
            ret = s.post(url, params=params, data=data, json=json)
        elif method.lower() == 'put':
            ret = s.put(url, params=params, data=data, json=json)
        elif method.lower() == 'patch':
            ret = s.patch(url, params=params, data=data, json=json)
        elif method.lower() == 'delete':
            ret = s.delete(url,params=params,data=data, json=json)
        return ret, s

    def connect_websocket(self, url, on_message=None, on_error=None, on_close=None):
        """Connect to a WebSocket server at the specified URL.

        Parameters:
            url (str): The URL of the WebSocket server.
            on_message (function): A function to be called when a message is received.
            on_error (function): A function to be called when an error occurs.
            on_close (function): A function to be called when the connection is closed.

        Returns:
            websocket.WebSocket: The WebSocket connection.
        """
        self.ws = websockets.WebSocketApp(url, on_message=on_message, on_error=on_error, on_close=on_close)
        self.ws.run_forever()
        return self.ws

    def send_websocket_message(self, message):
        """Send a message over a WebSocket connection.

        Parameters:
            ws (websocket.WebSocket): The WebSocket connection.
            message (str): The message to send.
        """
        self.ws.send(message)

    def close_websocket(self):
        """Close a WebSocket connection.

        Parameters:
            ws (websocket.WebSocket): The WebSocket connection.
        """
        self.ws.close()

    def check_connection(self, url:str=''):
        """
            check_connections()
            -------------------

            This method is to check if there is internet connection avaiable or not.

            Returns:
            --------
                returns: This metho returns a bool (True or False). Returns `True` if conncetion is available and `False` if not available.   
        """
        try:
            url = url if url!='' else 'https://www.google.com' 
            res = self.request(url)
            res.raise_for_status()
            return True
        except requests.RequestException:
            return False

class AsyncRequester:
    """
        AsyncRequester()
        ================

        AsyncRequester is a class for making HTTP & HTTPS requests easier especially during the time of development. 
    """

    def __init__(self, agent=[], header={}, proxy=[], ref=[], ref_file='', proxy_file='', agent_file='', set_agent=True, set_header=True, set_ref=False, set_proxy=False, break_pt=[]):
        self.agent, self.ref, self.proxy, self.header = 0, '', 0, 0
        self.break_pt = break_pt

        if agent_file != '':
            self.agent = read(agent_file, '\n')
        elif agent != []:
            self.agent = agent
        else:
            self.agent = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3']

        if ref_file != '':
            self.ref = read(ref_file, '\n')
        elif ref is not None:
            self.ref = ref

        if proxy_file != '':
            self.proxy = read(proxy_file, '\n')
        elif proxy != []:
            self.proxy = proxy
        else:
            self.proxy = []

        if set_header:
            self.header = header

    async def get_proxy(self):
        """
            This method gives a proxy url randomly.     
        """
        if self.proxy != []:
            return random.choice(self.proxy)

    async def headers(self, agent='', ref='', header=None, change=False):
        """
            The header method of the class gives out the headers necessary for the requests.

            Args:
                agent (str, optional): User-agent string. Defaults to ''.
                ref (str, optional): Referer URL. Defaults to ''.
                header (dict, optional): Additional headers. Defaults to None.
                change (bool, optional): Whether to change headers or not. Defaults to False.

            Returns:
                dict: Request headers.
        """
        headers = {'connection': 'keep-alive', 'accept-Encoding': 'gzip, deflate, br', 'cache-Control': 'max-age=0', 'dnt': '1', 'upgrade-insecure-requests': '1', 'user-agent': '', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'navigate', 'sec-fetch-user': '?1', 'referer': '', 'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}

        if (self.header != {}) and (header is None) and (not change):
            return self.header
        elif (header is not None):
            self.header = header
            return header
        else:
            if (agent == '') and (type(self.agent) is list):
                agent = random.choice(self.agent)
            elif agent != '':
                agent = agent

            if ref == '' and self.ref != []:
                if isinstance(self.ref, list):
                    ref = random.choice(self.ref)
                elif isinstance(self.ref, str):
                    ref = self.ref

            headers['user-agent'] = str(agent)
            headers['referer'] = str(ref)

            return headers

    async def set_url_params(self, url, params={}):
        """Set the parameters in a URL."""
        if params != {}:
            params = {k: v for k, v in params.items() if v != None or v != ''}
            encoded_params = urlencode(params)
            url = f"{url}?{encoded_params}"
        return url

    async def get_urlinfo(self, url):
        """Return the info of the URL."""
        ino = urlparse(url)
        return {'scheme':ino.scheme, 'hostname':ino.hostname, 'path':ino.path,'params':dict(parse_qsl(ino.params)), 'query':ino.query, 'fragment':ino.fragment}

    async def parse_url_parameters(self, url):
        """Get parameters from the URL."""
        return await self.get_urlinfo(url)['params']

    async def request(self, url, method='get', params=None, data=None, json=None, header=None, cookies=None, timeout=5, redirect=True, verify=True, proxy=None, ref='', agent='', break_pt=[]):
        """Make an asynchronous HTTP request."""
        break_pt = self.break_pt if break_pt == [] else break_pt
        if break_pt != []:
            await asyncio.sleep(random.uniform(break_pt[0], break_pt[1]))
        proxy = await self.get_proxy() if proxy is None else proxy
        header = await self.headers(agent, ref) if header is None else header

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, params=params, data=data, json=json, headers=header, cookies=cookies, timeout=timeout, allow_redirects=redirect, verify_ssl=verify, proxy=proxy) as response:
                return await response.text(), response

    async def requestSessions(self, url, method='get', params=None, data=None, json=None, header=None, cookies=None, timeout=5, sessions=None, redirect=True, verify=True, proxy=None, ref='', agent='', pre_request=False, break_pt=[]):
        """Make an asynchronous HTTP request with sessions."""
        break_pt = self.break_pt if break_pt == [] else break_pt
        if break_pt != []:
            await asyncio.sleep(random.uniform(break_pt[0], break_pt[1]))
        proxy = await self.get_proxy() if proxy is None else proxy
        header = await self.headers(agent, ref) if header is None else header 

        s = sessions if sessions is not None else aiohttp.ClientSession()
        if header is not None:
            s.headers.update(header)
        if cookies is not None:
            s.cookies.update(cookies)
        s.connector.verify_ssl = verify
        s.connector.timeout = aiohttp.ClientTimeout(total=timeout)
        s.connector.allow_redirects = redirect

        if pre_request and sessions is None:
            if isinstance(pre_request, bool):
                info = await self.get_urlinfo(url)
                prevon = info['scheme'] + '://' + info['hostname']
                await s.get(prevon)
            else:
                await s.get(pre_request)

        async with s.request(method, url, params=params, data=data, json=json) as response:
            return await response.text(), response

    async def connect_websocket(self, url, on_message=None, on_error=None, on_close=None):
        """Connect to a WebSocket server at the specified URL."""
        async with websockets.connect(url, on_message=on_message, on_error=on_error, on_close=on_close) as ws:
            await ws.wait_closed()
            return ws

    async def send_websocket_message(self, ws, message):
        """Send a message over a WebSocket connection."""
        await ws.send(message)
    
    async def close_websocket(self, ws):
        """Close a WebSocket connection."""
        await ws.close()

    async def check_connection(self, url=''):
        """
            check_connections()
            -------------------

            This method is to check if there is an internet connection available or not.

            Args:
                url (str, optional): URL to check the internet connection. Defaults to ''.

            Returns:
                bool: True if connection is available, False otherwise.
        """
        try:
            url = url if url != '' else 'https://www.google.com'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return True
        except aiohttp.ClientError:
            return False



if __name__ == '__main__':
    requester = Requester()
    # Make a synchronous HTTP GET request
    response_text, response = requester.request('https://api.example.com/data')
    # Print the response text
    print(response_text)



