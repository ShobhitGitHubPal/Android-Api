
from flask import Flask, request, jsonify , make_response, send_file,render_template
from functools import wraps
from pymongo import MongoClient
from bson import ObjectId
import math
import random
import datetime
import re
import bcrypt
import smtplib
import pymongo
import os
import jwt
from twilio.rest import Client

from flask_mail import Mail, Message
from uuid import uuid4
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['ACCOUNT_SID'] = 'AC5f88040e6854cb8c340f77e38e03970d',
app.config['ACCESS_KEY'] = 'f539a994081b7ca5e327827c48bf1b15',
app.config['TWILIO_PHONE_NUMBER'] = "+12565888672"

message_service = Client('AC5f88040e6854cb8c340f77e38e03970d', 'f539a994081b7ca5e327827c48bf1b15')

client = MongoClient("mongodb://localhost:27017")
db = client['Game']
collection = db['game_get']
signup_data = db['signup']
reporting_data = db['reporting']
version_data = db['version']


frindUserColl = db['friendUser']
deletedSignup = db['deletedSignup']
feedback_collection=db['feedback_collection']
Add_Friends = db['Add_Friends']
balance_data = db['update_balance']

################### mail #############################################################################

app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USERNAME'] = 'shobhit.pal@fourbrick.com' 
app.config['MAIL_PASSWORD'] = 'qdve zeva rvuc iecp'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
######################### stop mail ################################################################
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[-1]
            # print(token,"dasgfhgfsahgdfsahgd")

        if not token:
            return jsonify({"message": " valid token is missing" ,'status':400})

        try:
            data = jwt.decode(
                token,
                algorithms="HS512",
                key="GameDev",
            )
            # print("dsifhsdkuhfkusdhfkuhsd", data)

            aggr = [
                {
                    '$match': {
                        '_id': ObjectId(data['userId'])
                    }
                }, {
                    '$addFields': {
                        '_id': {
                            '$toString': '$_id'
                        }
                    }
                }
            ]
            
            current_user = list(signup_data.aggregate(aggr))
            
            database_data = len(current_user)

            if database_data == 0:
                return jsonify({"message": "Token is invalid",'status':400})

        except Exception as e:
            return jsonify({"message": "Token is invalid",'status':400})
        return f(current_user[0], *args, **kwargs)

    return decorator



####################### signup page ####################################################
@app.route("/signup", methods=['POST'])
def signup():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get("email")
        password = request.form.get("password")
        mobile = request.form.get("mobile")
        country = request.form.get("country")
        gender = request.form.get("gender")
        city = request.form.get("city")
        email_exist = signup_data.find_one({"email":email})
        phone_exist = signup_data.find_one({"mobile":mobile})

        if email_exist:
            return jsonify({"message":"Email is already exist",'status':400})
        if phone_exist:
            return jsonify({"message":"Phone no. is already exist",'status':400})
        otp = random.randint(1000, 9999)
        try:
            msg = Message("OTP for Registration", sender='shohit.pal@fourbrick.com', recipients=[email])
            msg.body = f"Your OTP for registration is: {otp}"
            mail.send(msg)
            print(otp,'otp')
            
        except Exception as e:
            print(e)
            return jsonify({"message": "Error sending OTP.",'status':400}), 500
        data = {
            "name":name,
            "email":email,
            "password":password,    
            "mobile":mobile,
            "country":country,
            "gender":gender,
            "city":city,
            "profile_icon":0,
            "kill_count":0,
            "death_count":0,
            "match_count":0,
            "win_count":0,
            "xp":0,
            "level":0,
            "total_coins":0,
            "total_diamonds":0,
            "verified":False,
            "OTP": otp,
        }
        signup_data.insert_one(data)
        return jsonify({"message": "Registration successful. Please check your email for OTP.",'status':200})

###################################################################################################################

############ verify #####################################################################################
@app.route("/verify", methods=['POST','GET'])
def verify():
    if request.method=='POST':
        email=request.form.get('email')
        input_otp=request.form.get('input_otp')
        user_data = signup_data.find_one({"email": email})
        print(user_data,'user_data')
        stored_otp = user_data.get("OTP") if user_data else None
        print(stored_otp)
        if email and stored_otp:
            if stored_otp is not None and input_otp == str(stored_otp):
                
                user_data = signup_data.update_one({"email": email}, {"$set": {"verified": True}})
                return jsonify({"message": "OTP verification successful.",'status':200})
            else:
                return jsonify({"message": "Invalid OTP.",'status':400}) 
        else:
            return jsonify({
                'message':'Email or OTP is invalid','status':400
            })
    else:
        return jsonify({
            'message':'Invalid request'
        })
#################### stop verify ##################################################

