import logging
import sys

# Setup logger
log_formatter = logging.Formatter('\n%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Log to file
file_handler = logging.FileHandler('MAP.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Log to console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)
