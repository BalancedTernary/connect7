import math
import numpy as np
import os
from connect7 import connect7
import wx
import threading
from Robot import Robot


#七子棋,三人游戏,每次下两子.最先下的人第一次下一子,最后下的人第一次下三子.
#右键单击使用机器人下一子
class GUI(wx.Frame):
    def __init__(self,parent,size = (480, 480),checkerboardSize=19): 
        super(GUI, self).__init__(parent, title = "轮玩家一走:红色",size = size)
        self.checkerboardSize=checkerboardSize
        self.connect=connect7(checkerboardSize)
        self.identy=1
        self.titles={1:"轮玩家一走:红色",2:"轮玩家二走:黄色",3:"轮玩家三走:蓝色",4:"玩家一获胜",5:"玩家二获胜",6:"玩家三获胜",7:"平局"}
        self.colors={1:wx.Colour(191,31,0,255),2:wx.Colour(255,223,0,255),3:wx.Colour(0,191,223,255)}
        self.identyList=[1,2,2,3,3,3]
        self.time=1
        self.mainGrid=wx.FlexGridSizer(rows=checkerboardSize,cols=checkerboardSize,vgap=0,hgap=0)
        for i in range(checkerboardSize):
            self.mainGrid.AddGrowableRow(i)
            self.mainGrid.AddGrowableCol(i)
        self.mainPanel=wx.Panel(self)
        self.buttons=[]
        for i in range(checkerboardSize*checkerboardSize):
            button=wx.Button(self.mainPanel,id=i,size=(0,0))
            self.buttons.append(button)
            self.mainGrid.Add(button,flag=wx.EXPAND)
            self.Bind(wx.EVT_BUTTON, self.onClick, button) 
            self.Bind(wx.EVT_CONTEXT_MENU, self.onRight, button)
        self.mainPanel.SetSizer(self.mainGrid)
        self.Show(True)
        self.mainGrid.Layout()
        self.Refresh()
        
    def clear(self):
        self.identy=1
        self.time=1
        for button in self.buttons:
            button.BackgroundColour=wx.Colour(240,240,240,255)
        for y in range(self.checkerboardSize):
            for x in range(self.checkerboardSize):
                self.connect.checkerboard[y][x]=0

    def chess(self,x,y):
        if self.time>self.checkerboardSize*self.checkerboardSize:
            return self.identy
        if self.connect.step(self.identy,x,y):
            self.buttons[y*self.checkerboardSize+x].BackgroundColour=self.colors[self.identy]
            flag=self.connect.check(self.identy,x,y)
            if(flag>0):
                self.SetTitle(self.titles[3+self.identy])
                self.time=self.checkerboardSize*self.checkerboardSize+1
                return self.identy #identy胜利
            if self.time==self.checkerboardSize*self.checkerboardSize:
                self.SetTitle(self.titles[7])
                self.identy=-1
                return self.identy #平局
            self.time+=1
            if self.time<7:
                self.identy=self.identyList[self.time-1]
            else:
                self.identy=((self.time-1)%6)//2+1
            self.SetTitle(self.titles[self.identy])
            return 0 #游戏正常进行
        else:
            return -2 #落子非法

    def onClick(self,e):
        self.chess(e.Id%self.checkerboardSize,e.Id//self.checkerboardSize)
      
    def onRight(self,e):
        robot=Robot(checkerboardSize=self.checkerboardSize,connect=self.connect.connect,players=3)
        x,y=robot.step(self.connect.read(),self.identy)
        self.chess(x,y)
     
class GUIThread (threading.Thread):
    def __init__(self,checkerboardSize=19):
        threading.Thread.__init__(self)
        self.checkerboardSize=checkerboardSize
        self.lock = threading.Lock()
        self.lock.acquire()
    def run(self):
        self.app = wx.App()
        self.frm = GUI(None,checkerboardSize=self.checkerboardSize)
        self.frm.Show()
        self.lock.release()
        self.app.MainLoop()
    
            
        

        
if __name__ == '__main__':
    thread = GUIThread()
    thread.start()
    thread.lock.acquire()
    thread.join()    
