import tkinter as tk
from tkinter import messagebox
import random
import time

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.grid = [[0 for i in range(9)] for j in range(9)]
        self.createWidgets()

    def createWidgets(self):
        self.frame = tk.Frame(self.root, bg="#f8d9d9")  
        self.frame.pack(pady=30)

        self.cells = [[tk.Entry(self.frame, width=4, font=("Helvetica", 18), justify="center", relief="flat", bd=1, bg="#ffffff", fg="#333333", highlightthickness=2, highlightbackground="#ffb3b3")
                       for i in range(9)] for j in range(9)]

        for i in range(9):
            for j in range(9):
                self.cells[i][j].grid(row=i, column=j, padx=(5 if j % 3 == 0 else 1), pady=(5 if i % 3 == 0 else 1))

        self.buttonsFrame = tk.Frame(self.root, bg="#f8d9d9")  # Light pink background
        self.buttonsFrame.pack(pady=20)

        tk.Button(self.buttonsFrame, text="Generate", command=self.generateSudoku, font=("Helvetica", 14), bg="#ff9999", fg="#4a4a4a", relief="flat", padx=15, pady=8, borderwidth=2, highlightbackground="#ff6666").grid(row=0, column=0, padx=10)
        tk.Button(self.buttonsFrame, text="Solve", command=self.solveSudoku, font=("Helvetica", 14), bg="#66cc66", fg="#4a4a4a", relief="flat", padx=15, pady=8, borderwidth=2, highlightbackground="#4dff4d").grid(row=0, column=1, padx=10)
        tk.Button(self.buttonsFrame, text="Clear", command=self.clearGrid, font=("Helvetica", 14), bg="#66b3ff", fg="#4a4a4a", relief="flat", padx=15, pady=8, borderwidth=2, highlightbackground="#4d9eff").grid(row=0, column=2, padx=10)

        self.difflabel = tk.Label(self.buttonsFrame, text="Difficulty  ", font=("Helvetica", 14), bg="#f8d9d9", fg="#4a4a4a")  
        self.difflabel.grid(row=1, column=0, padx=20, pady=12)

        self.diff = tk.StringVar()
        self.diff.set("Medium")
        self.menu = tk.OptionMenu(self.buttonsFrame, self.diff, "Easy", "Medium", "Hard")
        self.menu.config(font=("Helvetica", 14), bg="#e8f5e9", fg="#4a4a4a", relief="flat", width=10)
        self.menu.grid(row=1, column=1, padx=10, pady=10)

        self.frame.pack_propagate(False)
        self.root.configure(bg="#f8d9d9")

    def generateSudoku(self):
        self.grid = self.generateValidSudoku()
        self.fillGrid(self.grid)

    def generateValidSudoku(self):
        board = [[0 for i in range(9)] for j in range(9)]

        def isValid(board, row, col, num):
            for i in range(9):
                if board[row][i] == num or board[i][col] == num:
                    return False
            strtrow, strtcol = 3 * (row // 3), 3 * (col // 3)
            for i in range(strtrow, strtrow + 3):
                for j in range(strtcol, strtcol + 3):
                    if board[i][j] == num:
                        return False
            return True

        def fillBoard(board):
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        nums = list(range(1, 10))
                        random.shuffle(nums)
                        for num in nums:
                            if isValid(board, row, col, num):
                                board[row][col] = num
                                if fillBoard(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True

        fillBoard(board)

        for _ in range(45):
            row, col = random.randint(0, 8), random.randint(0, 8)
            board[row][col] = 0

        return board

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
        if self.solveBacktracking():
            messagebox.showinfo("Sudoku Solver", "Solved!")
        else:
            messagebox.showerror("Sudoku Solver", "No solution exists.")

    def solveBacktracking(self):
        emptycells = [(i, j) for i in range(9) for j in range(9) if self.grid[i][j] == 0]
        return self.solve(emptycells)

    def solve(self, emptycells):
        if not emptycells:
            return True

        row, col = emptycells.pop()

        for num in range(1, 10):
            if self.isSafe(self.grid, row, col, num):
                self.grid[row][col] = num
                self.cells[row][col].delete(0, tk.END)
                self.cells[row][col].insert(0, num)
                self.root.update_idletasks()
                time.sleep(0.001)

                if self.solve(emptycells):
                    return True
                self.grid[row][col] = 0
                self.cells[row][col].delete(0, tk.END)

        emptycells.append((row, col))
        return False

    def isSafe(self, grid, row, col, num):
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False
        strtrow, strtcol = 3 * (row // 3), 3 * (col // 3)
        for i in range(strtrow, strtrow + 3):
            for j in range(strtcol, strtcol + 3):
                if grid[i][j] == num:
                    return False
        return True

if __name__ == "__main__":
    root = tk.Tk()  
    app = SudokuSolver(root)  
    root.mainloop()  
