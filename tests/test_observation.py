from rdflib import Literal, URIRef
from rdflib.namespace import OWL, RDF, XSD

from client.model import (
    Concept,
    Dataset,
    FeatureOfInterest,
    Value,
    Observation,
)
from client.model._TERN import TERN


# TODO: Confirm this testing is sufficient
def test_basic_rdf():
    tern_dataset1 = Dataset()
    foi1 = FeatureOfInterest(
        Concept(),
        tern_dataset1,
    )

    s1 = Observation(
        tern_dataset1,
        Value(),
        foi1,
        URIRef("https://example.com/simpleresult/x"),
        URIRef("http://example.com/observedproperty/x"),
        URIRef("http://example.com/instant/x"),
        Literal("2001-01-01", datatype=XSD.date),
        URIRef("https://example.com/procedure/x/"),
    )
    rdf = s1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Observation)
