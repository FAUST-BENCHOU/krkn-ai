from krkn_ai.models.custom_errors import ScenarioParameterInitError
from krkn_ai.utils.rng import rng
from krkn_ai.models.scenario.base import Scenario
from krkn_ai.models.scenario.parameters import *


class KubeVirtOutageScenario(Scenario):
    name: str = "kubevirt-outage"
    krknctl_name: str = "kubevirt-outage"
    krknhub_image: str = "quay.io/krkn-chaos/krkn-hub:kubevirt-outage"

    namespace: NamespaceParameter = NamespaceParameter()
    vm_name: VMNameParameter = VMNameParameter()
    timeout: KubeVirtTimeoutParameter = KubeVirtTimeoutParameter()
    kill_count: KillCountParameter = KillCountParameter()

    def __init__(self, **data):
        super().__init__(**data)
        self.mutate()

    @property
    def parameters(self):
        return [
            self.namespace,
            self.vm_name,
            self.timeout,
            self.kill_count,
        ]

    def mutate(self):
        if len(self._cluster_components.namespaces) == 0:
            raise ScenarioParameterInitError("No namespaces found in cluster components for kubevirt outage scenario")
        
        # Pre-filter: only consider namespaces with VMs
        namespaces_with_vms = [
            ns for ns in self._cluster_components.namespaces 
            if len(ns.vms) > 0
        ]
        
        if len(namespaces_with_vms) == 0:
            raise ScenarioParameterInitError("No VMs found in cluster components for kubevirt outage scenario")
        
        # Select a random namespace with VMs
        namespace = rng.choice(namespaces_with_vms)
        self.namespace.value = namespace.name
        
        num_vms = len(namespace.vms)
        self.kill_count.value = rng.randint(1, num_vms)
        self.vm_name.value = ".*"

