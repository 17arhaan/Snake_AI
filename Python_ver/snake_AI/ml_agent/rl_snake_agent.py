# ml_agent/rl_snake_agent.py

import gym
from stable_baselines3 import PPO

# Import the custom snake environment
import ml_agent.snake_env

# Create the snake game environment
env = gym.make('Snake-v0')

# Define and train the PPO model
model = PPO('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=100000)

# Save the model
model.save("ppo_snake_model")

# Load the model and test it
model = PPO.load("ppo_snake_model")

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()

    if dones:
        obs = env.reset()