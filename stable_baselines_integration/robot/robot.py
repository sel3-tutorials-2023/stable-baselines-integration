from stable_baselines_integration.robot.specification import BrittleStarRobotSpecification
from erpy.instances.phenomes.controllers.stable_baselines import SBController
from erpy.interfaces.mujoco.phenome import MJCRobot
from simulation_environment.brittle_star.morphology.morphology import MJCBrittleStarMorphology


class BrittleStarRobot(MJCRobot):
    def __init__(self, specification: BrittleStarRobotSpecification) -> None:
        super().__init__(specification)

    @property
    def morphology(self) -> MJCBrittleStarMorphology:
        return super().morphology

    @property
    def controller(self) -> SBController:
        return super().controller

    def _build_morphology(self) -> MJCBrittleStarMorphology:
        morphology = MJCBrittleStarMorphology(specification=self.specification)
        return morphology

    def _build_controller(self) -> SBController:
        controller = SBController(specification=self.specification)
        return controller
