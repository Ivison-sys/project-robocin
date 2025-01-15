import numpy as np
from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point
from functions import tool
from time import sleep as sp
import time
# self.robot = primeiro, self.obstacles, self.teammates

def distancia(position_robot, position_oponent):
    return ((position_robot[0] - position_oponent[0])**2 + (position_robot[1] - position_oponent[1])**2)**0.5


class ExampleAgent(BaseAgent, tool):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)
    


    def decision(self):
        if len(self.targets) == 0:
            return

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, self.targets[0])
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)
        
        opa= 100
        for op in self.opponents:
            position_op = (self.opponents[op].x, self.opponents[op].y)
            position_robo = (self.robot.x, self.robot.y)

 
            if distancia(position_robo, position_op) <= 0.3:
                print('colisão')
                print(target_velocity)
                vel_x, vel_y = target_velocity
                # a,b = Navigation.goToPoint(self.robot, Point(positon[0]+ang, positon[1]+ang))
                ang = self.calcularDesvio(position_op, self.robot, self.targets[0])
                if ang < 80 and op != opa:
                    self.set_vel(Point(vel_x - 0.5, vel_y + 0.45))
                if ang < 20:
                    self.set_vel(Point(vel_x - 1.3, vel_y + 2))
                    
                         
                                    
                    
                    
                
                # self.set_vel(target_velocity)



        return
    

    def post_decision(self):
        pass
