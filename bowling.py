import tkinter
import sys
import re

"""bowling.py

A Python program for keeping track of a bowling game score. This program
dynamically updates the scores.

Requires - Python 3.0+
Author - Carr, Crecen
Date - 09222022
"""
class Bowling:

    """The Bowling class sets up the Graphical User Interface (GUI). It also
    sets up the filler text and default variables.
    """
    def __init__(self):

        # Holds a list of Input Entry Widgets
        self.entryList = []
        # Holds the values of the Final Score Labels
        self.finalList = []

        # This holds the entry values of the frame in the list as numbers
        self.frameValues = []
        # This combines the total values of each group of frames
        self.frameTotal = []
        # This holds the final total of each group of frames totaled up
        self.frameFinal = []

        # Default Text Variables
        self.titleText = "Bowling Score Game"
        self.resetText = "Reset"
        self.exitText = "Exit"
        self.validateText = "key"
        self.normalColor = "white"
        self.errorColor = "yellow"

        # Starts up the graphical user interface
        self.displayWindow()

    """This sets up the entire graphical user interface with all the
    frames, labels, and entries.
    """
    def displayWindow(self):
        # Sets up a tkinter window with a background frame
        self.root = tkinter.Tk()
        self.frame = tkinter.Frame(self.root)

        # This allows entries to validate text as it is being typed
        # %d = The type of action (1=insert, 0=delete)
        # %i = index of char string to be inserted
        # %P = Value of entry if editing is allowed
        self.vcmd = (self.frame.register(self.onValidate), '%d', '%i', '%P')

        # Sets up the title of the application window
        self.root.title(self.titleText)

        # This sets up all the normal frames and the last long frame
        for i in range(9):
            self.normalFrame(i)
        self.longFrame()

        # This sets up the reset button functionality
        self.resetButton = tkinter.Button(self.frame, text=self.resetText,
                                            command=self.resetFrame)
        self.resetButton.grid(row=5, column=0)

        # This sets up the exit button functionality
        self.exitButton = tkinter.Button(self.frame, text=self.exitText,
                                            command=self.exitFrame)
        self.exitButton.grid(row=5, column=len(self.entryList)-1)
        # This allows you to exit by pressing the Application Red Close Button
        self.root.protocol('WM_DELETE_WINDOW', self.exitFrame)
        # This allows you to exit the applciation by pressing escape
        self.root.bind('<Escape>', self.exitFrame)

        # This displays the window
        self.frame.pack()
        self.root.mainloop()

    """This allows multiple normal frames to be set up

    column - The index of the column to fill in
    """
    def normalFrame(self, column=0):

        # Each frame label will have a header number
        self.tmpLabel = tkinter.Label(self.frame, text="{}".format(column+1))
        self.tmpLabel.grid(row=0, column=(column*2), columnspan=2)

        # Each frame label will have two entries
        self.entryList.append(tkinter.Entry(self.frame, width=6,
                                            validate=self.validateText,
                                            validatecommand=self.vcmd,
                                            justify=tkinter.CENTER))
        self.entryList[-1].grid(row=1, column=(column*2))
        self.entryList.append(tkinter.Entry(self.frame, width=6,
                                            validate=self.validateText,
                                            validatecommand=self.vcmd,
                                            justify=tkinter.CENTER))
        self.entryList[-1].grid(row=1, column=(column*2)+1)

        # Each frame label will have one final score entry
        self.finalList.append(tkinter.Label(self.frame, text="-"))
        self.finalList[-1].grid(row=4, column=(column*2), columnspan=2)

    """This allows multiple final frames to be set up

    column - The index of the column to fill in
    """
    def longFrame(self, column=9):

        # Each final frame label will have a header number
        self.tmpLabel = tkinter.Label(self.frame, text="{}".format(column+1))
        self.tmpLabel.grid(row=0, column=(column*2), columnspan=3)

        # Each final frame label will have three entries
        self.entryList.append(tkinter.Entry(self.frame, width=6,
                                            validate=self.validateText,
                                            validatecommand=self.vcmd,
                                            justify=tkinter.CENTER))
        self.entryList[-1].grid(row=1, column=(column*2))
        self.entryList.append(tkinter.Entry(self.frame, width=6,
                                            validate=self.validateText,
                                            validatecommand=self.vcmd,
                                            justify=tkinter.CENTER))
        self.entryList[-1].grid(row=1, column=(column*2)+1)
        self.entryList.append(tkinter.Entry(self.frame, width=6,
                                            validate=self.validateText,
                                            validatecommand=self.vcmd,
                                            justify=tkinter.CENTER))
        self.entryList[-1].grid(row=1, column=(column*2)+2)

        # Each final frame label will have one final score entry
        self.finalList.append(tkinter.Label(self.frame, text="-"))
        self.finalList[-1].grid(row=4, column=(column*2), columnspan=3)

    """This function add functionality to the reset button
    """
    def resetFrame(self):

        # Reset all the entries
        for i in range(len(self.entryList)):
            self.entryList[i].delete(0, tkinter.END)

        # Reset all the scores
        for i in range(len(self.finalList)):
            self.finalList[i].config(text="-")

        # Reset all the values
        for i in range(len(self.frameValues)):
            self.frameValues[i] = 0
            self.frameTotal[i] = 0
            self.frameFinal[i] = 0

        # Set the cursor back to the beginning
        self.entryList[0].focus_set()

    """This function sets up the functionality for exiting the program

    event - Holds the key binding used to exit the game
    """
    def exitFrame(self, event=None):

        # Removes the tkinter window
        self.root.destroy()
        sys.exit(0)

    """This function is used to check every entry for validation

    d - The type of action (1=insert, 0=delete)
    i - index of char string to be inserted
    P - Value of entry if editing is allowed
    """
    def onValidate(self, d, i, P):

        # Only one character per entry field
        if int(i) > 0:
            self.frame.bell()
            return False

        # If the character check is passed, calculate the score
        self.calculateEntries(P)
        return True

    # This function will take all the entries and calculate all the scores
    """This function will take all the entries to validate all the scores and
    check for errors

    P - Value of entry if editing is allowed
    """
    def calculateEntries(self, P):

        # Sets the base values to empty arrays
        self.frameValues = []
        self.frameTotal = []
        self.frameFinal = []

        # This holds some of the temporary variables for the frame shots
        tmpShots = []
        tmpShotsScore = []

        # This gets the current entry frame in focus
        curFrame = self.frame.focus_get()

        # This prevents the final score from writing past the entry point
        writeScore = True
        # This allows the entry to skip twice when there is a strike
        skipTwice = False

        # Let's turn the shots into values
        for i in range(len(self.entryList)):

            # Sets the default fields to all yellow
            self.entryList[i].config(bg=self.errorColor)

            # This gets all the entries with data within them
            if curFrame == self.entryList[i]:
                tmpStr = P
            else:
                tmpStr = self.entryList[i].get()

            # This makes sure only valid entries are shown in white
            if tmpStr:
                if re.search('[0-9xX/]', tmpStr):
                    self.entryList[i].config(bg=self.normalColor)
            # If an entry hasn't been written yet, it is also in white
            else:
                self.entryList[i].config(bg=self.normalColor)

            # This portion moves the entries by two if there is a strike
            tmpShots.append(0)
            if curFrame == self.entryList[i]:
                tmpStr = P
                if tmpStr.lower() == 'x' and i%2 == 0 and i/2 < len(self.finalList)-1:
                    skipTwice = True
            else:
                tmpStr = self.entryList[i].get()

            # This translates the inputs into shots
            if re.search('[0-9]', tmpStr):
                tmpShots[i] = int(tmpStr)
            elif tmpStr.lower() == 'x':
                tmpShots[i] = 10
            elif i%2 == 1 and tmpStr == "/":
                tmpShots[i] = 10-tmpShots[i-1]
            else:
                tmpShots[i] = 0

                # Spares in illegal spaces will result in an error
                if tmpStr == "/":
                    self.entryList[i].config(bg=self.errorColor)

        # This makes strikes a lot more visible to the system
        for i in range(len(tmpShots)):
            tmpShotsScore.append(tmpShots[i])
            if i%2 == 1 and i/2 < len(self.finalList)-1:
                if tmpShots[i-1] == 10:
                    tmpShotsScore[i] = -1

        # This gets the total frame shots and calculates the totals
        for i in range(len(self.entryList)):

            # This sets up the frame totals and frame final totals
            if len(self.frameValues) < len(self.finalList):
                if i%2==0 and int(i/2) <= len(self.frameValues):
                    if writeScore:
                        self.frameValues.append(0)
                        self.frameTotal.append(0)
                        self.frameFinal.append(0)

            # This makes sure that both pin values adds up to ten, if not
            # it'll show an error marker to the user
            tmpVal = int(i/2)
            if writeScore:
                if tmpVal >= len(self.frameValues):
                    tmpVal -= 1
                    if self.frameValues[tmpVal] >= 10:
                        self.frameValues[tmpVal] += tmpShots[i]
                    elif self.frameValues[tmpVal] < 10 and tmpShots[i] > 0:
                        self.entryList[i].config(bg=self.errorColor)
                elif i%2 == 1:
                    self.frameValues[tmpVal] = tmpShots[i] + tmpShots[i-1]
                    if self.frameValues[tmpVal] > 10 and self.frameValues[tmpVal] < 20:
                        self.entryList[i].config(bg=self.errorColor)
                else:
                    self.frameValues[tmpVal] = tmpShots[i]

                self.frameTotal[tmpVal] = self.frameValues[tmpVal]

            # Makes sure the score doesn't update past the cursor
            if curFrame == self.entryList[i]:
                writeScore = False

        # This section adds the spare and strike totals
        for i in range(len(self.frameTotal)):
            if i > 0 and self.frameValues[i-1] >= 10:

                # This adds the totals for the spare frame
                self.frameTotal[i-1] += tmpShots[(i*2)]

                # This adds the totals for the strike frame
                if i > 1 and tmpShotsScore[((i-2)*2)+1] == -1:
                    self.frameTotal[i-2] += tmpShots[(i*2)]
                    if i == 9 and (self.frameValues[i] >= 10 or tmpShotsScore[(i*2)+1] == 10):
                        self.frameTotal[i-1] += tmpShots[(i*2)+1]

        # Takes all the values and combines them for display
        for i in range(len(self.frameTotal)):
            for j in range(i+1):
                self.frameFinal[i] += self.frameTotal[j]

        # This takes all the values and makes them visible on the labels
        for i in range(len(self.frameValues)):
            self.finalList[i].config(text=self.frameFinal[i])

        # This the functionality for selecting the next entry
        curFrame = self.frame.focus_get()
        for i in range(len(self.entryList)):
            if self.entryList[i] == curFrame:
                if i < len(self.entryList)-1:
                    self.entryList[i+1].focus_set()
                    if skipTwice:
                        if i+1 < len(self.entryList)-1:
                            self.entryList[i+2].focus_set()
                break

# This runs the python program
if __name__ == "__main__":
    Bowling()
