class P2Test(object):
	# Private Vars: ############################################################################################
	_headLen = 20

	_unprocessed = None
	_parsed = None
	_uniquified = None
	_explicated = None
	_heapified = None
	_stageDict = self._enum('parse', 'uniquify', 'explicate', 'heapify', 'closure' , 'flatten', 'selection', 'allocation', 'removeifs', 'output')
	# Private Methods: #########################################################################################
	def __init__(self, toProcess):
		self._unprocessed = toProcess

	# Desc: Creates an enum object.
	#	eg: Numbers = enum('ZERO', 'ONE', 'TWO')
	#		Numbers.ZERO == 0
	#		Numbers.ONE ==1
	# Credit: http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python/1695250#1695250
	def _enum(self, *sequential, **named):
		enums = dict(zip(sequential, range(len(sequential))), **named)
		return type('Enum', (), enums)

	def _printHeading(self, text):
		print "-"*self._headLen + str(text) + "-"*self._headLen 
		
	def _parseAndPrint(self, toParse):
		self._printHeading("Parsed AST")
		if os.path.isfile(toParse):
			print compiler.parseFile(sys.argv[1])
			parsed_ast = compiler.parseFile(sys.argv[1])
		else:
			print compiler.parse(toParse)
			parsed_ast = compiler.parse(sys.argv[1])
		return parsed

	def _uniquifyAndPrint(self, toUniquify):
		self._printHeading("Uniquified AST")
		uniquified = P2Uniquify().visit(toUniquify)
		P2Uniquify().print_ast(uniquified.node)
		return uniquified
		
	def _explicateAndPrint(self, toExplicate)	
		self._printHeading("Explicated AST")
		explicated = P2Explicate().visit(toExplicate)
		P2Uniquify().print_ast(explicated.node)
		return explicated

	def _heapifyAndPrint(self, toHeapify)
		self._printHeading("Heapified AST")
		heapified = P2Heapify().visit(toHeapify)
		P2Heapify().print_ast(heapified.node)

	def doParse(self):
		self._parsed = self._parseAndPrint(self._unprocessed)

	def doUniquify(self):
		self.doParse(self._unprocessed)
		self._uniquified = self._

	def doAll(self, lastStep):
		self._parsed = self._parseAndPrint(self._unprocessed)
		if lastStep == self._stageDict.parse:
			return self._parsed

		self._uniquified = self._uniquifyAndPrint(self._parsed)
		if lastStep == self._stageDict.uniquified:
			return self._uniquified
	
if __name__ == "__main__":
	import sys 
	import compiler
	import os
	from p2uniquify import *
	from p2explicate import *
	testTools = P2Test()
	testTools.parseAndPrint(sys.argv[2])
	if sys.argv[2] == "uniquifiy":
		return
	if sys.argv
