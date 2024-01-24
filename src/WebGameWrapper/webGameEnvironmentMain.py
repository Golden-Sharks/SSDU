import matplotlib.pyplot as plt
import pyautogui
import time

from WebGameTrainer import WebGameTrainer
import numpy as np
from LogginCallback import LogginCallback
from stable_baselines3 import DQN
from stable_baselines3.common import env_checker


def main():
    params_dino = {
        'capture': {'mon': 1, 'top': 130, 'left': 0, 'width': 1600, 'height': 700},
        'gameOver': [{'mon': 1, 'top': 400, 'left': 600, 'width': 700, 'height': 150}, "GAME OVER", (800, 490)],
        'Inputs': {0: 'space', 1: 'down'},
        'model': {'model': 'DQN', 'hyper_param': None},
        'preprocessing': {'preprocessing': True, 'grayscale': True, 'resize': (200, 100), 'compression': 0}
    }

    params_dino_2 = {
        'capture': {'mon': 2, 'top': 130, 'left': 50, 'width': 1800, 'height': 800},
        'gameOver': [{'mon': 2, 'top': 400, 'left': 600, 'width': 700, 'height': 150}, "GAME OVER", (-960, 250)],
        'Inputs': {0: 'space', 1: 'down'},
        'model': {'model': 'DQN', 'hyper_param': None},
        'preprocessing': {'preprocessing': True, 'grayscale': True, 'resize': (200, 100), 'compression': 0}
    }

    params_snake = {
        'capture': {'mon': 2, 'top': 300, 'left': 675, 'width': 575, 'height': 600},
        'gameOver': [{'mon': 2, 'top': 760, 'left': 900, 'width': 75, 'height': 75}, "JOUER", (-980, 440)],
        'input': {0: 'up', 1: 'down', 2: 'left', 3: 'right'},
        'model': {'model': 'PPO', 'hyper_param': None},
        'preprocessing': {'preprocessing': True, 'grayscale': True, 'resize': (100, 200), 'compression': 0}
    }

    dico = {
        'capture': {'top': 0, 'left': 0, 'width': 1600, 'height': 900, 'mon': 1},
        'gameOver': [{'top': 0, 'left': 0, 'width': 1920, 'height': 1080, 'mon': 1}, 'Game Over', (800.0, 450.0)],
        'Inputs': {},
        'model': {
            'model': 'DQN',
            'buffer_size': 1000,
            'tensorboard_name': 'requin',
            'total_timesteps': 1000,
            'policy': 'MlpPolicy',
            'tau': 1.00,
            'gamma': 0.99,
            'trainingStart': 100
        },
        'preprocessing': {'preprocessing': False, 'resize': (800, 450), 'grayscale': False}}

    env = WebGameTrainer(dico)
    #env.construct(params_dino_2)

    # print("capture")
    # time.sleep(2)
    # plt.figure()
    # plt.imshow(env.getEnvironment().get_observation())
    # plt.show()

    # Useful function to check environment completion
    # env_checker.check_env(env.getEnvironment())

    # while 1:
    #     print(pyautogui.position())
    #     time.sleep(5)
    #oint_dir = '../../dat/train'
    # log_dir = '../../dat/logs/'
    #
    # callback = LogginCallback(check_freq=200, save_path=checkpoint_dir)
    # model = DQN('CnnPolicy', env.getEnvironment(), tensorboard_log=log_dir, verbose=1, buffer_size=100,
    #             learning_starts=1000, tau=1.0, gamma=0.99, train_freq=4)
    # print("groink")
    # checkp
    # start = time.time()
    # model.learn(total_timesteps=10000, callback=callback, tb_log_name="S10kT1G99B100")
    # end = time.time()
    # print("duration : ", (end - start) // 60, "min ", int((end - start) % 60), "s")

    #  R    0-1
    # tau  gamma

    # 1    0.99   => Default    11 min
    # 0.1  0.99                 13 min
    # 10   0.99                 11 min
    # 100  0.99                 12 min
    # 1    0.001                11 min
    # 1    0.01                 13 min
    # 1    0.1                  12 min
    # 1    0.5                  12 min


if __name__ == '__main__':
    main()
