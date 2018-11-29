from flask import Blueprint, request, render_template
from api.utils import responses as resp
from api.utils.responses import response_with
import pymysql

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
            except Exception as e:
                print(e)

        if emp_salary != '':
            query = f'UPDATE salaries SET salary="{emp_salary}" WHERE emp_no={emp_no}'
            try:
                cursor.execute(query)
                db.commit()
            except Exception as e:
                print(e)

        # postToTwitter("$first_name $last_name was just promoted to $emp_title");

    if request.method == 'GET':
        first_name = request.args['firstName']
        last_name = request.args['lastName']
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='RootRoot', db='employees')
        cursor.execute(f'SELECT employees.*, titles.title '
                       f'FROM employees '
                       f'INNER JOIN titles ON employees.emp_no = titles.emp_no '
                       f'WHERE employees.first_name = "{first_name}" '
                       f'AND employees.last_name = "{last_name}";')
        data = cursor.fetchone()
        print(data)

    db.close()
    return response_with(resp.SUCCESS_200, value={"data": "yo"})
