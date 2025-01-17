import numpy as np

class tool:

    def distancia(self, position_robot, position_oponent):
      return ((position_robot[0] - position_oponent[0])**2 + (position_robot[1] - position_oponent[1])**2)**0.5
    
    def criarVetor(self, pos_robot:tuple, pos_obs:tuple):
        vetor = np.array(pos_obs) - np.array(pos_robot)
        return vetor
    
    def angulo_entre_vetores(self, vetor_u, vetor_v):
   
        produto_escalar = np.dot(vetor_u, vetor_v)
        
        norma_u = np.linalg.norm(vetor_u)
        norma_v = np.linalg.norm(vetor_v)
        
        cos_theta = produto_escalar / (norma_u * norma_v)
        
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        
        angulo_rad = np.arccos(cos_theta)
        
        angulo_graus = np.degrees(angulo_rad)
        
        return angulo_graus

    def calcularAngulo(self, oppenent, robot:dict, target:tuple):
        robot_position = (robot.x, robot.y)
        destino = self.criarVetor(robot_position, target)
        colisao = self.criarVetor(robot_position, oppenent)

        return  self.angulo_entre_vetores(destino, colisao)
    
    def calcularSentidoDesvio(self, pos_robot: tuple, pos_target: tuple):
        destino = self.criarVetor(pos_robot, pos_target)
        perp1 = self.angulo_entre_vetores([0,1], destino)
        perp2 = self.angulo_entre_vetores([1,0], destino)

        if(perp1 <= perp2):       
            sentido = 1 if pos_target[0] >= pos_robot[0] else -1
            sentido = sentido if pos_target[1] >= pos_robot[1] else sentido * -1
            eixo = "eixo y"
        else:
            sentido = 1 if pos_target[1] >= pos_robot[1] else -1
            sentido = sentido if pos_target[0] >= pos_robot[0] else sentido * -1
            eixo = "eixo x"
        
        return sentido, eixo
    