####################### resend code ###############################################################
@app.route("/resend_code", methods=['POST'])
def resend_code():
    email = request.form.get("email")

    new_otp = random.randint(1000, 9999)

    signup_data.update_one({"email": email}, {"$set": {"OTP": new_otp,"verifying_link":str(uuid4())}})

    try:
        msg = Message("OTP for Registration", sender='shohit.pal@fourbrick.com', recipients=[email])
        msg.body = f"Your OTP for registration is: {new_otp}"
        mail.send(msg)
        print(new_otp,'otp')
        
    except Exception as e:
        print(e)
        return jsonify({"message": "Error sending OTP.",'status':400})

    return jsonify({"message": "New OTP sent successfully.",'status':200})


@app.route("/resend_code_link", methods=['POST'])
def resend_code_link():
    email = request.form.get("email")

    new_otp = random.randint(1000, 9999)

    verifying_link=str(uuid4())

    signup_data.update_one({"email": email}, {"$set": {"OTP": new_otp,"verifying_link":verifying_link}})

    try:
        msg = Message("Password Reset Link", sender='shohit.pal@fourbrick.com', recipients=[email])
        msg.body = f"Your Link for Reset Password {verifying_link} <a href='{verifying_link}'>Verify Link</a>"
        mail.send(msg)
        print(new_otp,'otp')
        
    except Exception as e:
        print(e)
        return jsonify({"message": "Error sending OTP.",'status':400}), 500

    return jsonify({"message": "Password Reset Link Check Your Mail.",'status':200})
########################## stopResendcode###################################################################################


