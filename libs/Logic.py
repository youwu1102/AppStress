__author__ = 'c_youwu'
from Utility import Utility

class Logic(object):
    def __init__(self, device, Print):
        self.device = device
        self.Print = Print

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
