from rdflib.namespace import OWL, RDF

from client.model import Concept, Dataset, FeatureOfInterest
from client.model._TERN import TERN


def test_basic_rdf():
    dataset1 = Dataset()
    foi1 = FeatureOfInterest(
        Concept(),
        dataset1,
    )
    rdf = foi1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.FeatureOfInterest) in rdf
