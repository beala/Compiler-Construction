from p2explicate import *
from p3ast import *
class P3Explicate(P2Explicate):

	def _iterateOverAndVisit(self, toIterate):
		result = []
		for item in toIterate:
			result.append(self.visit(item))
		return result 

	def visit_If(self,node):
		myTest = self.visit(node.tests[0][0])
		myThen = self.visit(node.tests[0][1])
		myElse_ = self.visit(node.else_)
		#tmpMyTest = Name(self._makeTmpVar())
		#return Let( tmpMyTest, myTest, If([(tmpMyTest,myThen)],myElse_))
		return If([(myTest,myThen)],myElse_)

	def visit_While(self, node):
		myTest = self.visit(node.test)
		myBody = self.visit(node.body)
		#tmpMyTest = Name(self._makeTmpVar())
		#return Let( tmpMyTest, myTest, While(tmpMyTest, myBody, None)) 
		return While(myTest, myBody, None)

	def visit_CreateClass(self, node):
		newBases = []
		for base in node.bases:
			newBases.append(self.visit(base))
		return InjectFrom(self._typeMap['big'],CreateClass(newBases))
	
	def visit_AssAttr(self, node):
		newExpr = self.visit(node.expr)
		return AssAttr(newExpr, node.attrname, node.flags)
	
	def visit_Getattr(self, node):
		newExpr = self.visit(node.expr)
		return Getattr(newExpr, node.attrname)
	def visit_HasAttr(self, node):
		newExpr = self.visit(node.expr)
		return InjectFrom(self._typeMap['int'], HasAttr(newExpr, node.attrname))

	def visit_CallFunc(self, node):
		if( isinstance(node.node, Name) and node.node.name == 'input'):
			myExpr = Name(self._makeTmpVar())
			return Let(myExpr, node, InjectFrom(self._typeMap['int'], myExpr))	
		newArgs = []
		newArgs = [self.visit(argument) for argument in node.args]
		newNode = self.visit(node.node)
		node.args = newArgs
		#if node is a class, we have to instantiate object and call constructor
		tmpFunName = Name(self._makeTmpVar())
		tmpLettedArgs = []
		tmpO = Name(self._makeTmpVar())
		tmpIni = Name(self._makeTmpVar())
		tmp_ = Name(self._makeTmpVar())
		for element in node.args:
			tmpLettedArgs.append(Name(self._makeTmpVar()))
		body = IfExp(InjectFrom(self._typeMap['int'], CallFunc(Name('is_class'),[tmpFunName])), \
			Let(tmpO, InjectFrom(self._typeMap['big'],CallFunc(Name('create_object'), [tmpFunName])), \
			IfExp(InjectFrom(self._typeMap['int'], HasAttr(tmpFunName, '__init__')), \
			Let(tmpIni, InjectFrom(self._typeMap['fun'],CallFunc(Name('get_function'),[Getattr(tmpFunName,'__init__')])) \
			,Let(tmp_, CallFunc(tmpIni, [tmpO] + tmpLettedArgs), tmpO)), tmpO)), \
				IfExp( InjectFrom(self._typeMap['int'], CallFunc(Name('is_bound_method'),[tmpFunName])), \
								CallFunc(InjectFrom(self._typeMap['fun'],CallFunc(Name('get_function'), [tmpFunName])),[InjectFrom(self._typeMap['big'], CallFunc(Name('get_receiver'), [tmpFunName]))]+tmpLettedArgs)  , \
				IfExp(InjectFrom(self._typeMap['int'], CallFunc(Name('is_unbound_method'),[tmpFunName])), InjectFrom(self._typeMap['fun'],CallFunc(Name('get_function'),tmpLettedArgs)) ,CallFunc(tmpFunName, tmpLettedArgs)) \
			))
		encapsBody = body
		counter = 0
		for element in node.args:
			encapsBody = Let(tmpLettedArgs[counter], element, encapsBody)
			counter += 1
		return Let(tmpFunName, newNode, encapsBody)
