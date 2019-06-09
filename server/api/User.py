from flask import Blueprint, render_template, abort,request,jsonify


api_user = Blueprint('api_user', __name__,
                        template_folder='templates')



USER = {"tuC3B1iWhpFO0S0LQeCVZAwm2hyMsX00":{"fio":"ФИО",
                                           "educationInstitution":"Учебное заведение",
                                            "sex":"Пол",
                                            "faculty":"факультет",
                                            "status":"Статус",
                                            "yearsOfEducation":"3"}}

@api_user.route("/api/user/",methods = ["GET"])
def getUserByInfo():
    data = request.json
    token = request.args["token"]

    global USER
    return jsonify(USER[token])


@api_user.route("/api/user/",methods = ["POST"])
def setUserInfo():
    data = request.json
    print(data)
    token = data["params"]["token"]
    print(data["params"]["data"])
    USER[token] = data["params"]["data"]
    return "ok"
