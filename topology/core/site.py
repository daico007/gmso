import warnings

import numpy as np
import unyt as u

from topology.core.atom_type import AtomType


class Site(object):
    """A general site."""

    def __init__(self,
                 name,
                 position=None,
                 charge=None,
                 element=None,
                 atom_type=None):
        self.name = str(name)
        if position is None:
            self.position = u.nm * np.zeros(3)
        else:
            self.position = _validate_position(position)

        self._element = element
        self._atom_type = _validate_atom_type(atom_type)
        self._charge = _validate_charge(charge)
        self._connections = list()

    def add_connection(self, other_site):
        self._connections.append(other_site)

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, element):
        self._element = element

    @property
    def connections(self):
        return self._connections

    @property
    def n_connections(self):
        return len(self._connections)

    @property
    def charge(self):
        if self._charge is not None:
            return self._charge
        elif self.atom_type is not None:
            return self.atom_type.charge
        else:
            return None

    @charge.setter
    def charge(self, charge):
        self._charge = _validate_charge(charge)

    @property
    def atom_type(self):
        return self._atom_type

    @atom_type.setter
    def atom_type(self, val):
        val = _validate_atom_type(val)
        self._atom_type = val

def _validate_position(position):
    if not isinstance(position, u.unyt_array):
        warnings.warn('Positions are assumed to be in nm')
        position *= u.nm

    input_unit = position.units

    position = np.asarray(position, dtype=float, order='C')
    np.reshape(position, newshape=(3, ), order='C')

    position *= input_unit
    position.convert_to_units(u.nm)

    return position

def _validate_charge(charge):
    if charge is None:
        return None
    elif not isinstance(charge, u.unyt_array):
        warnings.warn("Charges are assumed to be elementary charge")
        charge *= u.elementary_charge
    elif charge.units.dimensions != u.elementary_charge.units.dimensions:
        warnings.warn("Charges are assumed to be elementary charge")
        charge = charge.value * u.elementary_charge
    else:
        pass

    return charge

def _validate_atom_type(val):
    if val is None:
        return None
    elif not isinstance(val, AtomType):
        raise ValueError("Passed value {} is not an AtomType".format(val))
    else:
        return val
