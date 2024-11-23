
from flask import Flask, render_template, request, jsonify
import razorpay

app = Flask(__name__)

# Razorpay credentials
RAZORPAY_KEY_ID = 'rzp_test_l57LNe7mJd4jWC'
RAZORPAY_KEY_SECRET = 'NMaXcuiRPNWPLygM2mn37gvw'

# Initialize Razorpay client
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_order', methods=['POST'])
def create_order():
    amount = request.form.get('amount')
    print(amount)
    order_data = {
        'amount': amount, 
        'currency': 'INR',
        'payment_capture': '1'  # Auto-capture after payment 
    }

    order = client.order.create(data=order_data)
    return jsonify(order)

@app.route('/payment/success', methods=['POST'])
def payment_success():
    # Payment details from frontend
    payment_id = request.form.get('razorpay_payment_id')
    order_id = request.form.get('razorpay_order_id')
    signature = request.form.get('razorpay_signature')

    # Verify the payment signature
    params_dict = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }

    try:
        client.utility.verify_payment_signature(params_dict)
        return "Payment verified successfully", 200
    except razorpay.errors.SignatureVerificationError:
        return "Payment verification failed", 400

if __name__ == '__main__':
    app.run(debug=True)
