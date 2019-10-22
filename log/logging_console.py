import logging
import sys

LEVELS = {
    'debug':    logging.DEBUG,
    'info':     logging.INFO,
    'warning':  logging.WARNING,
    'error':    logging.ERROR,
    'critical': logging.CRITICAL,
}

if len(sys.argv) > 1:
  level_name = sys.argv[1]
  level = LEVELS.get(level_name, logging.NOTSET)
else:
  print('Usage: python {} logging_lever'.format(sys.argv[0]))
  sys.exit(0)

# set logging format
logging.basicConfig(
  format='%(asctime)s.%(msecs)03d %(pathname)s:%(lineno)d] %(levelname)s: %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S', 
  level=level
  )

logging.debug('debug')
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.critical('critical')
logging.log(level,'log')



