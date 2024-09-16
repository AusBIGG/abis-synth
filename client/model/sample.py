from typing import Optional, List, Union

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS, SOSA, VOID

from client.model._TERN import TERN
import client.model as model
from .concept import Concept
from .klass import Klass
from .tern_dataset import Dataset
from .site import Site



class Sample(Klass):
    def __init__(
        self,
        is_sample_of: List[Union["model.FeatureOfInterest", Site]],
        feature_type: Concept,
        in_dataset: Dataset,
        is_result_of: Union["model.Sampling", None],
        iri: Optional[str] = None,
    ):
        assert (
            len(is_sample_of) >= 1
        ), "You must supply a minimum of 1 FeatureOfInterest objects for the property is_sample_of"

        assert all(
            isinstance(el.__class__, model.FeatureOfInterest.__class__) for el in is_sample_of
        ), "Every object supplied in the property is_sample_of must be of type FeatureOfInterest"

        assert isinstance(is_result_of.__class__, model.Sampling.__class__), \
            "The object supplied for the property is_result_of must be of type Sampling"

        assert isinstance(
            feature_type.__class__, Concept.__class__
        ), "The object supplied for the property feature_type must be of type Concept"

        assert isinstance(
            in_dataset.__class__, Dataset.__class__
        ), "The object supplied for the property in_dataset must be of type Dataset"

        """Receive and use or make an IRI"""
        if iri is None:
            self.id = self.make_uuid()
            iri = URIRef(f"http://example.com/sample/{self.id}")

        self.iri = URIRef(iri)

        super().__init__(iri)

        self.label = f"Sample with ID {self.id if hasattr(self, 'id') else self.iri.split('/')[-1]}"

        self.is_sample_of = is_sample_of
        self.is_result_of = is_result_of
        self.feature_type = feature_type
        self.in_dataset = in_dataset

    def to_graph(self) -> Graph:
        g = super().to_graph()
        g.remove((self.iri, RDF.type, OWL.Class))
        g.add((self.iri, RDF.type, TERN.Sample))
        g.remove((self.iri, RDFS.label, None))
        g.add((self.iri, RDFS.label, Literal(self.label)))
        for iso in self.is_sample_of:
            g.add((self.iri, SOSA.isSampleOf, iso.iri))
            if (iso.iri, RDF.type, None) not in g:
                g += iso.to_graph()
        g.add((self.iri, TERN.featureType, self.feature_type.iri))
        g.add((self.iri, VOID.inDataset, self.in_dataset.iri))
        if (self.in_dataset.iri, RDF.type, None) not in g:
            g += self.in_dataset.to_graph()
        if self.is_result_of is not None:
            g.add((self.iri, SOSA.isResultOf, self.is_result_of.iri))
            # if (self.is_result_of.iri, RDF.type, None) not in g:
            #     g += self.is_result_of.to_graph()

        return g
