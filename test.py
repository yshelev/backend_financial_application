import requests

def create_user():
	response = requests.post("http://127.0.0.1:8000/users/", json={
		"username": "m_username",
		"password": "1234",
		"email": "32411@gmail.com"
	})
	print(response.text)


def check_users():
	response = requests.get("http://127.0.0.1:8000/users/")
	print(response.text)

def create_card():
	response = requests.post("http://127.0.0.1:8000/cards/", json={
		"masked_number": "1234",
		"name": "моя первая карточка",
		"owner_id": 1
	})
	print(response.text)

def check_cards():
	response = requests.get("http://127.0.0.1:8000/users/m_username/cards/")
	print(response.text)


if __name__ == "__main__":
	create_user()
	check_users()
	create_card()
	check_cards()