import logging
from blurring.data import WorkFolder

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)


folder = WorkFolder()
folder.setup()
