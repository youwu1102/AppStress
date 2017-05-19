# -*- encoding:UTF-8 -*-
__author__ = 'c_youwu'
import threading
import time
from PrintInfo import Print


class TestExecution(threading.Thread):
    def __init__(self, device, cases, output):
        threading.Thread.__init__(self)
        self.device = device
        self.cases = cases
        self.Print = Print(output, device)

    def run(self):
        while True:
            for case in self.cases:
                self.Print.info(self.device + case)
