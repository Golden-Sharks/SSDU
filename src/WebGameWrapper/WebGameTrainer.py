from stable_baselines3 import DQN, PPO

from src.WebGameWrapper.WebGameEnvironment import WebGame
from src.WebGameWrapper.LogginCallback import LogginCallback
from stable_baselines3.common.callbacks import CallbackList


class WebGameTrainer:
    def __init__(self, dict):
        self.__env = None
        self.__model = None
        self.construct(dict)
        self.start()

    def __create_env(self):
        pass

    def __build_model(self, dict):
        model_dict = dict.get('model')
        if model_dict.get('model') == 'DQN':
            print("DQN")
            print(model_dict.get('policy'))
            print(self.getEnvironment())
            print(self.log_dir)
            print(model_dict.get('buffer_size'))
            print(model_dict.get('trainingStart'))
            print(model_dict.get('tau'))
            print(model_dict.get('gamma'))
            print("Groink")
            self.__model = DQN(model_dict.get('policy'),
                               self.getEnvironment(),
                               tensorboard_log=self.log_dir,
                               verbose=1,
                               buffer_size=model_dict.get('buffer_size'),
                               learning_starts=model_dict.get('trainingStart'),
                               tau=model_dict.get('tau'),
                               gamma=model_dict.get('gamma'),
                               train_freq=4)
            # model = DQN('CnnPolicy', env.getEnvironment(), tensorboard_log=log_dir, verbose=1, buffer_size=100,
            #             learning_starts=1000, tau=1.0, gamma=0.99, train_freq=4)
            print('groink2')
            print("MODEL", self.__model)
        elif  model_dict.get('model') == 'PPO':
            print("PPO")
            self.__model = PPO(policy=model_dict.get('policy'),
                               env=self.getEnvironment(),
                               tensorboard_log=self.log_dir,
                               verbose=1,
                               n_steps=model_dict.get('n_steps'),
                               n_epochs=model_dict.get('n_epochs'),
                               learning_rate=model_dict.get('learning_rate'),
                               gamma=model_dict.get('gamma'),
                               gae_lambda=model_dict.get('gae_lambda'))
        print("END MODEL", self.__model)
    def construct(self, dict):
        print("Construct")
        self.__env = WebGame(dict)
        print("ENV OK")
        self.checkpoint_dir = 'dat/train'
        self.log_dir = 'dat/logs/'
        self.__tbLogName = dict.get('model').get('tensorboard_name')
        print("logboard OK")
        self.__build_model(dict)
        print("model OK")
        #self.__start()

    def start(self):
        print("Training start !")
        self.__callback = LogginCallback(check_freq=200, save_path=self.checkpoint_dir)
        self.__callback_list = CallbackList([self.__callback])
        try:
            self.__model.learn(total_timesteps=10000, callback=self.__callback_list, tb_log_name=self.__tbLogName)
        finally:
            pass

    def stop(self):
        self.__callback_list.model.s

    def getEnvironment(self):
        if self.__env is not None:
            return self.__env

    def getModel(self):
        if self.__model is not None:
            return self.__model
