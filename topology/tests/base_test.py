import pytest
import numpy as np
import unyt as u

from topology.core.box import Box
from topology.core.topology import Topology
from topology.core.element import Element
from topology.core.site import Site
from topology.core.atom_type import AtomType


class BaseTest:
    @pytest.fixture(autouse=True)
    def initdir(self, tmpdir):
        tmpdir.chdir()

    @pytest.fixture
    def lengths(self):
        return u.nm * np.ones(3)

    @pytest.fixture
    def angles(self):
        return u.degree * [90, 90, 90]

    @pytest.fixture
    def charge(self):
        return u.elementary_charge * 1

    @pytest.fixture
    def mass(self):
        return 1 * u.gram/u.mol

    @pytest.fixture
    def box(self):
        return Box(lengths=u.nm*np.ones(3))

    @pytest.fixture
    def top(self):
        return Topology(name='mytop')

    @pytest.fixture
    def topology_site(self):
        def _topology(sites=1):
            top = Topology()
            top.box = Box(lengths=[1, 1, 1])
            H = Element(name='H', symbol='H', mass=1)
            for i in range(sites):
                site = Site(name='site{}'.format(int(i)),
                            element=H,
                            atom_type=AtomType(name="at1", mass=H.mass),
                            )
                top.add_site(site)

            return top

        return _topology
