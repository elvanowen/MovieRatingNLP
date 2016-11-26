import logging

logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler('tweet.log', mode='w'))

def log(message):
  logger.info('• ' + message)
  logger.info('')