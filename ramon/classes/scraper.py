import requests, os
from requests_toolbelt      import MultipartEncoder
from bs4                    import BeautifulSoup    
from classes.preferences    import Preferences
from classes.log            import Log
from classes.database       import DDBB
from peewee import *

class Scraper:

    class Meta:
        database = DDBB.db

    def __init__(self, protocol="https", host="locahost", port=None, needs_login=False, login_form_url='', login_post_url='', login_username='', login_password='', target_url='', login_fields=[], login_tokens=[], cookies=[], form_boundary=False):
        # Please check if this association is even used on the code or remove it
        Preferences.data            = self     
        self.protocol               = protocol
        self.targets                = {}
        self.host                   = host
        self.port                   = port
        self.session                = None
        self.needs_login            = needs_login
        self.login_fields           = login_fields
        self.cookies                = { x : "" for x in cookies   }
        self.login_tokens           = { x : "" for x in login_tokens    }
        self.login_username         = login_username
        self.login_password         = login_password
        self.logged_in              = False
        self.parsed                 = None
        self.payload                = {}
        self.form_boundary          = form_boundary
        self.login_form_url         = self.url( login_form_url )
        self.login_post_url         = self.url( login_post_url )
        self.target_url             = self.url( target_url )
        #self.user_agent             = '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"'
        self.user_agent             = f'tRAckOverlayer/{ login_username }'
        self.form_data              = None        
        self.login_last_username    = None
        self.response               = None
        self.response_text          = None
        self.response_code          = None
        self.response_content       = None
        self.session                = requests.Session() if self.session is None else self.session
    
    def url(self, url):
        return f'{ self.protocol }://{ self.host }{ f":{ self.port }/" if self.port else "/"}{url}'

    def parse(self):
        self.parsed = BeautifulSoup( self.response_text, features='html.parser' )            
        return True
    
    def getPayload(self):
        self.request( self.target_url, filename="target" )
        if not self.response_text:
            Log.error("SCRAPER : Cannot get default Payload")
            return False
        self.payload = {}
        for key,targets in self.targets.items():
            try:
                self.payload.update({
                    key : self.response_content.decode('utf-8').split(targets[0])[1].split(targets[1])[0],
                })
            except Exception as E:
                Log.error(f"Cannot resolve target {key} while parsing {self.target_url}", E)
        return True
    
    def getCookies(self):
        cookie_root = self.session.cookies._cookies[self.host]['/']
        cookies     = { x : cookie_root[x].value for x in self.cookies }
        cookie_str  = []
        for key,value in cookies.items():
            cookie_str.append(f'{key}={value}')
        self.session.headers.update({ 'Cookie': ';'.join(cookie_str) })
    
    def getLoginTokens(self, response):
        tokens      = {}
        soup        = BeautifulSoup(response.text, features='html.parser')
        tags        = soup.find_all()
        for token in self.login_tokens.keys():
            for tag in tags:
                if 'name' in tag.attrs:
                    if tag.get('name') == token:
                        tokens[token] = tag.get('value')
        self.login_tokens = tokens
    
    def getFormPayload(self):
        # Login page form request.
        response    = self.session.get( self.login_form_url )
    
        # Extract payload data from login page.
        self.getCookies()
        
        # Find first field (_token) and capture value.
        self.getLoginTokens( response )
        
        self.form_data = {}

        for name,value in self.login_fields.items():
            self.form_data.update(
                {
                    name : value,
                }
            )

        for name,value in self.login_tokens.items():
            self.form_data.update(
                {
                    name : value,
                }
            )
        if self.form_boundary:
            self.getMultiPartBoundaryFormData()
        
    def get(self):
        if self.needs_login:
            Log.info('SCRAPER : Checking login...')
            if not self.login():
                Log.error("SCRAPER : Login failed")
                return False
        #print("SCRAPER : Getting payload...")
        if not self.getPayload():
            Log.error("SCRAPER : Cannot parse get payload HTML")
            return False
        #print("SCRAPER : Parsing payload...")
        return self.parse()
    
    def validateLoginUsername(self):
        return False if (
            ''  in [ self.login_username, self.login_password ] or  
            ' ' in [ self.login_username, self.login_password ] 
        ) else True
    
    def sameLoginUsername(self):
        return self.login_last_username == self.login_username
    
    def storeSession(self):
        return
        
    def retrieveSession(self):
        return
    
    def login(self):
        try:
            # Avoid double login, but keep ability to re-login if username changes during execution
            if self.sameLoginUsername() and self.logged_in: return True
            if not self.validateLoginUsername() : return False
        
            Log.info("SCRAPER : Logging in...")
            
            # Inject headers for future requests
            self.session = requests.Session() if self.session is None else self.session
            self.session.headers.update({
                'Host'                      : self.host,
                # 'User-Agent'                : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31',
                'User-Agent'                : f'tRAckOverlayer/{self.login_username}',
                'Accept'                    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language'           : 'ES,es;q=0.9,en;q=0.8,fr;q=0.7,gl;q=0.6',
                'Accept-Encoding'           : 'gzip, deflate',
                'Cache-Control'             : 'max-age=0',
                'Origin'                    : f'{self.protocol}://{ self.host }',
                'Referer'                   : self.login_form_url,
                'Content-Type'              : f'multipart/form-data',
                'Sec-Ch-Ua'                 : self.user_agent,
                'Sec-Ch-Ua-Mobile'          : '?0',
                'Sec-Ch-Ua-Platform'        : '"Windows"',
                'Sec-Fetch-Dest'            : 'document',
                'Sec-Fetch-Mode'            : 'navigate',
                'Sec-Fetch-Site'            : 'same-origin',
                'Sec-Fetch-User'            : '?1',
                'Upgrade-Insecure-Requests' : '1',
            })
            
            # Get form and Create form response
            self.getFormPayload()
            Log.info("SCRAPER : Got login response, sending payload...")
            # Request for login.
            result = self.request( self.login_post_url, self.form_data, 'login-response', post=True)
            
            # Memorize user if login was sucessful before returning
            self.login_last_username = self.login_username if result else None
            Log.info("SCRAPER : Logged in successfully!")
            return result
        
        except Exception as E:
            Log.error(f"SCRAPER : Cannot log into {self.host}", E)
            self.session    = None
            self.logged_in  = False
            return False

    def getMultiPartBoundaryFormData( self ):
            import random, string
            boundary_token = ''.join(
                random.sample(
                    string.ascii_letters + string.digits, 
                    16
                )
            )
            self.session.headers.update({
                'Content-Type' : f'multipart/form-data;boundary=----WebKitFormBoundary{boundary_token}'
            })
            self.form_data = MultipartEncoder(
                fields   = self.form_data, 
                boundary = f'----WebKitFormBoundary{boundary_token}'
            )

    def request( self, url, data=None,  filename="request", post=False):
        self.response = None
        try:
            if self.needs_login: 
                self.getCookies()
            response                = self.session.post( url, data=data ) if post else self.session.get( url, data=data ) 
            self.response           = response
            self.response_text      = response.text
            self.response_code      = response.status_code
            self.response_content   = response.content
            with open(f'{ Preferences.settings["root"] }/data/{ filename }.html', "wb") as file:
            # Dump copy of profile HTML at data/profile.html
                file.write( self.response_content )            
        
            return True
        except Exception as E:
            Log.error(f"SCRAPER : Request for { url } failed", E)
            self.response_code      = None
            self.response_content   = None
            self.response_text      = str(E)
            self.response_content   = str(E)
            return False
