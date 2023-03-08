import csv
import scipy.optimize as opt
import random
import numpy as np
import sys
class Demon:
    def __init__(self,staminaLost: int, turnsToRecover: int,staminaRecPerTurn:int, turnsFragment: int, fragmentList:list, index) -> None:
        self._staminaLost= staminaLost
        self._turnsToRecover= turnsToRecover
        self._staminaRecPerTurn= staminaRecPerTurn
        self._turnsFragment= turnsFragment
        self._index= index
        if self._turnsFragment!= len(fragmentList):
            self._fragmentList= [0 for i in range(self._turnsFragment)]
        else:self._fragmentList= fragmentList
    def __str__(self) -> str:
        return f'index: {self._index} staminaLost: {self._staminaLost}, turnsToRecover: {self._turnsToRecover}, staminaRecPerTurn: {self._staminaRecPerTurn}, turnsFragment: {self._turnsFragment}, fragmentList: {self._fragmentList}\n'
    def __repr__(self) -> str:
        return self.__str__()
class Pandora:
    def __init__(self, staminaMax:int, stamina:int) -> None:
        self._staminaMax= staminaMax
        self._stamina=stamina
        self.fragments=0
        
    def recover(self, staminarec:int):
        assert(staminarec>=0 and self._stamina+staminarec<=self._staminaMax)
        self._stamina+=staminarec
    def increaseFragments(self,amount:int):
        self.fragments+=amount
    def dmg(self,amount:int):
        self._stamina-=amount
        assert(self._stamina>=0)
    def __str__(self) -> str:
        return f'staminaMax: {self._staminaMax}, stamina: {self._stamina}, fragments: {self.fragments}'
class GameManager:
    def __init__(self, turnMax:int,numDemons:int,listOfDemons:list,pandora:Pandora) -> None:
        self._turn=0
        self._turnMax=turnMax
        self._numDemons=numDemons
        self._listOfDemons=listOfDemons
        self._listofDemonClasses=[]
        self._defeatedDemons=[]
        self._turnstoRecover=[0 for i in range(self._turnMax)]
        self._turnstoFragments=[0 for i in range(self._turnMax)]
        self.choices=[]
        if self._numDemons!= len(self._listOfDemons):
            raise(Exception(f'numDemons: {numDemons}, lenDemons: {len(self._listOfDemons)}'))
        for i in range(self._numDemons):
            self._listofDemonClasses.append(Demon(self._listOfDemons[i][0], self._listOfDemons[i][1], self._listOfDemons[i][2], self._listOfDemons[i][3], self._listOfDemons[i][4:],i))
        self._pandora= pandora
    def turn(self):
        if self._turn==self._turnMax-1:
            return self.end()
        self._pandora.recover(self._turnstoRecover[self._turn])
        self._pandora.increaseFragments(self._turnstoFragments[self._turn])
        if demon:=self.decide():
            self._pandora.dmg(demon._staminaLost)
            self._listofDemonClasses.pop(self._listofDemonClasses.index(demon))
            self._defeatedDemons.append(demon)
            if self._turn+demon._turnsToRecover<self._turnMax:
                self._turnstoRecover[self._turn+demon._turnsToRecover]+=demon._staminaRecPerTurn
            for i in range(demon._turnsFragment):
                if self._turn+i<self._turnMax:
                    self._turnstoFragments[self._turn+i]+=demon._fragmentList[i]
        self._turn+=1
        return self.turn()
    def decide(self):
        demonsavailable= [i for i in self._listofDemonClasses if i not in self._defeatedDemons and i._staminaLost<=self._pandora._stamina]
        if demonsavailable:
            choice= max(demonsavailable, key=lambda x:sum(x._fragmentList[:self._turnMax-self._turn]))
            self.choices.append(choice._index)
            return choice
        return None
    def start(self):
        return self.turn()
    def end(self):
        print(f'GAME FINISHED\n\n\nTurns: {self._turn}\n\nDefeated Demons: {self._defeatedDemons}\n\nChoices: {self.choices}\n\nFragments: {self._pandora.fragments}')
    def __str__(self) -> str:
        return f'Turns Max= {self._turnMax}\n\nnumDemons: {self._numDemons}, listOfDemons: \n{self._listofDemonClasses}\n\npandora: {self._pandora}'
        
def main():
    sys.setrecursionlimit(100000)
    lista=[]
    with open('replyChallenge/2022/03-etheryum.txt', 'r') as f:
        reader= csv.reader(f, delimiter=' ')
        lista= list(reader)
        lista= [[int(i) if i else 0 for i in j] for j in lista]
    settings=lista.pop(0)
    pandora= Pandora(settings[1], settings[0])
    manager=GameManager(settings[2],settings[3],lista,pandora)
    #print(f'GAME:{manager}')
    manager.start()
    with open('replyChallenge/2022/output.txt', 'w+') as f:
        for choice in manager.choices:
            f.write(f'{choice}\n')
    
if __name__ == '__main__':
    main()