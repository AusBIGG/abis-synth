from rdflib.namespace import OWL, RDF

from client.model import Dataset
from client.model._TERN import TERN


def test_basic_rdf():
    d1 = Dataset()
    rdf = d1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Dataset) in rdf
