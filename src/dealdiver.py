import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
import schedule

class DealDiver:
    def __init__(self, url, target_price, email, phone):
        self.url = url
        self.target_price = target_price
        self.email = email
        self.phone = phone
        self.current_price = None

    def get_price(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find('span', {'class': 'a-offscreen'})
        if price_element:
            self.current_price = float(price_element.text.replace('$', '').replace(',', ''))
        else:
            self.current_price = None

    def check_price(self):
        self.get_price()
        if self.current_price and self.current_price <= self.target_price:
            self.notify_user()

    def notify_user(self):
        subject = "Price Drop Alert!"
        body = f"The price of the product at {self.url} has dropped to ${self.current_price:.2f}."
        
        # Send email
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'your_email@example.com'
        msg['To'] = self.email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('your_email@example.com', 'your_password')
            server.send_message(msg)

        # Send text message (SMS)
        sms_body = f"Price Alert: {body}"
        sms_url = f"https://textbelt.com/text?number={self.phone}&message={sms_body}"
        requests.post(sms_url)

    def run(self):
        schedule.every(1).hours.do(self.check_price)  # Check price every hour
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    url = "https://www.amazon.com/dp/B077S5F9BG"  # Example Amazon product URL
    target_price = 299.99  # Target price in dollars
    email = "user@example.com"  # User's email
    phone = "+1234567890"  # User's phone number

    deal_diver = DealDiver(url, target_price, email, phone)
    deal_diver.run()
