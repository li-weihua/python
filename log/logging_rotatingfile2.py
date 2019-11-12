import glob
import logging
import logging.handlers

LOG_FILENAME = 'logging_rotatingfile.out'

# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=1024, # 1kb
    backupCount=20,
)

formatter = logging.Formatter(
  fmt='%(asctime)s.%(msecs)03d %(levelname).1s %(pathname)s:%(lineno)d] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S')

handler.setFormatter(formatter)

my_logger.addHandler(handler)

# Log some messages
for i in range(100):
    my_logger.debug('i = %d' % i)

# See what files are created
logfiles = glob.glob('%s*' % LOG_FILENAME)
for filename in sorted(logfiles):
    print(filename)
