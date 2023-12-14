# from flask import Flask, request, jsonify , make_response
# from functools import wraps
# from pymongo import MongoClient
# from bson import ObjectId
# import math
# import random
# import datetime
# import re
# import bcrypt
# import smtplib
# import pymongo
# import os
# import jwt
# from twilio.rest import Client
# from flask_mail import Mail, Message
# from uuid import uuid4

# app = Flask(__name__)

# app.config['ACCOUNT_SID'] = 'AC5f88040e6854cb8c340f77e38e03970d',
# app.config['ACCESS_KEY'] = 'f539a994081b7ca5e327827c48bf1b15',
# app.config['TWILIO_PHONE_NUMBER'] = "+12565888672"

# message_service = Client('AC5f88040e6854cb8c340f77e38e03970d', 'f539a994081b7ca5e327827c48bf1b15')

# client = MongoClient("mongodb://localhost:27017")
# db = client['GameShoot']
# collection = db['game_get']
# signup_data = db['signup']
# frindUserColl = db['friendUser']
# deletedSignup = db['deletedSignup']

# Add_Friends = db['Add_Friends']
# balance_data = db['update_balance']

# ################### mail #############################################################################

# app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
# app.config['MAIL_PORT'] = 587 
# app.config['MAIL_USERNAME'] = 'shobhit.pal@fourbrick.com' 
# app.config['MAIL_PASSWORD'] = 'qdve zeva rvuc iecp'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# mail = Mail(app)
# ######################### stop mail ################################################################
# def token_required(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):

#         token = None
#         if "Authorization" in request.headers:
#             token = request.headers["Authorization"].split(" ")[-1]
#             # print(token,"dasgfhgfsahgdfsahgd")

#         if not token:
#             return jsonify({"msg": "a valid token is missing"}), 401

#         try:
#             data = jwt.decode(
#                 token,
#                 algorithms="HS512",
#                 key="GameDev",
#             )
#             # print("dsifhsdkuhfkusdhfkuhsd", data)

#             aggr = [
#                 {
#                     '$match': {
#                         '_id': ObjectId(data['userId'])
#                     }
#                 }, {
#                     '$addFields': {
#                         '_id': {
#                             '$toString': '$_id'
#                         }
#                     }
#                 }
#             ]
            
#             current_user = list(signup_data.aggregate(aggr))
            
#             database_data = len(current_user)

#             if database_data == 0:
#                 return jsonify({"msg": "token is invalid"}), 401

#         except Exception as e:
#             return jsonify({"msg": "token is invalid"}), 401
#         return f(current_user[0], *args, **kwargs)

#     return decorator



# ####################### signup page ####################################################
# @app.route("/signup", methods=['POST'])
# def signup():
#     if request.method == "POST":
#         name = request.form.get('name')
#         email = request.form.get("email")
#         password = request.form.get("password")
#         mobile = request.form.get("mobile")
#         country = request.form.get("country")
#         gender = request.form.get("gender")
#         city = request.form.get("city")
#         email_exist = signup_data.find_one({"email":email})
#         phone_exist = signup_data.find_one({"mobile":mobile})

#         if email_exist:
#             return jsonify({"msg":"email is already exist "})
#         if phone_exist:
#             return jsonify({"msg":"phone no. is already exist "})
#         otp = random.randint(1000, 9999)
#         try:
#             msg = Message("OTP for Registration", sender='shohit.pal@fourbrick.com', recipients=[email])
#             msg.body = f"Your OTP for registration is: {otp}"
#             mail.send(msg)
#             print(otp,'otp')
            
#         except Exception as e:
#             print(e)
#             return jsonify({"message": "Error sending OTP."}), 500
#         data = {
#             "name":name,
#             "email":email,
#             "password":password,    
#             "mobile":mobile,
#             "country":country,
#             "gender":gender,
#             "city":city,
#             "Profile Icon":0,
#             "Kill Count":0,
#             "Death Count":0,
#             "Match Count":0,
#             "Win Count":0,
#             "XP":0,
#             "Level":0,
#             "Total_Coins":0,
#             "Total_Diamonds":0,
#             "OTP": otp,
#         }
#         signup_data.insert_one(data)
#         return jsonify({"message": "Registration successful. Please check your email for OTP."}), 200

# ###################################################################################################################

# ############ verify #####################################################################################
# @app.route("/verify", methods=['POST'])
# def verify():
#     if request.method=='POST':
#         email=request.form.get('email')
#         input_otp=request.form.get('input_otp')
#         user_data = signup_data.find_one({"email": email})
#         stored_otp = user_data.get("OTP") if user_data else None

#         if stored_otp is not None and input_otp == str(stored_otp):

#             return jsonify({"message": "OTP verification successful."}), 200
#         else:
#             return jsonify({"message": "Invalid OTP."}), 400  
# #################### stop verify ##################################################

# ####################### resend code ###############################################################
# @app.route("/resend_code", methods=['POST'])
# def resend_code():
#     email = request.form.get("email")

#     new_otp = random.randint(1000, 9999)

#     signup_data.update_one({"email": email}, {"$set": {"OTP": new_otp,"verifying_link":str(uuid4())}})

