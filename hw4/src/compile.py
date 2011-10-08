#!/usr/bin/python

#csci4555_compiler.py
from compiler.ast import *
import compiler
import sys
import string
import x86
import p1flattener
import Myx86Selector
import compiler
import InterferenceGraph
import p1removex86ifs
import p1explicate
class csci4555_compiler:
	myGraph = None
	def __init__(self,codefile):
		explicated_ast = p1explicate.P1Explicate().visit(compiler.parseFile(codefile))
		flattened_ast = p1flattener.P1ASTFlattener().visit(explicated_ast)
		ir = Myx86Selector.Myx86Selector().generate_x86_code(flattened_ast)
		#x86IRObj.calculateLiveSets()
		self.my_graph = InterferenceGraph.InterferenceGraph(ir)
		#self.my_graph.drawEdges()
		#self.my_graph.doColor()
		#print my_graph.printGraph()
		#x86IRObj.setIR(self.my_graph.getIR())
		self.my_graph.allocateRegisters()
		removethings = p1removex86ifs.P1Removex86Ifs(self.my_graph.getIR())
		final_ir = removethings.removeIfs()
		self.my_graph.setIR(final_ir)

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
