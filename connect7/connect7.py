import math
import numpy as np
import os
#七子棋,三人游戏,每次下两子.最先下的人第一次下一子,最后下的人第一次下三子.
class connect7():
    def __init__(self,checkerboardSize=19):
        self.checkerboard=np.zeros((checkerboardSize,checkerboardSize))
        self.checkerboardSize=checkerboardSize
        self.connect=7
    def step(self,identy,x,y):
        if(identy>0 and identy<4):
            if(x>=0 and y>=0 and x<self.checkerboardSize and y<self.checkerboardSize):
                if self.checkerboard[y][x]==0:
                    self.checkerboard[y][x]=identy
                    return True
                else:
                    print("在已经有子的地方落子(%d,%d)"%(x,y))
            else:
                print("坐标超限(%d,%d)"%(x,y))
        else:
            print("落子者超限(%d)"%(identy))
        return False

    def horizontalCheck(self,identy,x,y):#横向 从落子点开始检查identy是否胜利,胜利返回identy,否则返回0
        t=0
        start=max(x-self.connect+1,0)
        end=min(x+self.connect-1,self.checkerboardSize-1)
        for i in range(start,end+1):
            if self.checkerboard[y][i]==identy:
                t+=1
                if(t>=self.connect):
                    return identy
            else:
                t=0
        return 0
        

    def slantCheck(self,identy,x,y):#斜向 从落子点开始检查identy是否胜利,胜利返回identy,否则返回0
        t=0
        start=max(min(x,y)-self.connect+1,0)-min(x,y)
        end=min(max(x,y)+self.connect-1,self.checkerboardSize-1)-max(x,y)
        for i in range(start,end+1):
            if self.checkerboard[y+i][x+i]==identy:
                t+=1
                if(t>=self.connect):
                    return identy
            else:
                t=0
        return 0
    def check(self,identy,x,y):#从落子点开始检查identy是否胜利,胜利返回identy,否则返回0
        flag=self.horizontalCheck(identy,x,y)
        if flag>0:
            return flag
        flag=self.slantCheck(identy,x,y)
        if flag>0:
            return flag
        self.checkerboard=self.checkerboard.transpose()
        flag=self.horizontalCheck(identy,y,x)
        if flag>0:
            self.checkerboard=self.checkerboard.transpose()
            return flag
        self.checkerboard=self.checkerboard.transpose()
        self.checkerboard=np.flip(self.checkerboard,axis=0)
        flag=self.slantCheck(identy,x,self.checkerboardSize-y-1)
        if flag>0:
            self.checkerboard=np.flip(self.checkerboard,axis=0)
            return flag
        self.checkerboard=np.flip(self.checkerboard,axis=0)
        return 0

    def draw(self):
        for y in range(self.checkerboardSize):
            for x in range(self.checkerboardSize):
                print("%d"%(self.checkerboard[y][x]),end='')
            print("\r\n",end='')

    def read(self):
        return self.checkerboard.copy()

        





                   
if __name__ == '__main__':
    a=connect7()
    while True:
        #identy,y,x=input("请输入identy,y,x.逗号分隔")
        identy=int(input("请输入identy"))
        x=int(input("请输入x"))
        y=int(input("请输入y"))
        a.step(identy,x,y)
        a.draw()
        flag=a.check(identy,x,y)
        if(flag>0):
            print(flag)
