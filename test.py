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
		"masked_number": "1333",
		"name": "моя уже четвертая карточка",
		"owner_email": "3@gmail.com",
		"date": "00/01"
	})
	print(response.text)

def check_cards():
	response = requests.get("http://127.0.0.1:8000/users/3@gmail.com/cards/")
	print(response.text)

def check_dashboard_activity():
	response = requests.get("http://127.0.0.1:8000/users/3@gmail.com/transactions")
	print(response.text)

def check_dashboard_activity2():
	response = requests.get("http://127.0.0.1:8000/users/3%40gmail.com/cards")
	print(response.text)

def create_transaction():
	response = requests.post("http://127.0.0.1:8000/transactions", json={
		"is_income": True,
		"amount": 100,
		"category": "Salary",
		"description": "фуфывфв",
		"card_id": 5,
		"icon_res_id": 2
	})

if __name__ == "__main__":
	create_transaction()
	# check_users()
	check_dashboard_activity()
	# check_dashboard_activity2()
	#
	# create_card()
	# check_cards()