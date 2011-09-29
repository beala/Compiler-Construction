#!/usr/bin/python

#csci4555_compiler.py
from compiler.ast import *
import compiler
import sys
import string
import x86
import MyFlattener
import Myx86Selector
import compiler
import InterferenceGraph

class csci4555_compiler:
	myGraph = None
	def __init__(self,codefile):
		flattened_ast = MyFlattener.P0FlattenAST().visit(compiler.parseFile(codefile))
		x86IRObj = Myx86Selector.Myx86Selector(flattened_ast)
		#x86IRObj.calculateLiveSets()
		self.my_graph = InterferenceGraph.InterferenceGraph(x86IRObj.getIR())
		#self.my_graph.drawEdges()
		#self.my_graph.doColor()
		#print my_graph.printGraph()
		#x86IRObj.setIR(self.my_graph.getIR())
		self.my_graph.allocateRegisters()
	def getColoredIR(self):
		return ".globl main\nmain:\n"+self.my_graph.emitColoredIR()+"\tleave\n\tret\n"
		#print x86IRObj.emitx86Text()
if __name__ == "__main__":
	myfile = sys.argv[1]
	basename = myfile[:len(myfile)-3]
	compileObj = csci4555_compiler(myfile)
	file = open(basename+".s","w")
	file.write(compileObj.getColoredIR())
	file.close()
