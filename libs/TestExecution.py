# -*- encoding:UTF-8 -*-
__author__ = 'c_youwu'
import threading
from PrintInfo import Print
from Utility import Utility
from os.path import join
from GlobalVariable import GlobalVariable
from UiAutomator import UiAutomator, TemporaryVariable
from time import sleep
from Logic import Logic



class TestExecution(threading.Thread):
    def __init__(self, serial, cases, output):
        threading.Thread.__init__(self)
        self.serial = serial
        self.cases = cases
        self.Print = Print(output, serial)
        self.device = UiAutomator(serial)
        self.Print.info('UiAutomator')
        self.tv = TemporaryVariable()

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
        self.tv = TemporaryVariable()
        steps = Utility.test_case_parse(case_path=case)
        for step in steps:
            self.Print.debug(self.switch_step(step=step))
    # ==========================================================






    def switch_step(self, step):
        step_name, step_value = step.tag, step.attrib
        self.Print.debug(step_name)
        self.Print.debug(step_value)
        if step_name == "if":
            self.__if(step_value)
        elif step_name == "while":
            pass
        elif step_name == "loop":
            self.__loop(step_value)
        elif step_name == "assign":
            self.__assign(step_value)
        elif step_name == "action":
            return self.device.do_action(**step_value)
        elif step_name == "function":
            return self.__funciton(step_value)


    def __loop(self, step_value):
        children = step_value.get('533ab525a8760351')
        try:
            time = int(step_value.get('time', '1'))
        except ValueError:
            time = 1
        if not children:
            self.Print.error("Loop body is empty")
            return
        for i in xrange(time):
            for child in children:
                self.switch_step(child)

    def __while(self):
        pass

    def __assign(self, step_value):
        children = step_value.get('533ab525a8760351')
        if not children:
            self.Print.error("The assignment statement cannot be found")
            return
        assignment = children[0]
        if assignment.tag != 'action':
            self.Print.error("Error assignment statement")
            return
        self.tv.__setattr__(step_value.get('variable'), self.device.do_action(**assignment.attrib))

    def __if(self, step_value):
        print step_value
        children = step_value.get('533ab525a8760351')
        if not children:
            return
        expression = self.__check_attrib(step_value, 'expression')
        value = self.__check_attrib(step_value, 'value')
        variable = self.__check_attrib(step_value, 'variable')
        if expression is False or value is False or variable is False:
            return
        if Utility.convert_expression(self.tv.__getattribute__(variable), expression, value):
            for child in children:
                self.switch_step(child)

    def __check_attrib(self, node, attrib_name):
        if attrib_name not in node.keys():
            self.Print.error("Can not find \"%s\" in %s" % (attrib_name, str(node)))
            return False
        return node.get(attrib_name)

    def __funciton(self,step_value):
        pass

if __name__ == '__main__':
    te = TestExecution('ce58ac0d', ['C:\\Users\\c_youwu\\Documents\\GitHub\\AppStress\\repository\\cases\\L\\d.xml'], None)
    te.run()