#     try:
#         msg = Message("OTP for Registration", sender='shohit.pal@fourbrick.com', recipients=[email])
#         msg.body = f"Your OTP for registration is: {new_otp}"
#         mail.send(msg)
#         print(new_otp,'otp')
        
#     except Exception as e:
#         print(e)
#         return jsonify({"message": "Error sending OTP."}), 500

#     return jsonify({"message": "New OTP sent successfully."})


# @app.route("/resend_code_link", methods=['POST'])
# def resend_code_link():
#     email = request.form.get("email")

#     new_otp = random.randint(1000, 9999)

#     verifying_link=str(uuid4())

#     signup_data.update_one({"email": email}, {"$set": {"OTP": new_otp,"verifying_link":verifying_link}})

#     try:
#         msg = Message("Password Reset Link", sender='shohit.pal@fourbrick.com', recipients=[email])
#         msg.body = f"Your Link for Reset Password {verifying_link} <a href='{verifying_link}'>Verify Link</a>"
#         mail.send(msg)
#         print(new_otp,'otp')
        
#     except Exception as e:
#         print(e)
#         return jsonify({"message": "Error sending OTP."}), 500

#     return jsonify({"message": "Password Reset Link Check Your Mail."})
# ########################## stopResendcode###################################################################################


# ###############################################################################################################################
# #################### login ################################################################################################################
# @app.route("/login", methods=['POST'])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password = request.form.get("password")


#         user_data = signup_data.find_one({"email": email})
#         if len(user_data):
#             if str(user_data['password']) == str(password):
#                 user_data['_id'] = str(user_data['_id'])
#                 del user_data['password']
#                 access_token = jwt.encode(
#                     {
#                         "userDetails": user_data, "userId": user_data["_id"]
#                     },
#                     key="GameDev",
#                     algorithm="HS512",
#                 )
#                 response = make_response(
#                     jsonify({"token": access_token, "user": user_data})
#                 )
#                 response.set_cookie(
#                     "token",
#                     access_token,
#                     # secure=True,
#                     httponly=True,
#                     samesite=None,

#                 )  
#                 data = jwt.decode(
#                 access_token,
#                 algorithms="HS512",
#                 key="GameDev",
#             )
#                 return jsonify({"msg":"Login successful." , "token":access_token,"token_Data":data})
#             else:
#                 return jsonify({"msg":"Email or Password wrong..."})
#         else:
#             return jsonify({"msg":"Email not found. Please register first."}),400
        
# ##########################################################################################################################

# ########## Forget password #####################################################################################
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
# ################# stop Forget password ###################################################################################

# ########### Delete Account ##############################################################################################





# @app.route("/delete_account", methods=['DELETE'])

# @token_required
# def Delete_Account(current_user):

#     print("current_user",current_user["_id"])
#     dataAll=signup_data.find_one({"_id":ObjectId(current_user["_id"])})
#     dataAll["oldId"]=dataAll["_id"]
#     del dataAll["_id"]
#     deletedSignup.insert_one({"_id":ObjectId(current_user["_id"])})
#     signup_data.delete_one({"_id":ObjectId(current_user["_id"])})
#     return jsonify({
#         "message": "Delete account successfully."
#     })
# ############### stop Delete_Account ##############################################################################################




# ############### Update Profile #####################################################
# @app.route("/Update_Profile", methods=['POST'])
# @token_required
# def Update_Profile(current_user):
    
#     print("current_user",current_user["_id"])
#     name = request.form.get('name')
#     email = request.form.get("email")
#     password = request.form.get("password")


#     user_data = signup_data.find_one({"_id": ObjectId(current_user["_id"])})

#     new_otp = random.randint(1000, 9999)
#     try:
#         msg = Message("Password OTP", sender='shohit.pal@fourbrick.com', recipients=[email])
#         msg.body = f"Your OTP Send to Email {new_otp} <a href='{new_otp}'>Verify Link</a>"
#         mail.send(msg)
#         print(new_otp,'otp')
        
#     except Exception as e:
#         print(e)
#         return jsonify({"message": "Error sending OTP."}), 500

#     if user_data:
#         update_data = {
#             "OTP":new_otp 
#         }
#         signup_data.update_one({"_id": ObjectId(current_user["_id"])}, {"$set": update_data})
#         return jsonify({
#             "message": "OTP Sent To mail."
#         }),200
#     else:
#         return jsonify({
#             "message": "Email not found in the database. Profile not updated."
#         }),400
# ####################### stop Update Profile######################################################



# @app.route("/updateStats", methods = ['POST'])
# @token_required
# def updateStats(current_user):
#     if request.method == "POST":
#         Kill_Count=request.form.get("Kill_Count ")
#         Death_Count=request.form.get("Death_Count")
#         Win_Count=request.form.get("Win_Count")
#         Match_Count=request.form.get("Match_Count")
#         Xp=request.form.get("Xp")
#         Level=request.form.get("Level")
        
#         updateBy={"_id":ObjectId(current_user['_id'])}
#         data={
#             "Kill_Count":Kill_Count,
#             "Death_Count":Death_Count,
#             "Win_Count":Win_Count,
#             "Match_Count":Match_Count,
#             "Xp":Xp,
#             "Level":Level
#         }
#         signup_data.update_one(updateBy,{"$set":data})
#         print(updateBy)
#         return jsonify({"message":"Update all informations of the user"})
#     else:
#         return jsonify({"msg":"invalid requeat"})






