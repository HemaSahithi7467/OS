import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class Process:
    def __init__(self, arrival_time, burst_time, priority):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.start_time = 0
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0

class CPUSchedulingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulation")
        
        self.processes = []

        # Create input fields
        self.create_input_fields()
        
        # Create buttons
        self.create_buttons()

    def create_input_fields(self):
        tk.Label(self.root, text="Number of Processes:").grid(row=0, column=0)
        self.num_processes_entry = tk.Entry(self.root)
        self.num_processes_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Arrival Time:").grid(row=1, column=0)
        self.arrival_time_entry = tk.Entry(self.root)
        self.arrival_time_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Burst Time:").grid(row=2, column=0)
        self.burst_time_entry = tk.Entry(self.root)
        self.burst_time_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Priority:").grid(row=3, column=0)
        self.priority_entry = tk.Entry(self.root)
        self.priority_entry.grid(row=3, column=1)

    def create_buttons(self):
        tk.Button(self.root, text="Add Process", command=self.add_process).grid(row=4, column=0, columnspan=2)
        tk.Button(self.root, text="Run Scheduling", command=self.run_scheduling).grid(row=5, column=0, columnspan=2)

    def add_process(self):
        try:
            arrival_time = int(self.arrival_time_entry.get())
            burst_time = int(self.burst_time_entry.get())
            priority = int(self.priority_entry.get())
            self.processes.append(Process(arrival_time, burst_time, priority))
            messagebox.showinfo("Success", "Process added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers for arrival time, burst time, and priority.")

    def run_scheduling(self):
        algorithms = ["FCFS", "SJF", "Priority"]
        for algorithm in algorithms:
            processes_copy = self.processes.copy()  # Create a copy to avoid modifying original processes
            self.run_algorithm(processes_copy, algorithm)
            self.visualize_gantt_chart(processes_copy, algorithm)
            avg_waiting_time, avg_turnaround_time, avg_response_time = self.calculate_metrics(processes_copy)
            print(f"{algorithm} Scheduling:")
            print(f"Average Waiting Time: {avg_waiting_time}")
            print(f"Average Turnaround Time: {avg_turnaround_time}")
            print(f"Average Response Time: {avg_response_time}")
            print()

    def run_algorithm(self, processes, algorithm):
        if algorithm == "FCFS":
            self.FCFS(processes)
        elif algorithm == "SJF":
            self.SJF(processes)
        elif algorithm == "Priority":
            self.Priority(processes)

    def FCFS(self, processes):
        current_time = 0
        for process in processes:
            process.start_time = max(current_time, process.arrival_time)
            process.finish_time = process.start_time + process.burst_time
            process.waiting_time = process.start_time - process.arrival_time
            process.turnaround_time = process.finish_time - process.arrival_time
            process.response_time = process.start_time - process.arrival_time
            current_time = process.finish_time

    def SJF(self, processes):
        processes.sort(key=lambda x: x.burst_time)
        current_time = 0
        for process in processes:
            process.start_time = max(current_time, process.arrival_time)
            process.finish_time = process.start_time + process.burst_time
            process.waiting_time = process.start_time - process.arrival_time
            process.turnaround_time = process.finish_time - process.arrival_time
            process.response_time = process.start_time - process.arrival_time
            current_time = process.finish_time

    def Priority(self, processes):
        processes.sort(key=lambda x: x.priority, reverse=True)
        current_time = 0
        for process in processes:
            process.start_time = max(current_time, process.arrival_time)
            process.finish_time = process.start_time + process.burst_time
            process.waiting_time = process.start_time - process.arrival_time
            process.turnaround_time = process.finish_time - process.arrival_time
            process.response_time = process.start_time - process.arrival_time
            current_time = process.finish_time

    def visualize_gantt_chart(self, processes, algorithm):
        fig, ax = plt.subplots()
        ax.set_xlim(0, max(process.finish_time for process in processes))
        ax.set_ylim(0, len(processes) + 1)
        ax.set_xlabel('Time')
        ax.set_ylabel('Process')

        for i, process in enumerate(processes):
            ax.barh(i, process.burst_time, left=process.start_time, color='blue', label=f'P{i + 1}')

        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.yticks(range(len(processes)), [f'P{i + 1}' for i in range(len(processes))])
        plt.grid(True)
        plt.title(f"{algorithm} Scheduling")
        plt.show()

    def calculate_metrics(self, processes):
        average_waiting_time = sum(process.waiting_time for process in processes) / len(processes)
        average_turnaround_time = sum(process.turnaround_time for process in processes) / len(processes)
        average_response_time = sum(process.response_time for process in processes) / len(processes)
        return average_waiting_time, average_turnaround_time, average_response_time

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulingApp(root)
    root.mainloop()
