import gymnasium as gym
import rsoccer_gym
from gymnasium.envs.registration import register
from utils.CLI import cli, Difficulty
import pygame

## Aumentar eixo y e dimunuir x a medidia que a distancia diminui.

args = cli()

register(
    id="VSS-Project",
    entry_point="vssenv:ExampleEnv"
)

register(
    id="SSL-Project",
    entry_point="sslenv:SSLExampleEnv"
)

env = gym.make("SSL-Project", difficulty=Difficulty(args.difficulty))

env.reset()

for i in range(1):
    terminated = False
    truncated = False
    while not (terminated or truncated):
        # Step using random actions
        action = env.action_space.sample()
        next_state, reward, terminated, _, _ = env.step(action)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
                break
            
    env.close()