from __future__ import annotations

from dataclasses import dataclass
from typing import Type, Optional, Callable

from stable_baselines_integration.robot.specification import BrittleStarRobotSpecification
from erpy.framework.genome import Genome, GenomeConfig


@dataclass
class BrittleStarGenomeConfig(GenomeConfig):
    specification_generator: Callable[[], BrittleStarRobotSpecification]

    @property
    def genome(self) -> Type[Genome]:
        return BrittleStarGenome


class BrittleStarGenome(Genome):
    def __init__(self, specification: BrittleStarRobotSpecification,
                 config: BrittleStarGenomeConfig, genome_id: int, parent_genome_id: Optional[int] = None):
        super().__init__(config, genome_id, parent_genome_id)
        self._specification = specification

    @property
    def specification(self) -> BrittleStarRobotSpecification:
        return super().specification

    @property
    def config(self) -> BrittleStarGenomeConfig:
        return super().config

    @staticmethod
    def generate(config: BrittleStarGenomeConfig, genome_id: int, *args, **kwargs) -> BrittleStarGenome:
        specification = config.specification_generator()
        return BrittleStarGenome(specification=specification, config=config, genome_id=genome_id)

    def mutate(self, child_genome_id: int, *args, **kwargs) -> BrittleStarGenome:
        return self

    def cross_over(self, partner_genome: Genome, child_genome_id: int) -> BrittleStarGenome:
        pass
