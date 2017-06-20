# -*- encoding:UTF-8 -*-
from uiautomator import Device
from random import randint
for x in range(999):
    print randint(0, 8)
device = Device()
print device.info
print device(resourceId='com.android.systemui:id/tile_label', instance='4').click()
print