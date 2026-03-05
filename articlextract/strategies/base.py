
from typing import *

class BaseStrategy:
    
    def __init__(self,html:str,url:str=None):
        self.html = html
        self.url = url
    
    def extract(self) -> Dict:
        raise  NotImplementedError
    
    