from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import vonage
import random
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import json_util
# from bson import ObjectIdpip
from bson.json_util import dumps
import json
import string
import secrets
from werkzeug.exceptions import BadRequestKeyError
import razorpay
from datetime import datetime, timedelta


app = Flask(__name__)

# Razorpay credentials
RAZORPAY_KEY_ID = "rzp_test_l57LNe7mJd4jWC"
RAZORPAY_KEY_SECRET = "NMaXcuiRPNWPLygM2mn37gvw"
# Initialize Razorpay client
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


### Razor Pay Section
# Razorpay credentials
RAZORPAY_KEY_ID = "rzp_test_l57LNe7mJd4jWC"
RAZORPAY_KEY_SECRET = "NMaXcuiRPNWPLygM2mn37gvw"

# Initialize Razorpay client
client1 = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


@app.route("/create_order", methods=["POST"])
def create_order():
    amount = request.form.get("amount")
    order_data = {
        "amount": amount,  # Amount in paise (500 INR)
        "currency": "INR",
        "payment_capture": "1",  # Auto-capture after payment
    }

    order = client1.order.create(data=order_data)
    return jsonify(order)


@app.route("/payment/success", methods=["POST"])
def payment_success():
    # Payment details from frontend
    payment_id = request.form.get("razorpay_payment_id")
    order_id = request.form.get("razorpay_order_id")
    signature = request.form.get("razorpay_signature")

    # Verify the payment signature
    params_dict = {
        "razorpay_order_id": order_id,
        "razorpay_payment_id": payment_id,
        "razorpay_signature": signature,
    }

    try:
        client1.utility.verify_payment_signature(params_dict)
        return "Payment verified successfully", 200
    except razorpay.errors.SignatureVerificationError:
        return "Payment verification failed", 400


### Razor Pay Section

