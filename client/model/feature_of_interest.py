from typing import Optional

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SOSA, OWL, VOID

from client.model._TERN import TERN
import client.model as model
from .concept import Concept
from .klass import Klass
from .tern_dataset import Dataset


class FeatureOfInterest(Klass):
    def __init__(
            self,
            feature_type: Concept,
            in_dataset: Dataset,
            iri: Optional[str] = None,
            has_sample: Optional["model.Sample"] = None,
    ):
        assert isinstance(
            feature_type.__class__, Concept.__class__
        ), f"The object supplied for the property feature_type must be of type Concept. You gave a {type(feature_type)}"

        assert isinstance(
            in_dataset.__class__, Dataset.__class__
        ), "The object supplied for the property in_dataset must be of type Dataset"

        # Unsure why Sample goes red TODO: Figure out why Sample is going red without importing
        # importing seems to trigger a circular ImportError

        if has_sample is not None:
            assert isinstance(model.Sample.__class__, has_sample.__class__), \
                f"The object supplied for the property has_sample must be of type Sample "

        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/featureofinterest/{self.id}")

        self.iri = URIRef(iri)

        super().__init__(iri)

        self.label = f"Feature of Interest with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"

        self.feature_type = feature_type
        self.in_dataset = in_dataset
        self.has_sample = has_sample

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        g.add((self.iri, RDF.type, TERN.FeatureOfInterest))
        g.remove((self.iri, RDFS.label, None))
        g.add((self.iri, RDFS.label, Literal(self.label)))
        g.add((self.iri, TERN.featureType, self.feature_type.iri))
        g.add((self.iri, VOID.inDataset, self.in_dataset.iri))
        if (self.in_dataset.iri, RDF.type, None) not in g:
            g += self.in_dataset.to_graph()
        if self.has_sample:
            g.add((self.iri, SOSA.hasSample, self.has_sample.iri))

        return g
