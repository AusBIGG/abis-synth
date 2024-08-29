from rdflib.namespace import OWL, RDF

from client.model import (
    Concept,
    Dataset,
    FeatureOfInterest,
    Sample,
)
from client.model._TERN import TERN


def test_basic_rdf():
    tern_dataset1 = Dataset()
    foi1 = FeatureOfInterest(
        Concept(),
        tern_dataset1,
    )
    s1 = Sample([foi1], Concept(), tern_dataset1, None)
    rdf = s1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Sample) in rdf