# @app.route("/verify_update", methods=['POST'])
# @token_required
# def verify_update(current_user):
    
#     print("current_user",current_user["_id"])
#     name = request.form.get('name')
#     email = request.form.get("email")
#     password = request.form.get("password")
#     OTP = request.form.get("OTP")



#     user_data = signup_data.find_one({"_id": ObjectId(current_user["_id"])})

#     if user_data:

#         if(user_data["OTP"]==OTP):
                
#             update_data = {
#                 "name": name,
#                 "password": password,
#                 "email":email
#             }
#             signup_data.update_one({"_id": ObjectId(current_user["_id"])}, {"$set": update_data})
#             return jsonify({
#                 "message": "Profile updated successfully."
#             }),200
#         else:
            
#             return jsonify({
#                 "message": "Please Check OTP."
#             }),400
#     else:
#         return jsonify({
#             "message": "Email not found in the database. Profile not updated."
#         }),400



# @app.route("/Search_friends", methods = ['POST'])
# @token_required
# def Search_friends(currend_user):
#     Userid = request.form.get('Userid')
#     Name = request.form.get('Name')

#     arra=[
#         {
#             '$addFields': {
#                 'uniqueId': {
#                     '$toString': '$_id'
#                 }
#             }
#         }, {
#             '$match': {
#                 "$or": [
#                     {"name": {"$regex": f".*{Name}.*", "$options": "i"}},
#                     {"uniqueId": Userid}
#                 ]
#             }
#         }
#     ]
#     matching_users = signup_data.aggregate(arra)

#     print()

#     results = []
#     for user in matching_users:
#         results.append({
#             "name": user["name"],
#             # "email": user["email"]

#         })

#     return jsonify({"results": results})


# ##################### Add friend###################################################################
# @app.route("/add_friend", methods = ['POST'])
# @token_required
# def Add_friend(current_user):

    
    
#     Userid = request.form.get('Userid')
    
#     if(len(Userid)==24):
#         aggr=[{
#             '$match': {
#                 '$and': [
#                     {
#                         '$or': [
#                             {
#                                 'senderId': ObjectId(current_user["_id"])
#                             }, {
#                                     'senderId': ObjectId(Userid)
#                             }
#                         ]
#                     }, {
#                         '$or': [
#                             {
#                                 'recieverId': ObjectId(current_user["_id"])
#                             }, {
#                                 'recieverId': ObjectId(Userid)
#                             }
#                         ]
#                     }
#                 ]
#             }
#         }]
    
#         alreadyCheck=list(frindUserColl.aggregate(aggr))
#         frindUser=signup_data.find_one({"_id":ObjectId(Userid)})
#         if current_user["_id"]!=Userid:
#             if frindUser:
#                 if(len(alreadyCheck)==0):
                    
#                     scorer={
#                         "senderId":ObjectId(current_user["_id"]),
#                         "recieverId":ObjectId(Userid),
#                         "status":1
#                     }
#                     frindUserColl.insert_one(scorer)

#                     return jsonify({'message': 'Friend request sent successfully'})
                
#                 else:
#                     return jsonify({'message': 'Both User Already Friend'}),400

#             else:
#                 return jsonify({'message': 'Friend User Not Exist'}),400
#         else:
#             return jsonify({'message': 'Same id'}),400
#     else:
#         return jsonify({'message': 'Please Enter a valid user id'}),400
# #####################stop Add friend###################################################################

# ##################### All requests ###################################################################
# @app.route("/all_requests", methods = ['GET'])
# @token_required
# def All_requests(current_user):
#     try:
        
#         aggr=[{
#             '$match': {
#                 '$or': [
#                     {
#                         'senderId': ObjectId(current_user["_id"])
#                     },
#                     {
#                         'recieverId': ObjectId(current_user["_id"])
#                     }
#                 ]
#             }
#         }]

#         # signup_data.aggregate([
#         #     {
#         #     $lookup: {
#         #             'senderId': ObjectId(current_user["_id"])                
#         #         }
#         #         }])

        
#         user_data=frindUserColl.aggregate(aggr)
        
#         return jsonify(user_data), 200
#     except Exception as e:
#         response = {"error": str(e)}
#         return jsonify(response), 500
#     pass
# ##################### stop All requests ###################################################################

# ################## Accept Request ###########################################################################
# @app.route("/Accept_Request", methods = ['Post'])
# # @token_required
# def Accept_Request():
#     user_email = request.json.get("user_email")

#     friend_email = request.json.get("friend_email")

#     user_data = signup_data.find_one({"email": user_email})
#     friend_data = signup_data.find_one({"email": friend_email})

#     if user_data and friend_data:

#         signup_data.update_one({"email": user_email}, {"$addToSet": {"friends": friend_email}})


#         signup_data.update_one({"email": friend_email}, {"$addToSet": {"friends": user_email}})

#         return jsonify({"message": "Friend request accepted successfully."})
#     else:
#         return jsonify({"message": "User or friend not found in the database. Request not accepted."})
# ##################stop Accept Request ###########################################################################

