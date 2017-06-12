# -*- encoding:UTF-8 -*-
__author__ = 'c_youwu'
import threading
from PrintInfo import Print
from Utility import Utility
from os.path import join
from GlobalVariable import GlobalVariable
from UiAutomator import UiAutomator
from time import sleep
from Logic import ExecutionModule



class TestExecution(threading.Thread):
    def __init__(self, serial, cases, output):
        threading.Thread.__init__(self)
        self.serial = serial
        self.cases = cases
        self.Print = Print(output, serial)
        self.device = UiAutomator(serial)
        self.Print.info('UiAutomator')
        self._exec = ExecutionModule(Print=self.Print, device=self.device)

    def run(self):
        self.__test_init()
        self.__test_exec()
        self.__test_end()

    def pause(self):
        pass

    def stop(self):
        pass

    def __test_init(self):
        self.destiny_time = GlobalVariable.test_start_time + GlobalVariable.test_time
        self.log_folder = Utility.create_folder(join(GlobalVariable.test_log_path, self.serial))

    def __test_exec(self):
        if GlobalVariable.test_policy == 'random':
            self.__random_test()
        elif GlobalVariable.test_policy == 'sequence':
            self.__sequence_test()

    def __test_end(self):
        pass


    def __random_test(self):
        from random import choice
        from time import time
        while time() < self.destiny_time:
            self.__test_unit(choice(self.cases))
            sleep(3)

    def __sequence_test(self):
        pass

    def __test_unit(self, case):
        self._exec.reset_variable()
        steps = Utility.test_case_parse(case_path=case)
        for step in steps:
            self.Print.debug(self._exec.switch_step(step=step))
    # ==========================================================






if __name__ == '__main__':
    te = TestExecution('ce58ac0d', ['C:\\Users\\c_youwu\\Documents\\GitHub\\AppStress\\repository\\cases\\L\\d.xml'], None)
    te.run()


