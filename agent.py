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
        
        ponto_destino = self.targets[0]

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, ponto_destino)
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)
        

        for op in self.opponents:
            position_op = (self.opponents[op].x, self.opponents[op].y)
            position_robo = (self.robot.x, self.robot.y)
            vel_x, vel_y = target_velocity
            

            dis = distancia(position_robo, position_op)
            velocidades =  (vel_x, vel_y)
            ang = self.calcularAngulo(position_op, self.robot, self.targets[0])
            
            
            if dis <= 0.3 and ang <= 40:
                velocidades = (vel_x/4, vel_y)

            elif dis <= 0.54 and ang <= 40:
                velocidades = (vel_x/2, vel_y)
                self.set_vel(Point(velocidades[0], velocidades[1]))

            if(distancia(position_op, ponto_destino) <= 0.2):
                return

            if dis <= 0.35:
                sentido_desvio, eixo = self.calcularSentidoDesvio(position_op, (ponto_destino[0], ponto_destino[1]))
                if dis <= 0.18:
                    print(target_velocity)
                    print(ang)

                prop = velocidades[0] if (dis < 0.2) else 0
                # a,b = Navigation.goToPoint(self.robot, Point(positon[0]+ang, positon[1]+ang))
                if ang <= 40:
                    self.set_vel(Point(velocidades[0] - 1.3 - prop, (velocidades[1]+ 1.5)*sentido_desvio))
                    print(sentido_desvio, eixo)

                elif ang <= 80 and dis <= 0.25:
                    self.set_vel(Point(velocidades[0] - 0.5 - prop, (velocidades[1] + 0.45)*sentido_desvio ))
                    print(sentido_desvio, eixo)

                

        return
    

    def post_decision(self):
        
        pass
