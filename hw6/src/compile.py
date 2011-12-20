import sys

import parse
import declassify

class Compiler(object):

    compiled = None
    inFilename = None
    outFilename = None

    def __init__(self, in_filename, out_filename):
        self.inFilename = in_filename
        self.outFilename = out_filename

    def compile(self):
        stages = [parse.Parse(),
                  declassify.Declassify()]
        stage_input = self.inFilename
        for stage in stages:
            stage.setInput(stage_input)
            stage_output = stage.do()
            stage_input = stage_output
        self.compiled = stage_output

    def write(self):
        out_file = open(self.outFilename, "w")
        out_file.write(str(self.compiled))
        out_file.close()

    def setFlags(self, flags):
        pass

    def setOutFile(self, filename):
        self.outFilename = filename

if __name__ == "__main__":
    compiler = Compiler(sys.argv[1], sys.argv[2])
    compiler.compile()
    compiler.write()
