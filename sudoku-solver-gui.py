import tkinter as tk
from tkinter import messagebox
import time
import random

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.createWidgets()

        self.timerStarted = False
        self.startTime = 0
        self.timerRunning = False

    def createWidgets(self):
        self.frame = tk.Frame(self.root, bg="#f4f4f4")
        self.frame.pack(pady=20)

        self.cells = [[tk.Entry(self.frame, width=2, font=("Arial", 18), justify="center", relief="solid", bd=1, bg="#ffffff")
                       for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                self.cells[i][j].grid(row=i, column=j, padx=(2 if j % 3 == 0 else 1), pady=(2 if i % 3 == 0 else 1))
                self.cells[i][j].bind("<KeyRelease>", self.onKeyRelease)
                self.cells[i][j].bind("<FocusIn>", lambda e, x=i, y=j: self.highlightCell(x, y))

        self.buttonsFrame = tk.Frame(self.root, bg="#f4f4f4")
        self.buttonsFrame.pack(pady=10)

        self.difficultyLabel = tk.Label(self.buttonsFrame, text="Difficulty:", font=("Arial", 14))
        self.difficultyLabel.grid(row=0, column=0, padx=5)

        self.difficultyVar = tk.StringVar()
        self.difficultyDropdown = tk.OptionMenu(self.buttonsFrame, self.difficultyVar, 'Easy', 'Medium', 'Hard')
        self.difficultyDropdown.grid(row=0, column=1, padx=5)

        tk.Button(self.buttonsFrame, text="Generate", command=self.generateSudoku, font=("Arial", 14), bg="#ff9999", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(self.buttonsFrame, text="Solve", command=self.solveSudoku, font=("Arial", 14), bg="#4caf50", fg="white").grid(row=0, column=3, padx=5)
        tk.Button(self.buttonsFrame, text="Clear", command=self.clearGrid, font=("Arial", 14), bg="#1e90ff", fg="white").grid(row=0, column=4, padx=5)

        self.timerLabel = tk.Label(self.root, text="Time: 00:00", font=("Arial", 14), bg="#f4f4f4")
        self.timerLabel.pack(pady=5)

    def highlightCell(self, i, j):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].config(bg="#ffffff")
        self.cells[i][j].config(bg="#e6f7ff")

    def onKeyRelease(self, event):
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                val = cell.get()
                if val.isdigit() and int(val) not in range(1, 10):
                    cell.config(bg="#ffcdd2")
                else:
                    cell.config(bg="#ffffff")

    def generateSudoku(self):
        difficulty = self.difficultyVar.get() if self.difficultyVar.get() else 'Medium'
        self.grid = self.generateValidSudoku(difficulty)
        self.fillGrid(self.grid)

    def generateValidSudoku(self, difficulty='Medium'):
        difficultyMap = {
            'Easy': 35,
            'Medium': 45,
            'Hard': 55
        }
        
        emptyCells = difficultyMap.get(difficulty, 45)

        def isValid(board, row, col, num):
            for i in range(9):
                if board[row][i] == num or board[i][col] == num:
                    return False
            startRow, startCol = 3 * (row // 3), 3 * (col // 3)
            for i in range(startRow, startRow + 3):
                for j in range(startCol, startCol + 3):
                    if board[i][j] == num:
                        return False
            return True

        def solve(board):
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        for num in range(1, 10):
                            if isValid(board, row, col, num):
                                board[row][col] = num
                                if solve(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True

        board = [[0 for _ in range(9)] for _ in range(9)]
        solve(board)

        attempts = 0
        while attempts < emptyCells:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if board[row][col] != 0:
                backup = board[row][col]
                board[row][col] = 0
                boardCopy = [row[:] for row in board]
                
                if self.isUniqueSolution(boardCopy):
                    attempts += 1
                else:
                    board[row][col] = backup
        return board

    def isUniqueSolution(self, board):
        solutions = []
        
        def solve(board):
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        for num in range(1, 10):
                            if self.isSafe(board, row, col, num):
                                board[row][col] = num
                                solve(board)
                                board[row][col] = 0
                        return
            solutions.append([row[:] for row in board])
        
        solve(board)
        return len(solutions) == 1

    def fillGrid(self, grid):
        self.clearGrid()
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    self.cells[i][j].insert(0, grid[i][j])
                    self.cells[i][j].config(state="disabled", disabledforeground="black")

    def clearGrid(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].config(state="normal")
                self.cells[i][j].delete(0, tk.END)

    def getGrid(self):
        for i in range(9):
            for j in range(9):
                val = self.cells[i][j].get()
                self.grid[i][j] = int(val) if val.isdigit() else 0

    def solveSudoku(self):
        self.getGrid()
    
        if not self.timerStarted:
            self.startTime = time.time()
            self.timerRunning = True
            self.updateTimer()
    
        if self.solveBacktracking():
            messagebox.showinfo("Sudoku Solver", "Solved!")
        else:
            messagebox.showerror("Sudoku Solver", "No solution exists for the given Sudoku.")

    def solveBacktracking(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.isSafe(self.grid, i, j, num):
                            self.grid[i][j] = num
                            self.cells[i][j].delete(0, tk.END)
                            self.cells[i][j].insert(0, num)
                            self.cells[i][j].config(state="disabled", disabledforeground="black")
                            self.root.update_idletasks()
                            time.sleep(0.1)
                            if self.solveBacktracking():
                                return True
                            self.grid[i][j] = 0
                            self.cells[i][j].delete(0, tk.END)
                            self.cells[i][j].config(state="normal")
                    return False
        return True

    def isSafe(self, grid, row, col, num):
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False
        startRow, startCol = 3 * (row // 3), 3 * (col // 3)
        for i in range(startRow, startRow + 3):
            for j in range(startCol, startCol + 3):
                if grid[i][j] == num:
                    return False
        return True

    def updateTimer(self):
        if self.timerRunning:
            elapsedTime = time.time() - self.startTime
            minutes, seconds = divmod(int(elapsedTime), 60)
            self.timerLabel.config(text=f"Time: {minutes:02}:{seconds:02}")
            self.root.after(1000, self.updateTimer)

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()
