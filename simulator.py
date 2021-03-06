#!/usr/bin/env python3

"""
Simulates Internet routing
"""

from argparse import ArgumentParser
import json

class AutonomousSystem:
    def __init__(self, number, prefix):
        self._number = number
        self._prefix = prefix
        self._customers = []
        self._providers = []
        self._peers = []
        self._paths = {self._prefix : Advertisement(self._prefix)}

    @property
    def number(self):
        """Get AS's number"""
        return self._number

    @property
    def prefix(self):
        """Get AS's own prefix"""
        return self._prefix

    def add_customer(self, customer):
        """Add a customer AS"""
        self._customers.append(customer)

    def add_provider(self, provider):
        """Add a provider AS"""
        self._providers.append(provider)

    def add_peer(self, peer):
        """Add a peer AS"""
        self._peers.append(peer)

    def send_advertisement(self, path):
        """Send an advertisement to all relevant neighbors"""
        # TODO

    def recv_advertisement(self, path):
        """Receive an advertisement from a neighbor"""
        # TODO

    def __str__(self):
        return ("AS %d (%s): cust=[%s]; prov=[%s]; peer=[%s]" % 
                (self._number, self._prefix, 
                ','.join([str(AS.number) for AS in self._customers]),
                ','.join([str(AS.number) for AS in self._providers]),
                ','.join([str(AS.number) for AS in self._peers])))

class Advertisement:
    def __init__(self, prefix, path=[]):
        self._prefix = prefix
        self._path = path

    @property
    def prefix(self):
        return self._prefix

    def prepend(self, AS):
        """Add an AS to the path"""
        self._path.insert(0, AS)

    def length(self):
        """Get the length of the path"""
        return len(self._path)

    def contains(self, AS):
        """Checks if AS already exists in the path"""
        return AS in self._path

    def head(self):
        """Gets the nexthop AS"""
        if len(self._path) > 0:
            return self._path[0]
        else:
            return None

    def copy(self):
        """Creates a copy of this path"""
        return Advertisement(self._prefix, self._path.copy())

    def __str__(self):
        return ("%s: %s" % (self._prefix, 
                " -> ".join([str(AS.number) for AS in self._path])))

def load_topology(filepath):
    """Load a network topology and return a dictionary of AS objects"""
    # Load JSON
    with open(filepath) as topo_file:
        topo = json.load(topo_file)
  
    # Create ASes 
    ASes = {}
    for AS in topo["ases"]:
        AS = AutonomousSystem(AS["number"], AS["prefix"])
        ASes[AS.number] = AS

    # Create relationships
    for relationship in topo["relationships"]:
        if "customer" in relationship:
            customer = ASes[relationship["customer"]]
            provider = ASes[relationship["provider"]]
            customer.add_provider(provider)
            provider.add_customer(customer)
        else:
            peerA = ASes[relationship["peerA"]]
            peerB = ASes[relationship["peerB"]]
            peerA.add_peer(peerB)
            peerB.add_peer(peerA)

    return ASes 

def compute_paths(ASes):
    """Send/receive advertisements between ASes and compute the paths used by 
    each AS to reach various prefixes
    """
    # TODO

    # Dump paths
    print("***** Paths *****")
    for AS in ASes.values():
        print("AS %d" % AS.number)
        # TODO

def main():
    # Parse arguments
    arg_parser = ArgumentParser(description='Internet routing simulator')
    arg_parser.add_argument('-t', '--topology', action='store',
            required=True, help='JSON file containing topology')
    settings = arg_parser.parse_args()

    # Load topology
    ASes = load_topology(settings.topology)
    print("***** Topology *****")
    for AS in ASes.values():
        print(AS)

    # Compute paths
    ASes = compute_paths(ASes)

if __name__ == '__main__':
    main()
