import tkinter as tk
from tkinter import messagebox
import heapq
class IrrigationNetwork:
    def __init__(self):
        self.locations = {} 
        self.graph = {}  
    def add_location(self, location):
        if location in self.locations:
            return False  
        self.locations[location] = None
        self.graph[location] = []
        return True
    def add_pipe(self, loc1, loc2, capacity):
        if loc1 in self.graph and loc2 in self.graph:
            self.graph[loc1].append((loc2, capacity))
            self.graph[loc2].append((loc1, capacity))  
            return True
        return False
    def dijkstra(self, start, end):
        dist = {location: float('inf') for location in self.locations}
        dist[start] = 0
        pq = [(0, start)] 
        while pq:
            current_dist, current = heapq.heappop(pq)
            if current_dist > dist[current]:
                continue
            for neighbor, capacity in self.graph[current]:
                new_dist = current_dist + capacity
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
        return dist.get(end, float('inf'))  
class IrrigationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Farm Irrigation Network")
        self.irrigation_system = IrrigationNetwork()
        tk.Label(root, text="Location Name").grid(row=0, column=0, padx=10, pady=5)
        self.location_entry = tk.Entry(root)
        self.location_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(root, text="Pipe Capacity (liters/hour)").grid(row=1, column=0, padx=10, pady=5)
        self.pipe_capacity_entry = tk.Entry(root)
        self.pipe_capacity_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(root, text="Add Location", command=self.add_location).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Add Pipe", command=self.add_pipe).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Label(root, text="Start Location").grid(row=4, column=0, padx=10, pady=5)
        self.start_location_entry = tk.Entry(root)
        self.start_location_entry.grid(row=4, column=1, padx=10, pady=5)
        tk.Label(root, text="End Location").grid(row=5, column=0, padx=10, pady=5)
        self.end_location_entry = tk.Entry(root)
        self.end_location_entry.grid(row=5, column=1, padx=10, pady=5)
        tk.Button(root, text="Find Optimal Path", command=self.find_optimal_path).grid(row=6, column=0, columnspan=2, pady=5)
    def add_location(self):
        location = self.location_entry.get()
        if location:
            if self.irrigation_system.add_location(location):
                messagebox.showinfo("Success", f"Location {location} added.")
            else:
                messagebox.showerror("Error", f"Location {location} already exists.")
        else:
            messagebox.showerror("Error", "Please enter a location name.")
    def add_pipe(self):
        loc1 = self.location_entry.get()
        pipe_capacity = self.pipe_capacity_entry.get()
        if loc1 and pipe_capacity:
            try:
                capacity = int(pipe_capacity)
                loc2 = self.end_location_entry.get()
                if self.irrigation_system.add_pipe(loc1, loc2, capacity):
                    messagebox.showinfo("Success", f"Pipe added between {loc1} and {loc2}.")
                else:
                    messagebox.showerror("Error", "One or both locations not found.")
            except ValueError:
                messagebox.showerror("Error", "Invalid pipe capacity.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    def find_optimal_path(self):
        start = self.start_location_entry.get()
        end = self.end_location_entry.get()
        if start in self.irrigation_system.locations and end in self.irrigation_system.locations:
            capacity = self.irrigation_system.dijkstra(start, end)
            if capacity == float('inf'):
                messagebox.showinfo("Result", "No path found.")
            else:
                messagebox.showinfo("Result", f"Optimal water flow capacity: {capacity} liters/hour")
        else:
            messagebox.showerror("Error", "One or both locations not found.")
def main():
    root = tk.Tk()
    app = IrrigationApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()