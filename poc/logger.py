import csv

class Logger:
    def __init__(self, path, fieldnames):
        self.file = open(path, "w", newline="")
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        self.writer.writeheader()

    def log(self, row):
        self.writer.writerow(row)
    
    def close(self):
        self.file.close()
