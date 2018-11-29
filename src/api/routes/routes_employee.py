from flask import Blueprint, request, render_template
from api.utils import responses as resp
from api.utils.responses import response_with
import pymysql
import tweepy

route_employee = Blueprint("route_employee", __name__)


@route_employee.route("/employee", methods=['POST', 'GET'])
def employee():
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='RootRoot', db='employees')
    cursor = db.cursor()

    if request.method == 'POST':
        emp_no = request.form['emp_no']
        emp_title = request.form['emp_title']
        emp_salary = request.form['emp_salary']

        if emp_title != '':
            query = f'UPDATE titles SET title="{emp_title}" WHERE emp_no={emp_no}'
            try:
                cursor.execute(query)
                db.commit()
                name = get_emp_name(emp_no, cursor)
                post_to_twitter(f'{name[0]} {name[1]} was just promoted to {emp_title}!')
            except Exception as e:
                print(e)

        if emp_salary != '':
            query = f'UPDATE salaries SET salary="{emp_salary}" WHERE emp_no={emp_no}'
            try:
                cursor.execute(query)
                db.commit()
            except Exception as e:
                print(e)

    if request.method == 'GET':
        first_name = request.args['firstName']
        last_name = request.args['lastName']
        cursor.execute(f'SELECT employees.*, titles.title '
                       f'FROM employees '
                       f'INNER JOIN titles ON employees.emp_no = titles.emp_no '
                       f'WHERE employees.first_name = "{first_name}" '
                       f'AND employees.last_name = "{last_name}";')
        data = cursor.fetchone()
        print(data)

    db.close()
    return response_with(resp.SUCCESS_200, value={"data": "yo"})


def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


def post_to_twitter(message):
    cfg = {
        "consumer_key": "BUo2i2DGfvgre5ZG7amnQJwuW",
        "consumer_secret": "CKR3aVJlKNFWr8BNKayy16Ir4NkfEUzqntvDKlcpfTAOAnbKTi",
        "access_token": "625448859-W8bxEXgl9j4EBdYZXCvrnAUWI4VTO4OwIeJjugHf",
        "access_token_secret": "zLWg68fUFQHI1OVKofya8Q3vR9NoxG0r14uhTs7OmEQL6"
    }
    api = get_api(cfg)
    status = api.update_status(status=message)
    print(status)


def get_emp_name(emp_no, cursor):
    try:
        cursor.execute(f'SELECT first_name, last_name FROM employees WHERE emp_no={emp_no}')
        data = cursor.fetchone()
        return data
    except Exception as e:
        print(e)
