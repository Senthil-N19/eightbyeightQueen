from random import shuffle

class eightbyeightQueen:

    def __init__(self):
        self.board = self.createBoard()
        self.solutions = []
        self.size = 8
        self.env = []
        self.goal = None
        self.goalIndex = -1

    def createBoard(self):
        board = [[0 for i in range(8)] for j in range(8)]
        return board

    def setBoard(self,board,gen):
        for i in range(self.size):
            board[gen[i]][i] = 1

    def genereteDNA(self):
        #genereates random list of length n
        DNA = list(range(self.size))
        shuffle(DNA)
        while DNA in self.env:
            shuffle(DNA)
        return DNA

    def initializeFirstGenereation(self):
        for i in range(500):
            self.env.append(self.genereteDNA())

    def utilityFunction(self,gen):

        hits = 0
        board = self.createBoard()
        self.setBoard(board,gen)
        col = 0

        for dna in gen:
            try:
                for i in range(col-1,-1,-1):
                    if board[dna][i] == 1:
                        hits+=1
            except IndexError:
                print(gen)
                quit()
            for i,j in zip(range(dna-1,-1,-1),range(col-1,-1,-1)):
                if board[i][j] == 1:
                    hits+=1
            for i,j in zip(range(dna+1,self.size,1),range(col-1,-1,-1)):
                if board[i][j] == 1:
                    hits+=1
            col+=1
        return hits

    def isGoalGen(self,gen):
        if self.utilityFunction(gen) == 0:
            return True
        return False


    def crossOverGens(self,firstGen,secondGen):
        for i in range(1,len(firstGen)):
            if abs(firstGen[i-1] - firstGen[i])<2:
                firstGen[i],secondGen[i] = secondGen[i],firstGen[i]
            if abs(secondGen[i-1] - secondGen[i])<2:
                firstGen[i],secondGen[i] = secondGen[i],firstGen[i]


    def MutantGen(self,gen):
        bound = self.size//2
        from random import randint as rand
        leftSideIndex = rand(0,bound)
        RightSideIndex = rand(bound+1,self.size-1)
        newGen = []
        for dna in gen:
            if dna not in newGen:
                newGen.append(dna)
        for i in range(self.size):
            if i not in newGen:
                # newGen.insert(rand(0,len(gen)),i)
                newGen.append(i)

        gen = newGen
        gen[leftSideIndex],gen[RightSideIndex] = gen[RightSideIndex],gen[leftSideIndex]
        return gen


    def crossOverAndMutant(self):
        for i in range(1,len(self.env),2):
            firstGen = self.env[i-1][:]
            secondGen = self.env[i][:]
            self.crossOverGens(firstGen,secondGen)
            firstGen = self.MutantGen(firstGen)
            secondGen = self.MutantGen(secondGen)
            self.env.append(firstGen)
            self.env.append(secondGen)

    def makeSelection(self):
        #index problem
        genUtilities = []
        newEnv = []

        for gen in self.env:
            genUtilities.append(self.utilityFunction(gen))
        if min(genUtilities) == 0:
            self.goalIndex = genUtilities.index(min(genUtilities))
            self.goal = self.env[self.goalIndex]
            return self.env
        minUtil=None
        while len(newEnv)<self.size:
            minUtil = min(genUtilities)
            minIndex = genUtilities.index(minUtil)
            newEnv.append(self.env[minIndex])
            genUtilities.remove(minUtil)
            self.env.remove(self.env[minIndex])

        return newEnv

    def solveGA(self):
        self.initializeFirstGenereation()
        for gen in self.env:
            if self.isGoalGen(gen):
                return gen
        count = 0
        while True:
            self.crossOverAndMutant()
            self.env = self.makeSelection()
            count +=1
            if self.goalIndex >= 0 :
                try:
                    print(count)
                    return self.goal
                except IndexError:
                    print(self.goalIndex)
            else:
                continue

if __name__ == "__main__":
    obj = eightbyeightQueen()
    print(obj.solveGA())
