from pathlib import Path

from erpy.framework.ea import EA
from erpy.interfaces.mujoco.viewer import evaluate_with_dm_control_viewer
from stable_baselines_integration.configs import create_ea_config
from stable_baselines_integration.robot.robot import BrittleStarRobot

if __name__ == '__main__':
    target_directory = "./output/summer-frost-409"

    target_directory = Path(target_directory)

    ea_config = create_ea_config()
    ea_config.logger_config.pre_initialise_wandb = False
    ea_config.saver_config.save_path = str(target_directory)

    ea = EA(ea_config)
    population = ea.saver.load()

    all_time_best = population.all_time_best_evaluation_result

    genome = all_time_best.genome
    specification = genome.specification
    robot = BrittleStarRobot(specification)
    evaluate_with_dm_control_viewer(env_config=ea_config.evaluator_config.environment_config,
                                    robot=robot)