app.secret_key = "hellow_EcoRecycle"
try:
    # Connect to the MongoDB server
    client = MongoClient("mongodb+srv://prajwalchaudhari762:CBXSxTBk5NUvgHkN@cluster0.r0i8k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    #mongodb://localhost:27017/
    
    client.server_info()  # This will raise an exception if the connection fails

    print("Connection successful!")

except ConnectionFailure as e:
    print(f"Connection failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
db = client["EcoRecycle"]
users_collection = db["users"]


##########################################################################################################################################################################################
# User Section  
@app.route("/")
def index():
    return render_template("start.html")


@app.route("/to_qr_scanner")
def to_qr_scanner():
    return render_template("qrscanner.html")


@app.route("/to_user")
def to_user():
    return render_template("users/home.html")


@app.route("/to_cc")
def to_cc():
    return render_template("collection_center/DashboardRC.html")


@app.route("/to_pickup_patner")
def to_pickup_patner():
    return render_template("pick_patner/home.html")


@app.route("/to_producer")
def to_producer():
    return render_template("producer/Dashboard.html")


@app.route("/signin")
def signin():
    return render_template("users/signin.html")


@app.route("/get_criteria", methods=["POST"])
def get_criteria():
    try:
        result = producer_collection.find()
        if result:
            return jsonify(
                {"status": "success", "message": "Data found", "data": dumps(result)}
            )
        else:
            return jsonify({"status": "error", "message": "Data not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/get_criteria1", methods=["POST"])
def get_criteria1():
    brand = request.form["brand"]
    filter = {"organization_name": brand}
    try:
        result = producer_collection.find_one(filter)
        if result:
            return jsonify(
                {"status": "success", "message": "Data found", "data": dumps(result)}
            )
        else:
            return jsonify({"status": "error", "message": "Data not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/to_find_recycle_centre_page")
def to_find_recycle_centre_page():
    return render_template("users/find_recycle_centre.html")


@app.route("/to_schedule_pick_up_page")
def to_schedule_pick_up_page():
    return render_template("users/schedule_pick_up.html")


@app.route("/to_details_page")
def to_details_page():
    return render_template("users/details.html")


@app.route("/get_filtered_recycle_centre", methods=["POST"])
def get_filtered_recycle_centre():
    try:
        brand = request.form["brand"]
        result = producer_collection.find_one({"organization_name": brand})
        if result:
            result = result["approve_cc"]
            cc_data_list = []
            for key in result:
                cc_data_id = result[key]
                cc_data = collection_centre.find_one({"_id": ObjectId(cc_data_id)})
                if cc_data:
                    cc_data_list.append(cc_data)
                    return jsonify(
                        {
                            "status": "success",
                            "message": "Data found",
                            "data": dumps(cc_data_list),
                        }
                    )
                else:
                    return jsonify({"status": "error", "message": "Data not found"})
        else:
            return jsonify({"status": "error", "message": "Data not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/get_cc_data", methods=["POST"])
def get_cc_data():
    try:
        id = request.form["id"]
        result = collection_centre.find_one({"_id": ObjectId(id)})
        if result:
            return jsonify(
                {"status": "success", "message": "Data found", "data": dumps(result)}
            )
        else:
            return jsonify({"status": "error", "message": "Data not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/set_pick_up_data", methods=["POST"])
def set_pick_up_data():
    try:
        data = request.form["data"]
        data = json.loads(data)
        cc_id = data["cc_id"]
        with open("user_data.txt", "r") as file:
            file_data = file.read()
            file_data = json.loads(file_data)
            user_id = file_data["_id"]["$oid"]
        data["user_id"] = user_id
        unique_id = generate_alphanumeric(12)
        query = {unique_id: data}
        result = collection_centre.find_one({"_id": ObjectId(cc_id)})
        if "pick_up_requests" in result:
            data1 = result["pick_up_requests"]
            data1[unique_id] = data
            result = collection_centre.update_one(
                {"_id": ObjectId(cc_id)}, {"$set": {"pick_up_requests": data1}}
            )
            if result.modified_count == 1:
                with open("user_data.txt", "r") as file:
                    data = file.read()
                    data = json.loads(data)
                    user_id = data["_id"]["$oid"]
                    result = users_collection.find_one({"_id": ObjectId(user_id)})
                    if "pick_up_requests" in result:
                        data1 = result["pick_up_requests"]
                        data1[unique_id] = cc_id
                        result = users_collection.update_one(
                            {"_id": ObjectId(user_id)},
                            {"$set": {"pick_up_requests": data1}},
                        )
                        return jsonify(
                            {
                                "status": "success",
                                "message": "Pick-up Schedule Successfully",
                            }
                        )
                    else:
                        result["pick_up_requests"] = {unique_id: cc_id}
                        result = users_collection.update_one(
                            {"_id": ObjectId(user_id)}, {"$set": result}
                        )
                        if result.modified_count == 1:
                            return jsonify(
                                {
                                    "status": "success",
                                    "message": "Pick-up Schedule Successfully",
                                }
                            )
                        else:
                            return jsonify(
                                {
                                    "status": "error",
                                    "message": "Unable to process request",
                                }
                            )

        else:
            result["pick_up_requests"] = query
            result = collection_centre.update_one(
                {"_id": ObjectId(cc_id)}, {"$set": result}
            )
            if result.modified_count == 1:
                with open("user_data.txt", "r") as file:
                    data = file.read()
                    data = json.loads(data)
                    user_id = data["_id"]["$oid"]
                    result = users_collection.find_one({"_id": ObjectId(user_id)})
                    if "pick_up_requests" in result:
                        data1 = result["pick_up_requests"]
                        data1[unique_id] = cc_id
                        result = users_collection.update_one(
                            {"_id": ObjectId(user_id)},
                            {"$set": {"pick_up_requests": data1}},
                        )
                        return jsonify(
                            {
                                "status": "success",
                                "message": "Pick-up Schedule Successfully",
                            }
                        )
                    else:
                        result["pick_up_requests"] = {unique_id: cc_id}
                        result = users_collection.update_one(
                            {"_id": ObjectId(user_id)}, {"$set": result}
                        )
                        if result.modified_count == 1:
                            return jsonify(
                                {
                                    "status": "success",
                                    "message": "Pick-up Schedule Successfully",
                                }
                            )
                        else:
                            return jsonify(
                                {
                                    "status": "error",
                                    "message": "Unable to process request",
                                }
                            )
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/to_profile_page")
def to_profile_page():
    return render_template("users/profile.html")


@app.route("/to_pick_up_history_page")
def to_pick_up_history_page():
    return render_template("users/history.html")


@app.route("/send_otp", methods=["POST"])
def send_otp():
    mobile_number = "91" + request.form["mobile_number"]
    session["mobile_no"] = mobile_number
    otp = str(random.randint(100000, 999999))
    print(otp)
    session["otp"] = otp
    client = vonage.Client(key="74d0f3a9", secret="xc5jQEu8TJAlf81e")
    sms = vonage.Sms(client)
    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": mobile_number,
            "text": "Hello users, your OTP is" + " " + otp,
        }
    )

    if responseData["messages"][0]["status"] == "0":
        return jsonify({"status": "success", "message": "OTP sent successfully."})
    else:
        return jsonify(
            {
                "status": "error",
                "message": f"Failed to send OTP: {responseData['messages'][0]['error-text']}",
            }
        )


@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    otp = session.get("otp")
    print(otp)
    enter_otp = request.form["enter_otp"]
    print(enter_otp)
    if otp == enter_otp:
        return jsonify({"message": "OTP verified successfully", "status": "correct"})
    else:
        return jsonify({"message": "Incorrect OTP", "status": "incorrect"})


@app.route("/more_details")
def more_details():
    return render_template("users/sign_up.html")


@app.route("/send_data_to_database", methods=["POST"])
def send_data_to_database():
    name = request.form["name"]
    print(name)
    email = request.form["email"]
    address = request.form["address"]
    password = request.form["password"]
    mobile_number = session.get("mobile_no")
    try:
        result = users_collection.insert_one(
            {
                "name": name,
                "email": email,
                "address": address,
                "password": password,
                "mobile_number": mobile_number,
            }
        )
        session["user_data_id"] = str(result.inserted_id)
        return jsonify({"status": "success", "message": str(result.inserted_id)})

    except Exception as e:
        return jsonify({"status": "error", "message": e})


@app.route("/get_pick_up_history", methods=["POST"])
def get_pick_up_history():
    try:
        with open("user_data.txt", "r") as file:
            data = file.read()
            data = json.loads(data)
            user_data_id = data["_id"]["$oid"]
        result = users_collection.find_one({"_id": ObjectId(user_data_id)})
        result = result["pick_up_requests"]
        history_list = []
        for key in result:
            cc_id = result[key]
            unique_id = key
            data = collection_centre.find_one({"_id": ObjectId(cc_id)})
            data = data["pick_up_requests"]
            for item in data:
                if unique_id == item:
                    object = {unique_id: data[item]}
                    history_list.append(object)
        return jsonify(
            {"status": "success", "message": "Data Found", "data": dumps(history_list)}
        )
    except Exception as e:
        return jsonify({"status": "error", "message": e})


@app.route("/home")
def home():
    return render_template("/users/home.html")


@app.route("/search_user_in_database", methods=["POST"])
def search_user_in_database():
    try:
        if "mobile_no" not in request.form:
            return jsonify({"error": "Mobile number not provided"}), 400

        mobile_number = request.form["mobile_no"]
        query = {"mobile_number": "91" + str(mobile_number)}
        result = users_collection.find_one(query)

        if result:
            json_result = json_util.dumps(result)
            return jsonify({"message": "user exist", "status": "success"})
        else:
            return jsonify({"message": "User not found", "status": "error"})
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"})


@app.route("/set_data_in_file", methods=["POST"])
def set_data_in_file():
    try:
        mobile_number = request.form["mobile_no"]
        query = {"mobile_number": "91" + str(mobile_number)}
        result = users_collection.find_one(query)
        json_result = json_util.dumps(result)
        with open("user_data.txt", "w") as file:
            file.write(json_result)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": e})


@app.route("/sign_out", methods=["POST"])
def sign_out():
    try:
        with open("user_data.txt", "w") as file:
            file.write("")
        return jsonify({"status": "success", "message": "Sign out successfully"})
    except Exception as e:
        return jsonify(
            {"status": "error", "message": "We have some technical problme", "code": e}
        )


@app.route("/check_status", methods=["POST"])
def check_status():
    try:
        with open("user_data.txt", "r") as file:
            data = file.read()
        if data:
            data = json.loads(data)
            data = data["_id"]["$oid"]
            result = users_collection.find_one({"_id": ObjectId(data)})
            return jsonify(
                {"status": "found", "message": "user exits", "data": dumps(result)}
            )
        else:
            return jsonify({"status": "not found", "message": "user not found"})
    except Exception as e:
        return jsonify(
            {"status": "error", "message": "we have some technical issue", "code": e}
        )


# User Section
###############################################################################################################################################

# Producer Section

producer_collection = db["producer"]


@app.route("/p_profile")
def p_profile():
    return render_template("producer/profile.html")


@app.route('/get_delivery_details',methods=['POST'])
def get_delivery_details():
    try:
        unique_id = request.form['unique_id']
        result = batches.find_one({"unique_id": unique_id})
        if result:
            return jsonify({"status": "success", "message": "Data Found", "data": dumps(result)})
        else:
            return jsonify({"status": "error", "message": "Data Not Found"})
    except Exception as e:
        return jsonify({"status": "error", "message": e})


@app.route('/to_ERP_dashboard')
def to_ERP_dashboard():
    return render_template('producer/EPRDashboard.html')

@app.route('/to_epr_report')
def to_epr_report():
    return render_template('producer/EPRReport.html')

@app.route("/mark_dispatched", methods=['POST'])
def mark_dispatched():
    try:
        unique_id = request.form['unique_id']
        result = batches.update_one({"unique_id": unique_id}, {"$set": {"status": "Dispatched"}})
        
        if result.modified_count > 0:
            return jsonify({"status": "success", "message": "Batch Marked 'Dispatched' Successfully"})
        else:
            return jsonify({"status": "error", "message": "Not able to mark 'Dispatched'"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

                       
    
@app.route("/p_sign_in")
def p_sign_in():
    return render_template("producer/sign_in_sign_up.html")


@app.route("/p_sign_up")
def p_sign_up():
    return render_template("producer/sign_in_sign_up.html")


@app.route("/p_to_approved_cc_page")
def p_to_approved_cc_page():
    return render_template("producer/available_cc.html")


@app.route("/p_to_list_item_page")
def p_to_list_item_page():
    return render_template("producer/list_item.html")


@app.route("/p_status", methods=["POST"])
def p_status():
    data = ""
    with open("p_user_data.txt", "r") as file:
        data = json.load(file)
    if data:
        dataId = data["_id"]["$oid"]
        result = producer_collection.find_one({"_id": ObjectId(dataId)})
        return jsonify(
            {"status": "success", "message": "user exists", "data": dumps(result)}
        )
    else:
        return jsonify({"status": "error", "message": "user not exists"})


@app.route("/p_get_cc", methods=["POST"])
def p_get_cc():
    try:
        result = collection_centre.find()
        if result:
            return jsonify(
                {
                    "status": "success",
                    "message": "Collection Centers Found",
                    "data": dumps(result),
                }
            )
        else:
            return jsonify(
                {"status": "error", "message": "Collection Centers Not Found"}
            )

    except Exception as e:
        jsonify({"message": e})


def p_send_sign_up_data(query):
    try:
        result = users_collection.insert_one(query)
        json_result = json_util.dumps(result)
        session["producer_data_id"] = str(json_result.inserted_id)
        return jsonify({"status": "success", "message": str(result.inserted_id)})
    except Exception as e:
        return jsonify({"status": "error", "message": e})


@app.route("/p_search_user_in_database", methods=["POST"])
def p_search_user_in_database():
    try:
        query = {"email": request.form["email"], "password": request.form["password"]}
        result = producer_collection.find_one({"email": request.form["email"]})
        if result:
            return jsonify(
                {
                    "status": "success",
                    "message": "User already exists with this email id",
                }
            )
        else:
            return jsonify({"status": "error", "message": "User not exist"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/p_send_user_data", methods=["POST"])
def p_send_user_data():
    query = {"email": request.form["email"], "password": request.form["password"]}
    try:
        result = producer_collection.insert_one(query)
        return jsonify({"status": "success", "message": "Sign up successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/p_get_batches", methods=["POST"])
def p_get_batches():
    try:
        with open("p_user_data.txt", "r") as file:
            data1 = json.load(file)
        dataId = data1["_id"]["$oid"]
        statuses = ["Received", "Dispatched", "Payment Released"]
        result = batches.find({"producer_id": dataId, "status": {"$in": statuses}})
        if result:
            return jsonify(
                {
                    "status": "success",
                    "message": "Batches Found",
                    "data": dumps(result),
                }
            )
        else:
            return jsonify({"status": "error", "message": "Batches Not Found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/p_get_accepted_batches", methods=["POST"])
def p_get_accepted_batches():
    try:
        with open("p_user_data.txt", "r") as file:
            data1 = json.load(file)
        dataId = data1["_id"]["$oid"]
        statuses = ["Accepted", "Pending", "Rejected"]
        result = batches.find({"producer_id": dataId, "status": {"$in": statuses}})
        if result:
            return jsonify(
                {
                    "status": "success",
                    "message": "Accepted Batches Found",
                    "data": dumps(result),
                }
            )
        else:
            return jsonify({"status": "error", "message": "Accepted Batches Not Found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/p_get_user_data", methods=["POST"])
def p_get_user_data():
    query = {"email": request.form["email"], "password": request.form["password"]}
    result = producer_collection.find_one(query)
    if result:
        with open("p_user_data.txt", "w") as file:
            json_result = json_util.dumps(result)
            file.write(json_result)
        return jsonify({"status": "success", "message": "Sign in successfully"})
    else:
        return jsonify({"status": "error", "message": "Invalid Email or Password"})


@app.route("/p_to_delivery_batch_details")
def p_to_delivery_batch_details():
    return render_template("producer/Delivery_Batch.html")


@app.route("/get_Delivery_batch_data", methods=["POST"])
def get_Delivery_batch_data():
    try:
        unique_id = request.form["unique_id"]
        result = batches.find({"unique_id": unique_id})
        if result:
            return jsonify(
                {
                    "status": "success",
                    "message": "Batch Found",
                    "data": dumps(result),
                }
            )
        else:
            return jsonify({"status": "error", "message": "Batch Not Found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


def generate_alphanumeric(length):
    alphanumeric_characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphanumeric_characters) for _ in range(length))


@app.route("/p_send_user_profile_data", methods=["POST"])
def p_send_user_profile_data():
    data = ""
    dataId = ""
    query = {
        "organization_name": request.form["organization_name"],
        "manager_name": request.form["manager_name"],
        "position": request.form["position"],
        "contact": request.form["contact"],
        "organization_address": request.form["organization_address"],
        "organization_description": request.form["organization_description"],
        "profile_url": request.form["profile_url"],
    }
    with open("p_user_data.txt", "r") as file:
        data = json.load(file)
        dataId = data["_id"]["$oid"]
    filter = {"_id": ObjectId(dataId)}
    update = {"$set": query}
    try:
        result = producer_collection.update_one(filter, update)
        if result.modified_count == 1:
            print("Document updated successfully")
            return jsonify(
                {"status": "success", "message": "Changes made successfully"}
            )
        else:
            print("Document not found or no changes made")
            return jsonify({"status": "error", "message": "Unable to make changes"})
    except Exception as e:
        return jsonify({"status": "error", "message": e})


@app.route("/p_set_listed_product", methods=["POST"])
def p_set_listed_product():
    try:
        unique_id = generate_alphanumeric(12)
        data = {
            "product_category": request.form["product_category"],
            "product_name": request.form["product_name"],
            "product_model": request.form["product_model"],
            "product_specification": request.form["product_specification"],
            "product_baseprice": request.form["product_baseprice"],
            "deductions": request.form["deductions"],
            "product_url": request.form["product_url"],
            "product_instructions": request.form["product_instructions"],
        }
        query = {unique_id: data}
        query1 = {"$set": {"listed_product": query}}
        with open("p_user_data.txt", "r") as file:
            data1 = json.load(file)
        dataId = data1["_id"]["$oid"]
        filter = {"_id": ObjectId(dataId)}
        existing_data = producer_collection.find_one(filter)
        if "listed_product" in existing_data:
            existing_data = existing_data["listed_product"]
            existing_data[unique_id] = data
            query1 = {"$set": {"listed_product": existing_data}}
            result = producer_collection.update_one(filter, query1)
        else:
            print("else")
            result = producer_collection.update_one(filter, query1)
        if result.modified_count == 1:
            print("Document updated successfully")
            return jsonify(
                {"status": "success", "message": "Product Listed Successfully"}
            )
        else:
            print("Document not found or no changes made")
            return jsonify({"status": "error", "message": "Unable to save data"})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify(
            {
                "status": "error",
                "message": "An error occurred while processing the request",
            }
        )


@app.route("/p_get_listed_product", methods=["POST"])
def p_get_listed_product():
    with open("p_user_data.txt", "r") as file:
        data1 = json.load(file)
    dataId = data1["_id"]["$oid"]
    filter = {"_id": ObjectId(dataId)}
    existing_data = producer_collection.find_one(filter)
    existing_data = existing_data["listed_product"]
    if existing_data:
        return jsonify(
            {"status": "success", "message": "Products Found", "data": existing_data}
        )
    else:
        return jsonify({"status": "error", "message": "No Product Found"})


@app.route("/p_get_listed_product_info", methods=["POST"])
def p_get_listed_product_info():
    data = ""
    with open("p_user_data.txt", "r") as file:
        data = json.load(file)
    dataId = data["_id"]["$oid"]
    result = producer_collection.find_one(
        {"_id": ObjectId(dataId)}, {"_id": 1, f"listed_product": 1}
    )
    result = result["listed_product"]
    if result:
        return jsonify(
            {"status": "success", "message": "user exists", "data": dumps(result)}
        )
    else:
        return jsonify({"status": "error", "message": "user not exists"})


@app.route("/listed_product_info_page")
def listed_product_info_page():
    return render_template("producer/listed_item_info.html")


@app.route("/p_approve_cc", methods=["POST"])
def p_approve_cc():
    cc_id = request.form["cc_id"]
    try:
        unique_id = generate_alphanumeric(12)
        query = {unique_id: cc_id}
        query1 = {"$set": {"approve_cc": query}}
        with open("p_user_data.txt", "r") as file:
            data1 = json.load(file)
        dataId = data1["_id"]["$oid"]
        filter = {"_id": ObjectId(dataId)}
        existing_data = producer_collection.find_one(filter)
        if existing_data:
            existing_data["approve_cc"] = query
            query1 = {"$set": {"approve_cc": existing_data["approve_cc"]}}
            result = producer_collection.update_one(filter, query1)
        else:
            query1 = {"$set": {"approve_cc": query}}
            result = producer_collection.update_one(filter, query1)
        if result.modified_count == 1:
            print("Document updated successfully")
            return jsonify({"status": "success", "message": "Approved Successfully"})
        else:
            print("Document not found or no changes made")
            return jsonify({"status": "error", "message": "Unable to Approve"})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify(
            {
                "status": "error",
                "message": "An error occurred while processing the request",
            }
        )


@app.route("/p_get_approved_cc", methods=["POST"])
def p_get_approved_cc():
    data = ""
    list = []
    with open("p_user_data.txt", "r") as file:
        data = json.load(file)
    dataId = data["_id"]["$oid"]
    result = producer_collection.find_one({"_id": ObjectId(dataId)})
    if result:
        result = result["approve_cc"]
        for key in result:
            data = collection_centre.find_one({"_id": ObjectId(result[key])})
            list.append(data)
        return jsonify(
            {"status": "success", "message": "Data found", "data": dumps(list)}
        )
    else:
        return jsonify({"status": "error", "message": "Data not found"})


@app.route("/to_manage_batch_page")
def to_manage_batch_page():
    return render_template("producer/manage_batches.html")


# Producer Section
################################################################################################################################################################################


# COLLECTION CENTER SECTION
################################################################################################################################################################################
collection_centre = db["collection_centre"]
pick_up_patners = db["pick-up patners"]


@app.route("/c_sign_in")
def c_sign_in():
    return render_template("collection_center/sign_in_sign_up.html")


@app.route("/c_profile")
def c_profile():
    return render_template("collection_center/profile.html")


@app.route("/c_sign_out", methods=["POST"])
def c_sign_out():
    with open("c_user_data.txt", "w") as file:
        file.write("")
        return jsonify({"status": "success", "message": "Sign out successfully"})


@app.route("/c_producer_listed_item_page")
def c_producer_listed_item_page():
    return render_template("collection_center/producer_listed_item.html")


@app.route("/create_batch_page")
def create_batch_page():
    return render_template("collection_center/create_and_manage_batch.html")


@app.route("/c_search_user_in_database", methods=["POST"])
def c_search_user_in_database():
    try:
        query = {"email": request.form["email"], "password": request.form["password"]}
        result = collection_centre.find_one({"email": request.form["email"]})
        if result:
            return jsonify(
                {
                    "status": "success",
                    "message": "User already exists with this email id",
                }
            )
        else:
            return jsonify({"status": "error", "message": "User not exist"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/c_Dashboard")
def c_Dashboard():
    return render_template("users/home.html")


@app.route("/add_partner", methods=["POST"])
def add_partner():
    username = request.form["username"]
    name = request.form["name"]
    try:
        with open("c_user_data.txt", "r") as file:
            data = json.load(file)
            dataId = data["_id"]["$oid"]
        query = {"username": username, "name": name, "added_by": dataId}
        result = pick_up_patners.insert_one(query)
        if result.inserted_id:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"})
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/c_list_patners", methods=["POST"])
def c_list_patners():
    try:
        # Read data from file and extract the id
        with open("c_user_data.txt", "r") as file:
            data = json.load(file)
            dataId = data.get("_id", {}).get("$oid")

        if not dataId:
            return jsonify({"status": "error", "message": "Invalid dataId"})

        # Perform the MongoDB query using the correct find() method
        result = pick_up_patners.find({"added_by": dataId})

        # Check if result is not empty
        result_list = list(result)  # Convert cursor to list for dumping
        if result_list:
            return jsonify({"status": "success", "data": dumps(result_list)})
        else:
            return jsonify({"status": "error", "message": "Data not found"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/fetch_pick_up_request", methods=["POST"])
def fetch_pick_up_request():
    try:
        with open("c_user_data.txt", "r") as file:
            data = json.load(file)
            dataId = data["_id"]["$oid"]
        print(dataId)
        result = collection_centre.find_one({"_id": ObjectId(dataId)})
        print(result)
        if result:
            if "pick_up_requests" in result:
                result = result["pick_up_requests"]
                return jsonify(
                    {"status": "success", "message": "Data found", "data": result}
                )
            else:
                return jsonify({"status": "error", "message": "Data not found"})
        else:
            return jsonify({"status": "error", "message": "Data not found"})
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/c_send_user_data", methods=["POST"])
def c_send_user_data():
    query = {"email": request.form["email"], "password": request.form["password"]}
    try:
        result = collection_centre.insert_one(query)
        return jsonify({"status": "success", "message": "Sign up successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/c_assign_patner", methods=["POST"])
def c_assign_patner():
    try:
        request_id = request.form[
            "request_id"
        ]  # ID of the specific pick-up request (e.g., "C4Xil31HTl3o")
        patner_id = request.form["patner_id"]
        data = {"assign_to": patner_id, "status": "Patner Assigned"}

        # Load the collection center ID from the file
        with open("c_user_data.txt", "r") as file:
            file_data = json.load(file)
            cc_id = file_data["_id"]["$oid"]

        result = collection_centre.update_one(
            {"_id": ObjectId(cc_id)},
            {
                "$set": {
                    f"pick_up_requests.{request_id}.assign_to": patner_id,
                    f"pick_up_requests.{request_id}.status": "Patner Assigned",
                }
            },
        )

        # Check if the update was successful
        if result.modified_count > 0:
            return {"status": "success", "message": "Partner assigned successfully"}
        else:
            return {
                "status": "error",
                "message": "Someone is already assigned to this pick-up or request not found",
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.route("/change_status_to_amount_released", methods=["POST"])
def change_status_to_amount_released():
    try:
        request_id = request.form["request_id"]
        result = batches.update_one(
            {"unique_id": request_id}, {"$set": {"status": "Amount Released"}}
        )
        if result.modified_count > 0:
            return jsonify(
                {"status": "success", "message": "Status updated successfully"}
            )
        else:
            return jsonify({"status": "error", "message": "Unable to update status"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/change_status", methods=["POST"])
def change_status():
    try:
        unique_id = request.form["id"]
        status = request.form["status"]
        with open("c_user_data.txt", "r") as file:
            data = json.load(file)
            cc_id = data["_id"]["$oid"]
        result = collection_centre.find_one({"_id": ObjectId(cc_id)})
        if result:
            result = result["pick_up_requests"]
            for item in result:
                if item == unique_id:
                    data = result[item]
                    data["status"] = status
                    result[unique_id] = data
                    result = collection_centre.update_one(
                        {"_id": ObjectId(cc_id)}, {"$set": {"pick_up_requests": result}}
                    )
                    if result.modified_count == 1:
                        return jsonify(
                            {"status": "success", "message": "Status Change"}
                        )
                    else:
                        return jsonify(
                            {"status": "error", "message": "Unable to make changes"}
                        )
        else:
            return jsonify({"status": "error", "message": "Data not Found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/c_get_user_data", methods=["POST"])
def c_get_user_data():
    query = {"email": request.form["email"], "password": request.form["password"]}
    result = collection_centre.find_one(query)
    if result:
        with open("c_user_data.txt", "w") as file:
            json_result = json_util.dumps(result)
            file.write(json_result)
        return jsonify({"status": "success", "message": "Sign in successfully"})
    else:
        return jsonify({"status": "error", "message": "Invalid Email or Password"})


@app.route("/c_send_user_profile_data", methods=["POST"])
def c_send_user_profile_data():
    data = ""
    dataId = ""
    query = {
        "organization_name": request.form["organization_name"],
        "address": request.form["address"],
        "description": request.form["description"],
        "operating_hours": request.form["operating_hours"],
        "contact_number": request.form["contact_number"],
        "email": request.form["email"],
        "charges": request.form["charges"],
        "profile_url": request.form["profile_url"],
    }
    with open("c_user_data.txt", "r") as file:
        data = json.load(file)
        dataId = data["_id"]["$oid"]
    filter = {"_id": ObjectId(dataId)}
    update = {"$set": query}
    try:
        result = collection_centre.update_one(filter, update)
        if result.modified_count == 1:
            print("Document updated successfully")
            return jsonify(
                {"status": "success", "message": "Changes made successfully"}
            )
        else:
            print("Document not found or no changes made")
            return jsonify({"status": "error", "message": "Unable to make changes"})
    except Exception as e:
        return jsonify({"status": "error", "message": e})


@app.route("/c_get_profile", methods=["POST"])
def c_get_profile():
    with open("c_user_data.txt", "r") as file:
        data1 = json.load(file)
    dataId = data1["_id"]["$oid"]
    filter = {"_id": ObjectId(dataId)}
    result = collection_centre.find_one(filter)
    if result:
        return jsonify(
            {"status": "success", "message": "Products Found", "data": dumps(result)}
        )
    else:
        return jsonify({"status": "error", "message": "No Product Found"})


@app.route("/get_listed_product_for_cc", methods=["POST"])
def get_listed_product_for_cc():
    try:
        with open("c_user_data.txt", "r") as file:
            data = file.read()
            data = json.loads(data)
            cc_id = data["_id"]["$oid"]
            print(cc_id)
        list_of_producer = []
        flag = 0
        result = producer_collection.find()
        for item in result:
            if "approve_cc" in item:
                producer_data = item
                approved_cc = item["approve_cc"]
                for key in approved_cc:
                    print(approved_cc[key])
                    if approved_cc[key] == cc_id:
                        flag = 1
                        list_of_producer.append(producer_data)
            else:
                print("approve_cc not found in item")
        if flag == 0:
            return jsonify(
                {"status": "error", "message": "Your are not approved by any producer"}
            )
        else:
            return jsonify(
                {
                    "status": "success",
                    "message": "Data found",
                    "data": dumps(list_of_producer),
                }
            )
    except Exception as e:
        return jsonify({"meaasge": str(e)})


@app.route("/c_create_batch", methods=["POST"])
def c_create_batch():
    try:
        unique_id = request.form["unique_id"]
        data = {
            "batch_name": request.form["batch_name"],
            "unique_id": request.form["unique_id"],
            "description": request.form["description"],
            "date": request.form["date"],
            "brand": request.form["brand"],
            "product_name": request.form["product_name"],
            "product_model": request.form["product_model"],
            "product_category": request.form["product_category"],
            "product_specification": request.form["product_specification"],
            "product_baseprice": request.form["product_baseprice"],
            "producer_id": request.form["producer_id"],
        }
        query = {unique_id: data}
        query1 = {"$set": {"batch_created": query}}
        with open("c_user_data.txt", "r") as file:
            data1 = json.load(file)
        dataId = data1["_id"]["$oid"]
        data["created_by"] = dataId
        result = batches.insert_one(data)
        if result.inserted_id:
            return jsonify(
                {"status": "success", "message": "Batch Created Successfully"}
            )
        else:
            return jsonify({"status": "error", "message": "Batch Creation Failed"})
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/to_batch_details")
def to_batch_details():
    return render_template("/producer/batch_details.html")


@app.route("/c_get_batches", methods=["POST"])
def c_get_batches():
    try:
        with open("c_user_data.txt", "r") as file:
            data = json.load(file)
            cc_id = data["_id"]["$oid"]
        filter = {"created_by": cc_id}
        result = batches.find(filter)
        if result:
            return jsonify(
                {"status": "success", "message": "Data Found", "data": dumps(result)}
            )
        else:
            return jsonify({"status": "error", "message": "Data Not Found"})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"status": "error", "message": str(e)})


@app.route("/c_get_items_for_batch", methods=["POST"])
def c_get_items_for_batch():
    try:
        # Retrieve user data
        with open("c_user_data.txt", "r") as file:
            data = json.load(file)
            cc_id = data["_id"]["$oid"]

        # Fetch brand and category from the request
        brand = request.form["brand"]
        category = request.form["category"]
        product_name = request.form["name"]
        model_name = request.form["model"]
        print(model_name)

        # Aggregation pipeline to filter nested documents within pick_up_requests
        pipeline = [
            {"$match": {"_id": ObjectId(cc_id)}},
            {
                "$project": {
                    "filtered_requests": {
                        "$filter": {
                            "input": {"$objectToArray": "$pick_up_requests"},
                            "as": "request",
                            "cond": {
                                "$and": [
                                    {"$eq": ["$$request.v.brand", brand]},
                                    {"$eq": ["$$request.v.category", category]},
                                    {"$eq": ["$$request.v.product_name", product_name]},
                                    {"$eq": ["$$request.v.model_name", model_name]},
                                    {"$eq": ["$$request.v.status", "Amount Released"]},
                                    {
                                        "$or": [
                                            {
                                                "$not": {
                                                    "$ifNull": [
                                                        "$$request.v.added_to_batch",
                                                        False,
                                                    ]
                                                }
                                            },
                                            {
                                                "$eq": [
                                                    "$$request.v.added_to_batch",
                                                    False,
                                                ]
                                            },
                                        ]
                                    },
                                ]
                            },
                        }
                    }
                }
            },
        ]

        # Execute the query
        result = list(collection_centre.aggregate(pipeline))

        # Check if there are matching requests
        if result and result[0].get("filtered_requests"):
            return jsonify(
                {
                    "status": "success",
                    "message": "Data Found",
                    "data": result[0]["filtered_requests"],
                }
            )
        else:
            return jsonify({"status": "error", "message": "No matching items found"})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"status": "error", "message": str(e)})


@app.route("/c_add_items_to_batch", methods=["POST"])
def c_add_items_to_batch():
    try:
        batch_id = request.form["batch_id"]
        item_id = request.form["item_id"]
        print(item_id)
        filter = {"_id": ObjectId(batch_id)}

        with open("c_user_data.txt", "r") as file:
            data = json.load(file)
            cc_id = data["_id"]["$oid"]

        # Updating collection_center
        cc_result = collection_centre.update_one(
            {"_id": ObjectId(cc_id)},
            {
                "$set": {
                    f"pick_up_requests.{item_id}.added_to_batch": batch_id,
                }
            },
        )

        # Updating batches
        batch_result = batches.update_one(filter, {"$addToSet": {"items": item_id}})

        if cc_result.modified_count > 0 and batch_result.modified_count:
            return jsonify({"status": "success", "message": "Item added successfully"})
        else:
            return jsonify({"status": "error", "message": "Item already added"})
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the error
        return jsonify({"message": str(e)})


################################################################################################################################################################################


@app.route("/recent_batches")
def recent_batches():
    return render_template("collection_center/batches.html")


@app.route("/manage_batches")
def request_for_pick_up():
    return render_template("collection_center/manage_batches.html")


# COLLECTION CENTER SECTION End HERE


##############################################################################################################################
# Batch Managment start here
#######################################################################################################################
batches = db["batches"]


@app.route("/c_send_request", methods=["POST"])
def c_send_request():
    try:
        data = request.form["data"]
        data = json.loads(data)
        print(data)
        with open("c_user_data.txt", "r") as file:
            file_data = file.read()
            file_data = json.loads(file_data)
            cc_id = file_data["_id"]["$oid"]
        data["sender_id"] = cc_id
        batch_id = data["unique_id"]
        for_batch = batches.insert_one(data)
        if for_batch.inserted_id:
            result = collection_centre.find_one(
                {"_id": ObjectId(cc_id)}, {"_id": 1, f"batch_created.{batch_id}": 1}
            )
            result = result["batch_created"][batch_id]
            result["storing_id"] = for_batch.inserted_id
            for_cc = collection_centre.update_one(
                {"_id": ObjectId(cc_id)},
                {"$set": {f"batch_created.{batch_id}": result}},
            )
            if for_cc.modified_count == 1:
                return jsonify(
                    {"status": "success", "message": "Request send successfully"}
                )
            else:
                return jsonify({"status": "error", "message": "Request send failed"})
    except Exception as e:
        print(str(e))
        return jsonify({"message", str(e)})


@app.route("/c_all_batches", methods=["POST"])
def c_all_batches():
    try:
        list_of_batches = []
        with open("c_user_data.txt", "r") as file:
            file_data = file.read()
            file_data = json.loads(file_data)
            cc_id = file_data["_id"]["$oid"]
            result = batches.find({"created_by": cc_id})
            if result:
                for doc in result:
                    list_of_batches.append(doc)
                return jsonify(
                    {
                        "status": "success",
                        "message": "Data Found",
                        "data": dumps(list_of_batches),
                    }
                )
            else:
                print("No Batche found")
                return jsonify({"status": "error", "message": "Data not found"})
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)})


@app.route("/p_fetch_request", methods=["POST"])
def p_fetch_request():
    try:
        list_of_batches = []
        with open("p_user_data.txt", "r") as file:
            file_data = file.read()
            file_data = json.loads(file_data)
            p_id = file_data["_id"]["$oid"]
            result = batches.find({"producer_id": p_id})
            if result:
                for doc in result:
                    list_of_batches.append(doc)
                return jsonify(
                    {
                        "status": "success",
                        "message": "Data Found",
                        "data": dumps(list_of_batches),
                    }
                )
            else:
                print("No Batche found")
                return jsonify({"status": "error", "message": "Data not found"})
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)})


@app.route("/p_set_status_to_approve", methods=["POST"])
def p_set_status_to_approve():
    try:
        doc_id = request.form["doc_id"]
        result = batches.update_one(
            {"_id": ObjectId(doc_id)}, {"$set": {"status": "Approved"}}
        )
        if result.modified_count == 1:
            return jsonify(
                {"status": "success", "message": "Status updated successfully"}
            )
        else:
            return jsonify({"status": "error", "message": "Failed to update status"})
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)})


@app.route("/p_change_batch_status", methods=["POST"])
def p_change_batch_status():
    try:
        unique_id = request.form["unique_id"]
        status = request.form["status"]
        result = batches.update_one(
            {"unique_id": unique_id}, {"$set": {"status": status}}
        )
        if result:
            return jsonify(
                {"status": "success", "message": "Status updated successfully"}
            )
        else:
            return jsonify({"status": "error", "message": "Failed to update status"})
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/p_all_batches", methods=["POST"])
def p_all_batches():
    try:
        list_of_batches = []
        with open("p_user_data.txt", "r") as file:
            file_data = file.read()
            file_data = json.loads(file_data)
            p_id = file_data["_id"]["$oid"]
            result = batches.find({"producer_id": p_id})
            if result:
                for doc in result:
                    list_of_batches.append(doc)
                return jsonify(
                    {
                        "status": "success",
                        "message": "Data Found",
                        "data": dumps(list_of_batches),
                    }
                )
            else:
                print("No Batche found")
                return jsonify({"status": "error", "message": "Data not found"})
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)})


@app.route("/c_get_batch_for_quotation", methods=["POST"])
def c_get_batch_for_quotation():
    try:
        batch_id = request.form["batch_id"]
        filter = {"_id": ObjectId(batch_id)}
        result = batches.find_one(filter)
        if result:
            return jsonify({"status": "success", "data": dumps(result)})
        else:
            return jsonify({"status": "error", "message": "Such Batch Not Found"})
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/get_quotation", methods=["POST"])
def get_quotation():
    try:
        batch_id = request.form["batch_id"]
        filter = {"unique_id": batch_id}
        result = batches.find_one(filter, {"quotation_data": 1})
        if result:
            return jsonify({"status": "success", "data": dumps(result)})
        else:
            return jsonify({"status": "error", "message": "Such Batch Not Found"})
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/finalize_quotation", methods=["POST"])
def finalize_quotation():
    try:
        data = request.get_json()  # Get the JSON data from the request
        batch_id = data.get("batch_id")
        quotation_data = data.get("quotation_data")
        filter = {"unique_id": batch_id}
        result = batches.update_one(
            filter, {"$set": {"status": "Accepted", "quotation_data": quotation_data}}
        )

        if result.modified_count == 1:
            return jsonify({"status": "success", "message": "Quotation Confirmed"})
        else:
            return jsonify(
                {"status": "error", "message": "Failed to confirm Quotation"}
            )
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/c_get_batch_cost", methods=["POST"])
def c_get_batch_cost():
    data = request.json  # Get the JSON data
    items = data.get("items", [])  # Safely get items, default to empty list
    cc_id = data.get("cc_id")
    total_amount = 0
    # MongoDB aggregation pipeline
    pipeline = [
        {"$match": {"_id": ObjectId(cc_id)}},  # Match the document by cc_id
        {
            "$project": {
                "matching_requests": {
                    "$objectToArray": "$pick_up_requests"  # Convert the pick_up_requests to an array of key-value pairs
                }
            }
        },
        {
            "$project": {
                "filtered_requests": {
                    "$filter": {
                        "input": "$matching_requests",
                        "as": "request",
                        "cond": {
                            "$in": [
                                "$$request.k",
                                items,
                            ]  # Filter based on the requested items
                        },
                    }
                }
            }
        },
        {
            "$replaceRoot": {
                "newRoot": {
                    "$arrayToObject": "$filtered_requests"  # Convert the filtered array back to an object
                }
            }
        },
    ]

    result = list(collection_centre.aggregate(pipeline))

    if result:
        for item in result:
            for key in item:
                deduce_amount = item[key].get(
                    "deduce_amount", 0
                )  # Get the deduce_amount
                # Convert to float to avoid TypeError if it's a string
                try:
                    total_amount += float(deduce_amount)
                except ValueError:
                    print(
                        f"Warning: Could not convert deduce_amount '{deduce_amount}' to float."
                    )
        return jsonify({"status": "success", "data": total_amount})
    else:
        return jsonify(
            {"status": "error", "message": "No matching pick-up requests found."}
        )


@app.route("/c_change_status", methods=["POST"])
def c_change_status():
    try:
        batch_id = request.form["batch_id"]
        status = request.form["status"]
        result = batches.update_one(
            {"unique_id": batch_id}, {"$set": {"status": status}}
        )
        if result.modified_count == 1:
            return jsonify(
                {"status": "success", "message": "Status Update Successfully"}
            )
        else:
            return jsonify({"status": "error", "message": "Unable to Status Update "})
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)})


@app.route("/c_get_producer_sender_details", methods=["POST"])
def c_get_producer_sender_details():
    try:
        producer_id = request.form.get("producer_id")
        cc_id = request.form.get("cc_id")

        projection1 = {
            "organization_name": 1,
            "organization_address": 1,
            "manager_name": 1,
            "contact": 1,
            "_id": 0,
        }
        projection2 = {
            "organization_name": 1,
            "address": 1,
            "contact_number": 1,
            "_id": 0,
        }

        # Query producer details
        producer_result = producer_collection.find_one(
            {"_id": ObjectId(producer_id)}, projection1
        )

        if producer_result:
            # Query collection centre details
            cc_result = collection_centre.find_one(
                {"_id": ObjectId(cc_id)}, projection2
            )

            if cc_result:
                return jsonify(
                    {"status": "success", "data1": producer_result, "data2": cc_result}
                )
            else:
                return jsonify(
                    {"status": "error", "message": "Collection centre not found"}
                )

        else:
            return jsonify({"status": "error", "message": "Producer not found"})

    except Exception as e:
        # Log the exception (you could replace this with actual logging)
        print(f"Error in c_get_producer_sender_details: {str(e)}")
        return jsonify(
            {
                "status": "error",
                "message": "An error occurred while processing your request",
            }
        )


@app.route("/send_quotation", methods=["POST"])
def send_quotation():
    try:
        # Retrieve JSON data
        data = request.get_json()
        quotation_data = data["quotation_data"]
        batch_id = quotation_data["batch_id"]

        # Update the document with $set operator
        result = batches.update_one(
            {"unique_id": batch_id},
            {"$set": {"status": "Pending", "quotation_data": quotation_data}},
        )

        if result.modified_count > 0:
            return jsonify(
                {"status": "success", "message": "Quotation sent successfully"}
            )
        else:
            return jsonify({"status": "error", "message": "Already send"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/p_change_status", methods=["POST"])
def p_change_status():
    try:
        batch_id = request.form["batch_id"]
        status = request.form["status"]
        result = batches.update_one(
            {"unique_id": batch_id}, {"$set": {"status": status}}
        )
        if result.modified_count == 1:
            return jsonify(
                {"status": "success", "message": "Status Update Successfully"}
            )
        else:
            return jsonify({"status": "error", "message": "Status is already updated with the same"})
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)})


