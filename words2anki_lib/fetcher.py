import re
from requests import get
from zipfile import ZipFile, ZIP_BZIP2
from os.path import exists, basename, sep
from time import sleep
from collections import namedtuple

class DataFetcher():
    cachefile:ZipFile = None
    requests_params:dict = None
    delay_params:dict = {'queries':30, 'delay':2, 'everyquery':0.1}
    query_counter = 0
    CachedRequest = namedtuple('CachedRequest', ['ok', 'content', 'fromcache', 'result'])
    dictionaries ={
        'ldoceonline':{'baseUrl':'https://www.ldoceonline.com', 'wordLookupUrl':'/dictionary/%s'}
    }
    currentDictionary = 'ldoceonline'

    def __init__(self, cachefile:str=None, requests_params:dict=None, currentDictionary:str='ldoceonline'):
        if cachefile:
            self.cachefile = ZipFile(cachefile, 'a' if exists(cachefile) else 'w', ZIP_BZIP2, compresslevel=9)
        self.requests_params = requests_params
        self.currentDictionary = currentDictionary

    def check_result(self, req, word:str, dictionary:str):
        if dictionary == 'ldoceonline':
            return not re.match(r'.*https:\/\/www\.ldoceonline\.com\/spellcheck\/.*', req.url)

        return True

    def get(self, url:str, word:str, type_:str, dictionary:str='ldoceonline'):
        # if url == None or url == '' or re.match('')
        name = f"{dictionary}/{type_}/{word}{'.html' if type_ == 'cache' else ''}"
        if self.cachefile:
            if name in self.cachefile.namelist():
                return self.CachedRequest(True, self.cachefile.read(name), True, True)
        if self.query_counter >= self.delay_params['queries']:
            self.query_counter = 0 # reset
            sleep(self.delay_params['delay'])
        else:
            sleep(self.delay_params['everyquery'])
        req = get(url, **self.requests_params)
        req.fromcache = False
        if req.ok:
            if self.check_result(req, word, dictionary):
                req.result = True
                if self.cachefile:
                    self.cachefile.writestr(name, req.content)
            else:
                req.result = False
            self.query_counter += 1
        return req
