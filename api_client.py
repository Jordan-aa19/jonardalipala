
import requests

url = "https://github.com/Jordan-aa19/jonardalipala"

response = requests.get(url)

print("Status Code:", response.status_code)
print("Response Text:", response.text)

if response.status_code == 200:
    data = response.json()

    print("Name:", data["name"])
    print("Email:", data["email"])
else:
    print("Request failed.")
