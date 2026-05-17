import os
import csv
import json
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from stable_baselines3.common.evaluation import evaluate_policy


def main():
    model_path = os.path.join(os.path.dirname(__file__), "logs", "best_model", "best_ppo_car_racing_model.zip")
    if not os.path.exists(model_path):
        print(f"Model not found: {model_path}")
        return

    print(f"Ładuję model z: {model_path}")
    model = PPO.load(model_path)

    # Stworzenie środowiska zgodnego z trenowaniem (stack 4 klatek), bez renderowania
    env = gym.make("CarRacing-v3", render_mode=None, continuous=True)
    env = Monitor(env)
    env = DummyVecEnv([lambda: env])
    env = VecFrameStack(env, n_stack=4)

    # Krótka ewaluacja bez renderowania
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=5, warn=False)
    print(f"Średnia nagroda (5 epizodów): {mean_reward:.2f} +/- {std_reward:.2f}")

    # Kilka epizodów rollout bez wizualizacji, by zobaczyć sumy nagród
    n_rollouts = 10
    rewards = []
    for ep in range(n_rollouts):
        obs = env.reset()
        if isinstance(obs, tuple):
            obs = obs[0]
        done = False
        total_reward = 0.0
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            step_result = env.step(action)
            obs, reward, terminated, truncated, info = step_result

            # Normalize reward extraction for vectorized env
            try:
                r = float(reward[0]) if hasattr(reward, '__len__') else float(reward)
            except Exception:
                r = float(reward)
            total_reward += r

            # Check done
            if hasattr(terminated, '__len__'):
                done = bool(terminated[0]) or bool(truncated[0])
            else:
                done = bool(terminated) or bool(truncated)

        rewards.append(total_reward)
        print(f"Epizod {ep+1}/{n_rollouts}: suma nagród = {total_reward:.2f}")

    mean_rollout = sum(rewards) / len(rewards) if rewards else 0.0
    print(f"Średnia suma nagród z {n_rollouts} rolloutów: {mean_rollout:.2f}")

    # Zapis wyników do pliku (CSV + JSON)
    out_dir = os.path.join(os.path.dirname(__file__), "logs", "inference")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "inference_rewards.csv")
    json_path = os.path.join(out_dir, "inference_summary.json")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["episode", "reward"])
        for idx, r in enumerate(rewards, start=1):
            writer.writerow([idx, f"{r:.6f}"])

    summary = {
        "model_path": model_path,
        "eval_mean_reward": float(mean_reward),
        "eval_std_reward": float(std_reward),
        "n_rollouts": n_rollouts,
        "rollout_mean_reward": float(mean_rollout),
        "rollout_rewards": [float(r) for r in rewards]
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Wyniki zapisano: {csv_path}")
    print(f"Podsumowanie zapisano: {json_path}")

    env.close()

    return summary


if __name__ == "__main__":
    main()
