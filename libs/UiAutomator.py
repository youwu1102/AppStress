# -*- encoding:UTF-8 -*-
from uiautomator import Device
from uiautomator import JsonRPCError
from Utility import Utility


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
        #action_name = ''
        if not action_name:
            return False
        elif action_name == 'press':
            self.__press(**kwargs)
        elif action_name == 'click':
            self.__click(**kwargs)


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
        except JsonRPCError, e:
            return e

    def __press(self, **kwargs):
        key = kwargs.get('key')
        if key == ''
            self.device.press.


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
    # def get_current_package_name(self):
    #     try:
    #         return self.device.info.get('currentPackageName')
    #     except Exception:
    #         return self.get_current_package_name()
    #
    #
    #     # press key via name or key code. Supported key name includes:
    #     # home, back, left, right, up, down, center, menu, search, enter,
    #     # delete(or del), recent(recent apps), volume_up, volume_down,
    #     # volume_mute, camera, power.
    #     # Usage:
    #     # d.press.back()  # press back key
    #     # d.press.menu()  # press home key
    #     # d.press(89)     # press keycode
    #     #
    #     #     key=["home", "back", "left", "right", "up", "down", "center",
    #     #          "menu", "search", "enter", "delete", "del", "recent",
    #     #          "volume_up", "volume_down", "volume_mute", "camera", "power"]
    #

    #
    # def edit(self, **kwargs):
    #     text = Utility.random_char(10)
    #     Utility.output_msg('Edit:%s' % kwargs)
    #     Utility.output_msg('Input:%s' % text)
    #     try:
    #         return self.device(**kwargs).set_text(text)
    #     except JsonRPCError, e:
    #         return 'Error'
    #
    # def exists(self, **kwargs):
    #     return self.device(**kwargs).exists

if __name__ == '__main__':
    ui = UiAutomator()
    #print ui.click(**{'className': u'android.widget.TextView', 'index': u'1', 'resourceId': u'com.android.contacts:id/menu_search', 'description': u'Search', 'text': u''})
    print ui.get_current_package_name()
