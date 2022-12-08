# Group#: G29
# Student Names: Liam Foster and Willem Van Dam

"""
    This program implements a variety of the snake 
    game (https://en.wikipedia.org/wiki/Snake_(video_game_genre))
"""

import threading
import queue        #the thread-safe queue from Python standard library

from tkinter import Tk, Canvas, Button
import random, time

class Gui():
    """
        This class takes care of the game's graphic user interface (gui)
        creation and termination.
    """
    def __init__(self, queue, game):
        """        
            The initializer instantiates the main window and
            creates the starting icons for the snake and the prey,
            and displays the initial gamer score.
        """
        #some GUI constants
        scoreTextXLocation = 60
        scoreTextYLocation = 15
        textColour = "white"
        #instantiate and create gui
        self.root = Tk()
        self.canvas = Canvas(self.root, width = WINDOW_WIDTH,
            height = WINDOW_HEIGHT, bg = BACKGROUND_COLOUR)
        self.canvas.pack()
        #create starting game icons for snake and the prey
        self.snakeIcon = self.canvas.create_line(
            (0, 0), (0, 0), fill=ICON_COLOUR, width=SNAKE_ICON_WIDTH)
        self.preyIcon = self.canvas.create_rectangle(
            0, 0, 0, 0, fill=ICON_COLOUR, outline=ICON_COLOUR)
        #display starting score of 0
        self.score = self.canvas.create_text(
            scoreTextXLocation, scoreTextYLocation, fill=textColour,
            text='Your Score: 0', font=("Helvetica","11","bold"))
        #binding the arrow keys to be able to control the snake
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", game.whenAnArrowKeyIsPressed)

    def gameOver(self):
        """
            This method is used at the end to display a
            game over button.
        """
        gameOverButton = Button(self.canvas, text="Game Over!",
            height = 3, width = 10, font=("Helvetica","14","bold"),
            command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)
    

class QueueHandler():
    """
        This class implements the queue handler for the game.
    """
    def __init__(self, queue, gui):
        self.queue = queue
        self.gui = gui
        self.queueHandler()
    
    def queueHandler(self):
        '''
            This method handles the queue by constantly retrieving
            tasks from it and accordingly taking the corresponding
            action.
            A task could be: game_over, move, prey, score.
            Each item in the queue is a dictionary whose key is
            the task type (for example, "move") and its value is
            the corresponding task value.
            If the queue.empty exception happens, it schedules
            to call itself after a short delay.
        '''
        try:
            while True:
                task = self.queue.get_nowait()
                if "game_over" in task:
                    gui.gameOver()
                elif "move" in task:
                    points = [x for point in task["move"] for x in point]
                    gui.canvas.coords(gui.snakeIcon, *points)
                elif "prey" in task:
                    gui.canvas.coords(gui.preyIcon, *task["prey"])
                elif "score" in task:
                    gui.canvas.itemconfigure(
                        gui.score, text=f"Your Score: {task['score']}")
                self.queue.task_done()
        except queue.Empty:
            gui.root.after(100, self.queueHandler)


