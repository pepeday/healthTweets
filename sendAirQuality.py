from tweetme import tweetme
from airQualityCy import airQuality
from pushover import pushover
import logging
app_name="Air Quality"

logging.basicConfig(format='%(levelname)s %(asctime)s: %(message)s', filename=f'{app_name}.log',level=logging.DEBUG)


push=pushover('Air Quality',config_file='config_pushover.json')
airQualityUpdater = airQuality()
twitter = tweetme(config_file='config_tweepy.json')
try:
    data = airQualityUpdater.getData()
    pollutants = airQualityUpdater.checkPollutants(data)
    if pollutants:
        text = airQualityUpdater.getTweet(pollutants)
        twitter.send(text)
        push.send(text)
        logging.info(text)
    else:
        push.send("Air Quality is not exceeding limits.")
        logging.warning('Air quality is not exceeding limits.')
except Exception as e:
    push.send(f'''Air Quality tweet failed!
{e.args}''')
    logging.error(e.args)