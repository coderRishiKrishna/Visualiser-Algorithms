import pygame
import time
from copy import deepcopy
import random
pygame.font.init()
def random_array_gen(size):
    random_list = random.sample(range(1,700),size)
    return random_list


class Bar:
    def __init__(self,id,value,window,n,base_padding,side_padding,height_factor):
        self.id = id
        self.window = window
        self.width = None
        self.height =value
        self.top_x = None
        self.top_y = None
        self.color= (255,0,0)
        self.base_padding = base_padding
        self.side_padding = side_padding
        self.height_factor = height_factor
        self.calculate_pos(n,base_padding,side_padding)
    def calculate_pos(self,n,base_padding,side_padding):
        # gap = 1
        win_width,win_height = self.window.get_width(),self.window.get_height()
        height_factor = (win_height-base_padding)/100
        bar_width = (win_width-2*side_padding)/n
        self.width = bar_width

    def draw(self):
        curr_height = self.height
        self.top_x = self.side_padding+self.id*self.width
        self.top_y = self.window.get_height()-self.base_padding-curr_height
        pygame.draw.rect(self.window,self.color,(self.top_x,self.top_y,self.width-1,curr_height))


        
    



class Algo:
    def __init__(self,window,size):
        self.size = size
        self.curr=None
        self.array = random_array_gen(size)
        self.window = window
        win_width,win_height = self.window.get_width(),self.window.get_height()
        base_padding = 20
        side_padding = 20
        height_factor = (win_height-base_padding)/100
        bar_width = (win_width-2*side_padding)/self.size
        self.bars = [Bar(i,self.array[i],window,self.size,base_padding,side_padding,height_factor) for i in range(size)]

        
    def bubble(self):
        n = len(self.array)
        for i in range(n):
            swapped = False
            for j in range(0,n-i-1):
                if self.array[j]>self.array[j+1]:
                    self.array[j],self.array[j+1] = self.array[j+1],self.array[j]
                    self.update_bars()
                    self.bars[j].color = (0,0,255)  #This is the element which will be placed to its final position in the current Ith iteration
                    self.update_window()
                    pygame.display.update()
                    pygame.time.delay(10)
                    swapped = True
                else:
                    self.bars[j+1].color = (0,0,255)
                    self.update_window()
                    pygame.display.update()
                    pygame.time.delay(10)
                self.bars[j].color = (255,0,0)
                self.bars[j+1].color = (255,0,0)
                self.update_bars()
                self.update_window()
                pygame.display.update()
                # pygame.time.delay(0)

            if not swapped:
                break

    def partition(self,low,high): 
        i = ( low-1 )         # index of smaller element 
        pivot = self.array[high]     # pivot 
        for j in range(low,high):
            self.bars[j].color = (0,0,255)
        self.bars[high].color = (0,255,0)       #pivot is represented in green color
        self.update_window()
        pygame.display.update()
        pygame.time.delay(20)

    
        for j in range(low , high): 

            if   self.array[j] < pivot: 

                i = i+1
                self.bars[i].color = (0,0,0)
                self.bars[j].color = (0,0,0)       # These two are the element sbeing swapped (represented using black color)
                self.array[i],self.array[j] = self.array[j],self.array[i]
                
                self.update_bars()
                self.update_window()
                pygame.display.update()
                pygame.time.delay(60)
                self.bars[i].color = (0,0,255)
                self.bars[j].color = (0,0,255)
            self.update_bars()
            self.update_window()
            pygame.display.update()
            pygame.time.delay(10)
        for j in range(low,high):
            self.bars[j].color = (255,0,0)
        self.array[i+1],self.array[high] = self.array[high],self.array[i+1] 
        self.update_bars()
        self.bars[high].color = (255,0,0)
        return ( i+1 ) 
    

    def quickSort(self,low,high): 
        if low < high: 
            pi = self.partition(low,high)
            self.quickSort( low, pi-1) 
            self.quickSort( pi+1, high)
    def quick(self):
        self.quickSort(0,len(self.array)-1)
        # print(self.array)




    def merge(self,low,mid,high):
        l1,l2 =[],[]
        n1 = mid - low + 1
        n2 = high - mid

        for i in range(0,n1):
            l1.append(self.array[low+i])
            self.bars[low+i].color = (0,255,0)      #the left subarray is represented in green
        for j in range(0,n2):
            l2.append(self.array[mid+1+j])
            self.bars[mid+1+j].color = (0,0,255)     # The right subarray is represented in blue
        i,j,k = 0,0,low
        self.update_bars()
        self.update_window()
        pygame.display.update()
        pygame.time.delay(500)
        while(i<n1 and j < n2):
            if l1[i] < l2[j]:
                self.array[k] = l1[i]
                self.bars[k].color = (255,0,0)      # at the time of merging the left and right part change their colour back to red
                i+=1
                k+=1
            else:
                self.array[k] = l2[j]
                self.bars[k].color = (255,0,0)   # at the time of merging the left and right part change their colour back to red
                j+=1
                k+=1


        while(i<n1):
            self.array[k] = l1[i]
            self.bars[k].color = (255,0,0)   # at the time of merging the left and right part change their colour back to red
            i+=1
            k+=1
        while(j<n2):
            self.array[k] = l2[j]
            self.bars[k].color = (255,0,0)   # at the time of merging the left and right part change their colour back to red

            j+=1
            k+=1
        self.update_bars()
        self.update_window()
        pygame.display.update()
        pygame.time.delay(50)
        return 


    def mergesort(self,low,high):
        if low < high:
            mid = (low + high)//2
            self.mergesort(low,mid)
            self.mergesort(mid+1,high)
            pygame.time.delay(1)
            self.merge(low,mid,high)
        return 

    def insertion_sort(self):
        for i in range(len(self.array)):
            current = self.array[i]
            j = i-1
            while(j>=0 and self.array[j]>current):
                self.array[j+1],self.array[j] = self.array[j],self.array[j+1]
                
                j-=1
                self.bars[j+1].color =(0,0,255)     # This (Blue bar) is the current element which is being placed to its position in sorted part of the array 
                self.update_bars()
                self.update_window()
                pygame.display.update()
                pygame.time.delay(10)
                self.bars[j+1].color =(0,255,0)     # this element is present in the sorted part hence make it green
            self.array[j+1] = current
            self.bars[i].color =(0,255,0) 
            self.update_bars()
            self.update_window()
            pygame.display.update()
            pygame.time.delay(20)
            # self.bars[j+1].color =(0,0,0)
        # return self.array


    def draw_bars(self,p = False):
        for i in range(self.size):
            bar= self.bars[i]
            bar.draw()

    def update_window(self):
        self.window.fill((255,255,255))
        self.draw_bars()
    def update_bars(self):
        for i in range(self.size):
            self.bars[i].height = self.array[i]

    




def main():
    win_width,win_height = 1000,800
    window = pygame.display.set_mode((win_width,win_height))
    pygame.display.set_caption("Bubble Sort")
    run = True
    size = 50
    key = None
    algo= Algo(window,size)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    key = "bubble" #start the bubble sort process
                    algo.bubble()
                    key = None
                if event.key == pygame.K_q:
                    key = "quick"
                    algo.quick()
                    key = None
                if event.key == pygame.K_m:
                    key = "Merge"
                    algo.mergesort(0,len(algo.array)-1)
                    # print(algo.array)
                if event.key == pygame.K_i:
                    key = "insertion sort"
                    algo.insertion_sort()
                if event.key == pygame.K_h:
                    key = "stop"  #Halt the  process....This has yet not been implemented at the time of code upload
                if event.key == pygame.K_DELETE:
                    key = "reset"
                    # temp = deepcopy(array)
                    pass
                if event.key == pygame.K_r:
                    key = "random_array"
                    # temp = random_array_gen(30)
        # print(key)
        algo.update_window()
        # print("outside update_function")
        pygame.display.update()
    # print(temp)
main()

