from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback
import os


class LogginCallback(BaseCallback):

    def __init__(self, check_freq, save_path, verbose=1):
        super(LogginCallback, self).__init__(verbose)
        self.stop_training_flag = False
        self.check_freq = check_freq
        self.save_path = save_path

    def _init_callback(self):
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self):
        if self.n_calls % self.check_freq == 0:
            model_path = os.path.join(self.save_path, 'best_model_{}'.format(self.n_calls))
            self.model.save(model_path)

    def _on_step(self) -> bool:
        if self.stop_training_flag:
            self.model.callback_manager.stop_training = True
        return True

    def stop_training(self):
        self.stop_training_flag = True
