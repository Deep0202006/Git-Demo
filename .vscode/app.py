import csv

# Open the CSV file for reading
with open('employees.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    
    # Read the header
    header = next(csv_reader)
    print(f"Header: {header}")

    # Read each row in the CSV
    for row in csv_reader:
        print(f"Row: {row}")

with open ('employee.csv','r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row) 

with open ('employee.csv','w',newline='')as csvfile:
    writer= csv.writer(csvfile)
    writer.writerow(['Name','Age','City'])
    writer.writerow(['Deep','18','Patan'])
    writer.writerow(['Daksh','19','Patan'])
    
csv.Dialect(open)
csv.DictWriter("This is the additional text added to the existing csv file")
csv_reader
#for execution
for x in csv_reader():
    x+=abs(csv_reader)
    x+=1
    print(x)
while True:
    try:
        


    

