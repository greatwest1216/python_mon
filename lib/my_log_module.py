import logging
import datetime

# log file name
today1 = datetime.date.today()

# Initiate logger
logger = logging.getLogger('LoggingTest')

# Logger level
logger.setLevel(10)

#logfile1 = ''

def logfile_name(name1):
    global logfile1, fh
    logfile1 = 'logs/' + str(today1) + '_' + name1 + '.log'
    # Log file
    fh = logging.FileHandler(logfile1)
    logger.addHandler(fh)
    # Log Format
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    fh.setFormatter(formatter)
    return 

