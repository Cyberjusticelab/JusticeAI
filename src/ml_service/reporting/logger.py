import datetime
import time
import os

class Log():
    __script_dir = os.path.abspath(__file__ + "/../")
    __rel_path = r'log.txt'
    __output_directory = os.path.join(__script_dir, __rel_path)

    filename = __output_directory
    verbose = False
    start = 0
    complete_log = ""

    @staticmethod
    def initialize(filename=None, header=None, verbose=False):
        if filename is not None:
            Log.filename = filename
        Log.verbose = verbose
        if header is not None:
            file = open(Log.filename, 'a')
            file.writelines('\n========================\n')
            file.writelines(header + '\n')
            file.writelines('========================\n\n')

    @staticmethod
    def write(information):
        if Log.verbose:
            print(information)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file = open(Log.filename, 'a')
        file.writelines(now + ': ' + information + '\n')
        Log.complete_log += now + ': ' + information + '\n'
        file.close()

    @staticmethod
    def report_start():
        Log.start = time.time()
        Log.write("Starting")

    @staticmethod
    def report_end():
        end = time.time()
        diff = (datetime.timedelta(seconds=(Log.start - end)))
        Log.write("Elapsed time: " + str(diff))

    @staticmethod
    def clear_log():
        Log.complete_log = ''
