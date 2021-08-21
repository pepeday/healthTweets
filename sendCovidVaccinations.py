from tweetme import tweetme
from covidCY import covidCY
from pushover import pushover
import logging

app_name="Covid Vaccinations Cy"

logging.basicConfig(format='%(levelname)s %(asctime)s: %(message)s', filename=f'{app_name}.log',level=logging.DEBUG)


push = pushover('Covid Vaccinations Cy',config_file='config_pushover.json')

try:
    covidUpdater = covidCY()
    twitter = tweetme(config_file='config_tweepy.json')
    text = covidUpdater.text()
    twitter.send(text)
    push.send(text)
    logging.info(text)
except Exception as e:
    push.send('Covid vaccinations tweet failed.')
    logging.error('Covid vaccinations tweet failed.')