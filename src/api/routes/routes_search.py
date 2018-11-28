from flask import Blueprint
from api.utils import responses as resp
from api.utils.responses import response_with
from api.utils.sql import sql

route_search = Blueprint("route_search", __name__)


@route_search.route("/search", methods=["GET"])
def search():
    s = sql()
    resp = s.query(sql="SELECT * from employees")
    return response_with(resp.SUCCESS_200, value={"data": "yo"})
