from xml.etree.ElementTree import parse

class Case(object):
    @staticmethod
    def parse(case_path):
        doc = parse(case_path)
        root = doc.getroot()
        return Case.__find_child(root)

    @staticmethod
    def __find_child(parent_node):
        children = parent_node.getchildren()
        if children:
            for child in children:
                child.attrib['533ab525a8760351'] = Case.__find_child(child)  # 533ab525a8760351 = child
        return children


    # @staticmethod
    # def parse(case_path):
    #     actions = list()
    #     doc = ElementTree.parse(case_path)
    #     nodes = doc.getiterator('action')
    #     for node in nodes:
    #         actions.append(node.attrib)
    #     return actions

# if __name__ == '__main__':
#     aa = Case.parse('C:\\Users\\c_youwu\\Documents\\GitHub\\AppStress\\repository\\cases\\L\\d.xml')
#     print 'ssssssssssssss'
#     for a in aa:
#         print a
#         children = a.attrib.get('child')
#         for child in children:
#             print child.tag, child.attrib
