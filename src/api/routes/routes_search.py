from flask import Blueprint
from api.utils import responses as resp
from api.utils.responses import response_with
import pymysql

route_search = Blueprint("route_search", __name__)


@route_search.route("/search", methods=["GET"])
def search():
    # resp = s.query(sql="SELECT * from employees")
    # Open database connection
    #RootRoot
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='RootRoot', db='employees')

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT VERSION()")

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print("Database version : %s " % data)

    # disconnect from server
    db.close()
    return response_with(resp.SUCCESS_200, value={"data": "yo"})
