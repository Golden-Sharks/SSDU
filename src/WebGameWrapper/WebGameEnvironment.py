import time

import numpy as np
import pyautogui
import pydirectinput
from gym import Env
from gym.spaces import Box, Discrete
from mss import mss
import pytesseract
import cv2

# tesseract path setup
with open('../../tesseract_path.txt') as f:
    pytesseract.pytesseract.tesseract_cmd = f.readline()


class WebGame(Env):
    def __init__(self, params):
        super().__init__()
        # screen capture object
        self.cap = mss()
        # game location
        self.game_location = self.__setup_observation_space(params.get('capture'))
        # game done information
        self.done_location = self.__setup_done_space(params.get('gameOver')[0])
        self.done_text = params.get('gameOver')[1].upper()
        self.restart_button = params.get('gameOver')[2]
        # action map
        self.action_map = params.get('Inputs')
        print(self.action_map)
        self.action_map.update({len(self.action_map): 'no_op'})
        # model and params
        self.model = params.get('model')
        # preprocessing options
        self.preprocessing = params.get('preprocessing')
        self.do_preprocessing = self.preprocessing.get('preprocessing')
        # environment observation space
        self.observation_space = Box(low=0, high=255, shape=self.get_observation().shape, dtype=np.uint8)
        # environment action space
        self.action_space = Discrete(len(self.action_map))

        # print(self.observation_space.shape)
        # print(self.get_observation().shape)

    def __setup_observation_space(self, capture):
        # get monitor number
        monitor_number = capture.get('mon')
        mon = self.cap.monitors[monitor_number]

        # Create dictionary with monitor
        capture_dic = {'top': mon['top'] + capture.get('top'),
                       'left': mon['left'] + capture.get('left'),
                       'width': capture.get('width'),
                       'height': capture.get('height'),
                       'mon': monitor_number}

        return capture_dic

    def __setup_done_space(self, done_zone):
        monitor_number = done_zone.get('mon')
        mon = self.cap.monitors[monitor_number]

        done_dic = {'top': mon['top'] + done_zone.get('top'),
                    'left': mon['left'] + done_zone.get('left'),
                    'width': done_zone.get('width'),
                    'height': done_zone.get('height'),
                    'mon': monitor_number}

        return done_dic

    def step(self, action):
        if action != len(self.action_map) - 1:
            pydirectinput.press(self.action_map[action])

        done, done_cap, res = self.get_done()
        new_observation = self.get_observation()

        reward = 1

        return new_observation, reward, done, {}

    # visualise the game
    def render(self):
        cv2.imshow('Game', self.get_observation())
        if cv2.waitKey(1) and 0xFF == ord('q'):
            self.close()

    # restart game
    def reset(self):
        time.sleep(1)
        pyautogui.click(self.restart_button[0], self.restart_button[1])

        return self.get_observation()

    # close game observation
    def close(self):
        cv2.destroyAllWindows()

    # get the observation of the game
    def get_observation(self):
        image = np.array(self.cap.grab(self.game_location))[:, :, :3].astype(np.uint8)
        if self.do_preprocessing:
            return self.preprocess(image)
        return image

    def preprocess(self, image):
        third_dim = image.shape[2]

        if self.preprocessing.get('grayscale') and self.do_preprocessing:
            image = image[:, :, 0]
            third_dim = 1

        # print('image   : ', image.shape)
        resize = cv2.resize(image, (self.preprocessing.get('resize')[0],
                                    self.preprocessing.get('resize')[1]))

        reshape = np.reshape(resize, (resize.shape[0], resize.shape[1], third_dim))

        return reshape

    # get done text in the game
    def get_done(self):
        done_cap = np.array(self.cap.grab(self.done_location))[:, :, :3].astype(np.uint8)
        done = False
        res = (pytesseract.image_to_string(done_cap)[:4]).upper()
        if res in self.done_text and res != "":
            done = True

        return done, done_cap, res
