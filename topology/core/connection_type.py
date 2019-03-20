import logging
import numpy as np
import sympy
import unyt as u

logger = logging.getLogger("TopLog")

class ConnectionType(object):
    """A connection type."""

    def __init__(self,
                 potential_function='0.5 * k * (r-r_eq)**2',
                 parameters={
                     'k': 1000 * u.joule / (u.mol * u.nm**2),
                     'r_eq': 1 * u.nm
                 }):

        if isinstance(parameters, dict):
            self._parameters = parameters
        else:
            raise ValueError("Please enter dictionary for parameters")

        if potential_function is None:
            self._potential_function = None
        elif isinstance(potential_function, str):
            self._potential_function = sympy.sympify(potential_function)
        elif isinstance(potential_function, sympy.Expr):
            self._potential_function = potential_function
        else:
            raise ValueError("Please enter a string, sympy expression, "
                             "or None for potential_function")

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, newparams):
        if not isinstance(newparams, dict):
            raise ValueError("Provided parameters "
                             "{} is not a valid dictionary".format(newparams))

        self._parameters.update(newparams)
        self._validate_function_parameters()

    @property
    def potential_function(self):
        return self._potential_function

    @potential_function.setter
    def potential_function(self, function):
        # Check valid function type (string or sympy expression)
        # If func is undefined, just keep the old one
        if isinstance(function, str):
            self._potential_function = sympy.sympify(function)
        elif isinstance(function, sympy.Expr):
            self._potential_function = function
        else:
            raise ValueError("Please enter a string or sympy expression")

        self._validate_function_parameters()

    def set_potential_function(self, function=None, parameters=None):
        """ Set the potential function and paramters for this connection type

        Parameters
        ----------
        function: sympy.Expression or string
            The mathematical expression corresponding to the bond potential
            If None, the function remains unchanged
        parameters: dict
            {parameter: value} in the function
            If None, the parameters remain unchanged

        Notes
        -----
        Be aware of the symbols used in the `function` and `parameters`.
        If unnecessary parameters are supplied, an error is thrown.
        If only a subset of the parameters are supplied, they are updated
            while the non-passed parameters default to the existing values
       """
        if function is not None:
            if isinstance(function, str):
                self._potential_function = sympy.sympify(function)
            elif isinstance(function, sympy.Expr):
                self._potential_function = function
            else:
                raise ValueError("Please enter a string or sympy expression")
                self.potential_function = function

        if parameters is not None:
            if not isinstance(parameters, dict):
                raise ValueError(
                    "Provided parameters "
                    "{} is not a valid dictionary".format(parameters))

            self._parameters.update(parameters)

        self._validate_function_parameters()

    def _validate_function_parameters(self):
        # Check for unused symbols
        symbols = sympy.symbols(set(self.parameters.keys()))
        unused_symbols = symbols - self.potential_function.free_symbols
        if len(unused_symbols) > 0:
            warnings.warn('You supplied parameters with '
                          'unused symbols {}'.format(unused_symbols))

        # Rebuild the parameters
        self._parameters = {
            key: val
            for key, val in self._parameters.items() if key in set(
                str(sym) for sym in self.potential_function.free_symbols)
        }
        symbols = sympy.symbols(set(self.parameters.keys()))
        if symbols != self.potential_function.free_symbols:
            extra_syms = symbols ^ self.potential_function.free_symbols
            raise ValueError("Potential function and parameter"
                             " symbols do not agree,"
                             " extraneous symbols:"
                             " {}".format(extra_syms))

    def __eq__(self, other):
        return ((self.parameters == other.parameters) &
                (self.potential_function == other.potential_function))
