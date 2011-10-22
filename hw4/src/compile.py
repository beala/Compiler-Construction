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
		#ir = Myx86Selector.Myx86Selector().reduceExtraMoves(ir)
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
	import sys 
	import compiler
	import os
	from p2uniquify import *
	from p2explicate import *
	from p2closure import *
	from p2flattener import *
	from Myx86Selector import *
	from InterferenceGraph import *
	from p1removex86ifs import *
	myfile = sys.argv[1]
	basename = myfile[:len(myfile)-3]
	to_explicate = compiler.parseFile(sys.argv[1])
	to_explicate = P2Uniquify().visit(to_explicate)
	to_closure_convert = P2Explicate().visit(to_explicate)
	(ast, fun_list) = P2Closure().visit(to_closure_convert)
	to_flatten = P2Closure().doClosure(to_closure_convert)
	flattened = P2ASTFlattener().visit(to_flatten)
	file = open(basename+".s","w")
	for func in flattened:
		tmpIR = Myx86Selector().generate_x86_code(func)
		ig = InterferenceGraph(tmpIR)
		coloredIR=ig.allocateRegisters()
		no_ifs = P1Removex86Ifs(coloredIR).removeIfs()
		ig.setIR(no_ifs)
		file.write(ig.emitColoredIR())
	file.close()