# ################## Reject Request  ###########################################################################
# @app.route("/Reject_Request", methods = ['Post'])
# # @token_required
# def Reject_Request():
#     user_email = request.json.get("user_email")

#     friend_email = request.json.get("friend_email")

#     user_data = signup_data.find_one({"email": user_email})
#     friend_data = signup_data.find_one({"email": friend_email})

#     if user_data and friend_data:
#         # Remove the friend from the user's friend request list
#         signup_data.update_one({"email": user_email}, {"$pull": {"friend_requests": friend_email}})
#         return jsonify({"message": "Friend request rejected successfully."})
#     else:
#         return jsonify({"message": "User or friend not found in the database. Request not rejected."})
# ################## stop Reject Request  ###########################################################################

# ################## If requested  ###########################################################################
# @app.route("/If_requested", methods = ['Get'])
# # @token_required
# def If_requested():
#     pass
# ################# stop If_requested ###########################################################################################

# ################All friends ###########################################################################################
# @app.route("/All_friends", methods = ['Get'])
# # @token_required
# def All_friends():

#     user_email = request.args.get("user_email")

#     user_data = collection_name.find_one({"email": user_email})

#     if user_data:

#         friends_list = user_data.get("friends", [])

#         friends_details = []
#         for friend_email in friends_list:
#             friend_data = collection_name.find_one({"email": friend_email})
#             if friend_data:
#                 friends_details.append({
#                     "name": friend_data["name"],
#                     "email": friend_data["email"]

#                 })

#         return jsonify({"friends": friends_details})
#     else:
#         return jsonify({"message": "User not found in the database."})

# ################ stop  All friends ###########################################################################################

# ################ Block User###########################################################################################
# @app.route("/Block_User", methods = ['Post'])
# # @token_required
# def Block_User():
#     email = request.json.get("email")
#     user_data = collection_name.find_one({"email": email})

#     if user_data:
#         collection_name.update_one({"email": email}, {"$set": {"status": "blocked"}})
#         return jsonify({
#             "message": "User blocked successfully."
#         })
#     else:
#         return jsonify({
#             "message": "User not found in the database. User not blocked."
#         })
# ################ stop Block User###########################################################################################

# ################ Block User's list###########################################################################################
# @app.route("/BlockUserlist", methods = ['Post'])
# # @token_required
# def BlockUserlist():

#     blocked_users_cursor = collection_name.find({"status": "blocked"})
#     blocked_users = []
#     for user in blocked_users_cursor:
#         blocked_users.append({
#             "name": user["name"],
#             "email": user["email"]

#         })

#     return jsonify({"blocked_users": blocked_users})
# ################ stop Block User's listr###########################################################################################









# @app.route("/post_game", methods=['POST'])
# def new_game():
#     if request.method == 'POST':
#         game = str(request.form.get('game'))
#         version = float(request.form.get("version"))
#         isforce = request.form.get("isforce")

#         if isforce == '1':
#             isforce = True
#         elif isforce == '0':
#             isforce = False
#         else:
#             return jsonify({"error": "invalid isforce value"})
#         data = {
#             "game": game,
#             "version": version,
#             "isforce": isforce
#         }
#         collection.insert_one(data)

#         return jsonify({"msg":"Game data added successfully"}),200
    


# @app.route("/get_game", methods=['GET'])
# def get_game():
#     if request.method == "GET":
#         game_data = list(collection.find({}, {'_id': 0}))
#         if not game_data:
#             return jsonify({"message": "No game data available"})
           
#         return jsonify(game_data[0])

# @app.route("/game_update/<id>", methods=['PUT'])
# def game_update(id):
#     game = request.form.get("game")
#     version = request.form.get("version")
#     isforce = request.form.get('isforce')

#     filter_criteria = {"_id": ObjectId(id)}

#     update_operation = {"$set": {"game": game, "version": version, "isforce": isforce}}

#     result = collection.update_one(filter_criteria, update_operation)

#     if result.modified_count == 1:
#         return jsonify({"msg": "Updated image successfully"})
#     else:
#         return jsonify({"msg": "No document was updated"})


    

# # read the image
# # @app.route("/get_login",methods=['GET'])
# # def get_login():
# #     data = list(signup_data.find())
# #     return jsonify("me:image read successful")

# # for testing purpose
# @app.route("/naveen", methods=['GET'])
# @token_required
# def naveenTesting(current_user):
#     print(current_user)
#     print("hgfhgfhgfhgf")
    
#     return current_user

# ##############update balance#############

# 
# # get the data
# @app.route("/get_update_balance", methods = ['GET'])
# def get_update_balance():
#     data = list(balance_data.find())
#     return jsonify({"message":"get_update_balance read successful"})

    
# ################### stop update balance#####################################################

# ############# verify update ###########################################################################
# @app.route("/Verify_Update", methods = ['POST'])
# # @token_required
# def Verify_Update():
#     pass
# ########### stop Verify_Update ###################################################################################

# #####################Update Stats ###################################################################
# @app.route("/Update_Stats", methods = ['POST'])
# # @token_required
# def Update_Stats():
#     pass
# ################## stop Update Stats ###################################################################

# ##################### Search friends ###################################################################

# ##################### stop Search friends ###################################################################

