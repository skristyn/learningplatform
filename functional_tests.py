import json
import requests

if __name__ == "__main__":
    base_url = "http://localhost:8000/api/v1/"
    
    # Send username and password to endpoint
    payload = {"username": "mikev", "password": "c4ardPlayer"}
    
    # pull out token to send on subsequent requests
    response = requests.post(base_url + "token-auth", 
        data=payload)

    token = json.loads(response.content)["token"]

    # Check base endpoint
    response = requests.get(base_url, 
        headers={"Authorization": f"Token {token}"})
    
    # print(json.loads(response.content))
    
    # How do we know who the user is?

    assert "lessons" in json.loads(response.content).keys()
    assert "sections" in json.loads(response.content).keys()
    assert "resources" in json.loads(response.content).keys()

    response = requests.get(base_url + "home/", 
        headers={"Authorization": f"Token {token}"})

    print(json.loads(response.content))

    response = requests.post(
        base_url + "grades/",
        headers={
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        },
        data={"section": 1, "student": 2},
    )

    print(response.content)

