import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, filedialog
import subprocess
import os

class GitCommander:
    def __init__(self, root):
        self.root = root
        self.root.title("Git Commander")
        self.root.geometry('670x550')  # Window size

        self.working_directory = os.getcwd()  # Start with the current working directory
        self.clone_path = None  # Variable to hold the selected path for cloning
        self.add_option = tk.StringVar(value="all")  # Default option for git add

        # ScrolledText widget for Git command output
        self.info_text = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD)
        self.info_text.grid(row=12, column=0, columnspan=3, pady=5, padx=5, sticky="nsew")

        # Entry for clone URL
        self.clone_url_entry = tk.Entry(root, width=60)
        self.clone_url_entry.grid(row=9, column=0, pady=5, padx=5, sticky='ew')

        # Button to select working directory
        tk.Button(root, text="Select Working Directory", command=self.select_working_directory).grid(row=0, column=0, padx=5, pady=5, sticky='ew', columnspan=3)

        # Paste button for clone URL
        tk.Button(root, text="Paste URL", command=self.paste_url).grid(row=9, column=1, pady=5, padx=5, sticky='ew')

        # Button to choose clone destination directory
        tk.Button(root, text="Select Clone Path", command=self.select_clone_path).grid(row=10, column=0, pady=5, padx=5, sticky='ew')

        # Button for git clone
        tk.Button(root, text="Clone Repository", command=self.git_clone).grid(row=10, column=1, pady=5, padx=5, sticky='ew')

        # Radio buttons for selecting add file option
        tk.Radiobutton(root, text="Add All Files", variable=self.add_option, value="all").grid(row=1, column=0, sticky='w', padx=5)
        tk.Radiobutton(root, text="Add Specific Files", variable=self.add_option, value="specific").grid(row=1, column=1, sticky='w', padx=5)

        # Button to perform the add operation
        tk.Button(root, text="Add Files", command=self.add_files).grid(row=1, column=2, padx=5, sticky='ew')

        # Other Git operation buttons
        tk.Button(root, text="Commit Changes", command=self.commit_changes).grid(row=4, column=0, columnspan=3, pady=5, padx=5, sticky='ew')
        tk.Button(root, text="Change Commit Name", command=self.change_commit_name).grid(row=5, column=0, columnspan=3, pady=5, padx=5, sticky='ew')
        tk.Button(root, text="Push Changes", command=self.push_changes).grid(row=6, column=0, columnspan=3, pady=5, padx=5, sticky='ew')
        tk.Button(root, text="Change Branch", command=self.change_branch).grid(row=7, column=0, columnspan=3, pady=5, padx=5, sticky='ew')
        tk.Button(root, text="Create Branch", command=self.create_branch).grid(row=8, column=0, columnspan=3, pady=5, padx=5, sticky='ew')
        tk.Button(root, text="Git Status", command=self.git_status).grid(row=11, column=0, columnspan=3, pady=5, padx=5, sticky='ew')

    def run_git_command(self, command):
        try:
            result = subprocess.run(["git"] + command, cwd=self.working_directory, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.info_text.insert(tk.END, f"$ git {' '.join(command)}\n{result.stdout}\n")
        except subprocess.CalledProcessError as e:
            self.info_text.insert(tk.END, f"Error:\n{e.stderr}\n")
        # Autoscroll to the bottom
        self.info_text.see(tk.END)

    def select_working_directory(self):
        directory = filedialog.askdirectory(mustexist=True)
        if directory:
            self.working_directory = directory
            self.info_text.insert(tk.END, f"Working directory changed to: {directory}\n")
            self.info_text.see(tk.END)

    def paste_url(self):
        try:
            self.clone_url_entry.delete(0, tk.END)
            self.clone_url_entry.insert(0, root.clipboard_get())
        except tk.TclError:
            messagebox.showerror("Error", "Nothing to paste!")

    def select_clone_path(self):
        self.clone_path = filedialog.askdirectory(mustexist=True)
        if self.clone_path:
            self.info_text.insert(tk.END, f"Clone path set to: {self.clone_path}\n")
            self.info_text.see(tk.END)

    def git_clone(self):
        url = self.clone_url_entry.get()
        if url and self.clone_path:
            self.run_git_command(["clone", url, self.clone_path])
        else:
            messagebox.showwarning("Warning", "Please enter a repository URL and select a clone path.")

    def add_files(self):
        if self.add_option.get() == 'all':
            self.run_git_command(["add", "."])
        else:
            file_to_add = simpledialog.askstring("Input", "Enter the file name to add:", parent=self.root)
            if file_to_add:
                self.run_git_command(["add", file_to_add])

    def commit_changes(self):
        commit_message = simpledialog.askstring("Input", "Enter commit message:", parent=self.root)
        if commit_message:
            self.run_git_command(["commit", "-m", commit_message])

    def change_commit_name(self):
        new_name = simpledialog.askstring("Input", "Enter new commit name:", parent=self.root)
        if new_name:
            self.run_git_command(["commit", "--amend", "-m", new_name])

    def push_changes(self):
        self.run_git_command(["push"])

    def change_branch(self):
        branch_name = simpledialog.askstring("Input", "Enter the name of the branch to checkout:", parent=self.root)
        if branch_name:
            self.run_git_command(["checkout", branch_name])

    def create_branch(self):
        new_branch_name = simpledialog.askstring("Input", "Enter the name of the new branch:", parent=self.root)
        if new_branch_name:
            self.run_git_command(["checkout", "-b", new_branch_name])

    def git_status(self):
        self.run_git_command(["status"])

# Run the application
if __name__ == '__main__':
    root = tk.Tk()
    app = GitCommander(root)
    root.mainloop()
