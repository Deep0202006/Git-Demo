import requests
url="https://jsonplaceholder.typicode.com/posts"

response=requests.get(url)
if response.status_code==200:
    data=response.json()
    print(data)
else:
    print(f"Error:{response.status_code}")
def main():

 print(f"{response} is related to {data}.")
 while True:
     print(f"{data} is only stored and displayed at {response.status_code}")

# params={"userId":1}
# response= requests.get(url,params=params)
# if response.status_code == 200:
#     data=response.json()
#     print(data)
# else:
#      print(f"Error:{response.status_code}")

    