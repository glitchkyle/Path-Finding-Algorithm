import pygame

WIDTH = 800
HEIGHT = 800
GRID_SIZE = 50
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Algorithm(object):
    def __init__(self, grid):
        self.running = False # Boolean for if program is currently running
        self.gridObject = grid # Array for all existing nodes in the program
        self.openList = [] # Nodes that are ready to be searched
        self.closedList = [] # Nodes that have been searched
        self.nodeStart = None # Starting node
        self.nodeEnd = None # End node

    def FindPath(self):
        self.running = True
        self.openList = []
        self.closedList = []
        if self.nodeStart != None:
            self.openList.append(self.nodeStart)
            while len(self.openList) > 0:
                self.gridObject.window.fill(WHITE)

                for node in self.openList:
                    if node == self.nodeStart or node == self.nodeEnd:
                        continue
                    node.changeNode(GREEN)
                for node in self.closedList:
                    if node == self.nodeStart or node == self.nodeEnd:
                        continue
                    node.changeNode(RED)
                

                # Finding cheapest F cost node
                currentNode = self.findCheapestNode()

                if currentNode == self.nodeEnd:
                    self.nodeEnd.parent = currentNode.parent
                    break

                self.openList.remove(currentNode)
                self.closedList.append(currentNode)

                # Get Neighbors

                # Get index of current node in grid 
                x, y = self.findNodeIndex(currentNode)
            
                # Top Center
                if (x - 1 >= 0 and x - 1 < self.gridObject.totalRows) and (y >= 0 and y < self.gridObject.totalColumns):
                    self.addSearchNode(self.gridObject.grid[x - 1][y], currentNode, 10)

                # Middle Left
                if (x >= 0 and x < self.gridObject.totalRows) and (y - 1 >= 0 and y - 1 < self.gridObject.totalColumns):
                    self.addSearchNode(self.gridObject.grid[x][y - 1], currentNode, 10)

                # Middle Right
                if (x >= 0 and x < self.gridObject.totalRows) and (y + 1 >= 0 and y + 1 < self.gridObject.totalColumns):
                    self.addSearchNode(self.gridObject.grid[x][y + 1], currentNode, 10)

                # Bottom Center
                if (x + 1 >= 0 and x + 1 < self.gridObject.totalRows) and (y >= 0 and y < self.gridObject.totalColumns):
                    self.addSearchNode(self.gridObject.grid[x + 1][y], currentNode, 10)
                
                self.gridObject.drawGrid()
                
                pygame.display.update()
            
            # Recursively go back to start if target node found
            if self.nodeEnd.parent != None:
                currentNode = self.nodeEnd.parent
                while currentNode is not self.nodeStart:
                    currentNode.changeNode(PURPLE)
                    currentNode = currentNode.parent
            
            self.running = False


    def addSearchNode(self, searchNode, currentNode, cost):
        if searchNode.wall != True and searchNode not in self.closedList:
            if currentNode != searchNode.parent:
                searchNode.parent = currentNode
            searchNode.calculateGCost(currentNode, cost)
            searchNode.calculateHCost(self.nodeEnd)
            searchNode.calculateFCost()
            if searchNode not in self.openList and searchNode not in self.closedList:
                self.openList.append(searchNode) 
    
    def findCheapestNode(self):
        searchNode = self.openList[0]
        for node in self.openList:
            if node.f == searchNode.f:
                if node.g < searchNode.g:
                    searchNode = node
            elif node.f < searchNode.f:
                searchNode = node
        return searchNode

    def findNodeIndex(self, searchNode):
        x, y = 0, 0
        for row in self.gridObject.grid:
            for node in row:
                if node == searchNode:
                    return x, y
                y += 1
            x += 1
            y = 0
        

