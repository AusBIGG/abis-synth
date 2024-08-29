from typing import Optional
from uuid import uuid4

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, OWL

from client.model._TERN import TERN


class Klass:
    iri: URIRef

    def __init__(self, iri: Optional[str] = None):
        """Receive and use or make an IRI"""
        if iri is None:
            self.uuid = self.make_uuid()
            iri = URIRef(f"http://example.com/{self.uuid}")

        self.iri = URIRef(iri)
        self.label = f"Class with ID {self.uuid if hasattr(self, 'uuid') else self.iri.split('/')[-1]}"

    def make_uuid(self):
        return uuid4()

    def to_graph(self) -> Graph:
        g = Graph()
        g.bind("tern", TERN)
        g.bind("geo", Namespace("http://www.opengis.net/ont/geosparql#"))

        g.add((self.iri, RDF.type, OWL.Class))
        g.add((self.iri, RDFS.label, Literal(self.label)))

        return g
