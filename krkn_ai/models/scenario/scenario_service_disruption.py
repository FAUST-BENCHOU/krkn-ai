from krkn_ai.models.custom_errors import ScenarioParameterInitError
from krkn_ai.utils.rng import rng
from krkn_ai.models.scenario.base import Scenario
from krkn_ai.models.scenario.parameters import *


class ServiceDisruptionScenario(Scenario):
    name: str = "service-disruption"
    krknctl_name: str = "service-disruption-scenarios"
    krknhub_image: str = "quay.io/krkn-chaos/krkn-hub:service-disruption-scenarios"

    namespace: NamespaceParameter = NamespaceParameter(value="openshift-etcd")
    delete_count: DeleteCountParameter = DeleteCountParameter()
    runs: RunsParameter = RunsParameter()

    def __init__(self, **data):
        super().__init__(**data)
        self.mutate()

    @property
    def parameters(self):
        return [
            self.namespace,
            self.delete_count,
            self.runs,
        ]

    def mutate(self):
        if len(self._cluster_components.namespaces) == 0:
            raise ScenarioParameterInitError("No namespaces found in cluster components")
        
        # Select a random namespace from cluster
        namespace = rng.choice(self._cluster_components.namespaces)
        self.namespace.value = namespace.name

