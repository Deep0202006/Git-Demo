def acces_element(lst,index):
    return lst[index]
#It is a program to access any element in the given array

def find_element(lst, target):
    for element in lst:
        if element == target:
            return True
    return False
#Finding an element in a list takes linear time

def bubble_sort(lst):
    for i in range(len(lst)):
        for j in range(len(lst) - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst
# Bubble sort algorithm has a quadratic time complexity

def merge_sort(lst):
    if len(lst)<=1:
        return lst
    mid=len(lst)
    left=merge_sort(lst[:mid])
    right=merge_sort(lst[mid:])

    return merge(left,right)

def merge(left,right):
    result=[]
    while left and right:
        if left[0]<right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left)
    result.extend(right)
    return result
#Merge sort algorithm has a linearithmic time complexity

def merge_sort(left,right):
    result=[]
    while left and right:
        if left[0]<right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left)
    result.extend(right)
    return result
#Merger is carried out in above code

def access_element(lst,index):
#Access any element in a list by its index
#Time complexity: 0(1)
 return lst[index]
lst=[1,2,3,4,5]
index=2
print(access_element(lst,index))
a=int(input("Enter the option:"))
b=int(input("Enter another option:"))
print(f"{acces_element(lst,index)}: {merge_sort(a,b)}: ")
print(f"{index}: {lst}")
c=int(input("Enter value:"))
while True:
   try:
    if a==1:
        print(f"{a}: {b}: {c}")
    elif a==2:
        print(f"{a}: {b}")
    elif a==3:
        print(f"{a}")
    else:
        print(f"{b}: {c}")
        break
   except:
       ValueError 

       
