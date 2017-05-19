# -*- encoding:UTF-8 -*-
from xml.dom.minidom import Document
from xml.dom.minidom import parse
class TestCasePlan(object):
    @staticmethod
    def save(test_cases, save_path):
        doc = Document()
        root = doc.createElement('CasePool')
        for test_case in test_cases:
            case = doc.createElement("Case")
            case.setAttribute('path', test_case)
            root.appendChild(case)
        doc.appendChild(root)
        xml=open(save_path, 'w')
        xml.write(doc.toprettyxml(indent='', encoding='utf-8'))
        xml.close()

    @staticmethod
    def read(test_plan):
        test_case = []
        doc = parse(test_plan)
        cases = doc.getElementsByTagName('Case')
        for case in cases:
            test_case.append(case.getAttribute('path'))
        return test_case

