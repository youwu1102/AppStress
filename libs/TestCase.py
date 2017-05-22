from xml.etree import ElementTree

class TestCase(object):
    @staticmethod
    def parse(case_path):
        actions = list()
        doc = ElementTree.parse(case_path)
        nodes = doc.getiterator('action')
        for node in nodes:
            actions.append(node.attrib)
        return actions


if __name__ == '__main__':
    print TestCase.parse('C:\\Users\\c_youwu\\Documents\\GitHub\\AppStress\\repository\\cases\\L\\d.xml')
    print 's'