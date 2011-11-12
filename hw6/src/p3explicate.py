from p2explicate import *
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
		newBases = self.visit(node.bases)
		return CreateClass(newBases)
	
	def visit_AssAttr(self, node):
		newExpr = self.visit(node.expr)
		return AssAttr(newExpr, node.attrname, node.flags)
	
	def visit_Getattr(self, node):
		newExpr = self.visit(node.expr)
		return Getattr(newExpr, node.attrname)

	
	
		
