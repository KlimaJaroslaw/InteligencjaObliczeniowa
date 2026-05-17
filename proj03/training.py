import os
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from stable_baselines3.common.evaluation import evaluate_policy # <--- Dodaj to


tb_log_dir = "logs2/"
gammas = [0.9, 0.99, 0.999]
runs_per_gamma = 10
total_timesteps = 50_000

best_mean_reward = -float('inf')
best_model_path = "best_ppo_car_racing_model"

for gamma in gammas:
    print(f"--- Rozpoczynam serię dla gamma={gamma} ---")
    for i in range(runs_per_gamma):
        run_name = f"g{gamma}_run_{i}"
        print(f"Trening: {run_name}...")
        env_car = gym.make("CarRacing-v3", render_mode="rgb_array", continuous=True)
        env_car = Monitor(env_car)
        env_car = DummyVecEnv([lambda: env_car])
        env_car = VecFrameStack(env_car, n_stack=4)
        model_car = PPO("CnnPolicy", env_car, gamma=gamma, verbose=0, tensorboard_log=tb_log_dir)
        model_car.learn(total_timesteps=total_timesteps, tb_log_name=f"05_mln_{run_name}")
        mean_reward, std_reward = evaluate_policy(model_car, env_car, n_eval_episodes=5)
        print(f"Wynik runu {i}: Średnia nagroda = {mean_reward:.2f} +/- {std_reward:.2f}")
        if mean_reward > best_mean_reward:
            best_mean_reward = mean_reward
            model_car.save(best_model_path)
            print(f"!!! NOWY NAJLEPSZY MODEL ZAPISANY (Reward: {mean_reward:.2f}, Gamma: {gamma}) !!!")
        env_car.close()

print(f"\nKoniec! Najlepszy uzyskany wynik to: {best_mean_reward:.2f}")
print(f"Model został zapisany jako: {best_model_path}.zip")