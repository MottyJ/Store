from bottle import route, run, template, static_file, get, post, delete, request, response
from sys import argv
import json
import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="secret",
    db="store",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)

@post("/category")
def category():
    category_name = request.forms.get("name")
    try:
        with connection.cursor() as cursor:
            if len(category_name) == 0:
                return json.dumps({"STATUS": "ERROR", "MSG": "Name parameter is missing", "CODE": response.status_code})
            else:
                sql = "INSERT INTO `categories` (`Name`) VALUES (%s)"
                cursor.execute(sql, (category_name))
                return json.dumps({"STATUS": "SUCCESS", "CAT_ID": cursor.lastrowid, "CODE": response.status_code})
    except:
        if response.status_code == 200:
            return json.dumps({"STATUS": "ERROR", "MSG": "Category already exists", "CODE": response.status_code})
        elif response.status_code == 400:
            return json.dumps({"STATUS": "ERROR", "MSG": "Bad request", "CODE": response.status_code})
        elif response.status_code == 500:
            return json.dumps({"STATUS": "ERROR", "MSG": "Internal error", "CODE": response.status_code})
        else:
            return json.dumps({"STATUS": "ERROR", "MSG": "I'm not sure if there are more errors possible, but if there are, this should suffice!", "CODE": response.status_code})



@get("/admin")
def admin_portal():
	return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


run(host='0.0.0.0', port=7000)
