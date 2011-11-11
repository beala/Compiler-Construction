class ASTVisitor(object):
	def visit(self, node, *extra):
		'''Visit a node'''
		# Find a specific visit method. Default to "default".
		methname = "visit_%s" % node.__class__.__name__
		method = getattr(self, methname, self.default)
		return method(node, *extra)
	
	def default(self, node, *extra):
		'''Visit node children'''
		raise TypeError("Uh oh: A method doesn't exist for this node type: %s" % node.__class__.__name__)
		import pdb; pdb.set_trace()