class Game():
    '''
        This class implements most of the game functionalities.
    '''
    def __init__(self, queue):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """
        self.queue = queue
        self.score = 0
        #starting length and location of the snake
        #note that it is a list of tuples, each being an
        # (x, y) tuple. Initially its size is 5 tuples.       
        self.snakeCoordinates = [(495, 55), (485, 55), (475, 55),
                                 (465, 55), (455, 55)]
        #initial direction of the snake
        self.direction = "Left"
        self.gameNotOver = True
        self.createNewPrey()

    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move" 
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = 0.15     #speed of snake updates (in secs)
        while self.gameNotOver:
            #complete the method implementation below
            #wait SPEED seconds and then call move
            time.sleep(SPEED)
            self.move()
            #add move task to queue
            self.queue.put({"move": self.snakeCoordinates})
            


    def whenAnArrowKeyIsPressed(self, e) -> None:
        """
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection = self.direction
        #ignore invalid keys
        if (currentDirection == "Left" and e.keysym == "Right" or
            currentDirection == "Right" and e.keysym == "Left" or
            currentDirection == "Up" and e.keysym == "Down" or
            currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym

    def move(self) -> None:
        """
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate.
            If based on this new movement, the prey has been
            captured, it adds a task to the queue for the updated
            score and also creates a new prey.
            It also calls a corresponding method to check if
            the game should be over.
            The snake coordinates list (representing its length
            and position) should be correctly updated.
        """
        NewSnakeCoordinates = self.calculateNewCoordinates()
        #complete the method implementation below

        #check if game is over
        self.isGameOver(NewSnakeCoordinates)

        #get prey coordinates
        preyCoords = gui.canvas.coords(gui.preyIcon)
        #check if new snake coordinates are in prey coordinates
        xMatch = NewSnakeCoordinates[0] in range(int(preyCoords[0]), int(preyCoords[2]))
        yMatch = NewSnakeCoordinates[1] in range(int(preyCoords[1]), int(preyCoords[3]))
        if xMatch and yMatch:
            #increment score
            self.score += 1
            #add score task to queue
            self.queue.put({"score": self.score})
            #get tail tuple and create tail direction for adding length to snake
            tail = self.snakeCoordinates[0]
            tailDirection = (tail[0]-self.snakeCoordinates[1][0], tail[1]-self.snakeCoordinates[1][1])
            #add new coordinate to end of snake 
            self.snakeCoordinates.insert(0,(tail[0] + tailDirection[0], tail[1] + tailDirection[1]))
            #call to create new prey
            self.createNewPrey()

        #remove snake tail and add new coordinates at snake head
        self.snakeCoordinates.pop(0)
        self.snakeCoordinates.append(NewSnakeCoordinates)

        

    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of
            head of the snake.
            It is used by the move() method.    
        """
        lastX, lastY = self.snakeCoordinates[-1]
        #complete the method implementation below
        #get current snake direction
        currentDirection = self.direction
        #check direction and depending on direction increase or decrease snake coordinate by 5 in either x or y
        if currentDirection == "Left":
            return (lastX-10, lastY)
        elif currentDirection == "Right":
            return (lastX+10, lastY)
        elif currentDirection == "Up":
            return (lastX, lastY-10)
        elif currentDirection == "Down":
            return (lastX, lastY+10)

    def isGameOver(self, snakeCoordinates) -> None:
        """
            This method checks if the game is over by
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver
            field and also adds a "game_over" task to the queue.
        """
        x, y = snakeCoordinates
        #complete the method implementation below
        #boolean expression for if the coordinates are out of bounds
        outOfBounds = x < 0 or x > WINDOW_WIDTH or y < 0 or y > WINDOW_HEIGHT
        #boolean expression for it the coordinates are in the snake's current coordinates
        cannibal = snakeCoordinates in self.snakeCoordinates
        #check if either boolean is true and if so end the game
        if outOfBounds or cannibal:
            #set gameNotOver to False to stop movement
            self.gameNotOver = False
            #queue game_over task in gameQueue
            self.queue.put({"game_over": True})

    def createNewPrey(self) -> None:
        """
            This methods picks an x and a y randomly as the coordinate 
            of the new prey and uses that to calculate the 
            coordinates (x - 5, y - 5, x + 5, y + 5). 
            It then adds a "prey" task to the queue with the calculated
            rectangle coordinates as its value. This is used by the 
            queue handler to represent the new prey.                    
            To make playing the game easier, set the x and y to be THRESHOLD
            away from the walls.
        """
        THRESHOLD = 15   #sets how close prey can be to borders
        #complete the method implementation below
        #generate random x and y coordinates within the threshold at increments of 10
        x = random.randrange(THRESHOLD, WINDOW_WIDTH-THRESHOLD, 10)
        y = random.randrange(THRESHOLD, WINDOW_HEIGHT-THRESHOLD, 10)
        #set prey coords as described in the given function description
        preyCoords = [x - 5, y - 5, x + 5, y + 5]
        #queue prey task in queue
        self.queue.put({"prey": preyCoords})


if __name__ == "__main__":
    #some constants for our GUI
    WINDOW_WIDTH = 500           
    WINDOW_HEIGHT = 300
    SNAKE_ICON_WIDTH = 15
    
    BACKGROUND_COLOUR = "green"   #you may change this colour if you wish
    ICON_COLOUR = "yellow"        #you may change this colour if you wish

    gameQueue = queue.Queue()     #instantiate a queue object using python's queue class

    game = Game(gameQueue)        #instantiate the game object

    gui = Gui(gameQueue, game)    #instantiate the game user interface
    
    QueueHandler(gameQueue, gui)  #instantiate our queue handler    
    
    #start a thread with the main loop of the game
    threading.Thread(target = game.superloop, daemon=True).start()

    #start the GUI's own event loop
    gui.root.mainloop()
    