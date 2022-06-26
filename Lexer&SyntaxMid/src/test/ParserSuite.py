import unittest
from TestUtils import TestParser

class ParserSuite(unittest.TestCase):
    def test_simple_program(self):
        """Simple program: int main() {} """
        input = """abc = 1 + 2 ?? 3;"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,201))
    
    def test_wrong_miss_close(self):
        """Miss variable"""
        input = """u = array(a1 => 3 . 4, a2 => 3 + (u2 % 5));"""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,202))
