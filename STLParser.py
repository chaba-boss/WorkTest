__author__ = 'chaba'

import numpy, os, copy


class STLFile:

    def __init__(self, path):
        self.path = path
        k = self.path.split('/')
        self.namefile = k[-1].split('.')[0]
        self.ext = k[-1].split('.')[1]

        if len(k) > 1:
            print(type(k), k)
            k.pop(-1)
            self.PathWithoutFileName = ''+'/'.join(k)
        else:
            self.PathWithoutFileName = ''
        print('===init=== namefile : ', self.namefile, " , PathWithoutFileName : ", self.PathWithoutFileName)

    def read_file_lines(self):
        '''

        '''
        print(self.path)
        self.f = open(self.path, 'r')
        self.lines = self.f.readlines()
        self.f.close()

    def Parse(self, np = 0):
        '''

        '''
        self.p = STLParse()
        if np == 0:
            self.p.parse(self.lines)
        else:
            self.p.parse_numpy(self.lines)
        self.body = self.p.body
        self.vertex = self.p.body["vertex"]
        self.facet = self.p.body["facet"]
        self.Name = self.p.name

    def bin_parser(self, np = 0):
        '''
        experiment
        '''
        print("numpy_parser")
        self.f = open(self.path, 'rb')

        #print("start head : ", self.f.seek(0))
        self.h80 = self.f.read(80)
        self.header = self.h80.decode('ascii').split('\x00')[0].split()

        print("heder : ", self.header)
        self.Name = self.header[1]

        print('header : ', self.header, "end head : ", self.f.tell(), " , name : ", self.Name)

        size = os.fstat(self.f.fileno()).st_size
        dt = numpy.dtype("uint32")

        self.number = numpy.fromfile(self.f, dtype=dt, count=1)
        print("num : ", int(self.number[0]))

        num = int(self.number[0])
        dt = numpy.dtype("3float32, (3,3)float32, uint16")
        #dt = numpy.dtype({'names': ['facet','vertex','end'],
        #                  'formats': ["3float32", "(3,3)float32,", "uint16"]})
        self.body = numpy.fromfile(self.f, dtype=dt, count=num)
        #print("z : ", self.body)
        if np == 0:
            self.vertex = list(map(self.for_map_vartex, self.body))
            self.facet = list(map(self.for_map_facet, self.body))
        else:
            self.vertex = list(map(lambda x: x[1], self.body))
            self.facet = list(map(lambda x: x[0], self.body))

        #print("vartex : ", self.vertex, "\nfacet : ", self.facet)
        self.f.close()

    def for_map_vartex(self, a):
        return list(map(lambda i: list(i), a[1]))

    def for_map_facet(self, a):
        return list(a[0])

    def write_file(self):
        '''

        '''
        space = ' '
        tab = space*4
        newLine = '\n'
        if self.PathWithoutFileName != '':
            self.file = open(self.PathWithoutFileName+'/'+self.namefile+'_copy.'+self.ext, 'w')
        else:
            self.file = open(self.namefile+'_copy.'+self.ext, 'w')
        self.file.write('solid ' + self.Name + '_copy\n')
        cnt = 0
        for line in self.facet:
            string = '{}{}{}{}{}'.format(tab, 'facet normal', space, ' '.join(list(map(str, line))), newLine)
            self.file.write(string)
            string = '{}{}{}'.format(tab*2, 'outer loop', newLine)
            self.file.write(string)
            string = '{}{}{}{}{}'.format(tab*3, 'vertex', space, ' '.join(list(map(str, self.vertex[cnt][0]))), newLine)
            self.file.write(string)
            string = '{}{}{}{}{}'.format(tab*3, 'vertex', space, ' '.join(list(map(str, self.vertex[cnt][1]))), newLine)
            self.file.write(string)
            string = '{}{}{}{}{}'.format(tab*3, 'vertex', space, ' '.join(list(map(str, self.vertex[cnt][2]))), newLine)
            self.file.write(string)
            string = '{}{}{}'.format(tab*2, 'endloop', newLine)
            self.file.write(string)
            string = '{}{}{}'.format(tab, 'endfacet', newLine)
            self.file.write(string)
            cnt += 1
        string = 'endsolid ' + self.Name + '_copy\n'
        self.file.write(string)
        self.file.close()

    def write_bin_file(self):
        '''

        '''
        space = ' '
        tab = space*4
        newLine = '\n'
        if self.PathWithoutFileName != '':
            self.file = open(self.PathWithoutFileName+'/'+self.namefile+'_copy.'+self.ext, 'wb')
        else:
            self.file = open(self.namefile+'_copy.'+self.ext, 'wb')

        self.file.write(self.h80)
        self.file.write(self.number)
        #self.body.tofile(self.file)

        for i in range(self.number):
            self.facet[i].tofile(self.file)
            self.vertex[i].tofile(self.file)
            self.body[i][2].tofile(self.file)


