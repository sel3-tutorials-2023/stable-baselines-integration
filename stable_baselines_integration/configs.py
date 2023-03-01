import numpy as np
from stable_baselines3 import PPO
from torch import nn
from wandb.integration.sb3 import WandbCallback

from stable_baselines_integration.robot.genome import BrittleStarGenomeConfig
from stable_baselines_integration.robot.robot import BrittleStarRobot
from stable_baselines_integration.robot.specification import BrittleStarRobotSpecification
from erpy import set_random_state
from erpy.framework.ea import EAConfig
from erpy.framework.evaluator import EvaluationCallback
from erpy.instances.evaluators.evaluation_callbacks.controller_saver import SaveControllerEvaluationCallback
from erpy.instances.evaluators.evaluation_callbacks.distributed_wandb_initialiser import \
    DistributedWandbInitialisationEvaluationCallback
from erpy.instances.evaluators.evaluation_callbacks.list import EvaluationCallbackList
from erpy.instances.evaluators.evaluation_callbacks.wrapper import EvaluationCallbackWrapper
from erpy.instances.evaluators.ray.evaluation_actors.controller_learning import RayControllerLearningEvaluatorConfig
from erpy.instances.loggers.wandb_logger import WandBLoggerConfig
from erpy.instances.phenomes.controllers.stable_baselines import SBControllerSpecification
from erpy.instances.populations.default import DefaultPopulationConfig
from erpy.instances.reproducers.default import DefaultReproducerConfig
from erpy.instances.savers.default import DefaultSaverConfig
from erpy.instances.selectors.default import DefaultSelectorConfig
from simulation_environment.brittle_star.specification.default import default_brittle_star_morphology_specification
from simulation_environment.environment.locomotion.task import LocomotionEnvironmentConfig


def specification_generator() -> BrittleStarRobotSpecification:
    morphology_specification = default_brittle_star_morphology_specification(num_arms=2, num_segments_per_arm=5,
                                                                             use_cartesian_actuation=True)

    # Hyperparameters are taken from https://github.com/DLR-RM/rl-baselines3-zoo/blob/master/hyperparams/ppo.yml#L386
    controller_specification = SBControllerSpecification(
        algorithm=PPO,
        stable_baseline_model_arguments=dict(
            policy="MultiInputPolicy",
            ent_coef=0.000401762,
            policy_kwargs=dict(
                log_std_init=-2,
                ortho_init=False,
                activation_fn=nn.ReLU,
                net_arch=dict(pi=[256, 256],
                              vf=[256, 256])
            ),
            batch_size=64,
            n_steps=512,
            gamma=0.98,
            learning_rate=2.0633e-05,
            clip_range=0.1,
            n_epochs=20,
            gae_lambda=0.92,
            max_grad_norm=0.8,
            vf_coef=0.58096,
        )
    )
    robot_specification = BrittleStarRobotSpecification(morphology_specification=morphology_specification,
                                                        controller_specification=controller_specification)
    return robot_specification


def create_evaluation_callback() -> EvaluationCallback:
    # Transform a stable baseline callback type to an erpy one
    #   WandbCallback is the stable baseline callback to allow logging to wandb
    wandb_sb_callback = EvaluationCallbackWrapper(WandbCallback, verbose=1)

    # We're training on a separate process -> need to initiate wandb on every such process with this callback
    wandb_initialiser = DistributedWandbInitialisationEvaluationCallback()

    # Necessary to continue learning in between generations
    controller_saver = SaveControllerEvaluationCallback()

    callback = EvaluationCallbackList(evaluation_callbacks=[wandb_initialiser, wandb_sb_callback, controller_saver])
    return callback


def create_ea_config() -> EAConfig:
    seed = 42
    set_random_state(seed_value=seed)

    environment_config = LocomotionEnvironmentConfig(with_target=False)

    callback = create_evaluation_callback()
    evaluator_config = RayControllerLearningEvaluatorConfig(environment_config=environment_config,
                                                            robot=BrittleStarRobot,
                                                            reward_aggregator=np.sum,
                                                            episode_aggregator=np.mean,
                                                            callback=callback,
                                                            num_eval_episodes=10,
                                                            num_workers=1,
                                                            num_cores_per_worker=1,  # psutil.cpu_count(),
                                                            hard_episode_reset=False,
                                                            debug=False,
                                                            log_to_driver=True,
                                                            logging_level="info",
                                                            total_timesteps=50000)

    population_config = DefaultPopulationConfig(population_size=1)
    selector_config = DefaultSelectorConfig(amount_to_select=1)

    genome_config = BrittleStarGenomeConfig(specification_generator=specification_generator)
    reproducer_config = DefaultReproducerConfig(genome_config=genome_config)
    logger_config = WandBLoggerConfig(project_name="sel3-controller-optimisation",
                                      group="test",
                                      tags=None,
                                      update_saver_path=True,
                                      enable_tensorboard_backend=True)
    saver_config = DefaultSaverConfig(save_freq=1,
                                      save_path="output")

    ea_config = EAConfig(population_config=population_config,
                         evaluator_config=evaluator_config,
                         selector_config=selector_config,
                         reproducer_config=reproducer_config,
                         logger_config=logger_config,
                         saver_config=saver_config,
                         num_generations=5)

    return ea_config
#
