import stable_baselines3
import shimmy
import gymnasium as gym
from stable_baselines3 import PPO, A2C
import os
from stable_baselines3.common.monitor import Monitor
from gymnasium.wrappers import FrameStackObservation
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
import matplotlib.pyplot as plt 
from stable_baselines3.common.results_plotter import plot_results
from stable_baselines3.common import results_plotter
from stable_baselines3.common.callbacks import EvalCallback, BaseCallback
import shutil
import os
import tensorboard

log_dir = "./logs/"
# To istnieje bo notebook się wyjebywał po 3 godzinach xD
source = "./logs/best_model/best_model.zip"
log_source = "./logs/monitor.csv"
log_dir_cont_09 = "./logs/cont_09"
log_dir_cont_99 = "./logs/cont_99"
log_dir_cont_999 = "./logs/cont_999"
log_dir_cont_A2C = "./logs/cont_A2C"
log_dir_disc_09 = "./logs/disc_09"
tb_log_dir = "./tb_logs/"

# --- MODEL ciągły z gamma=0.9 --- 
env_car = gym.make("CarRacing-v3",render_mode="rgb_array",continuous=True)
env_car = Monitor(env_car,log_dir_cont_09)
env_car = DummyVecEnv([lambda: env_car])
env_car = VecFrameStack(env_car, n_stack=4)

eval_env = gym.make("CarRacing-v3",render_mode="rgb_array",continuous=True)
eval_env = Monitor(eval_env)
eval_env = DummyVecEnv([lambda: eval_env])
eval_env = VecFrameStack(eval_env, n_stack=4)
eval_callback = EvalCallback(
    eval_env, 
    best_model_save_path="./logs/best_model/",
    log_path="./logs/results/", 
    eval_freq=10000,
    deterministic=True,
    n_eval_episodes=10,
    render=False,
    verbose=0,
)
model_car = PPO("CnnPolicy",env_car,gamma=0.9,verbose=0,tensorboard_log=tb_log_dir)
model_car.learn(total_timesteps=500_000,callback=eval_callback,tb_log_name="05_mln_g09_cont")
shutil.copy(source, "./modele_archiwum/model_05mln_g09_cont.zip")
# ----------------------------



# --- MODEL ciągły z gamma=0.99

env_car = gym.make("CarRacing-v3",render_mode="rgb_array",continuous=True)
env_car = Monitor(env_car,log_dir_cont_99)
env_car = DummyVecEnv([lambda: env_car])
env_car = VecFrameStack(env_car, n_stack=4)

eval_env = gym.make("CarRacing-v3",render_mode="rgb_array",continuous=True)
eval_env = Monitor(eval_env)
eval_env = DummyVecEnv([lambda: eval_env])
eval_env = VecFrameStack(eval_env, n_stack=4)
eval_callback = EvalCallback(
    eval_env, 
    best_model_save_path="./logs/best_model/",
    log_path="./logs/results/", 
    eval_freq=10000,
    deterministic=True,
    n_eval_episodes=10,
    render=False,
    verbose=0,
)
model_car = PPO("CnnPolicy",env_car,gamma=0.99,verbose=0,tensorboard_log=tb_log_dir)
model_car.learn(total_timesteps=500_000,callback=eval_callback,tb_log_name="05_mln_g99_cont")
shutil.copy(source, "./modele_archiwum/model_05mln_g99_cont.zip")
# ----------------------------


# --- MODEL ciągły z gamma=0.999

env_car = gym.make("CarRacing-v3",render_mode="rgb_array",continuous=True)
env_car = Monitor(env_car,log_dir_cont_99)
env_car = DummyVecEnv([lambda: env_car])
env_car = VecFrameStack(env_car, n_stack=4)

eval_env = gym.make("CarRacing-v3",render_mode="rgb_array",continuous=True)
eval_env = Monitor(eval_env)
eval_env = DummyVecEnv([lambda: eval_env])
eval_env = VecFrameStack(eval_env, n_stack=4)
eval_callback = EvalCallback(
    eval_env, 
    best_model_save_path="./logs/best_model/",
    log_path="./logs/results/", 
    eval_freq=10000,
    deterministic=True,
    n_eval_episodes=10,
    render=False,
    verbose=0,
)
model_car = PPO("CnnPolicy",env_car,gamma=0.999,verbose=0,tensorboard_log=tb_log_dir)
model_car.learn(total_timesteps=500_000,callback=eval_callback,tb_log_name="05_mln_g999_cont")
shutil.copy(source, "./modele_archiwum/model_05mln_g999_cont.zip")
# ----------------------------


# --- MODEL A2C z gamma=0.99

env_car = gym.make("CarRacing-v3",render_mode="rgb_array",continuous=True)
env_car = Monitor(env_car,log_dir_cont_A2C)
env_car = DummyVecEnv([lambda: env_car])
env_car = VecFrameStack(env_car, n_stack=4)

eval_env = gym.make("CarRacing-v3",render_mode="rgb_array",continuous=True)
eval_env = Monitor(eval_env)
eval_env = DummyVecEnv([lambda: eval_env])
eval_env = VecFrameStack(eval_env, n_stack=4)
eval_callback = EvalCallback(
    eval_env, 
    best_model_save_path="./logs/best_model/",
    log_path="./logs/results/", 
    eval_freq=10000,
    deterministic=True,
    n_eval_episodes=10,
    render=False,
    verbose=0,
)
model_car = A2C("CnnPolicy",env_car,gamma=0.99,verbose=0,tensorboard_log=tb_log_dir)
model_car.learn(total_timesteps=500_000,callback=eval_callback,tb_log_name="05_mln_g99_cont_a2c")
shutil.copy(source, "./modele_archiwum/model_05mln_g99_cont_a2c.zip")