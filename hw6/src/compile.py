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
from p3testast import *
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
	if sys.argv[1] == "-O":
		x86.x86.optimizeBehavior = True
		srcFile = sys.argv[2]
	else:
		x86.x86.optimizeBehavior = False 
		srcFile = sys.argv[1]
	myTester = P3TestAST()
	compiled = myTester.compileToStage(srcFile, 'print', False)
	basename = srcFile[:len(srcFile)-3]
	asmFile = open(basename + ".s", "w")
	asmFile.write(compiled)
	asmFile.close()

#if __name__ == "__main__":
#	import sys 
#	import compiler
#	import os
#	from p3declassify import *
#	from p3uniquify import *
#	from p3explicate import *
#	from p3closure import *
#	from p3flattener import *
#	from Myx86Selector import *
#	from InterferenceGraph import *
#	from p3removestructuredcontrolflow import *
#	from p3heapify import *
#	myfile = sys.argv[1]
#	basename = myfile[:len(myfile)-3]
#	parsed = compiler.parseFile(sys.argv[1])
#	declassified = P3Declassify().visit(parsed, None)
#	to_explicate = P3Uniquify().visit(declassified)
#	to_heapify = P3Explicate().visit(to_explicate)
#	to_closure_convert = P3Heapify().visit(to_heapify)
#	#(ast, fun_list) = P3Closure().visit(to_closure_convert)
#	to_flatten = P3Closure().doClosure(to_closure_convert)
#	flattened = P3ASTFlattener().visit(to_flatten)
#	file = open(basename+".s","w")
#	for func in flattened:
#		tmpIR = Myx86Selector().generate_x86_code(func)
#		ig = InterferenceGraph(tmpIR)
#		coloredIR=ig.allocateRegisters()
#		no_ifs = P3RemoveStructuredControlFlow().removeIfs(coloredIR)
#		ig.setIR(no_ifs)
#		file.write(ig.emitColoredIR())
#	file.close()
