import numpy as np
import threading
from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point
from functions import tool
from time import sleep as sp
import time

class ExampleAgent(BaseAgent, tool):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)
        self.ponto_destino = (0, 0)
        self.tempo = time.time()
        self.position_past = (0, 0)
        self.ignore =  []
        # print(self.position_past)
    
    def decision(self):
        if len(self.targets) == 0:
            return
        
        
        robot_close_targets = {}
        
        for id_target in range(len(self.targets)):
            menor_dist = float("inf")
            robot_close = -1
            
            for id_robot in range(len(self.teammates)): 
                if id_robot not in robot_close_targets:               
                    position_robot = (self.teammates[id_robot].x, self.teammates[id_robot].y)
                    position_target =  self.targets[id_target]
                    dist = self.distancia(position_robot, position_target)
                    if dist < menor_dist:
                        menor_dist = dist
                        robot_close = id_robot
                       
                        
            robot_close_targets.update({robot_close: id_target})             
                    
        
       
        
        if self.robot.id not in robot_close_targets:
            self.ponto_destino = -1
            return
                        
        self.ponto_destino = self.targets[robot_close_targets[self.robot.id]]

        return
    

    def post_decision(self):
        if self.ponto_destino == -1:
            return

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, self.ponto_destino)
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)
    
           
        
        for op in self.opponents:
            if time.time() - self.tempo >= 3.5:
                position_now = (self.robot.x, self.robot.y)
                if self.distancia(position_now, self.position_past) <= 0.2:
                    print(f"Robô {self.robot.id}: loop detectado")
                    self.ignore.append(self.opponents[op].id)
                    print(self.ignore)                        
                else:
                    self.ignore = []
                
                self.tempo = time.time()
                self.position_past = position_now  

            if self.opponents[op].id in self.ignore:
                return
            
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

            if(self.distancia(position_op, self.ponto_destino) <= 0.2):
                return

            if dis <= 0.35:
                sentido_desvio, eixo = self.calcularSentidoDesvio(position_op, (self.ponto_destino[0], self.ponto_destino[1]))
                
                # if dis <= 0.18:
                    # print(f'robot {self.robot.id}: {ang:.2f}')

                prop = velocidades[0] if (dis < 0.2) else 0

                if ang <= 40:
                    self.set_vel(Point(velocidades[0] - 1.3 - prop, (velocidades[1]+ 1.5)*sentido_desvio))
                    # print(sentido_desvio, eixo)

                elif ang <= 80 and dis <= 0.25:
                    self.set_vel(Point(velocidades[0] - 0.5 - prop, (velocidades[1] + 0.45)*sentido_desvio ))
                    # print(sentido_desvio, eixo)
        
        return
    
 
        
    