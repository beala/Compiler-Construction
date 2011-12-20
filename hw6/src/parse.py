import compiler

class Parse(object):
    def __init__(self):
        pass

    def setInput(self, src_filename):
        self.srcFilename = src_filename

    def do(self):
        return compiler.parseFile(self.srcFilename)
