from CVRP import CVRP
import numpy as np
from multiprocessing.pool import ThreadPool
import time, sys


class BRKGA:
    def __init__(self,path:str, population_size:int =100, elite_size:float = 0.15, mutant_size:float = 0.15, inheritance:float = 0.7):
        
        self.instance = CVRP(path)
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutant_size = mutant_size
        self.inheritance = inheritance

        self.n_elites = int(self.elite_size * self.population_size)
        self.n_mutants = int(self.mutant_size * self.population_size)

        self.population = np.random.random([self.population_size, self.instance.dimmension-1])
        self.eval, self.population = self._eval(self.population)
        self.population = self.population[np.argsort(self.eval)]
        self.elite = self.population[:self.n_elites]
        


    def _decoder(self,chromosome):
        of, _ = self.instance.get_of(np.argsort(chromosome)+1)
        return of, chromosome


    def _combine(self, elite, n_elite):

        return np.array([e if np.random.random() < self.inheritance else n for e, n in zip(elite,n_elite)])

    def _eval(self,pop):
        OF = []
        popa = []
        with ThreadPool() as pool:
            for of, item in pool.map(self._decoder, pop):
                OF.append(of)
                popa.append(item)
        #for i in pop:
        #    OF.append(self._decoder(i))
        return np.array(OF), np.array(popa)
    
    def _mutate(self):
        self.population = self.population[:-self.n_mutants]
        self.population = np.append(self.population, np.random.random([self.n_mutants, self.instance.dimmension - 1]), axis = 0)
        #self.population.append([np.random.random([self.n_mutants, self.instance.dimmension - 1])])

    def _evolve_n(self):
        self._mutate()
        pop = []
        for elite in self.elite:
            for n_elite in self.population[self.n_elites:]:
                pop.append(self._combine(elite,n_elite))
        return np.array(pop)

    def _evolve(self):
        self._mutate()
        pop = []
        for i in range(self.population_size-self.n_elites):
            elite = self.population[np.random.choice(np.arange(self.n_elites))]
            n_elite = self.population[np.random.choice(np.arange(self.n_elites,self.population_size))]
            pop.append(self._combine(elite,n_elite))
        return np.array(pop)


    def solve(self,n_it =10, patience:int= None):
        it = 0
        pt = 0
        if patience == None:
            patience = n_it
        self.best_of = np.inf
        best_sofar = np.inf
        self.best_sol = self.elite[0]
        start_time = time.time()
        while True:

            #Restart mechanism
            if pt >= patience-1:
                best_sofar = np.inf
                self.population = np.random.random([self.population_size, self.instance.dimmension-1])
                self.eval, self.population = self._eval(self.population)
                self.population = self.population[np.argsort(self.eval)]
                self.elite = self.population[:self.n_elites]

            pop = self._evolve()
            pop_eval, pop = self._eval(pop)
            best_itens = np.argsort(pop_eval)
            self.population = pop[best_itens][:self.population_size]
            self.eval = pop_eval[best_itens]
            self.elite = self.population[:self.n_elites]
            it += 1
            if self.eval[0] < self.best_of:
                self.best_of = self.eval[0]
                self.best_sol = self.elite[0]
                pt = 0

            if self.eval[0]< best_sofar:
                best_sofar = self.eval[0]
                pt = 0

            else:
                pt += 1

            if it >= n_it:
                break
            print(best_sofar)
        r_time = time.time() - start_time

        return self.best_of, self.best_sol, r_time, it


if __name__ =='__main__':

    obj = {}
    solver = {}

    for i, com in enumerate(sys.argv):
        if com =='--path':
            obj['path'] = sys.argv[i+1]
        elif com == '--pop_size':
            obj['population_size'] = int(sys.argv[i+1])
        elif com == '--elite_size':
            obj['elite_size'] = float(sys.argv[i+1])
        elif com == '--mutant_size':
            obj['mutant_size'] = float(sys.argv[i+1])
        elif com == '--inheritance':
            obj['inheritance'] = float(sys.argv[i+1])
        elif com == '--n_it':
            solver['n_it'] = int(sys.argv[i+1])
        elif com == '--patience':
            solver['patience'] = int(sys.argv[i+1])
    
    inst = BRKGA(**obj)
    best_of, best_sol, r_time, it = inst.solve(**solver)

    print(best_of)
