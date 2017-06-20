# -*- encoding:UTF-8 -*-
from uiautomator import Device
from uiautomator import JsonRPCError
from time import sleep
from random import randint

# http://xiaocong.github.io/slides/android-uiautomator-and-python/#/first-usage
class UiAutomator(object):
    def __init__(self, serial=None):
        self.device = Device(serial)
        self.selector_mapping = {'text': 'text',
                                 'id': 'resourceId',
                                 'desc': 'description',
                                 'class': 'className',
                                 'index': 'index'}

    def do_action(self, **kwargs):
        action_name = kwargs.get('name').lower()
        if not action_name:
            return False
        elif action_name == 'press':
            return self.__press(**kwargs)
        elif action_name == 'click':
            return self.__click(**kwargs)
        elif action_name == 'random_click':
            return self.__random_click(**kwargs)
        elif action_name == 'edit':
            return self.__edit(**kwargs)
        elif action_name == 'wait':
            return self.__wait(**kwargs)
        elif action_name == 'wakeup':
            return self.__wakeup()
        elif action_name == 'sleep':
            return self.__sleep()
        elif action_name == 'objectinfo':
            return self.__get_object_info(**kwargs)
        elif action_name == 'orientation':
            return self.__orientation(**kwargs)
        elif action_name == 'get_current_package_name':
            return self.__get_current_package_name()
        elif action_name == 'open':
            return self.__open(**kwargs)

    def __get_selector(self, **kwargs):
        tmp = dict()
        for key in self.selector_mapping.keys():
            parameter_value = kwargs.get(key)
            if parameter_value:
                tmp[self.selector_mapping.get(key)] = parameter_value
        return tmp

    def __click(self, **kwargs):
        selector = self.__get_selector(**kwargs)
        try:
            return self.device(**selector).click()
        except JsonRPCError:
            return False

    def __random_click(self, **kwargs):
        selector = self.__get_selector(**kwargs)
        count = self.device(**selector).count
        if count <= 0:
            return False
        selector['instance'] = randint(0, count-1)
        self.device(**selector).click()




    def __press(self, **kwargs):
        key = kwargs.get('key')
        if key in ["home", "back", "left", "right", "up", "down", "center", "menu", "search", "enter",
                   "delete", "del", "recent", "volume_up", "volume_down", "volume_mute", "camera", "power"]:
            return self.device.press.__getattr__(key)()
        else:
            try:
                key_code = int(key)
                return self.device.press(key_code)
            except ValueError:
                return False

    def __open(self,**kwargs):
        key = kwargs.get('key')
        if key in ["notification", "quick_settings"]:
            return self.device.open.__getattr__(key)()
        return False

    def __orientation(self, **kwargs):
        # left/l:       rotation=90 , displayRotation=1
        # right/r:      rotation=270, displayRotation=3
        # natural/n:    rotation=0  , displayRotation=0
        # upsidedown/u: rotation=180, displayRotation=2
        value = kwargs.get('value')
        if value in ['l', 'r', 'n', 'u', 'left', 'right', 'natural', 'upsidedown']:
            self.device.orientation = value
            return True
        return False

    def __freeze_rotation(self, **kwargs):
        value = kwargs.get('value', 'true')
        if value in ['False', 'false', 'f']:
            return self.device.freeze_rotation(freeze=False)
        return self.device.freeze_rotation(True)

    def __edit(self, **kwargs):
        selector = self.__get_selector(**kwargs)
        text_input = kwargs.get('input')
        return self.device(**selector).set_text(text=text_input)

    def __get_object_info(self, **kwargs):
        selector = self.__get_selector(**kwargs)
        key = kwargs.get('key')
        if key:
            return self.device(**selector).info.get(key)
        return self.device(**selector).info

    def __wait(self, **kwargs):
        try:
            wait_time = int(kwargs.get('time'))
            sleep(wait_time/1000.0)
        except ValueError:
            sleep(1)
        return True

    def __wakeup(self):
        return self.device.wakeup()

    def __sleep(self):
        return self.device.sleep()


    # def info(self):
    #     return self.device.info
    #
    # def dump(self, filename=None, compressed=True, pretty=True):
    #     Utility.output_msg('Dump device window and pull to \"%s\".' % filename)
    #     return self.device.dump(filename=filename, compressed=compressed, pretty=pretty)
    #
    # def screenshot(self, filename, scale=1.0, quality=100):
    #     Utility.output_msg('Take screenshot and save to \"%s\".' % filename)
    #     return self.device.screenshot(filename=filename, scale=scale, quality=quality)
    #

    #
    # def long_click(self, **kwargs):
    #     try:
    #         return self.device(**kwargs).long_click()
    #     except JsonRPCError, e:
    #         return 'Error'
    #
    # def scroll(self, **kwargs):
    #     return self.device(**kwargs).scroll(steps=steps)
    #
    def __get_current_package_name(self):
        return self.device.info.get('currentPackageName')

    def get_device_info(self):
        return self.device.info



