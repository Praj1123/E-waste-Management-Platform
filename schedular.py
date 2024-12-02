import os
import re
import schedule
import time
from datetime import datetime, timedelta
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bson.json_util import dumps
from app import retailer_collection  # Assuming retailer_collection is from your app
from werkzeug.exceptions import BadRequestKeyError
from bson.objectid import ObjectId

# Function to get items from MongoDB
def get_items():
    try:
        result = retailer_collection.find()
        if result:
            data = list(result)  # Convert cursor to list
            return data
        else:
            return 'No Data Found'
    except Exception as e:
        return str(e)

# Function to calculate the expiry dates
def calculate_expiry_dates(purchase_date_str, expiry_range):
    # Parse the expiry range like "5-7 years"
    match = re.match(r'(\d+)-(\d+) years', expiry_range)
    if match:
        min_years = int(match.group(1))
        max_years = int(match.group(2))

        # Convert purchase date string to a date object
        purchase_date = datetime.strptime(purchase_date_str, "%Y-%m-%d").date()

        # Calculate the minimum and maximum expiry dates
        try:
            min_expiry_date = purchase_date.replace(year=purchase_date.year + min_years)
            max_expiry_date = purchase_date.replace(year=purchase_date.year + max_years)
        except ValueError:  # Handles errors in case of invalid date (e.g., leap years)
            if purchase_date.month == 2 and purchase_date.day == 29:  # Handle leap year
                min_expiry_date = purchase_date.replace(year=purchase_date.year + min_years, day=28)
                max_expiry_date = purchase_date.replace(year=purchase_date.year + max_years, day=28)
            else:
                raise

        return min_expiry_date, max_expiry_date

    return None, None

# Function to send email
def send_email(to_email, customer_name, product_id, model, documentId, updated_data):
    from_email = 'prajwalchaudhari762@gmail.com'
    password = "piie zngp ijpj xtrp"  # Get the password from an environment variable

    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = 'Product Expiry Notification'
    
    # Email body
    if updated_data:
        body = (
        f"Dear {customer_name},\n\n"
        f"You had extended expiry of product with ID {product_id} and Model {model}\n"
        f" to Date : {updated_data}.\n\n"
        f"Please send it for recycling.\n\n"
        f"Visit the link below to extend the expiry:\n"
        f"http://127.0.0.1:5000/update_expirary?id={documentId}\n\n"
        "Thank you."
    )
    else:
        body = (
        f"Dear {customer_name},\n\n"
        f"Your product with ID {product_id},\n"
        f"Model {model} has expired.\n\n"
        f"Please send it for recycling.\n\n"
        f"Visit the link below to extend the expiry:\n"
        f"http://127.0.0.1:5000/update_expirary?id={documentId}\n\n"
        "Thank you."
    )
        
    message.attach(MIMEText(body, 'plain'))
    
    # Send the email via SMTP server
    try:
        with SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(message)
            print(f"Email sent to {to_email}")
            return True  # Email sent successfully
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        return False  # Email failed to send

# Main function to process the documents
def check_expiry_and_send_email():
    today = datetime.today().date()
    
    data = get_items()  # Get items from MongoDB
    
    if isinstance(data, str):  # Error handling in case 'data' is a string (like 'No Data Found')
        print(data)
        return
    
    total_products = 0  # Counter for total products
    emails_sent = 0  # Counter for emails sent
    
    for document in data:
        purchase_date = document.get('purchaseDate', '')
        expiry_range = document.get('expiry', '')
        
        if not purchase_date or not expiry_range:
            print(f"Skipping document with missing purchaseDate or expiry range: {document}")
            continue
        
        # Calculate expiry dates
        min_expiry_date, max_expiry_date = calculate_expiry_dates(purchase_date, expiry_range)
        
        if min_expiry_date and max_expiry_date:
            # Check if today is within the expiry range
            if min_expiry_date <= today <= max_expiry_date:
                updated_data = ''
                if document['updated_expiry']:
                    updated_data = document['updated_expiry']
                # Send an email to the customer
                if send_email(document['email'], document['customerName'], document['serialNumber'], document['model'], str(document['_id']), updated_data):
                    emails_sent += 1  # Increment email sent counter
            total_products += 1  # Increment total product counter
    
    # Log the results
    print(f"Total products processed: {total_products}")
    print(f"Total emails sent: {emails_sent}")

# Scheduler function
def schedule_email_check():
    # Set the scheduler to run every day at a specific time (e.g., 9:00 AM)
    schedule.every().day.at("06:09").do(check_expiry_and_send_email)
    
    while True:
        # Run pending tasks
        schedule.run_pending()

# Run the scheduler
if __name__ == "__main__":
    schedule_email_check()
