import os 
import time
import cv2
import numpy as np 
outside=[]  
side=[]
output=[]
kernel_15=np.ones((13,13),np.uint8)
#邻接表
class Node:
    def __init__(self,vex=None,x=None,y=None):
        self.vex=vex
        self.next=None
        self.x=x
        self.y=y
class Graph:
    def __init__(self):
        self.graph=[]
        self.acount=0
    def use_vex_findNode(self,vex):
        for node in self.graph:
            if node.vex==vex:
                return node
    def creat_graph(self,side):
        #side_num=len(side)
        for arc in side:
            p1=arc[0]#得到边的一端
            p2=arc[1]
            arc_side1=Node(p2)
            screen_bgr_node=self.use_vex_findNode(p1)#得到目标结点
            while screen_bgr_node.next:
                screen_bgr_node=screen_bgr_node.next
            screen_bgr_node.next=arc_side1
            #无向图
            arc_side2=Node(p1)
            screen_bgr_node=self.use_vex_findNode(p2)#得到目标结点
            while screen_bgr_node.next:
                screen_bgr_node=screen_bgr_node.next
            screen_bgr_node.next=arc_side2

    def test_print(self,vex):
        screen_bgr_node=self.use_vex_findNode(vex)
        print("[")
        while screen_bgr_node:
            print(screen_bgr_node.vex)
            screen_bgr_node=screen_bgr_node.next
        print("]")
    def dfs(self,sscreen_bgrt,visit):
        visit[sscreen_bgrt]=1
        node=self.use_vex_findNode(sscreen_bgrt)
        output.append(node.vex)
        self.acount=self.acount+1
        node=node.next        
        while node:
            if visit[node.vex]==0:
                self.dfs(node.vex,visit)
            node=node.next
            if node==None and self.acount!=len(visit)-1:
                pop_vex=output.pop()
                visit[pop_vex]=0#恢复none的节点
                self.acount=self.acount-1
os.system("adb shell screencap -p /sdcard/game.png")
time.sleep(2)
os.system("adb pull /sdcard/game.png")
time.sleep(1)
os.system("adb shell rm /sdcard/game.png")
screen_bgr=cv2.imread("C:/Users/shuiyihang/game.png")
screen_hsv=cv2.cvtColor(screen_bgr,cv2.COLOR_BGR2HSV)

low_gray=np.array([175,40,40])
upper_gray=np.array([200,255,255])
gray_mask=cv2.inRange(screen_hsv,low_gray,upper_gray)
gray_erosion=cv2.erode(gray_mask,kernel_15,iterations=1)

cnts = cv2.findContours(gray_erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
c = max(cnts, key=cv2.contourArea)#找边界最大区域
rect = cv2.minAreaRect(c)
box = cv2.boxPoints(rect)
box=np.int0(box)
x, y, width, height = cv2.boundingRect(box)
outside.append([x,y])
cv2.rectangle(screen_bgr,(x,y),(x+width,y+height),(0,255,255),1)
#获取灰色
max_width=150
low_gray=np.array([0,0,46])
upper_gray=np.array([180,43,220])
gray_mask=cv2.inRange(screen_hsv,low_gray,upper_gray)
gray_erosion=cv2.erode(gray_mask,kernel_15,iterations=1)
cnts = cv2.findContours(gray_erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
for i in cnts:
    x, y, width, height = cv2.boundingRect(i)
    if width>max_width:
        max_width=width
    if abs(width-height)<10 and abs(width-max_width)<10:
        outside.append([x,y])
        cv2.rectangle(screen_bgr,(x,y),(x+width,y+height),(0,255,0),1)


Gmap=Graph()
#初始化顶点
cnt=1
for pt in outside:
    temp_node=Node(cnt,pt[0],pt[1])
    cv2.putText(screen_bgr, str(cnt), (pt[0],pt[1]), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1.2, (255,0,0), 2)
    cnt=cnt+1
    Gmap.graph.append(temp_node)
#获取图的边关系
data_len=len(Gmap.graph)
for pto in range(data_len):
    for pti in range(pto+1,data_len):
        if (abs(Gmap.graph[pto].x-Gmap.graph[pti].x)<250 and abs(Gmap.graph[pto].y-Gmap.graph[pti].y)<100)\
        or(abs(Gmap.graph[pto].x-Gmap.graph[pti].x)<100 and abs(Gmap.graph[pto].y-Gmap.graph[pti].y)<250):
            side.append([Gmap.graph[pto].vex,Gmap.graph[pti].vex])
#打印边关系
for i in side:
    print(i)

Gmap.creat_graph(side)

#初始化辅助数组,深度遍历
visit=[]
for i in range(len(Gmap.graph)+1):
    visit.append(0)
Gmap.dfs(1,visit)
#打印解法
print("-----------")
for i in output:
    print(i)
#adb命令从各个中心滑动
for i in range(len(output)-1):
    pos1=Gmap.use_vex_findNode(output[i])
    pos2=Gmap.use_vex_findNode(output[i+1])
    text="adb shell input swipe "+str(pos1.x+width/2)+" "+str(pos1.y+height/2)+" "+str(pos2.x+width/2)+" "+str(pos2.y+height/2)
    os.system(text)

cv2.namedWindow("image",0)
cv2.resize(screen_bgr,(1080,1920))
cv2.imshow("image",screen_bgr)
cv2.waitKey()
cv2.destroyAllWindows()

