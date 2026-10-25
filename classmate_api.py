
import requests

url = "https://CLASSMATE-URL.onrender.com/hello"

params = {"name": "Jordan"}

try:
    response = requests.get(url, params=params, timeout=30)

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        data = response.json()
        print("Response:", data)
    else:
        print("Request failed.")
        print(response.text)

except requests.RequestException as error:
    print("Connection error:", error)
