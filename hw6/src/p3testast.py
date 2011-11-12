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
import x86
class P3TestAST(object):

	stageDict = { 	"parse"		: 0,
					"declassify"	: 1,
					"uniquify"	: 2,
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

		if self.stageDict[stage] < self.stageDict["declassify"]: return
		to_uniquify = P3Declassify().visit(to_declassify, None)
		if debug: self.print_ast(to_uniquify, "Declassified")

		if self.stageDict[stage] < self.stageDict["uniquify"]: return
		to_explicate = P3Uniquify().visit(to_uniquify)
		if debug: self.print_ast(to_explicate, "Uniquified")

		if self.stageDict[stage] < self.stageDict["explicate"]: return
		to_heapify = P3Explicate().visit(to_explicate)
		if debug: self.print_ast(to_heapify, "Explicated")

		if self.stageDict[stage] < self.stageDict["heapify"]: return
		to_closure_convert = P3Heapify().visit(to_heapify)
		if debug: self.print_ast(to_closure_convert, "Heapified")

		if self.stageDict[stage] < self.stageDict["close"]: return
		(ast, fun_list) = P3Closure().visit(to_closure_convert)
		to_flatten = P3Closure().doClosure(to_closure_convert)
		if debug: self.print_ast(Stmt(to_flatten), "Closure Conversion")

		if self.stageDict[stage] < self.stageDict["flatten"]: return
		flattened = P3ASTFlattener().visit(to_flatten)
		if debug: self.print_ast(Stmt(flattened), "Flattened AST")

		asmString = ""
		data_section = ""
		for func in flattened:
			selector = Myx86Selector()
			tmpIR = selector.generate_x86_code(func)
			data_section += selector.dataSection
			ig = InterferenceGraph(tmpIR)
			coloredIR=ig.allocateRegisters()
			no_ifs = P3RemoveStructuredControlFlow().removeIfs(coloredIR)
			ig.setIR(no_ifs)
			asmString += ig.emitColoredIR()
		return "\n"+ data_section +"\n.text"+asmString

		if self.stageDict[stage] < self.stageDict["select"]: return
		selected = []
		data_section = ""
		#x86Selector = Myx86Selector()
		for func in flattened:
			#selected.append(x86Selector.generate_x86_code(func))
			x86Selector = Myx86Selector()
			selected.append(x86Selector.generate_x86_code(func))
			data_section += x86Selector.dataSection
			if debug: self.print_ast(selected[-1], "Instruction Selection")
		if debug: print data_section
		#if debug: print x86Selector.dataSection

		if self.stageDict[stage] < self.stageDict["allocate"]: return
		allocated = []
		igList = []
		for func in selected:
			igList.append(InterferenceGraph(func))
			allocated.append(igList[-1].allocateRegisters())
			if debug: self.print_ast(allocated[-1], "Register Allocation")

		if self.stageDict[stage] < self.stageDict["remove"]: return
		removed = []
		for func in allocated:
			removed.append(P3RemoveStructuredControlFlow().removeIfs(func))
			if debug: self.print_ast(removed[-1], "Remove Struct Control Flow")

		if self.stageDict[stage] < self.stageDict["print"]: return
		counter = 0
		for func in removed:
			igList[counter].setIR(func) 
			returnString += igList[counter].emitColoredIR()
			counter += 1
		return "\n"+ data_section +"\n.text"+returnString
		#return "\n"+x86Selector.dataSection+"\n.text"+returnString

	def print_stage(self, stage):
		print "-"*20 + str(stage) + "-"*20

	def print_ast(self, stmt_ast, stage, tabcount=0):
		if tabcount == 0:
			self.print_stage(stage)
		if not isinstance(stmt_ast, Stmt):
			if isinstance(stmt_ast, Function):
				stmt_ast = stmt_ast.code
			elif isinstance(stmt_ast, Module):
				stmt_ast = stmt_ast.node
			else:
				print "\t" * tabcount + str(stmt_ast)
				return
		for node in stmt_ast.nodes:
			if isinstance(node, x86.Ifx86):
				print "\t" * tabcount + "If: " + str(node.operandList[0])
				self.print_ast(node.operandList[1], stage, tabcount+1)
				print "\t" * tabcount + "Else:"
				self.print_ast(node.operandList[2], stage, tabcount+1)
				print "\t" * tabcount + "EndIf"
			elif isinstance(node, x86.Whilex86):
				print "\t" * tabcount + "While: " + str(node.operandList[0])
				self.prettyPrint(node.operandList[1], stage, tabcount+1)
				print "\t" * tabcount + "EndWhile"
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
	
	if sys.argv[2]  == "print":
		basename = myfile[:len(myfile)-3]
		file = open(basename + ".s", "w")
		file.write(programString)
		file.close()
