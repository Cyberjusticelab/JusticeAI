import logging
import os
from util.constant import Path


class Log:
    __output_dir = Path.root_directory
    __rel_path = 'server.log'
    __filename = os.path.join(__output_dir, __rel_path)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s: %(message)s',
                        datefmt='%y/%m/%d-%H:%M:%S',
                        filename=__filename,
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)-0s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__filename)

    @staticmethod
    def write(text):
        Log.logger.info(text)