# ##################### Add friend###################################################################
# # @app.route("/Add_friend", methods = ['POST'])
# # # @token_required
# # def Add_friend():
# #     user_email = request.json.get("user_email")

# #     friend_email = request.json.get("friend_email")

# #     user_data = signup_data.find_one({"email": user_email})
# #     print(user_data,'user_data')
# #     friend_data = signup_data.find_one({"email": friend_email})
# #     print(friend_data,'friend_data')
# #     if user_data and friend_data:

# #         signup_data.update_one({"email": user_email}, {"$addToSet": {"friends": friend_email}})
# #         return jsonify({"message": "Friend added successfully."})
# #     else:
# #         return jsonify({"message": "User or friend not found in the database. Friend not added."})
# # #####################stop Add friend###################################################################

# # ##################### All requests ###################################################################
# # @app.route("/All_requests", methods = ['Get'])
# # # @token_required
# # def All_requests():
# #     user_email = request.args.get("user_email")
# #     user_data = signup_data.find_one({"email": user_email})

# #     if user_data:
# #         friend_requests_list = user_data.get("friend_requests", [])
# #         friend_requests_details = []
# #         for friend_email in friend_requests_list:
# #             friend_data = signup_data.find_one({"email": friend_email})
# #             if friend_data:
# #                 friend_requests_details.append({
# #                     "name": friend_data["name"],
# #                     "email": friend_data["email"]
# #                 })

# #         return jsonify({"friend_requests": friend_requests_details})
# #     else:
# #         return jsonify({"message": "User not found in the database."})
# # ##################### stop All requests ###################################################################

# # ################## Accept Request ###########################################################################
# # @app.route("/Accept_Request", methods = ['Post'])
# # # @token_required
# # def Accept_Request():
# #     user_email = request.json.get("user_email")

# #     friend_email = request.json.get("friend_email")

# #     user_data = signup_data.find_one({"email": user_email})
# #     friend_data = signup_data.find_one({"email": friend_email})

# #     if user_data and friend_data:

# #         signup_data.update_one({"email": user_email}, {"$addToSet": {"friends": friend_email}})


# #         signup_data.update_one({"email": friend_email}, {"$addToSet": {"friends": user_email}})

# #         return jsonify({"message": "Friend request accepted successfully."})
# #     else:
# #         return jsonify({"message": "User or friend not found in the database. Request not accepted."})
# # ##################stop Accept Request ###########################################################################

# # ################## Reject Request  ###########################################################################
# # @app.route("/Reject_Request", methods = ['Post'])
# # # @token_required
# # def Reject_Request():
# #     user_email = request.json.get("user_email")

# #     friend_email = request.json.get("friend_email")

# #     user_data = signup_data.find_one({"email": user_email})
# #     friend_data = signup_data.find_one({"email": friend_email})

# #     if user_data and friend_data:
# #         # Remove the friend from the user's friend request list
# #         signup_data.update_one({"email": user_email}, {"$pull": {"friend_requests": friend_email}})
# #         return jsonify({"message": "Friend request rejected successfully."})
# #     else:
# #         return jsonify({"message": "User or friend not found in the database. Request not rejected."})
# # ################## stop Reject Request  ###########################################################################

# # ################## If requested  ###########################################################################
# # @app.route("/If_requested", methods = ['Get'])
# # # @token_required
# # def If_requested():
# #     pass
# # ################# stop If_requested ###########################################################################################

# # ################All friends ###########################################################################################
# # @app.route("/All_friends", methods = ['Get'])
# # # @token_required
# # def All_friends():

# #     user_email = request.args.get("user_email")

# #     user_data = collection_name.find_one({"email": user_email})

# #     if user_data:

# #         friends_list = user_data.get("friends", [])

# #         friends_details = []
# #         for friend_email in friends_list:
# #             friend_data = collection_name.find_one({"email": friend_email})
# #             if friend_data:
# #                 friends_details.append({
# #                     "name": friend_data["name"],
# #                     "email": friend_data["email"]

# #                 })

# #         return jsonify({"friends": friends_details})
# #     else:
# #         return jsonify({"message": "User not found in the database."})

# # ################ stop  All friends ###########################################################################################

# # ################ Block User###########################################################################################
# # @app.route("/Block_User", methods = ['Post'])
# # # @token_required
# # def Block_User():
# #     email = request.json.get("email")
# #     user_data = collection_name.find_one({"email": email})

# #     if user_data:
# #         collection_name.update_one({"email": email}, {"$set": {"status": "blocked"}})
# #         return jsonify({
# #             "message": "User blocked successfully."
# #         })
# #     else:
# #         return jsonify({
# #             "message": "User not found in the database. User not blocked."
# #         })
# # ################ stop Block User###########################################################################################

# # ################ Block User's list###########################################################################################
# # @app.route("/BlockUserlist", methods = ['Post'])
# # # @token_required
# # def BlockUserlist():

# #     blocked_users_cursor = collection_name.find({"status": "blocked"})
# #     blocked_users = []
# #     for user in blocked_users_cursor:
# #         blocked_users.append({
# #             "name": user["name"],
# #             "email": user["email"]

# #         })

