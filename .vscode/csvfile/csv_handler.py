import csv
def read_csv(file_name):
    with open(file_name, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)
def write_csv(file_name, data):
    with open(file_name, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Age', 'City'])  # Write header
        writer.writerows(data)  # Write multiple rows
def main():
    # Sample data to write to CSV
    data = [
        ['John Doe', 30, 'New York'],
        ['Jane Smith', 25, 'Los Angeles'],
        ['Alice Johnson', 28, 'Chicago'],
        ['Bob Brown', 22, 'Miami']
    ]

    # Write data to CSV in a different directory
    write_csv(r"C:/Users/dcp69/Desktop/data.csv", data)  # Use your actual username

    # Read data from CSV
    print("Reading from CSV file:")
    read_csv(r"C:/Users/dcp69/Desktop/data.csv")  # Use your actual username

   
if __name__ == "__main__":
    main()