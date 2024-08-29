from rdflib import Literal, URIRef, Namespace
from rdflib.namespace import OWL, RDF, XSD

from client.model import Concept, FeatureOfInterest, Dataset, Sample, Sampling
from client.model._TERN import TERN
GEO = Namespace("http://www.opengis.net/ont/geosparql#")
from shapely.geometry import Point


def test_basic_rdf():
    tern_dataset1 = Dataset()
    foi1 = FeatureOfInterest(
        Concept(),
        tern_dataset1,
    )
    sample1 = Sample([foi1], Concept(), tern_dataset1, None)
    s1 = Sampling(
        foi1,
        Literal("2001-01-01", datatype=XSD.date),
        URIRef("http://example.com/procedure/x"),
        [sample1],
    )
    sample1.is_result_of = (
        s1  # link the Sample to the Sampling, now that both are declared
    )
    rdf = s1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.Sampling) in rdf


def test_coordinates_point():
    ds = Dataset()
    foi1 = FeatureOfInterest(
        Concept(),
        ds,
    )
    s1 = Sampling(
        foi1,
        Literal("2001-01-01", datatype=XSD.date),
        URIRef("http://example.com/procedure/x"),
        [Sample([foi1], Concept(), ds, None)],
        geometry=Point(118.4435416, -29.9785035)
    )

    g = s1.to_graph()

    for s in g.subjects(RDF.type, TERN.Sampling):
        for o in g.objects(s, GEO.hasGeometry):
            assert (o, GEO.asWKT, Literal("POINT (118.4435416 -29.9785035)", datatype=GEO.wktLiteral)) in g