# #     return jsonify({"blocked_users": blocked_users})
# ################ stop Block User's listr###########################################################################################

# # if __name__ == "__main__":
# app.run(debug=True , port=8080)




from flask import Flask, request, jsonify , make_response, send_file
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
            return jsonify({"message": "a valid token is missing"}), 401

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
                return jsonify({"message": "token is invalid","status": 400})

        except Exception as e:
            return jsonify({"message": "token is invalid","status":400})
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
            return jsonify({"message":"email is already exist "})
        if phone_exist:
            return jsonify({"message":"phone no. is already exist "})
        otp = random.randint(1000, 9999)
        try:
            msg = Message("OTP for Registration", sender='shohit.pal@fourbrick.com', recipients=[email])
            msg.body = f"Your OTP for registration is: {otp}"
            mail.send(msg)
            print(otp,'otp')
            
        except Exception as e:
            print(e)
            return jsonify({"message": "Error sending OTP."}), 500
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
        return jsonify({"message": "Registration successful. Please check your email for OTP."}), 200

###################################################################################################################

############ verify #####################################################################################
@app.route("/verify", methods=['POST'])
def verify():
    if request.method=='POST':
        email=request.form.get('email')
        input_otp=request.form.get('input_otp')
        user_data = signup_data.find_one({"email": email})
        stored_otp = user_data.get("OTP") if user_data else None

        if stored_otp is not None and input_otp == str(stored_otp):
            
            user_data = signup_data.update_one({"email": email}, {"$set": {"verified": True}})
            return jsonify({"message": "OTP verification successful."}), 200
        else:
            return jsonify({"message": "Invalid OTP."}), 400  
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
        return jsonify({"message": "Error sending OTP."}), 500

    return jsonify({"message": "New OTP sent successfully."})


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
        return jsonify({"message": "Error sending OTP."}), 500

    return jsonify({"message": "Password Reset Link Check Your Mail."})
########################## stopResendcode###################################################################################


