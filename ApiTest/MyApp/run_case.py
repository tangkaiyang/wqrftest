import unittest

from A_WQRFhtmlRunner import HTMLTestRunner


class Test(unittest.TestCase):
    '测试类'

    def test_01(self):
        print("####test#####")


def run(Case_id, Case_name):
    suit = unittest.makeSuite(Test)
    filename = 'MyApp/templates/Reports/%s.html' % Case_id
    with open(filename, 'wb') as fp:
        runner = HTMLTestRunner(fp, title='接口测试平台测试报告: %s' % Case_name, description='用例描述')
        runner.run(suit)


if __name__ == '__main__':
    run()
