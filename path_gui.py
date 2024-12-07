import pygame 
import time
from copy import deepcopy
pygame.font.init()
import sys 
sys.setrecursionlimit(20000)
import heapq



class Algo:
    def __init__(self):
        self.visited = set()
        self.path = []
    def neighbours2(self,board,node):
        rows = board.rows
        cols = board.cols
        pos = node
        i,j = pos[0],pos[1]
        for x in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
            if x[0]<0 or x[1]>=rows or x[1]<0 or x[0]>=cols:
                continue
            if not board.cells[x[0]][x[1]].wall :
                yield x

    def neighbours(self,board,node):
        rows = board.rows
        cols = board.cols
        pos = node
        for i in range(max(0, pos[0] - 1), min(rows, pos[0] + 2)):
            for j in range(max(0, pos[1] - 1), min(cols, pos[1] + 2)):
                if (i, j) != pos and not board.cells[i][j].wall :

                    yield (i,j)

    def dfs(self,board,start,path):
        if start in self.visited:
            return None
        if board.cells[start[0]][start[1]].end == True:
            return path+[start]
        board.cells[start[0]][start[1]].color = (150,150,150)
        window_update(board.window,board)
        pygame.time.delay(5)
        pygame.display.update()
        self.visited.add(start)
        for neighbour in self.neighbours2(board,start):
            a = self.dfs(board,neighbour,path+[start])
            if a:
                return a
        return None


    def bfs(self,board,start):
        queue = [start]
        prev = None
        parent = dict()
        parent[start] = None
        while queue:
            node  = queue.pop(0)
            if node not in self.visited:
                self.visited.add(node)
                for next_node in self.neighbours2(board,node):
                    board.cells[next_node[0]][next_node[1]].color = (150,150,150)
                    window_update(board.window,board)
                    # pygame.time.delay(1)
                    pygame.display.update()
                    if next_node not in self.visited:
                        if next_node not in parent:                                
                            parent[next_node] = node 
                            if board.cells[next_node[0]][next_node[1]].end == True:
                                return parent

                        queue.append(next_node)
        return None

    def hueristic(self,start,end):
        return abs(start[0]-end[0])+abs(start[1]-end[1])

    def A_star(self,board):
        start = board.start
        end = board.end
        open_set = set()
        queue = []
        heapq.heapify(queue)
        heapq.heappush(queue,(0,start))
        g_cost = {start:0}
        f_cost = dict()
        parent = {start:None}

        while queue:
            total_cost,node = heapq.heappop(queue)
            self.visited.add(node)
            if node == end:
                return parent
            for child in self.neighbours(board,node):
                if child in self.visited:
                    continue
                board.cells[child[0]][child[1]].color = (150,150,150)
                window_update(board.window,board)
                pygame.time.delay(5)
                pygame.display.update()
                g_cost[child] = g_cost[node]+1
                hue = self.hueristic(child,end)
                cost = g_cost[child]+hue
                if child in f_cost:
                    if f_cost[child] > cost:
                        f_cost[child] = cost
                        parent[child] = node
                        heapq.heappush(queue,(cost,child))
                else:
                    f_cost[child] = cost
                    parent[child] = node
                    heapq.heappush(queue,(cost,child))
                
        return parent
        



    def solve(self,key,board):
        path = []
        if key == "dfs":
            path = self.dfs(board,board.start,path)
        elif key == "bfs":
            parent  = self.bfs(board,board.start)
            if not parent:
                return
            end = board.end
            while end:
                path.append(end)
                end = parent[end]
            path = path[::-1]
        
        elif key == "a_star":
            parent = self.A_star(board)
            if board.end in parent:
                end = board.end
                while end:
                    path.append(end)
                    end = parent[end]
                path = path[::-1]
        if not path:
            return 
        for pos in path:
            cell = board.cells[pos[0]][pos[1]]
            cell.in_path = True

    def reset(self):
        self.path = []
        self.visited = set()

        




