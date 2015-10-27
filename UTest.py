__author__ = 'chaba'

#import hypothesis
from hypothesis import given, Settings
import hypothesis.strategies as st

import time
import unittest
import STLParser
#import FOAMdata
import math
import copy
#import time


class ParserTests(unittest.TestCase):

    def setUp(self):
        print('start')
        self.file = open("Test.stl", 'w')
        self.file.write('solid TestSTL')
        self.file.close()


class SecondTestParser(ParserTests):
    NameFile = ['Moon.stl',
                'DiceCube.stl',
                'HalfDonut.stl',
                'FileSTL/DiceCube.stl',
                'FileSTL/HalfDonut.stl']

    with Settings(max_examples=500):
        @given(
                st.integers(
                             min_value = 0,
                             max_value = 4
                           )
              )
        def test_STLParser(self, n):
            print("n : ", n)
            a = STLParser.STLFile(self.NameFile[n])
            a.read_file_lines()
            a.Parse()
            a.write_file()
            print('name', a.Name)
            #print('vertex', a.vertex, "\nlen[vertex] : ", len(a.vertex))
            #print('facet', a.facet, "\nlen[facet] : ", len(a.facet))

    with Settings(max_examples=500):
        @given(st.lists(
                        st.lists(
                                 st.floats(
                                           min_value=-10,
                                           max_value=10
                                          ),
                                 min_size=3,
                                 max_size=3
                                ),
                        min_size=1000
                       )
              )
        def test_parse(self, l):
            print("************************l : ", l)
            self.file = open("Test.stl", 'w')
            self.file.write('solid TestSTL\n')

            cnt = 0

            for line in l:
                if cnt == 0:
                    #print('line : ',line)
                    string = '\tfacet normal '+' '.join(list(map(str, line)))+'\n'
                    self.file.write(string)
                    string = '\t\touter loop\n'
                    self.file.write(string)
                    cnt = 1
                elif cnt >= 1 and cnt <= 4:
                    string = '\t\t\tvertex '+' '.join(list(map(str, line)))+'\n'
                    self.file.write(string)
                    cnt += 1
                    if cnt == 4:
                        string = '\tendloop\n'
                        self.file.write(string)
                        cnt = 0


            self.file.close()
            print("len(l) : ", len(l))

            a = STLParser.STLFile('Test.stl')
            a.read_file_lines()
            a.Parse()
            print('name', a.Name)
            #print('vertex', a.vertex, "\nlen[vertex] : ", len(a.vertex))
            #print('facet', a.facet, "\nlen[facet] : ", len(a.facet))



if __name__ == '__main__':
    unittest.main()