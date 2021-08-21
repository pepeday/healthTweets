import requests

class pushover:
    def __init__(self,app:str) -> None:
        self.token="a3984bqyabhrqo8be2ji49xoktz5ss"
        self.userKey="u3fcgbb9pcj5dw8tmuzzs4s5a4hccm"
        self.url="https://api.pushover.net/1/messages.json"
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

        