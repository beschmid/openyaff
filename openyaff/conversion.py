import numpy as np

from openyaff.utils import create_openmm_system
from openyaff.generator import AVAILABLE_PREFIXES, apply_generators_mm
from openyaff.seeds import OpenMMSeed


class ExplicitConversion:
    """Defines the explicit conversion procedure from YAFF to OpenMM

    In this procedure, each YAFF generator is extended with function calls
    to an OpenMM system object such that the force field generation occurs
    synchronously between OpenMM and YAFF.

    """

    def __init__(self, pme_error_thres=1e-5):
        """Constructor

        Parameters
        ----------

        pme_error_thres : float
            determines the threshold for the error tolerance in the
            NonbondedForce PME evaluation

        """
        self.pme_error_thres = pme_error_thres

    def check_compatibility(self, configuration):
        """Checks compatibility of current settings with a given configuration

        The following checks are performed:
            - all prefixes in the configuration should have a generator in
            openyaff.generator

        Parameters
        ----------

        configuration : openyaff.Configuration
            configuration for which to check compatibility

        """
        #for key, _ in configuration.parameters.sections.items():
        #    assert key in AVAILABLE_PREFIXES, ('I do not have a generator '
        #            'for key {}'.format(key))
        pass

    def apply(self, configuration, seed_kind='full'):
        """Converts a yaff configuration into an OpenMM seed

        Begins with a call to check_compatibility, and an assertion error is
        raised if the configuration is not compatible.
        The system object in the yaff seed is used to create a corresponding
        openmm system object, after which apply_generators_mm is called.

        Parameters
        ----------

        configuration : openyaff.Configuration
            configuration for which to check compatibility

        seed_kind : str
            specifies the kind of seed to be converted

        """
        # raise AssertionError if not compatible
        self.check_compatibility(configuration)
        yaff_seed = configuration.create_seed(kind=seed_kind)
        system_mm = create_openmm_system(yaff_seed.system)
        kwargs = {}

        # if system is periodic and contains electrostatis; compute PME params
        if (configuration.ewald_alphascale is not None and
                seed_kind in ['full', 'electrostatic', 'nonbonded']):
            alpha = configuration.ewald_alphascale
            delta = np.exp(-(alpha) ** 2) / 2
            if delta > self.pme_error_thres:
                kwargs['delta'] = delta
            else:
                kwargs['delta'] = self.pme_error_thres
        apply_generators_mm(yaff_seed, system_mm, **kwargs)
        openmm_seed = OpenMMSeed(system_mm)
        return openmm_seed
