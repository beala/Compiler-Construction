class Stage(object):
    # Private Variables:
    # These are the function names that are reserved by the runtime.
    _reservedFuns = ['input', 'type_error', 'create_class', 'create_object',
                     'is_class', 'get_function', 'get_receiver',
                     'is_bound_method', 'is_unbound_method']

    # Public Methods:
    def do(self):
        """This method needs to be overridden by each stage that's derived from it.
           It should carry out all the processes necessary to complete that stage of
           the compile.
        """
        pass

    # Private Methods:
    def _genName(self, prefix):
        """Generate a name starting with prefix and a number from 0 to 1."""
        counter = 0
        while True:
            yield prefix + str(counter)
            counter += 1
