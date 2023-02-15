import numpy as np


class CVRP:
    """
    bla bla bal
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
            self.coord.append(np.array([int(c[1]), int(c[2])]))
        self.coord = np.array(self.coord)

        #Demand

        self.demand = []
        for i in range(self.dimmension + 8, self.dimmension * 2 +8):
            c = line[i].split(' ')
            self.demand.append(int(c[1]))

        #depot

        self.depot = int(line[self.dimmension *2 +9])

if __name__ == '__main__':
    print('Hello world')
    teste = CVRP('teste.vrp')
    print(f'name : {teste.name}\nComment : {teste.comment}\n Type : {teste.type}')
    print(teste.coord)
    print(teste.demand)
    print(teste.depot)