########################################################################################################################
#############Pick-up Patner Section###########################################################################################################
@app.route("/find_pick_up_patner", methods=["POST"])
def find_pick_up_patner():
    username = request.form["username"]
    result = pick_up_patners.find_one({"username": username})
    if result:
        data = json_util.dumps(result)
        with open("pick-up_patner_data.txt", "w") as file:
            file.write(data)
        return jsonify({"status": "success", "data": dumps(result)})
    else:
        return jsonify({"status": "error", "message": "No User Found"})


@app.route("/login")
def login():
    return render_template("/pick_patner/login.html")


@app.route("/pick_up_home")
def pick_up_home():
    return render_template("/pick_patner/home.html")


@app.route("/pp_sign_out", methods=["POST"])
def pp_sign_out():
    with open("pick-up_patner_data.txt", "w") as file:
        file.write("")
    return jsonify({"status": "success"})


@app.route("/pp_fetch_request", methods=["POST"])
def pp_fetch_request():
    try:
        with open("pick-up_patner_data.txt", "r") as file:
            file_data = file.read()
            file_data = json.loads(file_data)
            pp_id = file_data["_id"]["$oid"]
            cc_id = file_data["added_by"]
        pipeline = [
            {"$match": {"_id": ObjectId(cc_id)}},
            {
                "$project": {
                    "filtered_requests": {
                        "$filter": {
                            "input": {"$objectToArray": "$pick_up_requests"},
                            "as": "request",
                            "cond": {
                                "$and": [
                                    {"$eq": ["$$request.v.status", "Patner Assigned"]},
                                ]
                            },
                        }
                    }
                }
            },
        ]
        result = list(collection_centre.aggregate(pipeline))
        if result and result[0].get("filtered_requests"):
            return jsonify(
                {
                    "status": "success",
                    "message": "Data Found",
                    "data": dumps(result[0]["filtered_requests"]),
                }
            )
        else:
            return jsonify({"status": "error", "message": "No matching items found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/to_pick_up_details")
def to_pick_up_details():
    return render_template("/pick_patner/details.html")


@app.route("/get_pick_up_details", methods=["POST"])
def get_pick_up_details():
    cc_id = request.form["cc_id"]
    request_id = request.form["request_id"]
    result = collection_centre.find_one(
        {
            "_id": ObjectId(cc_id),  # Matching the document with the provided cc_id
            f"pick_up_requests.{request_id}": {
                "$exists": True
            },  # Checking if the request_id exists in pick_up_requests
        }
    )
    if result:
        found_object = result["pick_up_requests"].get(request_id)
        if found_object:
            return jsonify({"status": "success", "data": dumps(found_object)}), 200
        else:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"Request ID '{request_id}' not found in pick_up_requests",
                    }
                ),
                404,
            )
    else:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Document with the given 'cc_id' not found",
                }
            ),
            404,
        )


