import numpy as np
from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point
from functions import tool
from time import sleep as sp
import time
# self.robot = primeiro, self.obstacles, self.teammates



class ExampleAgent(BaseAgent, tool):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)
    
    def decision(self):
        if len(self.targets) == 0:
            return
        
        ponto_destino = self.targets[np.clip(self.robot.id, 0, len(self.targets)- 1)]

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, ponto_destino)
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)
        
        # print(self.teammates)

        

        for op in self.opponents:
            position_op = (self.opponents[op].x, self.opponents[op].y)
            position_robo = (self.robot.x, self.robot.y)
            vel_x, vel_y = target_velocity
            

            dis = self.distancia(position_robo, position_op)
            velocidades =  (vel_x, vel_y)
            ang = self.calcularAngulo(position_op, self.robot, self.targets[0])
            
            
            if dis <= 0.3 and ang <= 40:
                velocidades = (vel_x/4, vel_y)

            elif dis <= 0.54 and ang <= 40:
                velocidades = (vel_x/2, vel_y)
                self.set_vel(Point(velocidades[0], velocidades[1]))

            if(self.distancia(position_op, ponto_destino) <= 0.2):
                return

            if dis <= 0.35:
                sentido_desvio, eixo = self.calcularSentidoDesvio(position_op, (ponto_destino[0], ponto_destino[1]))
                
                if dis <= 0.18:
                    print(target_velocity)
                    print(ang)

                prop = velocidades[0] if (dis < 0.2) else 0

                if ang <= 40:
                    self.set_vel(Point(velocidades[0] - 1.3 - prop, (velocidades[1]+ 1.5)*sentido_desvio))
                    # print(sentido_desvio, eixo)

                elif ang <= 80 and dis <= 0.25:
                    self.set_vel(Point(velocidades[0] - 0.5 - prop, (velocidades[1] + 0.45)*sentido_desvio ))
                    # print(sentido_desvio, eixo)

                

        return
    

    def post_decision(self):
        
        pass
