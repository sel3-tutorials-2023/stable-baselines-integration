from erpy.framework.ea import EA
from stable_baselines_integration.configs import create_ea_config

if __name__ == '__main__':
    ea_config = create_ea_config()
    ea = EA(config=ea_config)
    ea.run()
