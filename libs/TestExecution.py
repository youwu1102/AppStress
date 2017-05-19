# -*- encoding:UTF-8 -*-
__author__ = 'c_youwu'
import threading
from PrintInfo import Print
from Utility import Utility


class TestExecution(threading.Thread):
    def __init__(self, device, cases, output):
        threading.Thread.__init__(self)
        self.device = device
        self.cases = cases
        self.Print = Print(output, device)

    def run(self):
        for case in self.cases:
            Utility.parse_case(case_path=case)

