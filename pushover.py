import requests
import json
class pushover:
    def __init__(self,app:str,config_file:str) -> None:
        try:
            with open(config_file) as configuration:
                settings = json.load(configuration)
                self.token =  settings["token"]
                self.userKey = settings['userKey']
                self.url= settings['url']
        except:
            raise Exception('The configuration file does not exist or is invalid.')
        self.app=app

    def send(self,message:str):
        data={
            'token':self.token,
            'user':self.userKey,
            'message':message,
            'title':self.app
        }
        result = requests.post(url=self.url,data=data)
        return result.status_code

        