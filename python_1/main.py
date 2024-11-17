import gymnasium as gym
import numpy as np
import time  # For adding delay between frames

# Set up environment
env = gym.make("CartPole-v1", max_episode_steps=5000)
num_buckets = (6, 12, 6, 12)  # Discretization bins for each state dimension

# Q-learning parameters
learning_rate = 0.1
discount_factor = 0.99
epsilon = 1.0         # Initial exploration rate
epsilon_min = 0.1     # Minimum exploration rate
epsilon_decay = 0.995 # Decay rate for epsilon
episodes = 1000     # Number of episodes for training

# Create a Q-table
q_table = np.zeros(num_buckets + (env.action_space.n,))

# Function to discretize the continuous state space
def discretize_state(state):
    upper_bounds = [env.observation_space.high[0], 0.5, env.observation_space.high[2], np.radians(50)]
    lower_bounds = [env.observation_space.low[0], -0.5, env.observation_space.low[2], -np.radians(50)]
    ratios = [(state[i] + abs(lower_bounds[i])) / (upper_bounds[i] - lower_bounds[i]) for i in range(len(state))]
    new_state = [int(round((num_buckets[i] - 1) * ratios[i])) for i in range(len(state))]
    new_state = [min(num_buckets[i] - 1, max(0, new_state[i])) for i in range(len(state))]
    return tuple(new_state)

# Training loop
for episode in range(episodes):
    state = discretize_state(env.reset()[0])
    done = False
    total_reward = 0

    while not done:
        # Epsilon-greedy action selection
        if np.random.rand() < epsilon:
            action = env.action_space.sample()  # Explore
        else:
            action = np.argmax(q_table[state])  # Exploit
        
        next_state, _, done, _, _ = env.step(action)
        next_state = discretize_state(next_state)
        
        # Get the angle of the pole (third element of the state)
        pole_angle = next_state[2]  # This corresponds to the third element in the state

        # Reward structure with penalties for tilting and falling
        angle_threshold = np.radians(15)  # 15 degrees in radians

        # Check if the episode is done due to falling
        if done:
            reward = -30
        else:
            # Apply penalties based on the pole's angle
            if abs(pole_angle) > angle_threshold:
                reward = -(abs(pole_angle) / np.radians(50))/10  # Scaled penalty
            else:
                reward = 1  # Small reward for staying upright

        total_reward += reward
        
        # Q-learning update
        best_next_action = np.argmax(q_table[next_state])
        td_target = reward + discount_factor * q_table[next_state][best_next_action]
        q_table[state][action] += learning_rate * (td_target - q_table[state][action])
        
        state = next_state

    # Decay epsilon
    epsilon = max(epsilon_min, epsilon * epsilon_decay)
    print(f"Episode: {episode + 1}, Total Reward: {total_reward}")

# Close environment post-training
env.close()

# Visualization of the learned policy
env = gym.make("CartPole-v1", max_episode_steps=5000, render_mode='human')
def display_agent():
    state = discretize_state(env.reset()[0])
    done = False
    total_reward = 0
    while not done:
        env.render()  # Display the current environment frame
        action = np.argmax(q_table[state])  # Choose action based on learned Q-table
        next_state, _, done, _, _ = env.step(action)
        state = discretize_state(next_state)
        total_reward += 1  # Reward for each step taken
        time.sleep(0.05)  # Slows down rendering for better visualization
    print(f"Total reward from display episode: {total_reward}")

# Call display_agent to watch the bot play
display_agent()

env.close()