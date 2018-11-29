from flask import Blueprint, request, render_template
from api.utils import responses as resp
from api.utils.responses import response_with
import pymysql
import tweepy
from twilio.rest import Client
import os

route_employee = Blueprint("route_employee", __name__)


@route_employee.route("/employee", methods=['POST', 'GET'])
def employee():
    if os.environ.get('WORK_ENV') == 'PROD':
        db = pymysql.connect(host='cmpe172.ccovvyr3arwg.us-west-1.rds.amazonaws.com', port=3306, user='cmpe172',
                             passwd='qwerty123', db='employees')
    else:
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='rajmakda', db='employees')

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
                message = f'{name[0]} {name[1]} was just promoted to {emp_title}!'
                post_to_twitter(message)
                send_sms(message)
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
        cursor.execute(f'SELECT employees.emp_no, employees.first_name, employees.last_name, employees.gender, titles.title '
                       f'FROM employees '
                       f'INNER JOIN titles ON employees.emp_no = titles.emp_no '
                       f'WHERE employees.first_name = "{first_name}" '
                       f'AND employees.last_name = "{last_name}";')
        data = cursor.fetchone()
        emp_no = data[0]
        gender = data[3]
        title = data[4]

        cursor.execute(f'SELECT salary FROM salaries WHERE emp_no="{emp_no}"')
        data = cursor.fetchone()
        emp_salary = data[0]

        cursor.execute(f'SELECT dept_no FROM dept_emp WHERE emp_no="{emp_no}"')
        data = cursor.fetchone()
        dept_no = data[0]

        cursor.execute(f'SELECT dept_name FROM departments WHERE dept_no="{dept_no}"')
        data = cursor.fetchone()
        dept_name = data[0]

        cursor.execute(f'SELECT emp_no FROM dept_manager WHERE dept_no="{dept_no}"')
        data = cursor.fetchone()
        emp_manager_no = data[0]

        cursor.execute(
            f'SELECT employees.first_name, employees.last_name, titles.title '
            f'FROM employees '
            f'INNER JOIN titles ON employees.emp_no = titles.emp_no '
            f'WHERE employees.emp_no = "{emp_manager_no}";')
        data = cursor.fetchone()
        emp_manager_first_name = data[0]
        emp_manager_last_name = data[1]
        emp_manager_title = data[2]

        return response_with(resp.SUCCESS_200, value={
            "emp_no": emp_no,
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "title": title,
            "emp_salary": emp_salary,
            "dept_name": dept_name,
            "emp_manager_first_name": emp_manager_first_name,
            "emp_manager_last_name": emp_manager_last_name,
            "emp_manager_title": emp_manager_title
        })

    db.close()
    return response_with(resp.SUCCESS_200, value={"data": "yo"})


def send_sms(message):
    account_sid = 'ACa439f7f51fb18d06389f4fa701bdc40e'
    auth_token = '6ed41c6c810733ae848311c77f3b7c8a'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(body=message, from_='+15106069597', to='+14087442075')
    print(f'Message sent. Status: {message.status}')


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
