import numpy as np
from scipy.spatial.distance import euclidean
from math import floor

class CVRP:
    """
    
    """
    def __init__(self, path: str):
        """
        path: String file location

        """
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
            c = line[i].strip(' ').split()
            self.coord.append(np.array([float(c[1]), float(c[2])]))
        self.coord = np.array(self.coord)

        #Demand

        self.demand = []
        for i in range(self.dimmension + 8, self.dimmension * 2 +8):
            c = line[i].strip(' ').split()
            self.demand.append(float(c[1]))

        self.demand = np.array(self.demand)

        #depot

        self.depot = int(line[self.dimmension *2 +9])

        #dist

        self.dist = np.zeros([self.dimmension,self.dimmension])

        for i in range(self.dimmension):
            for j in range(i):
                d = floor(euclidean(self.coord[i], self.coord[j])+0.5)
                self.dist[i][j] = d
                self.dist[j][i] = d

    def get_of(self, res_vec:list):
        """
        res_vec: list size dimmension - 1
        return of, routes
        """
        
        #Assert the size of the res_vec
        assert len(res_vec) == self.dimmension-1
        
        #generate routes
        routes = self._gen_routes(res_vec)
        
        #Calculate the cost of the routes
        of = self._get_of(routes)

        return of, routes


    def _gen_routes(self,res_vec:list) -> list:

        routes = []
        route = []
        for client in res_vec:
            if np.sum(np.append(self.demand[[route]],self.demand[client])) <= self.capacity:
                route.append(client)
            else:
                routes.append(route)
                route = [client]
        routes.append(route)
        return routes

    def _get_of(self, routes:list) -> float:

        of = 0
        for route in routes:
            of += self.dist[self.depot - 1][route[0]] + self.dist[route[-1]][self.depot - 1] + np.sum([self.dist[route[i]][route[i + 1]] for i in range(len(route) - 1)])

        return of




if __name__ == '__main__':
    print('Hello world')
    teste = CVRP('teste.vrp')
    print(f'name : {teste.name}\nComment : {teste.comment}\n Type : {teste.type}')
    print(teste.coord)
    print(teste.demand)
    print(teste.depot)
