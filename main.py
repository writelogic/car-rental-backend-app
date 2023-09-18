import pandas

df = pandas.read_csv("cars.csv", dtype={"id": str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pandas.read_csv("card_security.csv", dtype=str)

class Car:
    def __init__(self, car_id):
        self.car_id = car_id
        self.name = df.loc[df["id"] == self.car_id, "name"].squeeze()

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.car_id, "available"] = "no"
        df.to_csv("cars.csv", index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.car_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, car_object):
        self.customer_name = customer_name
        self.car = car_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.customer_name}
        Car: {self.car.name}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration,
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


print(df)
car_ID = input("Enter the id of the car: ")
car = Car(car_ID)

if car.available():
    credit_card = SecureCreditCard(number="1234567890123456")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate(given_password="mypass"):
            car.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(customer_name =name, car_object=car)
            print(reservation_ticket.generate())
        else:
            print("Credit card authentication failed.")
    else:
        print("There was a problem with your payment")
else:
    print("Car is not free.")