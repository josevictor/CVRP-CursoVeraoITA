import numpy as np
from scipy.spatial.distance import euclidean

class CVRP:
    """
    blaa bla bal
    """
    def __init__(self, path: str):
        with open(path, 'r') as inst:
            line = inst.read()

        line = line.split('\n')

        #Header

        self.name = str(line[0].split(' : ')[1])
        self.comment = str(line[1].split(' : ')[1])
        self.type = str(line[2].split(' : ')[1])
        self.dimmension = int(line[3].split(' : ')[1])
        self.edge_weight_type = str(line[4].split(' : '[1]))
        self.capacity = int(line[5].split(' : ')[1])

        #coord

        self.coord = []
        for i in range(7, self.dimmension + 7):
            c = line[i].split(' ')
            self.coord.append(np.array([float(c[1]), float(c[2])]))
        self.coord = np.array(self.coord)

        #Demand

        self.demand = []
        for i in range(self.dimmension + 8, self.dimmension * 2 +8):
            c = line[i].split(' ')
            self.demand.append(int(c[1]))

        #depot

        self.depot = int(line[self.dimmension *2 +9])

        #dist

        self.dist = np.zeros([self.dimmension,self.dimmension])

        for i in range(self.dimmension):
            for j in range(i):
                d = euclidean(self.coord[i], self.coord[j])
                self.dist[i][j] = d
                self.dist[j][i] = d


if __name__ == '__main__':
    print('Hello world')
    teste = CVRP('teste.vrp')
    print(f'name : {teste.name}\nComment : {teste.comment}\n Type : {teste.type}')
    print(teste.coord)
    print(teste.demand)
    print(teste.depot)
