from rdflib import Literal
from rdflib import URIRef
from rdflib.namespace import OWL, RDF, XSD

from client.model import (
    Concept,
    Dataset,
    FeatureOfInterest,
    Observation,
    Site,
    Value,
)
from client.model._TERN import TERN


def test_basic_rdf():
    tern_dataset1 = Dataset()
    foi1 = FeatureOfInterest(Concept(), tern_dataset1)
    obs1 = Observation(
        tern_dataset1,
        Value(),
        foi1,
        Literal("timple result"),
        URIRef("http://example.com/observedproperty/n"),
        URIRef("http://example.com/instant/z"),
        Literal("2000-01-01", datatype=XSD.date),
        URIRef("http://example.com/procedure/a"),
    )
    s1 = Site(obs1, [foi1], tern_dataset1, Concept())
    rdf = s1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Site) in rdf