@app.route("/pp_confirm_pick_up", methods=["POST"])
def pp_confirm_pick_up():
    try:
        # Get parameters from request
        cc_id = request.form["cc_id"]
        request_id = request.form["request_id"]
        status = request.form["status"]

        # Update the status in the nested pick_up_requests object
        result = collection_centre.update_one(
            {
                "_id": ObjectId(cc_id),
                f"pick_up_requests.{request_id}": {"$exists": True},
            },
            {"$set": {f"pick_up_requests.{request_id}.status": status}},
        )

        # Check the update result
        if result.modified_count == 1:
            return jsonify({"status": "success"})
        else:
            return jsonify(
                {
                    "status": "error",
                    "message": "Pick-up request not found or already updated.",
                }
            )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


#############Pick-up Patner Section###########################################################################################################

@app.route('/get_ewaste_metrics', methods=['GET'])
def get_ewaste_metrics():
    try:
        # Logging the start of the endpoint
        print("Starting /get_ewaste_metrics endpoint...")

        # Calculate total e-waste collected
        total_ewaste_collected = 0
        batches = db.batches.find()  # Fetch all batches
        print("Fetched batches:", batches)
        
        for batch in batches:
            items = batch.get("items", [])
            for item_id in items:
                # Fetch the item's weight from collection_centre
                item_data = db.collection_centre.find_one({"pick_up_requests." + item_id: {"$exists": True}})
                print("Item Data for", item_id, ":", item_data)
                if item_data:
                    item = item_data["pick_up_requests"].get(item_id)
                    if item:
                        total_ewaste_collected += float(item.get("weight", 0))
        print("Total e-waste collected:", total_ewaste_collected)

        # Step 1: Initialize a variable to calculate total and compliant batches
        total_batches = 0
        compliant_batches = 0

        # Step 2: Get all batches, then calculate compliance based on `compliance_status`
        batches = db.batches.find()  # Fetch all batches
        for batch in batches:
            # Check the producer_id for the batch
            producer_id = batch.get("producer_id")
            if producer_id:
                # Increment total batches
                total_batches += 1
                # Check if the batch is compliant
                compliance_status = batch.get("compliance_status")
                if compliance_status == "compliant":
                    compliant_batches += 1

        # Step 3: Calculate the compliance rate
        compliance_rate = 0
        if total_batches > 0:
            compliance_rate = (compliant_batches / total_batches) * 100
        
        print(f"Total Batches: {total_batches}, Compliant Batches: {compliant_batches}")
        print(f"Compliance Rate: {compliance_rate}%")

        # E-waste processed in the last 4 months
        current_date = datetime.now()

# Calculate the date for 4 months ago (rough estimate, assuming 30 days per month)
        four_months_ago = current_date - timedelta(days=4*30)

# Initialize the processed e-waste total
        ewaste_processed_last_4_months = 0

# Query for batches processed in the last 4 months, ensuring that 'processed_weight' exists
        processed_batches = db.batches.find({
            "date": {"$gte": four_months_ago, "$lt": current_date},
            "processed_weight": {"$exists": True}  # Ensure the processed_weight field exists
        })

# Sum up the weights for the previous 4 months
        for batch in processed_batches:
    # Add the processed_weight to the total for this batch
            ewaste_processed_last_4_months += float(batch.get("processed_weight", 0))

# Print the result
        print("E-waste processed in the last 4 months:", ewaste_processed_last_4_months)

        
        # Return metrics as JSON response
        return jsonify({
            "status": "success",
            "total_ewaste": total_ewaste_collected,
            "compliance_rate": round(compliance_rate, 2),
            "processed_this_month": ewaste_processed_last_4_months
        })

    except Exception as e:
        print("Error in /get_ewaste_metrics:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
