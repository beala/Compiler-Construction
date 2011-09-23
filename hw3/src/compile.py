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
	def __init__(self,codefile):
		flattened_ast = MyFlattener.MyFlattener().flatten(compiler.parseFile(codefile))
		x86IRObj = Myx86Selector.Myx86Selector(flattened_ast)
		x86IRObj.calculateLiveSets()
		my_graph = InterferenceGraph.InterferenceGraph(x86IRObj.getIR())
		my_graph.drawEdges()
		my_graph.doColor()
		print my_graph.printGraph()
		x86IRObj.setIR(my_graph.getIR())
		print x86IRObj.emitx86Text()
if __name__ == "__main__":
	myfile = sys.argv[1]
	basename = myfile[:len(myfile)-3]
	compileObj = csci4555_compiler(myfile)
	#file = open(basename+".s","w")
	#file.write(compileObj.get_generated_code())
	#file.close()
