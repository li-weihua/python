import glob
import logging
import logging.handlers

LOG_FILENAME = 'logging_rotatingfile.out'

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=1024, # 1kb
    backupCount=20,
)

# use the basic logger
logging.basicConfig(
  format='%(asctime)s.%(msecs)03d %(pathname)s:%(lineno)d] %(levelname)s: %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S', 
  level=logging.DEBUG,
  handlers = [handler]
  )

# log some messages
for i in range(100):
    logging.debug('i = %d' % i)

# See what files are created
logfiles = glob.glob('%s*' % LOG_FILENAME)
for filename in sorted(logfiles):
    print(filename)
