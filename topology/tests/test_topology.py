from topology.core.topology import Topology
from topology.core.site import Site
from topology.core.connection import Connection


def test_new_topology():
    top = Topology(name='mytop')
    assert top.name == 'mytop'

def test_add_site():
    top = Topology()
    site = Site(name='site')

    assert top.n_sites == 0
    top.add_site(site)
    assert top.n_sites == 1

def test_add_connection():
    top = Topology()
    site1 = Site(name='site1')
    site2 = Site(name='site2')
    connect = Connection(site1=site1, site2=site2)

    top.add_site(site1)
    top.add_site(site2)

    top.update_connection_list()

    assert len(top.connection_list) == 1