###############################################################################################################################
#################### login ################################################################################################################
@app.route("/login", methods=['POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")


        user_data = signup_data.find_one({"email": email,'password':password})
        print(user_data)
        if user_data:
            if user_data['verified']:

                if str(user_data['password']) == str(password):
                    user_data['_id'] = str(user_data['_id'])
                    del user_data['password']
                    access_token = jwt.encode(
                        {
                            "userDetails": user_data, "userId": user_data["_id"]
                        },
                        key="GameDev",
                        algorithm="HS512",
                    )
                    response = make_response(
                        jsonify({"token": access_token, "user": user_data})
                    )
                    response.set_cookie(
                        "token",
                        access_token,
                        # secure=True,
                        httponly=True,
                        samesite=None,

                    )  
                    data = jwt.decode(
                    access_token,
                    algorithms="HS512",
                    key="GameDev",
                )
                    return jsonify({"message":"Login successful." , "token":access_token,"token_Data":data ,'status':200})
                
            else:
                return jsonify({"message":"User Not Verified.",'status':400})
        else:
            return jsonify({"message":"Email or Password wrong...",'status':400})
        
    else:
        return jsonify({"message":"Email not found. Please register first.",'status':400})
        
##########################################################################################################################

########## Forget password #####################################################################################
# @app.route("/forgot_password", methods=['PUT','GET','POST'])
# def forgot_password():

#     if request.method == "POST":
#         email = request.form.get("email")  
#         new_password = request.form.get("new_password")
#         verify_link = request.form.get("verify_link")
        

#         user_data = list(signup_data.find({"email": email}))

#         if user_data:
#             if(user_data[0]["verifying_link"]==verify_link):
#                 signup_data.update_one({"email": email}, {"$set": {"password": new_password,"verifying_link":""}})
                
#                 return jsonify({
#                     "message": "Password updated successfully."
#                 })
#             else:
#                 return jsonify({
#                     "message": "Verify Link is not Valid."
#                 })
#         else:
#             return jsonify({
#                 "message": "Email not found in the database."
#             })
#     else:
#         return jsonify({
#             "message": "Invalid request."
#         })



@app.route("/forgot_password", methods=['PUT','GET','POST'])
def forgot_password():

    if request.method == "POST":
        email = request.form.get("email")  
       
        user_data = signup_data.find_one({"email": email})
        print(user_data,'user_data1')
        
        if user_data:           
            otp = random.randint(1000, 9999)
            try:
                msg = Message("OTP for Reset password", sender='shohit.pal@fourbrick.com', recipients=[email])
                msg.body = f"Your OTP for Reset password is: {otp}"
                mail.send(msg)
                print(otp,'otp')
                signup_data.update_one({"email": email}, {"$set": {"OTP": otp}})
                
                return jsonify({"message": "Send OTP Successfull.",'status':200})
            except Exception as e:
                print(e)
                return jsonify({"message": "Error sending OTP.",'status':400})
            
        else:
            return jsonify({
                "message": "Email invalid.",'status':400
            })
    else:
        return jsonify({
            "message": "Invalid request.",'status':400
        })
################# stop Forget password ###################################################################################
################# new password ###################################################################################
@app.route("/new_password", methods=['PUT','GET','POST'])
def new_password():
    if request.method == "POST":
        email = request.form.get("email")  
        new_password = request.form.get("new_password")
        # verify_link = request.form.get("verify_link")
        input_otp = request.form.get("input_otp")

        user_data = signup_data.find_one({"email": email},{'OtP':input_otp})
        print(user_data)
        if user_data:
            # verifying_otp = user_data.get("OTP")
        # # if user_data:
        # #     if(user_data[0]["verifying_otp"]==input_otp):
            # if verifying_otp and verifying_otp ==(input_otp):
            signup_data.update_one({"email": email}, {"$set": {"password": new_password,"verified":True}})
            
            return jsonify({
                "message": "Password updated successfully.",'status':200
            })
            # else:
            #     return jsonify({
            #         "message": "Verify otp is not Valid.",'status':400
            #     })
        else:
            return jsonify({
                "message": "Email not found.",'status':400
            })
    else:
        return jsonify({
            "message": "Invalid request.",'status':400
        })
#################stop new password ########################################################################new

########### Delete Account ##############################################################################################
@app.route("/delete_account", methods=['POST', 'GET'])
@token_required
def Delete_Account(current_user):
    user_id = current_user.get("_id")
    email=request.form.get('email')
    print(email)
    if user_id:
        dataAll = signup_data.find_one({"_id": ObjectId(user_id)})
        print(dataAll,'dataAll')
        
        if dataAll:
            em = dataAll.get("email") 
            print(email,'email')
            if email == em:
                otp =str( random.randint(1000, 9999))
                try:
                    msg = Message("OTP for Delete Account", sender='shohit.pal@fourbrick.com', recipients=[email])
                    msg.body = f"Your OTP for Delete Account is: {otp}"
                    mail.send(msg)
                    print(otp, 'otp')
                    signup_data.update_one({"email": email}, {"$set": {"OTP": otp}})

                    return jsonify({"message": "Send OTP Successfully And Check your email.",'status':200})
                except Exception as e:
                    print(e)
                    return jsonify({"message": "Error sending OTP.",'status':400})
            else:
                return jsonify({"message": "Email address not found .",'status':400})
        else:
            return jsonify({"message": "User data not found.",'status':400})
    else:
        return jsonify({"message": "user_id not found.",'status':400})







    # print("current_user",current_user["_id"])
    # dataAll=signup_data.find_one({"_id":ObjectId(current_user["_id"])})
    # dataAll["oldId"]=dataAll["_id"]
    # del dataAll["_id"]
    # deletedSignup.insert_one({"_id":ObjectId(current_user["_id"])})
    # signup_data.delete_one({"_id":ObjectId(current_user["_id"])})
    # return jsonify({
    #     "message": "Delete account successfully."
    # })

@app.route("/confirm_delete_account", methods=['POST', 'DELETE'])
@token_required
def confirm_delete_account(current_user):
    user_data = signup_data.find_one({"_id": ObjectId(current_user["_id"])})
    print(current_user,'current_user') 
    email = request.form.get("email") 
    password = request.form.get("password")
    input_otp = request.form.get("input_otp")
    print(email,password,input_otp,'email')
    data = signup_data.find_one({"email": email, 'password': password,'OTP':input_otp})
    print(user_data,'user_data')
    print(user_data['email'] ,email,password,input_otp,'user_data')
    if request.method == "DELETE":
        # return "KDSHFGSDJFH"
        try:
            if user_data['email'] == email and user_data['password'] == password and user_data['OTP'] == input_otp:
                #33  user_data['email']==email and user_data['password']==password and    and user_data['OTP']==input_otp
                print('yes')
                # if request.method == 'DELETE':
                deletedSignup.insert_one({"_id":ObjectId(current_user["_id"])})
                signup_data.delete_one({"_id": ObjectId(current_user["_id"])})
                return jsonify({
                    "message": "Delete account successfully.",'status':200
                })
            else:
                return jsonify({
                    "message": "Input data invalid",'status':400
                })
        except Exception as e:
            return e
    else:
        return jsonify({
            "message": "invalid request",'status':400
        }), 404
# else:
#     return jsonify({
#         'message': 'Invalid request.'
#     }), 400
    


@app.route("/viewProfile", methods=['GET'])
@token_required
def viewProfile(current_user):

    print("current_user",current_user["_id"])

    
    arra=[{
            '$match': {
                '_id': ObjectId(current_user["_id"])
            }
        }
        # {
        #     '$project': {
        #         '_id': 0, 
        #         'name': '$name', 
        #         'email': '$email', 
        #         'password': '$password', 
        #         'mobile': '$mobile', 
        #         'country': '$country', 
        #         'Gender': '$gender', 
        #         'City': '$city', 
        #         'profile_icon': '$profile_icon', 
        #         'kill_count': '$kill_count', 
        #         'death_count': '$death_count', 
        #         'match_count': '$match_count', 
        #         'win_count': '$win_count', 
        #         'xp': '$xp', 
        #         'level': '$level', 
        #         'total_coins': '$total_coins', 
        #         'total_diamonds': '$total_diamonds',
        #         "profile":"$profile"
        #     }
        # }
        ,{
            "$project":{
                "_id":0
            }
        }
    ]
    dataAll=list(signup_data.aggregate(arra))
    return jsonify({
        "message": "View Profile.",'status':200,
        "data":dataAll[0]
    })
############### stop Delete_Account ##############################################################################################



UPLOAD_FOLDER = os.path.join('uploads')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
############### Update Profile #####################################################
@app.route("/profile_images/<icon>", methods=['GET'])
def profile_images(icon):
    return send_file(os.path.join(os.getcwd(),"profile_images",icon))


@app.route("/update_profile", methods=['POST'])
@token_required
def Update_Profile(current_user):
    # print(current_user,'kkkk')
    user_id = current_user.get("_id")
    current_user_email = current_user.get("email") 
    print(user_id,'user_id')
    if request.method == "POST":
        user_id = current_user.get("_id")
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        # profile_icon=None
        profile_icon_name=None
        if("profile_icon" in request.files):
            profile_icon=request.files["profile_icon"]
            filename = secure_filename(profile_icon.filename)
            # filename = secure_filename(profile_icon.filename)
            # profile_icon_name=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profile_icon_name = os.path.join(UPLOAD_FOLDER,filename)

            profile_icon.save(profile_icon_name)
        
        
        user_data = signup_data.find_one({"_id": ObjectId(current_user["_id"])})
        
        if (email!=user_data["email"]) or (mobile!=user_data["mobile"]):
        
            otp = random.randint(1000, 9999)
            try:
                msg = Message("OTP for update_profile", sender='shohit.pal@fourbrick.com', recipients=[current_user_email])
                msg.body = f"Your OTP for update_profile is: {otp}"
                mail.send(msg)
                print(otp, 'otp')
                signup_data.update_one({"_id": ObjectId(current_user["_id"])}, {"$set": {"OTP": otp}})
                # signup_data.update_one({"email": email}, {"$set": {"OTP": otp}})
                # return data

                update_data={
                    
                    'tempEmail':email,
                    'tempMobile':mobile
                }

                if(profile_icon_name!=None):
                    update_data["profile_icon"]=profile_icon_name

                signup_data.update_one({"_id": ObjectId(current_user["_id"])}, {"$set": update_data})
                return jsonify({"message": "Send OTP Successfully And Check your email.",'status':200})
            except Exception as e:
                print(e)
                return jsonify({"message": "Error sending OTP.",'status':400})
        else:
            print('no')
            update_data={
                        'name':name,
                    }
            
            
            if(profile_icon_name!=None):
                update_data["profile_icon"]=profile_icon_name

            signup_data.update_one({"_id": ObjectId(current_user["_id"])}, {"$set": update_data})
            return jsonify({
                'message':'Update profile successfull','status':200
            })
            
    else:
        return jsonify({
            'message':'Invalid request','status':400
        })
        
@app.route("/confirm_update_profile", methods=['POST'])
@token_required
def confirm_update_profile(current_user):
    # print(current_user,'current user')
    if request.method=='POST':
        user_id = current_user.get("_id")
        print(user_id,'user_id')
        input_otp=request.form.get('input_otp')
        user_data = signup_data.find_one({"_id": ObjectId(user_id)})
        
        if user_data and user_data['OTP'] == int(input_otp):

            # curr_email = user_data['tempEmail']
            # curr_mobile = user_data['tempMobile']

            curr_email = user_data['tempEmail']
            curr_mobile = user_data['tempMobile']

            print(curr_email,'curr_email')
            
            update_data = {
                'email': curr_email,  
                'mobile': curr_mobile,
                'tempEmail': '',
                'tempMobile': ''
            } 
            signup_data.update_one({"_id": ObjectId(user_id)},{"$set": update_data})
            
            return jsonify({
                "message": "Profile Update Sucessfully.",'status':200
            }),200
        else:
            return jsonify({
                'message':'Invalid otp','status':400
            })
    else:
        return jsonify({
            'message':'Invalid request'
        })
    
    # name = request.form.get('name')
    # # email = request.form.get("email")
    # profile_icon=None
    # if("profile_icon" in request.files):
    #     profile_icon=request.files["profile_icon"]
    #     filename = secure_filename(profile_icon.filename)
    #     filename = secure_filename(profile_icon.filename)

    #     profile_icon_name=os.path.join(app.config['UPLOAD_FOLDER'], filename)

    #     profile_icon.save(profile_icon_name)
    # password = request.form.get("password")


    # user_data = signup_data.find_one({"_id": ObjectId(current_user["_id"])})

    

    # new_otp = random.randint(1000, 9999)
    
    # # try:
    # #     msg = Message("Password OTP", sender='shohit.pal@fourbrick.com', recipients=[email])
    # #     msg.body = f"Your OTP Send to Email {new_otp} <a href='{new_otp}'>Verify Link</a>"
    # #     mail.send(msg)
    # #     print(new_otp,'otp')
        
    # # except Exception as e:
    # #     print(e)
    # #     return jsonify({"message": "Error sending OTP."}), 500

    # if user_data:
    #     update_data={}

    #     print(password)
    #     if(password):
    #         update_data["password"]=password
    #     if(profile_icon):
    #         update_data["profile_icon"]=profile_icon_name
    #     if(name):
    #         update_data["name"]=name

    #     signup_data.update_one({"_id": ObjectId(current_user["_id"])}, {"$set": update_data})
    #     return jsonify({
    #         "message": "Profile Update Sucessfully."
    #     }),200
    # else:
    #     return jsonify({
    #         "message": "Email not found in the database. Profile not updated."
    #     }),400
####################### stop Update Profile######################################################



# @app.route("/updateStats", methods = ['POST'])
# @token_required
# def updateStats(current_user):
#     if request.method == "POST":
#         kill_count=request.form.get("Kill_Count ")
#         death_count=request.form.get("Death_Count")
#         win_count=request.form.get("Win_Count")
#         match_count=request.form.get("Match_Count")
#         xp=request.form.get("Xp")
#         level=request.form.get("Level")
        
#         updateBy={"_id":ObjectId(current_user['_id'])}
#         print(updateBy)
#         data={
#             "kill_count":kill_count,
#             "death_count":death_count,
#             "win_count":win_count,
#             "match_count":match_count,
#             "xp":xp,
#             "level":level
#         }
#         bb=signup_data.update_one(updateBy,{"$set":data})
#         print(bb,'khjguu')
#         return jsonify({"message":"Successfully Updated all informations of the user",'status':200})
#     else:
#         return jsonify({"message":"Invalid request",'status':400})

@app.route("/update_stats", methods=['POST'])
@token_required
def update_stats(current_user):
    if request.method == 'POST':
        level = request.form.get('level')
        xp = request.form.get('xp')
        kill_count = request.form.get('kill_count')
        death_count = request.form.get('death_count')
        win_count = request.form.get('win_count')
        match_count = request.form.get('match_count')
        
        update_data = {
            'level': level,
            'xp': xp,
            'kill_count': kill_count,
            'death_count': death_count,
            'win_count': win_count,
            'match_count': match_count
        }
        
        user_id = current_user.get('_id')
        result = signup_data.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
        
        if result.modified_count > 0:
            return jsonify({"message": "Statistics updated successfully.",'status':200})
        else:
            return jsonify({"message": "Failed to update statistics.",'status':400})
    else:
        return jsonify({"message": "Invalid request method.",'status':400})




@app.route("/verify_update", methods=['POST'])
@token_required
def verify_update(current_user):
    
    print("current_user",current_user["_id"])
    name = request.form.get('name')
    email = request.form.get("email")
    password = request.form.get("password")
    OTP = request.form.get("OTP")



    user_data = signup_data.find_one({"_id": ObjectId(current_user["_id"])})

    if user_data:

        if(user_data["OTP"]==OTP):
                
            update_data = {
                "name": name,
                "password": password,
                "email":email
            }
            signup_data.update_one({"_id": ObjectId(current_user["_id"])}, {"$set": update_data})
            return jsonify({
                "message": "Profile updated successfully.",'status':200
            })
        else:
            
            return jsonify({
                "message": "Please Check OTP.",'status':400
            })
    else:
        return jsonify({
            "message": "Email not found in the database. Profile not updated.",'status':400
        })



@app.route("/search_friends", methods = ['POST'])
@token_required
def Search_friends(current_user):
    Userid = request.form.get('Userid')
    Name = request.form.get('Name')

    arra=[
        {
            '$addFields': {
                'Userid': {
                    '$toString': '$_id'
                }
            }
        }, {
            '$match': {
                "$or": [
                    {"name": {"$regex": f".*{Name}.*", "$options": "i"}},
                    {"Userid": Userid}
                ]
            }
        },{
            '$project': {
                '_id': 0,
                "Userid":1,
                "name":1,
            }
        }
    ]
    matching_users = list(signup_data.aggregate(arra))

    print(matching_users)
    if matching_users:
        return jsonify({"results": matching_users, 'status':200})
    else:
        return jsonify({
            'message':'Friend not found','status':400
        })


##################### Add friend###################################################################
@app.route("/add_friend", methods = ['POST'])
@token_required
def Add_friend(current_user):      
    Userid = request.form.get('Userid')
    if Userid is not None: 
        print(Userid)
        if(len(Userid)==24):
            aggr=[{
                '$match': {
                    '$and': [
                        {
                            '$or': [
                                {
                                    'senderId': ObjectId(current_user["_id"])
                                }, {
                                    'senderId': ObjectId(Userid)
                                }
                            ]
                        }, {
                            '$or': [
                                {
                                    'recieverId': ObjectId(current_user["_id"])
                                }, {
                                    'recieverId': ObjectId(Userid)
                                }
                            ]
                        }
                    ]
                }
            }]
        
            alreadyCheck=list(frindUserColl.aggregate(aggr))
            frindUser=signup_data.find_one({"_id":ObjectId(Userid)})
            if current_user["_id"]!=Userid:
                if frindUser:
                    if(len(alreadyCheck)==0):
                        
                        scorer={
                            "senderId":ObjectId(current_user["_id"]),
                            "recieverId":ObjectId(Userid),
                            "status":1
                        }
                        frindUserColl.insert_one(scorer)

                        return jsonify({'message': 'Friend request sent successfully','status':200})
                    
                    else:
                        return jsonify({'message': 'User Already Friend','status':400})

                else:
                    return jsonify({'message': 'Friend User Not Exist','status':400})
            else:
                return jsonify({'message': 'Invalid UserId','status':400})
        else:
            return jsonify({'message': 'Please Enter a valid user id','status':400})
    else:
        return jsonify({'message': 'Please Enter a user id','status':400})
#####################stop Add friend###################################################################

##################### All requests ###################################################################
@app.route("/all_requests", methods = ['GET'])
@token_required
def All_requests(current_user):
    print(current_user,'current_user')
    try:
        aggr=[
            {
                '$match': {
                    'recieverId': ObjectId(current_user["_id"])
                }
            }, {
                '$lookup': {
                    'from': 'signup', 
                    'localField': 'senderId', 
                    'foreignField': '_id', 
                    'as': 'result'
                }
            }, {
                '$unwind': {
                    'path': '$result', 
                    'preserveNullAndEmptyArrays': True
                }
            }, {
                '$addFields': {
                    'Name': '$result.name', 
                    'senderId': {
                        '$toString': '$senderId'
                    }, 
                    'recieverId': {
                        '$toString': '$recieverId'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'recieverId': 0, 
                    'result': 0
                }
            }, {
                '$addFields': {
                    'status': {
                        '$switch': {
                            'branches': [
                                {
                                    'case': {
                                        'status': 1
                                    }, 
                                    'then': 'Pending'
                                }, {
                                    'case': {
                                        'status': 2
                                    }, 
                                    'then': 'Accepted'
                                }, {
                                    'case': {
                                        'status': 3
                                    }, 
                                    'then': 'Blocked'
                                }
                            ]
                        }
                    }
                }
            }
        ]

        
        user_data = list(frindUserColl.aggregate(aggr))
        print(user_data)
        
        return jsonify(user_data), 200
    except Exception as e:
        response = {"error": str(e)}
        return jsonify(response), 500
    

@app.route("/all_friends", methods = ['GET'])
@token_required
def all_friends(current_user):
    try:
        
        aggr=[
            {
                '$match': {
                    '$and': [{
                        '$or': [
                            {
                                'senderId': ObjectId(current_user["_id"])
                            }, {
                                'recieverId': ObjectId(current_user["_id"])
                            }
                        ]
                    }, {
                        "status":2
                    }
                ]
                }
            }, {
                '$lookup': {
                    'from': 'signup', 
                    'localField': 'senderId', 
                    'foreignField': '_id', 
                    'as': 'result'
                }
            }, {
                '$unwind': {
                    'path': '$result', 
                    'preserveNullAndEmptyArrays': True
                }
            }, {
                '$addFields': {
                    'Name': '$result.name', 
                    'senderId': {
                        '$toString': '$senderId'
                    }, 
                    'recieverId': {
                        '$toString': '$recieverId'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'recieverId': 0, 
                    'result': 0
                }
            }, {
                '$addFields': {
                    'status': {
                        '$switch': {
                            'branches': [
                                {
                                    'case': {
                                        'status': 1
                                    }, 
                                    'then': 'Pending'
                                }, {
                                    'case': {
                                        'status': 2
                                    }, 
                                    'then': 'Accepted'
                                }, {
                                    'case': {
                                        'status': 3
                                    }, 
                                    'then': 'Blocked'
                                }, {
                                    'case': {
                                        'status': 4
                                    }, 
                                    'then': 'Reject'
                                }
                            ]
                        }
                    }
                }
            }
        ]

        
        user_data = list(frindUserColl.aggregate(aggr))
        print(user_data)
        
        return jsonify({'data':user_data,'status':200}), 200
    except Exception as e:
        response = {"error": str(e)}
        return jsonify({'response': response ,'status':500}), 500

##################### stop All requests ###################################################################

################## Accept Request ###########################################################################
@app.route("/accept_request", methods = ['POST','GET'])
@token_required
def Accept_Request(current_user):

    if request.method == "POST":
        try:
            senderId = request.form.get('senderId')
            
            new_status = 2

            agr = frindUserColl.update_one(
                {
                    'senderId': ObjectId(senderId),
                    'recieverId': ObjectId(current_user["_id"])
                },
                {
                    '$set': {
                        'status': new_status
                    }
                }
            )
            
            print(f"Matched Count: {agr.matched_count}")
            print(f"Modified Count: {agr.modified_count}")
            if agr.matched_count > 0 and agr.modified_count > 0:
                return jsonify({"message": "Accept Successfully.", 'status': 200})
            else:
                return jsonify({"message": "No matching document found for update.", 'status': 404})


            # return jsonify({"message":"Accept Successfully.",'status':200})
        except Exception as e:
            response = {"error": str(e)}
            return jsonify(response), 500
    else:
        return jsonify({
            'message':'invalid request','status':400
        })   

@app.route("/reject_request", methods = ['POST','GET'])
@token_required
def reject_request(current_user):

    if request.method == "POST":
              
        try:
            senderId = request.form.get('senderId')
            new_status = 4

            #userData=frindUserColl.÷

            agr = frindUserColl.update_one(
                {
                    'senderId': ObjectId(senderId),
                    'recieverId': ObjectId(current_user["_id"])
                },
                {
                    '$set': { 
                        'status': new_status
                    }
                }
            )
                  
            return jsonify({"message":"Rejected Successfully.",'status':200})
        except Exception as e:
            response = {"error": str(e)}
            return jsonify({'response':response,'status':400}), 500
    else:
        return jsonify({"message":"Invalid request.",'status':400})



# @app.route("/blocking_id", methods = ['POST','GET'])
# @token_required
# def block_user_(current_user):
#     user_id= current_user.get('_id')
#     if request.method=="POST":
#         blocking_id=request.form.get('blocking_id')
#         user_data=frindUserColl.find_one(blocking_id)
#         print(user_data)


@app.route("/block_user", methods = ['POST','GET'])
@token_required
def block_user(current_user):

    if request.method == "POST":
        try:
            senderId = request.form.get('senderId')
            new_status = 3

            #userData=frindUserColl.÷

            agr = frindUserColl.update_one(
                {
                    'senderId': ObjectId(senderId),
                    'recieverId': ObjectId(current_user["_id"])
                },
                {
                    '$set': {
                        'status': new_status
                    }
                }
            )
                  
            return jsonify({"message":"Blocked Successfully.",'status':200})
        except Exception as e:
            response = {"error": str(e)} 
            return jsonify({'response':response,'status':400}), 500
    else:
        return jsonify({
            "message":'Invalid method '
        })


@app.route("/block_user_list", methods = ['POST','GET'])
@token_required
def block_user_list(current_user):
    try:
        aggr = [
            {
                '$match': {
                    '$or': [
                        {
                            'senderId': ObjectId(current_user["_id"]), 
                            'status': 3
                        }, {
                            'recieverId': ObjectId(current_user["_id"]), 
                            'status': 3
                        }
                    ]
                }
            }, {
                '$lookup': {
                    'from': 'signup', 
                    'localField': 'senderId', 
                    'foreignField': '_id', 
                    'as': 'result'
                }
            }, {
                '$unwind': {
                    'path': '$result', 
                    'preserveNullAndEmptyArrays': True
                }
            }, {
                '$addFields': {
                    'Name': '$result.name', 
                    'senderId': {
                        '$toString': '$senderId'
                    }, 
                    'recieverId': {
                        '$toString': '$recieverId'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'recieverId': 0, 
                    'result': 0
                }
            }, {
                '$addFields': {
                    'status': 'Blocked'
                }
            }
        ]


        print(aggr)

        user_data = list(frindUserColl.aggregate(aggr))
        print(user_data)
        return jsonify({"message": "Data Get Successfully.", 'status': 200, "data": user_data}), 200
    except Exception as e:
        response = {"error": str(e)}
        return jsonify({'response': response, 'status': 500}), 500


###################stop Accept Request ###########################################################################

###################ifRequested  ###########################################################################
@app.route("/ifRequested", methods = ['GET'])
@token_required
def ifRequested(current_user):
    try:
        
        aggr=[
            {
                '$match': {
                    'recieverId': ObjectId(current_user["_id"]),
                    "status":1
                }
            }, {
                '$lookup': {
                    'from': 'signup', 
                    'localField': 'senderId', 
                    'foreignField': '_id', 
                    'as': 'result'
                }
            }, {
                '$unwind': {
                    'path': '$result', 
                    'preserveNullAndEmptyArrays': True
                }
            }, {
                '$addFields': {
                    'Name': '$result.name', 
                    'senderId': {
                        '$toString': '$senderId'
                    }, 
                    'recieverId': {
                        '$toString': '$recieverId'
                    }, 
                    'unqId': {
                        '$toString': '$_id'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'recieverId': 0, 
                    'result': 0
                }
            }, {
                '$addFields': {
                    'status': {
                        '$switch': {
                            'branches': [
                                {
                                    'case': {
                                        'status': 1
                                    }, 
                                    'then': 'Pending'
                                }, {
                                    'case': {
                                        'status': 2
                                    }, 
                                    'then': 'Accepted'
                                }, {
                                    'case': {
                                        'status': 3
                                    }, 
                                    'then': 'Blocked'
                                }
                            ]
                        }
                    }
                }
            }
        ]

        
        user_data = list(frindUserColl.aggregate(aggr))
        print(user_data)
        
        return jsonify({'user_data':user_data,'status':200}), 200
    except Exception as e:
        response = {"error": str(e)}
        return jsonify({'response':response,'status':400}), 500


@app.route("/updateBalance", methods=['POST'])
@token_required
def create_update(current_user):
    if request.method == "POST":
        user_id = current_user.get('_id')
        totalcoins = request.form.get("totalcoins")
        totaldiamonds = request.form.get("totaldiamonds")
        data = {
            "total_coins":str(totalcoins),
            "total_diamonds":str(totaldiamonds)
        }
        signup_data.update_one({"_id":ObjectId(user_id)},{'$set':data})
        return jsonify({"message":"Update Balance successful",'status':200})
    else:
        return jsonify({
            'message':'Invalid request.','status':400
        })


@app.route("/report_user", methods=['POST','GET'])
@token_required
def report_user(current_user):
    if request.method=='POST':
        
        user_id = current_user.get('_id')
        reporting_id=request.form.get('reporting_id')

        data=reporting_data.find({"user_id":user_id,"reporting_id":reporting_id})
        if data:
            return jsonify({"message":"Report Already Exist",'status':400})
        else:
            reporting_data.insert_one({"user_id":user_id,"reporting_id":reporting_id})
            return jsonify({"message":"Report successful",'status':200})




@app.route("/version", methods=['POST'])
@token_required
def version(current_user):
    force_update=request.form.get('force_update')
    app_version=request.form.get('app_version')
    if force_update and app_version:
        version_data.insert_one({"force_update":force_update,"app_version":app_version})
        return jsonify({
            'message':"New Version Added Successfully",
            'status':200
        })
    else:
        return jsonify({
            'message':"Please Added Field",
            'status':400
        })



@app.route("/getversion", methods=['GET'])
def getversion():

    data = list(version_data.find({},projection={"_id":False}))

    return jsonify({
        'message':"Version Get successfull",
        'status':200,
        "data":data,
        "latest_app_version": data[-1]["app_version"] if len(data)>0 else "",
        "latest_force_update": data[-1]["force_update"] if len(data)>0 else ""
    })




# @app.route("/getLeaderboard", methods=['POST','GET'])
# @token_required
# def getLeaderboard(current_user):
#     if request.method =='GET':
#         user_id=request.form.get('user_id')
#         country=request.form.get('country')
#         city=request.form.get('city')
#         data={
#             'user_id':user_id,
#             'country':country, 
#             'city':city
#         }
#         find_user=signup_data.find(data)
#         print(find_user)
#         return jsonify({
#             'message':"find user successfull",'status':200
#         })


 


        

@app.route("/feedback", methods=['POST'])
@token_required
def feedback(current_user):
    user_id = current_user.get('_id')
    if request.method == 'POST':
        
        feedback_text = request.form.get('feedback')
        star = request.form.get('star')
        if star<='5':
            feedback_doc = {
                "user_id": user_id,
                "feedback": feedback_text,
                "star": star
            }
            
            result =feedback_collection.insert_one(feedback_doc)
        
        
            if result.acknowledged:
                return jsonify({"message": "Feedback saved successfully.",'status':200})
            else:
                return jsonify({"message": "Failed to save feedback.",'status':400})
        else:
            return jsonify({
                'message':'Please provide correct star','status':400
            })
    else:
        return jsonify({"message": "Invalid Request Method.",'status':400})



###  this api use for link page ################################################################

@app.route("/linkDelete", methods=['DELETE','GET','POST'])  # 
def LinkDelete():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # print(email,password,'passwordpassword')
        data = signup_data.find_one({'email': email, 'password': password})
        # print(data,'data')
        if data:
            signup_data.delete_one({'_id': data['_id']})
            return 'Deleted Successfull'
        else:
            return 'Email or Password wrong'
            # print('email or password wrong')

    return render_template('index.html')










if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0", port=8080)