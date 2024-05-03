import tkinter as tk
import random
from tkinter import messagebox

class SudokuGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku")
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.create_widgets()
        self.generate_puzzle()
        self.update_entries()

    def create_widgets(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.entries = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.entries[i][j] = tk.Entry(self.frame, width=3, font=('Helvetica', 16), justify='center')
                self.entries[i][j].grid(row=i, column=j, padx=1, pady=1)
                
                if (i in (2, 5) and j % 3 == 0) or (i % 3 == 0 and j in (2, 5)):
                    self.entries[i][j].config(highlightthickness=5)  # Add padding in the 3x3 to seperate the squares

        check_button = tk.Button(self.master, text="Check", command=self.check_solution)
        check_button.pack()

        solve_button = tk.Button(self.master, text="Solve", command=self.solve_puzzle_gui)
        solve_button.pack()

    def solve_puzzle_gui(self):
        if self.solve_puzzle():
            self.update_entries()

    def generate_puzzle(self):
        # Generate a complete valid Sudoku puzzle
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_puzzle()
        
        for _ in range(50):  # Number of values that being removed from the compelete game
            row, col = random.randint(0, 8), random.randint(0, 8)
            while self.board[row][col] == 0: # If the choosen cell is already 0 then this loop will choose another one
                row, col = random.randint(0, 8), random.randint(0, 8)
            self.board[row][col] = 0

    def solve_puzzle(self):
        # A simple backtracking algorithm to solve the complete puzzle
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True  # Puzzle solved
        row, col = empty_cell
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                self.board[row][col] = num
                if self.solve_puzzle():
                    return True
                self.board[row][col] = 0
        return False  # No solution

    def find_empty_cell(self):
        # Find the first empty cell in the puzzle
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None  # No empty cells

    def check_solution(self):
        self.board = [[0 if self.entries[i][j].get() == '' else int(self.entries[i][j].get()) for j in range(9)] for i in range(9)]
        if self.is_valid_solution():
            messagebox.showinfo("Congratulations", "Congratulations! You solved the Sudoku puzzle!")
        else:
            messagebox.showerror("Incorrect", "Sorry, the solution is incorrect. Please try again.")

    def is_valid_solution(self):
        # Check rows and columns
        for i in range(9):
            row_set = set()
            col_set = set()
            for j in range(9):
                if self.board[i][j] in row_set or self.board[j][i] in col_set:
                    return False
                row_set.add(self.board[i][j])
                col_set.add(self.board[j][i])

        # Check 3x3 grids
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                grid_set = set()
                for k in range(3):
                    for l in range(3):
                        if self.board[i+k][j+l] in grid_set:
                            return False
                        grid_set.add(self.board[i+k][j+l])

        return True

    def is_valid_move(self, row, col, num):
        # Check if the move is valid in the current state of the board
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False
        return True

    def update_entries(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.entries[i][j].insert(tk.END, self.board[i][j])
                    self.entries[i][j].config(state='disabled')

def main():
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
