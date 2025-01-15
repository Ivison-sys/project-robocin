import numpy as np

class tool:
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
    
    def calcularDesvio(self, oppenent, robot:dict, target:tuple):
        robot_position = (robot.x, robot.y)
        destino = self.criarVetor(robot_position, target)
        colisao = self.criarVetor(robot_position, oppenent)

        return self.angulo_entre_vetores(destino, colisao)

