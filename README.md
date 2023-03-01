# stable-baselines-integration

This repository contains a code example ony how to
integrate  [Stable-Baselines3 (SB3)](https://stable-baselines3.readthedocs.io/en/master/) into ERPY.

Some notes:

* The main trick to incorporate SB3, is to use the
  pre-made [SBController](https://github.com/Co-Evolve/erpy/blob/main/erpy/instances/phenomes/controllers/stable_baselines.py)
  instance.
* Go through the `configs.py` file and see how you can use the SBController.
* You will also need to update the `BrittleStarRobotSpecification` and `BrittleStarRobot` classes, such that they return
  correct types and instances.
* The current code supports continual learning, i.e. continuing the training of a controller over multiple generations.
  WandB logs from subsequent training iterations will be appended to the original genome's log.
* A decent set of basic hyperparameters for SB3 algorithms can be
  found [here](https://github.com/DLR-RM/rl-baselines3-zoo/tree/master/hyperparams).
* Disclaimer: this code trains a controller for the same (targetless) locomotion environment as in the tutorial. The
  actions here directly control the four actuators (2 per arm), and thus not the amplitude of a lower-level oscillator.
  You will need to implement this controller hierarchy yourself (by overwriting the SBController and
  SBControllerSpecification). Do not expect this code (in this current state) to optimize good controllers. It is merely
  provided as an example on how to integrate stable baselines into the ERPY framework.

Questions or issues? -> dries.marzougui@ugent.be


