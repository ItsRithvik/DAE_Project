import tensorflow as tf
import gymnasium as gym
import keras as rl
import ale_py
import random

#creating enviroment
gym.register_envs(ale_py)
env = gym.make('ALE/Breakout-v5',render_mode='human')

#assigning number of possible states/actions
height, width, channels = env.observation_space.shape
actions = env.action_space.n

def test(env, episodes=5, agent='random'):

    for episode in range(1,episodes+1):
        state = env.reset()
        terminated = False
        score = 0

        while not terminated:
            env.render()
            if agent=='random':
                action = random.choice([0,1,2,3])
            else:
                action = agent.predict()
            observation, reward, terminated, truncated, info = env.step(action)
            score += reward
        print('Episode {}: {}'.format(episode, score))
    env.close()

def base_model(height, width, channels, actions):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(32, (8,8), strides=(4,4), activation='relu', input_shape=( height, width, channels)))
    model.add(tf.keras.layers.Conv2D(64, (4,4), strides=(2,2), activation='relu'))
    model.add(tf.keras.layers.Conv2D(64, (3,3), activation='relu'))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(512, activation='relu'))
    model.add(tf.keras.layers.Dense(256, activation='relu'))
    model.add(tf.keras.layers.Dense(actions, activation='softmax'))
    return model

model = base_model(height, width, channels, actions)
print(model.summary())