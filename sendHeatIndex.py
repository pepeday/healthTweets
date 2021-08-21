from heatIndex import heatIndex
from tweetme import tweetme
from pushover import pushover
import logging
app_name="Heat Index"

logging.basicConfig(format='%(levelname)s %(asctime)s: %(message)s', filename=f'{app_name}.log',level=logging.DEBUG)

push=pushover("Heat Index")
heat=heatIndex()
twitter=tweetme(config_file='config.json')
img='heat index explanatory.png'

try:
    results=heat.getResponse()
    values=heat.extractValues(results,heat.stationList,heat.observationNames)
    isOver=heat.checkIfExceeding(values)
    if heat.checkIfAnyIsExceeding(values):
        text=heat.getTweet(values)
        twitter.send(status=text,media=img)
        push.send(text)
        logging.info(text)
    else:
        push.send("No value was exceeding")
        logging.warning('No value was exceeding')
        pass
except Exception as e:
    push.send(f'''Heat index failed to send. Error:
    {e.args}''')
    logging.error(e.args)
    pass