class Cell:
    def __init__(self,window,x,y,rows,cols,width,height):
        self.window = window
        self.x = x
        self.y = y
        self.id = None
        self.height =height
        self.width = width
        self.color = None
        self.pos_in_grid = None
        self.calculate_pos(rows,cols)
        self.wall = False
        self.start = False
        self.end = False
        self.in_path = False



    def calculate_pos(self,rows,cols):
        x_coordinate  = 0+self.x*self.width
        y_cordinate = 0+self.y*self.height
        self.pos_in_grid = (x_coordinate,y_cordinate)
    
    def draw(self):
        x,y = self.pos_in_grid
        if self.start:
            pygame.draw.rect(self.window,(0,0,255),(x,y,self.width,self.height))

        elif self.wall:
            pygame.draw.rect(self.window,(0,0,0),(x,y,self.width,self.height))
        elif self.end:
            pygame.draw.rect(self.window,(255,0,0),(x,y,self.width,self.height))

        # elif self.color:
        elif self.in_path:
            pygame.draw.circle(self.window,(0,255,0),(x+self.width//2,y+self.height//2),(self.height//2))

        elif self.color:
            pygame.draw.circle(self.window,self.color,(x+self.width//2,y+self.height//2),(self.height//2)-2)

        else:
            return








class Grid:
    def __init__(self,rows,cols,window):
        self.rows = rows
        self.cols = cols
        self.window = window
        self.cells = [[None for i in range(cols)]for j in range(rows)]
        self.cell_width = None
        self.cell_height = None
        self.calculate_cell_data()
        self.start = (self.rows//2,self.cols//2)
        self.end = (self.rows//4,self.cols//4)
        self.cells[self.start[0]][self.start[1]].start = True
        self.cells[self.end[0]][self.end[1]].end = True
        # self.path = []

    def reset(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.cells[i][j]
                cell.color = None
                # cell.pos_in_grid = None
                # cell.calculate_pos(rows,cols)
                cell.wall = False
                cell.start = False
                cell.end = False
                cell.in_path = False
                        
        self.start = (self.rows//2,self.cols//2)
        self.end = (self.rows//4,self.cols//4)
        self.cells[self.start[0]][self.start[1]].start = True
        self.cells[self.end[0]][self.end[1]].end = True


    def calculate_cell_data(self):

        win_width = self.window.get_width()
        win_height = self.window.get_height()
        width = win_width//self.cols
        height = win_height//self.rows
        self.cell_width = width
        self.cell_height = height
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j] = Cell(self.window,i,j,self.rows,self.cols,width,height)
           
    def get_cell(self,pos):
        x,y = pos[0],pos[1]
        i = x//self.cell_width
        j = y//self. cell_height
        return (i,j)
    
    def select(self,pos):
        i,j = pos

        if self.cells[i][j].start or self.cells[i][j].end:
            return 
        else:
            self.cells[i][j].wall = True
        # print(i,j,"--")

    def draw(self):
        cell_width = self.cell_width
        cell_height = self.cell_height
        #drawing vertical lines
        for i in range(self.cols-1):
            x1 = (i+1)*cell_width
            y1 = 0
            x2 = x1
            thick  =1
            y2 = self.window.get_height()
            pygame.draw.line(self.window, (0,0,0), (x1,y1), (x2,y2), thick)

        #drawing horizontal lines
        for i in range(self.rows-1):
            x1 = 0  
            y1 = (i+1)*cell_height
            x2 = self.window.get_width()
            y2 = y1
            thick =1
            pygame.draw.line(self.window, (0,0,0), (x1,y1), (x2,y2), thick)

        for i in range(len(self.cells)):
            for j in range(len(self.cells[0])):
                self.cells[i][j].draw()

    #     return 
    # def solve(self,key):
    #     pass


def window_update(window,board):
    window.fill((255,255,255))
    board.draw()
    pass


def main():
    win_width,win_height = 800,800
    window = pygame.display.set_mode((win_width,win_height))
    pygame.display.set_caption("Path Finder Visualistation")
    run = True
    key = None
    build_wall = False
    drag_start = False
    drag_end = False
    board = Grid(40,40,window)
    algo  = Algo()
    while run:
        pressed = pygame.key.get_pressed()
        
        # alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # print(event.key,"--")
                if event.key == pygame.K_DELETE:
                    board.reset()
                    algo.reset()
                if event.key == pygame.K_d:
                    key = "dfs"
                    algo.solve(key,board)
                if event.key == pygame.K_b:
                    key = "bfs"
                    algo.solve(key,board)
                if event.key == pygame.K_a:
                    key = "a_star"
                    algo.solve(key,board)
                if event.key == pygame.K_RETURN:
                    print(key,"--")
                    
                    key = None
            # print(event.type,"---",pygame.MOUSEMOTION)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                cell_pos = board.get_cell(pos)

                if cell_pos == board.start or cell_pos == board.end:
                    build_wall = False
                    if ctrl_held and cell_pos == board.start:
                        drag_start = True
                    if ctrl_held and cell_pos == board.end:
                        drag_end = True
                else:
                    build_wall = True
                board.select(cell_pos)

            if event.type == pygame.MOUSEBUTTONUP:
                build_wall = False
                drag_end = False
                drag_start = False
                cell_pos = board.get_cell(pos)
                board.select(cell_pos)
            if event.type == pygame.MOUSEMOTION :
                if build_wall ==True:
                    pos = pygame.mouse.get_pos()
                    cell_pos = board.get_cell(pos)
                    board.select(cell_pos)
                if drag_start == True:
                    pos = pygame.mouse.get_pos()
                    cell_pos = board.get_cell(pos)
                    if cell_pos == board.end or board.cells[cell_pos[0]][cell_pos[1]].wall == True:
                        continue
                    else:

                        prev_start = board.start
                        board.cells[prev_start[0]][prev_start[1]].start = False
                        board.cells[cell_pos[0]][cell_pos[1]].start = True
                        board.start = cell_pos
                
                if drag_end == True:
                    pos = pygame.mouse.get_pos()
                    cell_pos = board.get_cell(pos)
                    if cell_pos == board.start or board.cells[cell_pos[0]][cell_pos[1]].wall == True:
                        continue
                    else:

                        prev_end = board.end
                        board.cells[prev_end[0]][prev_end[1]].end = False
                        board.cells[cell_pos[0]][cell_pos[1]].end = True
                        board.end = cell_pos


        window_update(window,board)
        pygame.display.update()
main()