###############################################################################################################################
#################### login ################################################################################################################
@app.route("/login", methods=['POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")


        user_data = signup_data.find_one({"email": email})
        if len(user_data):
            if user_data['verified']:
            # if user_data is verify:
            # if user_data:
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
                    return jsonify({"message":"Login successful." , "token":access_token,"token_Data":data})
                else:
                    return jsonify({"message":"Email or Password wrong..."})
            else:
                    return jsonify({"message":"User Not Verified."})
        else:
            return jsonify({"message":"Email not found. Please register first."}),400
        
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
       
        user_data = signup_data.find({"email": email})
        # print(user_data,'user_data1')
        
        if user_data:           
            otp = random.randint(1000, 9999)
            try:
                msg = Message("OTP for Reset password", sender='shohit.pal@fourbrick.com', recipients=[email])
                msg.body = f"Your OTP for Reset password is: {otp}"
                mail.send(msg)
                print(otp,'otp')
                signup_data.update_one({"email": email}, {"$set": {"OTP": otp}})
                
                return jsonify({"message": "Send OTP Successfull."}), 500
            except Exception as e:
                print(e)
                return jsonify({"message": "Error sending OTP."}), 500
        else:
            return jsonify({
                "message": "Email not found in the database."
            })
    else:
        return jsonify({
            "message": "Invalid request."
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

        user_data = signup_data.find({"email": email})
        if user_data:
            verifying_otp = user_data[0].get("OTP")
        # if user_data:
        #     if(user_data[0]["verifying_otp"]==input_otp):
            if verifying_otp and verifying_otp == int(input_otp):
                signup_data.update_one({"email": email}, {"$set": {"password": new_password,"verified":""}})
                
                return jsonify({
                    "message": "Password updated successfully."
                })
            else:
                return jsonify({
                    "message": "Verify otp is not Valid."
                })
        else:
            return jsonify({
                "message": "Email not found in the database."
            })
    else:
        return jsonify({
            "message": "Invalid request."
        })
#################stop new password ########################################################################new

########### Delete Account ##############################################################################################
@app.route("/delete_account", methods=['POST', 'GET'])
@token_required
def Delete_Account(current_user):
    user_id = current_user.get("_id")
    email=request.form.get('email')
    
    if user_id:
        dataAll = signup_data.find_one({"_id": ObjectId(user_id)})
        
        if dataAll:
            email = dataAll.get("email") 
            if email:
                otp = random.randint(1000, 9999)
                try:
                    msg = Message("OTP for Delete Account", sender='shohit.pal@fourbrick.com', recipients=[email])
                    msg.body = f"Your OTP for Delete Account is: {otp}"
                    mail.send(msg)
                    print(otp, 'otp')
                    signup_data.update_one({"email": email}, {"$set": {"OTP": otp}})

                    return jsonify({"message": "Send OTP Successfully And Check your email."}), 200
                except Exception as e:
                    print(e)
                    return jsonify({"message": "Error sending OTP."}), 500
            else:
                return jsonify({"message": "Email address not found in user data."}), 400
        else:
            return jsonify({"message": "User data not found."}), 404
    else:
        return jsonify({"message": "user_id not found."}), 404







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
    if request.method == "DELETE":
        email = request.form.get("email")
        password = request.form.get("password")
        input_otp = request.form.get("input_otp")

        user_data = signup_data.find_one({"email": email, 'password': password,'OTP':input_otp})
        print(user_data,'user_data')
        if user_data:

            if request.method == 'DELETE':
                deletedSignup.insert_one({"_id":ObjectId(current_user["_id"])})
                signup_data.delete_one({"_id": ObjectId(current_user["_id"])})
                return jsonify({
                    "message": "Delete account successfully."
                })
            else:
                return jsonify({
                    "message": "error in request."
                })
        else:
            return jsonify({
                "message": "Invalid OTP."
            })
    else:
        return jsonify({
            "message": "invalid"
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
        }, {
            '$project': {
                '_id': 0, 
                'Name': '$name', 
                'Email': '$email', 
                'Password': '$password', 
                'Mobile': '$mobile', 
                'Country': '$country', 
                'Gender': '$gender', 
                'City': '$city', 
                'profile_icon': '$profile_icon', 
                'kill_count': '$kill_count', 
                'death_count': '$death_count', 
                'match_count': '$match_count', 
                'win_count': '$win_count', 
                'xp': '$xp', 
                'level': '$level', 
                'total_coins': '$total_coins', 
                'total_diamonds': '$total_diamonds',
                "profile":"$profile"
            }
        },{
            "$project":{
                "_id":0
            }
        }
    ]
    dataAll=list(signup_data.aggregate(arra))
    return jsonify({
        "message": "View Profile.",
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
                signup_data.update_one({"email": email}, {"$set": {"OTP": otp}})
                # return data

                update_data={
                    'name':name,
                    'tempEmail':email,
                    'tempMobile':mobile
                }

                if(profile_icon_name!=None):
                    update_data["profile_icon"]=profile_icon_name

                signup_data.update_one({"_id": ObjectId(current_user["_id"])}, {"$set": update_data})
                return jsonify({"message": "Send OTP Successfully And Check your email."}), 200
            except Exception as e:
                print(e)
                return jsonify({"message": "Error sending OTP."}), 500
        else:
            print('no')
            update_data={
                        'name':name,
                    }
            
            
            if(profile_icon_name!=None):
                update_data["profile_icon"]=profile_icon_name

            signup_data.update_one({"_id": ObjectId(current_user["_id"])}, {"$set": update_data})
            return jsonify({
                'message':'update prpfile successfull'
            })
            
    else:
        return jsonify({
            'message':'invalid request'
        })
        
@app.route("/confirm_update_profile", methods=['POST'])
@token_required
def confirm_update_profile(current_user):
    # print(current_user,'current user')
    if request.method=='POST':
        user_id = current_user.get("_id")
        input_otp=request.form.get('input_otp')

        print(user_id)
       
        user_data = signup_data.find_one({ "_id" : ObjectId(user_id), 'OTP': input_otp})     
        print(user_data) 
        if user_data:
            curr_email : user_data['tempEmail']
            curr_mobile : user_data['tempMobile']

            
            update_data={
                'email':curr_email,
                'mobile':curr_mobile, 
                'tempEmail':'',
                'tempMobile':''
            }

            signup_data.update_one({"_id": ObjectId(current_user["_id"])}, {"$set": update_data})

            return jsonify({
                "message": "Profile Update Sucessfully."
            }),200
        else:
            return jsonify({
                'message':'Invalid otp'
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



@app.route("/updateStats", methods = ['POST'])
@token_required
def updateStats(current_user):
    if request.method == "POST":
        Kill_Count=request.form.get("Kill_Count ")
        Death_Count=request.form.get("Death_Count")
        Win_Count=request.form.get("Win_Count")
        Match_Count=request.form.get("Match_Count")
        Xp=request.form.get("Xp")
        Level=request.form.get("Level")
        
        updateBy={"_id":ObjectId(current_user['_id'])}
        data={
            "Kill_Count":Kill_Count,
            "Death_Count":Death_Count,
            "Win_Count":Win_Count,
            "Match_Count":Match_Count,
            "Xp":Xp,
            "Level":Level
        }
        signup_data.update_one(updateBy,{"$set":data})
        print(updateBy)
        return jsonify({"message":"Update all informations of the user"})
    else:
        return jsonify({"message":"invalid requeat"})






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
                "message": "Profile updated successfully."
            }),200
        else:
            
            return jsonify({
                "message": "Please Check OTP."
            }),400
    else:
        return jsonify({
            "message": "Email not found in the database. Profile not updated."
        }),400



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

    print()

    return jsonify({"results": matching_users})


##################### Add friend###################################################################
@app.route("/add_friend", methods = ['POST'])
@token_required
def Add_friend(current_user):  
    
    Userid = request.form.get('Userid')
    
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

                    return jsonify({'message': 'Friend request sent successfully'})
                
                else:
                    return jsonify({'message': 'Both User Already Friend'}),400

            else:
                return jsonify({'message': 'Friend User Not Exist'}),400
        else:
            return jsonify({'message': 'Same id'}),400
    else:
        return jsonify({'message': 'Please Enter a valid user id'}),400
#####################stop Add friend###################################################################

##################### All requests ###################################################################
@app.route("/all_requests", methods = ['GET'])
@token_required
def All_requests(current_user):
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
            
           
            return jsonify({"message":"Data Updated Successfully."}), 200
        except Exception as e:
            response = {"error": str(e)}
            return jsonify(response), 500
        

@app.route("/reject_request", methods = ['POST','GET'])
@token_required
def reject_request(current_user):

    if request.method == "POST":
        try:
            senderId = request.form.get('senderId')
            new_status = 3

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
            
           
            return jsonify({"message":"Data Updated Successfully."}), 200
        except Exception as e:
            response = {"error": str(e)}
            return jsonify(response), 500
        


@app.route("/block_user_", methods = ['POST','GET'])
@token_required
def block_user_(current_user):
    user_id= current_user.get('_id')
    if request.method=="POST":
        blocking_id=request.form.get('blocking_id')
        user_data=frindUserColl.find_one(blocking_id)
        print(user_data)



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
            return jsonify({"message": "Statistics updated successfully."}), 200
        else:
            return jsonify({"message": "Failed to update statistics."}), 500
    else:
        return jsonify({"message": "Invalid request method."}), 405


@app.route("/block_user", methods = ['POST','GET'])
@token_required
def block_user(current_user):

    aggr=[
            {
                '$match': {
                    '$and':[{
                        '$or': [
                            {
                                'senderId': ObjectId(current_user["_id"])
                            },
                            {
                                'recieverId': ObjectId(current_user["_id"])
                            },
                            
                        ]
                    },{
                        'status': 2
                    }]
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
    try:
        return jsonify({"message":"Data Get Successfully.","data":user_data}), 200
    except Exception as e:
        response = {"error": str(e)}
        return jsonify(response), 500
    


@app.route("/block_user_list", methods = ['POST','GET'])
@token_required
def block_user_list(current_user):

    aggr=[
            {
                '$match': {
                    '$and':[{
                        '$or': [
                            {
                                'senderId': ObjectId(current_user["_id"])
                            },
                            {
                                'recieverId': ObjectId(current_user["_id"])
                            },
                            
                        ]
                    },{
                        'status': 2
                    }]
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
    try:
        return jsonify({"message":"Data Get Successfully.","data":user_data}), 200
    except Exception as e:
        response = {"error": str(e)}
        return jsonify(response), 500
        

###################stop Accept Request ###########################################################################

################### Reject Request  ###########################################################################
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
                                        'status': 1
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


@app.route("/updateBalance", methods=['POST'])
@token_required
def create_update(current_user):
    if request.method == "POST":
        user_id = current_user.get('_id')
        totalcoins = request.form.get("totalcoins")
        totaldiamonds = request.form.get("totaldiamonds")
        data = {
            "total_coins":int(totalcoins),
            "total_diamonds":int(totaldiamonds)
        }
        signup_data.update_one({"_id":ObjectId(user_id)},{'$set':data})
        return jsonify({"message":"Update Balance successful"})



@app.route("/report_user", methods=['POST','GET'])
@token_required
def report_user(current_user):
    if request.method=='POST':
        
        user_id = current_user.get('_id')
        reporting_id=request.form.get('reporting_id')

        data=reporting_data.find({"user_id":user_id,"reporting_id":reporting_id})
        if data:
            return jsonify({"message":"Report Already Exist"})
        else:
            reporting_data.insert_one({"user_id":user_id,"reporting_id":reporting_id})
            return jsonify({"message":"Report successful"})


        


    pass


@app.route("/version", methods=['POST'])
@token_required
def version(current_user):
    force_update=request.form.get('force_update')
    app_version=request.form.get('app_version')
    if force_update and app_version:
        version_data.insert_one({"force_update":force_update,"app_version":app_version})
        return jsonify({
            'message':"New Version Added Successfully"
        })
    else:
        return jsonify({
            'message':"Please Added Field"
        })
    pass


@app.route("/getversion", methods=['GET'])
@token_required
def getversion(current_user):

    data = list(version_data.find({},projection={"_id":False}))

    return jsonify({
        'message':"Version Get successfull",
        "data":data,
        "latest_app_version": data[-1]["app_version"] if len(data)>0 else "",
        "latest_force_update": data[-1]["force_update"] if len(data)>0 else ""
    })
    pass



@app.route("/getLeaderboard", methods=['POST','GET'])
@token_required
def getLeaderboard():
    if request.method =='GET':
        user_id=request.form.get()
        country=request.form.get()
        city=request.form.get()
        data={
            'user_id':user_id,
            'country':country,
            'city':city
        }
        find_user=signup_data.find(data)
        print(find_user)
        return jsonify({
            'message':"find user successfull"
        })
        


@app.route("/feedback", methods=['POST'])
@token_required
def feedback(current_user):
    user_id = current_user.get('_id')
    if request.method == 'POST':
        
        feedback_text = request.form.get('feedback')
        star = request.form.get('star')

        feedback_doc = {
            "user_id": user_id,
            "feedback": feedback_text,
            "star": star
        }
        
        result =feedback_collection.insert_one(feedback_doc)
        
        if result.acknowledged:
            return jsonify({"message": "Feedback saved successfully."}), 200
        else:
            return jsonify({"message": "Failed to save feedback."}), 500
    else:
        return jsonify({"message": "Invalid request method."}), 405



if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0", port=8080)