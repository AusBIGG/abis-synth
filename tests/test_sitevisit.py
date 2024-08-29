from rdflib import Literal, URIRef
from rdflib.namespace import OWL, PROV, RDF, SOSA, XSD

from client.model import Dataset, SiteVisit
from client.model._TERN import TERN
from client.model import (Site, Sample, Observation, Dataset, Value, FeatureOfInterest, Concept, Sampling)


def test_basic():
    sv1 = SiteVisit(Dataset(), Literal("2001-01-01T00:00:01", datatype=XSD.dateTime))
    rdf = sv1.to_graph()

    assert (None, RDF.type, OWL.Class) not in rdf
    assert (None, RDF.type, TERN.SiteVisit) in rdf


def test_simple_sitevisit_with_site():
    tern_dataset1 = Dataset()
    foi1 = FeatureOfInterest(
        Concept(),
        tern_dataset1,
    )
    sv = SiteVisit(tern_dataset1, Literal("2000-01-01+09:00", datatype=XSD.dateTime))
    s1 = Observation(
        tern_dataset1,
        Value(),
        foi1,
        URIRef("https://example.com/simpleresult/x"),
        URIRef("http://example.com/observedproperty/x"),
        URIRef("http://example.com/instant/x"),
        Literal("2001-01-01", datatype=XSD.date),
        URIRef("https://example.com/procedure/x/"),
        has_site_visit=sv
    )
    site1 = Site(s1, [foi1], tern_dataset1, Concept(), has_site_visit=sv)

    rdf = site1.to_graph()

    assert (None, RDF.type, TERN.SiteVisit) in rdf
    assert (site1.iri, TERN.hasSiteVisit, sv.iri) in rdf
    assert (s1.iri, TERN.hasSiteVisit, sv.iri) in rdf
    assert (sv.iri, PROV.startedAtTime, None) in rdf


def test_sitevisit_with_site_and_sampling():
    tern_dataset1 = Dataset()
    foi1 = FeatureOfInterest(
        Concept(),
        tern_dataset1,
    )
    sv = SiteVisit(tern_dataset1, Literal("2000-01-01+09:00", datatype=XSD.dateTime))
    obs = Observation(
        tern_dataset1,
        Value(),
        foi1,
        URIRef("https://example.com/simpleresult/x"),
        URIRef("http://example.com/observedproperty/x"),
        URIRef("http://example.com/instant/x"),
        Literal("2001-01-01", datatype=XSD.date),
        URIRef("https://example.com/procedure/x/"), has_site_visit=sv
    )
    site1 = Site(obs, [foi1], tern_dataset1, Concept(), has_site_visit=sv)

    sample1 = Sample([site1], Concept(), tern_dataset1, None)

    sampling1 = Sampling(foi1, Literal("2000-01-01+09:00", datatype=XSD.dateTime),
                         URIRef("https://example.org/procedure/x"), [sample1], has_site_visit=sv)
    sample1.is_result_of = sampling1
    foi1.has_sample = sample1

    rdf = sampling1.to_graph()

    assert (None, RDF.type, TERN.SiteVisit) in rdf
    assert (site1.iri, TERN.hasSiteVisit, sv.iri) in rdf
    assert (obs.iri, TERN.hasSiteVisit, sv.iri) in rdf
    assert (sampling1.iri, TERN.hasSiteVisit, sv.iri) in rdf
    assert (foi1.iri, SOSA.hasSample, sample1.iri) in rdf
