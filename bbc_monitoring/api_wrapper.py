# standard library
import requests
import json
import sys
sys.path.append('..')
# third party imports
from bs4 import BeautifulSoup
# local imports
from bbc_monitoring.error_handling import *

class BBCMonitoringApi:
    
    def __init__(self, api_key_path:str='..data/api_key.json', 
                 base_url:str='https://monitoring.bbc.co.uk/api/v0/'):
        """A class to set up a BBC monitoring sesison and to handle searches and
        queries.
        
        parameters
        ----------
        api_key_json : str
            Path to  the json containing the api username and password.
        base_url : str
            The base url for accessing BBC-Monitoring.
            
        attributes
        ----------
        base_url : str
            The base url for accessing BBC-Monitoring.
        session : requests.session
            A session object      
        """
        # set up the base url and add the trailing / if missing
        self.base_url = base_url
        if self.base_url[-1] != '/':
            self.base_url += '/'
        
        # set up headers
        self.headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json'}
        
        # get the authorization details
        try:
            with open(api_key_path, 'r') as f:
                key = json.load(f)[0]
        except FileNotFoundError:
            print('Check api_key_path is valid')
    
        # initialize session with authorization details    
        self.session = self.__start_session(key)
        
    def __start_session(self, key:dict):
        """Starts a session using the provided api key.
        parameters:
            key (dict) : username and password for BBC monitoring. 
        returns:
            session (requests.Session) : An authorized session.
        raises:
            various errors if session.status_code != 204.
        """
        # set up the session
        session = requests.session()
        # specify the login URL
        login_url = f'{self.base_url}login/'
        response = session.post(login_url, headers=self.headers, json=key)
        if response.status_code == 204:
            return session
        else:
            self.__raise_error(response.status_code, url=login_url, key=key)
            
    def __raise_error(self, status_code, **kwargs):
        if status_code == 404:
            raise URLNotFoundError(kwargs['url'])
        elif status_code == 401:
            raise AuthorizationError(kwargs['key'])
        elif status_code == 402:
            raise SubscriptionError()
        elif status_code == 403:
            raise TsAndCsError()
        elif status_code == 500:
            raise InternalServerError()
                    
    def end_session(self):
        """Closes the current session."""
        logout_url = f'{self.base_url}logout'
        self.session.post(logout_url, headers=self.headers)
        
    def search_by_id(self, id:str):
        """Searches for an article using id
        
        parameters:
            id (str) : a valid product id.
            
        returns:
            dict : A json describing the content related to the id.
            
        raises:
            URLNotFoundError : If a product with the given id can not be found.
        """
        url = f'{self.base_url}product/{id}'
        result = self.session.get(url)
        if result.status_code == 200:
            return result.json()
        else:
            raise URLNotFoundError(url, f"Article with id {id} not found")
    
    def parse_article(self, article:dict):
        """Parses an article to retun the body text as a single string
        
        parameters:
            article (dict) : the json result from searching by id.
            
        returns:
            str : The text in the main body of the article.
        """
        # get the text html only, removing headers etc.
        html_text = article['bodyHtml'].split('<p class="text">')[1]
        soup = BeautifulSoup(html_text, features="html.parser")
        raw_text = soup.get_text()
        # split into lines
        lines = [line.strip() for line in raw_text.splitlines()]
        text = ' '.join(line for line in lines if line)
        return text
    
    def search_headlines(self, query:str, limit:int=None):
        """Searches the API for articles with the query term within the headline
        
        parameters:
            query (str) : The term being searched.
            limit (int) : The max number of articles to be returned
        """
        url = f'{self.base_url}/search?headline={query}/'
        if limit:
            url += f'limit={limit}'
        result = self.session.get(url)
        return result.json()
    
    
    
    
            
        