class Node(object):
    def __init__(self, position=None, wall=False, color=GREY):
        self.parent = None # Parent Node 
        self.position = position # X and Y values
        self.g = 1000 # Distance between start and current nodes
        self.h = 1000 # Distance between end and current nodes
        self.f = self.g + self.h # Total cost of node
        self.wall = wall # Boolean for value

        # Visualization Tool Variables
        self.color = color # Node color for visualization tool
        self.unique = False # Boolean for if node is either a wall, start, or end node
    
    def calculateGCost(self, parentNode, moveCost=10):
        self.g = parentNode.g + moveCost

    def calculateHCost(self, endNode):
        self.h = abs(endNode.position[0] - self.position[0]) + abs(endNode.position[1] - self.position[1])

    def calculateFCost(self):
        self.f = self.g + self.h

    def resetNode(self):
        self.g = 1000
        self.h = 1000
        self.f = self.g + self.h
        self.color = GREY
        self.wall = False

    def changeNode(self, color):
        self.color = color
        if self.color == BLACK:
            self.wall = True
        else:
            self.wall = False

class Grid(object):
    def __init__(self, window, width, height, totalRows=50):
        self.grid = [] # 2D array which stores all nodes
        self.window = window # Surface for pygame
        self.width = width # Width of screen
        self.height = height # Height of screen
        self.totalRows = totalRows # Number of rows on grid
        self.totalColumns = totalRows # Number of columns on grid
        self.gap = width // totalRows # Size of nodes

    # Instantiate nodes for grid
    def createGrid(self):
        for row in range(self.totalRows):
            tempRowArray = []
            for column in range(self.totalColumns):
                newNode = Node((row * self.gap, column * self.gap), False, GREY)
                tempRowArray.append(newNode)
            self.grid.append(tempRowArray)

    # Draw the grid through pygame
    def drawGrid(self):
        for row in self.grid:
            for node in row:
                newRect = (node.position[0], node.position[1], self.gap, self.gap)
                if node.color == GREY:
                    pygame.draw.rect(self.window, node.color, newRect, 1)
                else:
                    pygame.draw.rect(self.window, node.color, newRect)

    # Reset the grid
    def resetGrid(self):
        for row in self.grid:
            for node in row:
                node.resetNode()

    # Retrieves the node corresponding to the mouse position
    def getMousePosNode(self, mousePosition):
        return self.grid[mousePosition[0] // self.gap][mousePosition[1] // self.gap]
    
    def changeGridNode(self, node, color):
        node.changeNode(color)
            
def main():
    running = True

    grid = Grid(WIN, WIDTH, HEIGHT, GRID_SIZE)
    grid.createGrid()
    pathAlgorithm = Algorithm(grid)

    while running:
        WIN.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    

            if pathAlgorithm.running == False:
                # If user pressed left mouse button
                if pygame.mouse.get_pressed()[0]:
                    mousePosX, mousePosY = pygame.mouse.get_pos()
                    node = grid.getMousePosNode((mousePosX, mousePosY))
                    # If node is empty
                    if node.unique == False:
                        # If start node does not exist, make this node the start node
                        if pathAlgorithm.nodeStart == None:
                            node.unique = True
                            pathAlgorithm.nodeStart = node
                            pathAlgorithm.nodeStart.g = 0
                            grid.changeGridNode(node, YELLOW)
                        # If end nodes does  not exist, make this node the end node
                        elif pathAlgorithm.nodeEnd == None:
                            node.unique = True
                            pathAlgorithm.nodeEnd = node
                            pathAlgorithm.nodeStart.h = pathAlgorithm.nodeStart.calculateHCost(pathAlgorithm.nodeEnd)
                            grid.changeGridNode(node, TURQUOISE)
                        else:
                            node.unique = True
                            grid.changeGridNode(node, BLACK)
                
                # If user pressed right mouse button, reset the node
                if pygame.mouse.get_pressed()[2]:
                    mousePosX, mousePosY = pygame.mouse.get_pos()
                    node = grid.getMousePosNode((mousePosX, mousePosY))
                    node.unique = False
                    if node == pathAlgorithm.nodeStart:
                        pathAlgorithm.nodeStart = None
                    elif node == pathAlgorithm.nodeEnd:
                        pathAlgorithm.nodeEnd = None
                    grid.changeGridNode(node, GREY)

                # If user pressed space, run the algorithm
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if pathAlgorithm.nodeStart != None and pathAlgorithm.nodeEnd != None:
                            pathAlgorithm.FindPath()
        
        grid.drawGrid()
        pygame.display.update()
    pygame.quit()

main()