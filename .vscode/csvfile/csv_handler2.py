import csv

def read_csv(file_name):
    """Read data from a CSV file using DictReader."""
    with open(file_name, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            data.append(row)
        return data

def write_csv(file_name, data):
    """Write data to a CSV file using DictWriter."""
    with open(file_name, mode='w', newline='') as csvfile:
        fieldnames = ['Name', 'Age', 'City']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write header
        for item in data:
            writer.writerow(item)

def main():
    # Specify the full path to the CSV file
    input_file = r"C:/Users/dcp69/Desktop/Python proj/.vscode/csvfile/data.csv"  # Change this path as needed
    data = read_csv(input_file)
    
    print("Original Data:")
    for row in data:
        print(row)

    # Modify the data (for example, increase age by 1)
    for row in data:
        row['Age'] = str(int(row['Age']) + 1)  # Increment age by 1

    # Write modified data to a new CSV file
    output_file = r"C:/Users/dcp69/Desktop/Python proj/.vscode/csvfile/modified_data.csv"  # Change this path as needed
    write_csv(output_file, data)

    print("\nModified Data written to 'modified_data.csv':")
    for row in data:
        print(row)

if __name__ == "__main__":
    main()