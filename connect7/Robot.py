import math
import numpy as np
import os
#七子棋,三人游戏,每次下两子.最先下的人第一次下一子,最后下的人第一次下三子.
class Robot():
    def __init__(self,checkerboardSize=19,connect=7,players=3):
        self.checkerboardSize=checkerboardSize
        self.connect=connect
        self.players=players
    def step(self,checkerboard,identy):
        outX=self.checkerboardSize//2
        outY=self.checkerboardSize//2
        maxScore=0
        for y in range(self.checkerboardSize):
            for x in range(self.checkerboardSize):
                if(checkerboard[y][x]==0):
                    score=self.accumulatedScore(checkerboard,(identy-1)%self.players+1,x,y)
                    a=self.accumulatedScore(checkerboard,(identy)%self.players+1,x,y)
                    b=self.accumulatedScore(checkerboard,(identy+1)%self.players+1,x,y)
                    score+=a
                    if score>maxScore:
                        maxScore=score
                        outX=x
                        outY=y
        return outX,outY


    def horizontalAccumulatedScore(self,checkerboard,identy,x,y):#横向 从落子点开始检查identy落子在(x,y)点的预计得分
        maxScore=0
        sumScore=0
        for dx in range(-self.connect//2,self.connect//2+1):
            t=1
            start=max((x+dx)-self.connect//2,0)
            end=min((x+dx)+self.connect//2,self.checkerboardSize-1)
            for i in range(start,end+1):
                if checkerboard[y][i]==identy:
                    t+=1
                elif checkerboard[y][i]==0:
                    pass
                else:
                    t=0
                    break

            score=math.ceil(self.checkerboardSize/2)*math.floor(5**(t-2))
            if t==0:
                score=0
            d=max(score/math.ceil(self.checkerboardSize/2),1)
            score=score+d*((self.checkerboardSize//2)-(abs((x+dx)-(self.checkerboardSize//2))+abs(y-(self.checkerboardSize//2)))/2)
            if score>maxScore:
                maxScore=score
            sumScore+=score
        return maxScore
        

    def slantAccumulatedScore(self,checkerboard,identy,x,y):#斜向 从落子点开始检查identy落子在(x,y)点的预计得分
        maxScore=0
        sumScore=0
        for dxy in range(-self.connect//2,self.connect//2+1):
            t=1
            start=max((min(x,y)+dxy)-self.connect//2,0)-(min(x,y)+dxy)
            end=min((max(x,y)+dxy)+self.connect//2,self.checkerboardSize-1)-(max(x,y)+dxy)
            for i in range(start,end+1):
                if checkerboard[y+i+dxy][x+i+dxy]==identy:
                    t+=1
                elif checkerboard[y+i+dxy][x+i+dxy]==0:
                    pass
                else:
                    t=0
                    break
            score=math.ceil(self.checkerboardSize/2)*math.floor(5**(t-2))
            if t==0:
                score=0
            d=max(score/math.ceil(self.checkerboardSize/2),1)
            score=score+d*((self.checkerboardSize//2)-(abs((x+dxy)-(self.checkerboardSize//2))+abs((y+dxy)-(self.checkerboardSize//2)))/2)
            if score>maxScore:
                maxScore=score
            sumScore+=score
        return maxScore


    def accumulatedScore(self,checkerboard,identy,x,y):#从落子点开始检查identy是否胜利,胜利返回identy,否则返回0
        score=0
        score+=self.horizontalAccumulatedScore(checkerboard,identy,x,y)
        score+=self.slantAccumulatedScore(checkerboard,identy,x,y)
        checkerboard=checkerboard.transpose()
        score+self.horizontalAccumulatedScore(checkerboard,identy,y,x)
        checkerboard=checkerboard.transpose()
        checkerboard=np.flip(checkerboard,axis=0)
        score+=self.slantAccumulatedScore(checkerboard,identy,x,self.checkerboardSize-y-1)
        checkerboard=np.flip(checkerboard,axis=0)
        return score
    

        





            