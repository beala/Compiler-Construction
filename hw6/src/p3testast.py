import sys 
import compiler
import os
from p3declassify import *
from p3uniquify import *
from p3explicate import *
from p3closure import *
from p3flattener import *
from Myx86Selector import *
from InterferenceGraph import *
from p3removestructuredcontrolflow import *
from p3heapify import *

class P3TestAST(object):

	stageDict = { 	"parse"		: 0,
					"declassify"	: 1,
					"uniquify"	: 2
					"explicate"	: 3,
					"heapify"	: 4,
					"close"		: 5,
					"flatten"	: 6,
					"select"	: 7,
					"allocate"	: 8,
					"remove"	: 9,
					"print"		: 10,	}

	def compileToStage(self, program,  stage, debug = False):
		returnString = ""

		to_declassify = compiler.parseFile(program)
		if debug: self.print_ast(to_declassify, "Parsed")
		if stageDict[stage] < stageDict["declassify"]: return
		to_uniquify = P3Declassify().visit(to_declassify)
		if debug: self.print_ast(to_uniquify, "Declassified")
		if stageDict[stage] < stageDict["uniquify"]: return
		to_explicate = P3Uniquify().visit(to_uniquify)
		if debug: self.print_ast(to_explicate, "Uniquified")
		if stageDict[stage] < stageDict["explicate"]: return
		to_heapify = P3Explicate().visit(to_explicate)
		if debug: self.print_ast(to_heapify, "Explicated")
		if stageDict[stage] < stageDict["heapify"]: return
		to_closure_convert = P3Heapify().visit(to_heapify)
		if debug: self.print_ast(to_closure_convert, "Heapified")
		if stageDict[stage] < stageDict["close"]: return
		(ast, fun_list) = P3Closure().visit(to_closure_convert)
		to_flatten = P3Closure().doClosure(to_closure_convert)
		if debug: self.print_ast(to_flatten, "Closure Conversion")
		if stageDict[stage] < stageDict["flatten"]: return
		flattened = P3ASTFlattener().visit(to_flatten)
		if debug: self.print_ast(flattened, "Flattened AST")
		if stageDict[stage] < stageDict["select"]: return
		selected = []
		for func in flattened:
			selected.append(Myx86Selector().generate_x86_code(func))
			if debug: self.print_ast(selected[-1], "Instruction Selection")
		if stageDict[stage] < stageDict["allocate"]: return
		allocated = []
		igList = []
		for func in selected:
			igList.append(InterferenceGraph(func))
			allocated.append(igList[-1].allocateRegisters())
			if debug: self.print_ast(allocated[-1], "Register Allocation")
		if stageDict[stage] < stageDict["remove"]: return
		removed = []
		for func in allocated:
			removed.append(P3RemoveStructuredControlFlow().removeIfs(func))
			if debug: self.print_ast(removed[-1], "Remove Struct Control Flow")
		if stageDict[stage] < stageDict["print"]: return
		counter = 0
		for func in removed:
			igList[counter].setIR(func) 
			returnString += igList[counter].emitColoredIR()
			counter += 1
		return returnString

	def print_stage(self, stage):
		print "-"*20 + str(stage) + "-"*20

	def print_ast(self, stmt_ast, stage, tabcount=0):
		if tabcount == 0:
			self.print_stage(stage)
		for node in stmt_ast.nodes:
			if isinstance(instruction, x86.Ifx86):
				print "\t" * indents + "If: " + str(instruction.operandList[0])
				self.print_ast(instruction.operandList[1], stage, indents+1)
				print "\t" * indents + "Else:"
				self.print_ast(instruction.operandList[2], stage, indents+1)
				print "\t" * indents + "EndIf"
			elif isinstance(instruction, x86.Whilex86):
				print "\t" * indents + "While: " + str(instruction.operandList[0])
				self.prettyPrint(instruction.operandList[1], stage, indents+1)
				print "\t" * indents + "EndWhile"
			elif isinstance(node, If):
				print '\t' * tabcount + 'If: ' + str(node.tests[0][0]) + ' then:'
				self.print_ast(node.tests[0][1], stage, tabcount+1)
				print '\t' * (tabcount) + 'Else: '
				self.print_ast(node.else_, stage, tabcount+1)
				print '\t' * (tabcount) + 'End If'
			elif isinstance(node, While):
				print '\t' * tabcount + 'While: ' + str(node.test) + ' then:'
				self.print_ast(node.body, stage, tabcount+1)
				print '\t' * (tabcount) + 'End While'
			elif isinstance(node, Lambda):
				print '\t' * tabcount + 'Lambda (' + str(node.argnames) + '):'
				self.print_ast(Stmt([node.code]), stage, tabcount+1)
				print '\t' * tabcount + 'EndLambda'
			elif isinstance(node, Function):
				print '\t' * tabcount + 'def ' + str(node.name) + '(' + str(node.argnames) + '):'
				self.print_ast(node.code, stage, tabcount+1)
				print '\t' * tabcount + 'EndFunc'
			else:
				print '\t' * (tabcount) + str(node)

if __name__ == "__main__":
	myfile = sys.argv[1]
	programString = P3TestAST().compileToStage(myfile, sys.argv[2], sys.argv[3])
	
	if sys.argv[3]  == "print":
		basename = myfile[:len(myfile)-3]
		file = open(basename + ".s", "w")
		file.write(programString)
		file.close()
