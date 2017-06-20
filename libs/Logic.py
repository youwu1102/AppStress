__author__ = 'c_youwu'
from Case import Case

class ExecutionModule(object):
    def __init__(self, device, Print):
        self.device = device
        self.Print = Print
        self.tv = TemporaryVariable()

    def reset_variable(self):
        self.tv = TemporaryVariable()

    def switch_step(self, step):
        step_name, step_value = step.tag, step.attrib
        #self.Print.debug(step_name)
        #self.Print.debug(step_value)
        if step_name == "if":
            self.__if(step_value)
        elif step_name == "loop":
            self.__loop(step_value)
        elif step_name == "assign":
            self.__assign(step_value)
        elif step_name == "action":
            return self.device.do_action(**step_value)

    def __loop(self, step_value):
        children = step_value.get('533ab525a8760351')
        try:
            time = int(step_value.get('time', '1'))
        except ValueError:
            time = 1
        if not children:
            return
        for i in xrange(time):
            for child in children:
                self.switch_step(child)

    def __while(self):
        pass

    def __assign(self, step_value):
        children = step_value.get('533ab525a8760351')
        assignment = children[0]
        variable = step_value.get('variable')
        value = self.device.do_action(**assignment.attrib)
        self.Print.debug('assign>> \"%s = %s\"' % (variable, value))
        self.tv.__setattr__(variable, value)

    def __if(self, step_value):
        children = self.__get_attrib(step_value, '533ab525a8760351')
        if not children:
            return
        expression = self.__get_attrib(step_value, 'expression')
        value = self.__get_attrib(step_value, 'value')
        variable = self.__get_attrib(step_value, 'variable')
        self.Print.debug('if>> \"%s %s %s\"' % (self.tv.__getattribute__(variable), expression, value))
        if ExecutionModule.__convert_expression(self.tv.__getattribute__(variable), expression, value):
            for child in children:
                self.switch_step(child)

    @staticmethod
    def __convert_expression(left, expression, right):
        if expression == "<":
            return left < right
        elif expression == "<=":
            return left <= right
        elif expression == ">":
            return left > right
        elif expression == ">=":
            return left >= right
        elif expression == "==":
            return left == right
        elif expression == "in":
            return left in right
        elif expression == "!=":
            return left != right
        else:
            print expression

    def __get_attrib(self, node, attrib_name):
        return node.get(attrib_name)

class CheckModule(object):
    def __init__(self, _print, cases):
        self._print = _print
        self.cases = cases
        self.__status = True

    def get_status(self):
        return self.__status

    def run(self):
        for case in self.cases:
            self._print('Processing: ' + case)
            steps = Case.parse(case_path=case)
            for step in steps:
                self.switch_step(step)

    def switch_step(self, step):
        step_name, step_value = step.tag, step.attrib
        if step_name == "if":
            self.__if(step_value)
        elif step_name == "loop":
            self.__loop(step_value)
        elif step_name == "assign":
            self.__assign(step_value)
        elif step_name == "action":
            pass

    def __assign(self, step_value):
        self.__step_msg('assign')
        children = self.__check_attrib(step_value, '533ab525a8760351')
        assignment = children[0]
        if assignment.tag != 'action':
            self._print("Error assignment statement")
            self.__status = False

    def __if(self, step_value):
        self.__step_msg('if')
        children = self.__check_attrib(step_value, '533ab525a8760351')
        expression = self.__check_attrib(step_value, 'expression')
        value = self.__check_attrib(step_value, 'value')
        variable = self.__check_attrib(step_value, 'variable')
        for child in children:
            self.switch_step(child)

    def __loop(self, step_value):
        self.__step_msg('loop')
        children = self.__check_attrib(step_value, '533ab525a8760351')
        time = self.__check_attrib(step_value, 'time')
        for child in children:
            self.switch_step(child)

    def __check_attrib(self, node, attrib_name):
        if attrib_name not in node.keys():
            if attrib_name == '533ab525a8760351':
                self._print("--can not found child")
            self._print("--can not found except attribute: \"%s\"" % attrib_name)
            self.__status = False
            return False
        return node.get(attrib_name)

    def __step_msg(self, step_name):
        self._print('-Step:%s' % step_name)

class TemporaryVariable (object):
    def __init__(self):
        pass
