# -*- encoding:UTF-8 -*-
from TimeFormat import TimeFormat
import traceback
from wx import CallAfter
from GlobalVariable import GlobalVariable
from os.path import join
from time import sleep

class Print(object):
    def __init__(self, output, log_name):
        self.__output = output
        self.log_path = join(GlobalVariable.log_folder, log_name + '.txt')

    def __print(self, msg):
        CallAfter(self.__output, msg + '\r\n')
        sleep(0.05)


    def info(self, msg):
        msg = TimeFormat.timestamp() + '  INFO: ' + str(msg)
        self.__print(msg)
        self.__write(msg)

    def warm(self, msg):
        msg = TimeFormat.timestamp() + '  WARM: ' + str(msg)
        self.__print(msg)
        self.__write(msg)

    def error(self, msg):
        msg = TimeFormat.timestamp() + ' ERROR: ' + str(msg)
        self.__print(msg)
        self.__write(msg)

    def debug(self, msg):
        msg = TimeFormat.timestamp() + ' DEBUG: ' + str(msg)
        self.__print(msg)
        self.__write(msg)


    def result(self, msg):
        msg = TimeFormat.timestamp() + '  RSLT: ' + str(msg)
        self.__print(msg)
        self.__write(msg)

    def __write(self, msg):
        log = open(self.log_path, 'a+', 1)
        msg = msg.strip('\r\n')+'\n'
        log.write(msg)
        log.close()

    def traceback(self):
        tmp = traceback.format_exc()
        if tmp != 'None\n':
            self.debug(tmp.strip('\n'))