class STLParse:

    def __init__(self):
        self.body = {"vertex": [], "facet": []}
        self.name = ''

    def parse(self, listLines):
        '''
        List lines ("string") is converted to a dictionary,
        that contains 2 keys "vertex" and "facet" to relevant content in the format list on list

        example:

        {"vertex": [[[1, 2, 3],
                     [1, 2, 3],
                     [1, 2, 3]],
                    [[1, 2, 3],
                     [1, 2, 3],
                     [1, 2, 3]]],
         "facet": [[1, 2, 3],[1, 2, 3],[1, 2, 3]]}
        '''
        cnt = 0
        for line in listLines:
            listLine = line.split()
            if listLine[0] == 'solid':
                self.name = listLine[1]
            elif listLine[0] == 'facet':
                listLine.pop(0)
                listLine.pop(0)
                l = list(map(float, listLine))
                self.body["facet"].append(l)
            elif len(listLine) > 1 and listLine[1] == 'loop':
                self.body["vertex"].append([])
            elif listLine[0] == 'vertex':
                listLine.pop(0)
                l = list(map(float, listLine))
                self.body["vertex"][cnt].append(l)
            elif listLine[0] == 'endloop':
                cnt += 1

    def parse_numpy(self, listLines):
        '''
        List lines ("string") is converted to a dictionary,
        that contains 2 keys "vertex" and "facet" to relevant content in the format array on list

        example:

        {"vertex": [array([[1, 2, 3],
                           [1, 2, 3],
                           [1, 2, 3]]),
                    array([[1, 2, 3],
                           [1, 2, 3],
                           [1, 2, 3]]]),
         "facet": [array([1, 2, 3]),array([1, 2, 3]),array([1, 2, 3])]}
        '''
        cnt = 0
        x = 0
        for line in listLines:
            listLine = line.split()
            if listLine[0] == 'solid':
                self.name = listLine[1]
            elif listLine[0] == 'facet':
                listLine.pop(0)
                listLine.pop(0)
                l = numpy.array(list(map(float, listLine)))
                #print("l : ", l)
                self.body["facet"].append(l)
            elif len(listLine) > 1 and listLine[1] == 'loop':
                self.body["vertex"].append([])
                x = 0
            elif listLine[0] == 'vertex':
                x += 1
                listLine.pop(0)
                l = (list(map(float, listLine)))
                ll = self.body["vertex"][cnt]
                ll.append(l)
                #print("ll : ", ll, " , x : ",x)
                if x == 3:
                    self.body["vertex"][cnt] = numpy.array(ll)
                else:
                    self.body["vertex"][cnt] = ll

            elif listLine[0] == 'endloop':
                cnt += 1


#a = STLFile('ktoolcav.stl')
#a = STLFile('FileSTL/ktoolcav.stl')
a = STLFile('DiceCube_binary.stl')

"""
try:
    a.read_file_lines()
except:
    a.numpy_parser()
"""

a.bin_parser(1)


#a.read_file_lines()
#a.Parse(1)
a.write_bin_file()
print('name : ', a.namefile)
#for i in range(len(a.facet)):
#print('facet\n', a.facet, " , type(a.facet[i]) : ", type(a.facet[0]))
#print('vertex\n', a.vertex, " , type(a.facet[i]) : ", type(a.facet[0]))

"""
a = STLFile('Moon.stl')
a.read_file_lines()
a.Parse()
a.write_file()
print('name', a.Name)
print('vertex', a.vertex, "\nlen[vertex] : ", len(a.vertex))
print('facet', a.facet, "\nlen[facet] : ", len(a.facet))

a = STLFile('DiceCube.stl')
a.read_file_lines()
a.Parse()
a.write_file()
print('name', a.Name)
print('vertex', a.vertex, "\nlen[vertex] : ", len(a.vertex))
print('facet', a.facet, "\nlen[facet] : ", len(a.facet))

a = STLFile('HalfDonut.stl')
a.read_file_lines()
a.Parse()
a.write_file()
print('name', a.Name)
print('vertex', a.vertex, "\nlen[vertex] : ", len(a.vertex))
print('facet', a.facet, "\nlen[facet] : ", len(a.facet))
"""