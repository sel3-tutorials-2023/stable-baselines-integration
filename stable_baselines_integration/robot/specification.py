from erpy.framework.specification import RobotSpecification
from erpy.instances.phenomes.controllers.stable_baselines import SBControllerSpecification
from simulation_environment.brittle_star.specification.specification import BrittleStarMorphologySpecification


class BrittleStarRobotSpecification(RobotSpecification):
    def __init__(self, morphology_specification: BrittleStarMorphologySpecification,
                 controller_specification: SBControllerSpecification) -> None:
        super().__init__(morphology_specification, controller_specification)

    @property
    def morphology_specification(self) -> BrittleStarMorphologySpecification:
        return super().morphology_specification

    @property
    def controller_specification(self) -> SBControllerSpecification:
        return super().controller_specification
