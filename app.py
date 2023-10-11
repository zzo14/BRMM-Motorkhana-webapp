from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)
app.secret_key = 'key'

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

# Driver Interface
@app.route("/")
def home():
    return render_template("base.html")

@app.route("/driversrun")
def driversrun():
    connection = getCursor()
    # Get all driver names for the dropdown
    connection.execute("SELECT DISTINCT d.driver_id, CONCAT(d.first_name, ' ' , d.surname) as driver_name, d.age FROM driver d;")
    all_drivers = connection.fetchall()

    selected_driver_id = request.args.get('driver_id', None)
    selected_driver = []
    if selected_driver_id:
        connection.execute("""SELECT d.driver_id, CONCAT(d.first_name, ' ' , d.surname) as driver_name, 
                              d.model, d.drive_class, CONCAT(r.crs_id,' - ', r.name) AS coures_name, r.run_num, 
                              r.seconds, r.cones, r.wd, FORMAT(r.seconds+IFNULL(r.cones,0)*5+r.wd*10, 2) AS total_time, d.age 
                              FROM (SELECT * FROM driver d JOIN car c ON d.car = c.car_num) d 
                              JOIN (SELECT * FROM run r JOIN course c ON r.crs_id = c.course_id) r 
                              ON d.driver_id = r.dr_id WHERE d.driver_id = %s ORDER BY r.crs_id, r.run_num;""", (selected_driver_id,))
        selected_driver = connection.fetchall()
    return render_template("driversrun.html", all_drivers=all_drivers, selected_driver=selected_driver, selected_driver_id=selected_driver_id)

@app.route("/allresult")
def allresult():
    connection = getCursor()
    connection.execute("""SELECT d.driver_id, CONCAT(d.first_name, ' ' , d.surname) as driver_name, d.age, d.model, 
                          r.crs_id, IF(MIN(r.seconds), MIN(FORMAT(r.seconds+IFNULL(r.cones,0)*5+r.wd*10, 2)), 'dnf') AS best_time
                          FROM (SELECT * FROM driver d JOIN car c ON d.car = c.car_num) d 
                          JOIN (SELECT * FROM run r JOIN course c ON r.crs_id = c.course_id) r 
                          ON d.driver_id = r.dr_id GROUP BY d.driver_id, r.crs_id ORDER BY d.driver_id; """)
    allresult = connection.fetchall()
    print(allresult)
    sorted_drivers = mod_allresult(allresult)
    return render_template("allresult.html", allresult=sorted_drivers)

@app.route("/listdrivers")
def listdrivers():
    connection = getCursor()
    connection.execute("""SELECT d1.driver_id, d1.first_name, d1.surname, d1.date_of_birth, d1.age, 
                          CONCAT(d2.first_name,' ',d2.surname) AS caregiver_name, d1.model, d1.drive_class 
                          FROM (SELECT * FROM driver d JOIN car c ON d.car = c.car_num) d1 LEFT JOIN driver d2 ON d1.caregiver = d2.driver_id 
                          ORDER BY d1.surname, d1.first_name;""")
    driverList = connection.fetchall()
    print(driverList)
    return render_template("driverlist.html", driver_list = driverList)    

@app.route("/listcourses")
def listcourses():
    connection = getCursor()
    connection.execute("SELECT * FROM course;")
    courseList = connection.fetchall()
    return render_template("courselist.html", course_list = courseList)

@app.route("/graph")
def showgraph():
    connection = getCursor()
    # Insert code to get top 5 drivers overall, ordered by their final results.
    # Use that to construct 2 lists: bestDriverList containing the names, resultsList containing the final result values
    # Names should include their ID and a trailing space, eg '133 Oliver Ngatai '
    connection.execute("""SELECT d.driver_id, CONCAT(d.first_name, ' ' , d.surname) as driver_name, d.age, d.model, 
                          r.crs_id, IF(MIN(r.seconds), MIN(FORMAT(r.seconds+IFNULL(r.cones,0)*5+r.wd*10, 2)), 'dnf') AS best_time
                          FROM (SELECT * FROM driver d JOIN car c ON d.car = c.car_num) d 
                          JOIN (SELECT * FROM run r JOIN course c ON r.crs_id = c.course_id) r 
                          ON d.driver_id = r.dr_id GROUP BY d.driver_id, r.crs_id ORDER BY d.driver_id; """)
    allresult = connection.fetchall()
    top5_result = mod_allresult(allresult)[:5]
    bestDriverList = [f"{dr['id']}-{dr['name']}" for dr in top5_result]
    resultsList = [dr['overall_result'] for dr in top5_result]
    print(bestDriverList)
    print(resultsList)
    return render_template("top5graph.html", name_list = bestDriverList, value_list = resultsList)

def mod_allresult(allresult):
    drivers = {}  # Dictionary to hold calculated data
    for row in allresult:
        driver_id = row[0]
        driver_name = row[1]
        age = row[2]
        car_model = row[3]
        course = row[4]
        best_time = row[5]

        if driver_id not in drivers:
            drivers[driver_id] = {
                "id": driver_id,
                "name": driver_name + (' (J)' if age and age <= 16 else ''),
                "car_model": car_model,
                "courses": {},
                "total_time": 0
            }
        drivers[driver_id]["courses"][course] = best_time

        # If not dnf, add time to total
        if best_time != 'dnf':
            drivers[driver_id]["total_time"] += float(best_time)

    # Check if driver is qualified
    for driver_id, data in drivers.items():
        if len(data["courses"]) < 6 or any(v == 'dnf' for v in data["courses"].values()):
            data["overall_result"] = "NQ"
        else:
            data["overall_result"] = data["total_time"]
        if data['overall_result'] != 'NQ':
            data["overall_result"] = f'{data["overall_result"]:.2f}'

    # Sort drivers by overall results, NQ at the bottom
    sorted_drivers = sorted(drivers.values(), key=lambda x: (x["overall_result"] == "NQ", x["overall_result"]))

    # Assign cup and prize
    if sorted_drivers:
        sorted_drivers[0]["award"] = "cup"
        for driver in sorted_drivers[1:5]:
            driver["award"] = "prize"
    print(sorted_drivers)
    return sorted_drivers


# Adminisrator Interface
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    connection = getCursor()
    result = []
    query = []
    if request.method == "POST":
        query = request.form.get("query")
        print(query)
        connection.execute("""SELECT * FROM driver WHERE first_name LIKE %s or surname LIKE %s;""", 
                           ("%" + query + "%" if query else None,"%" + query + "%" if query else None))
        result = connection.fetchall()
        print(result)
        session['result'] = result
        session['query'] = query
        return redirect(url_for('admin'))
    result = session.get('result')
    query = session.get('query')  # Retrieve the query from the session
    session['result'] = None
    session['query'] = None  # Clear the query from the session after retrieving it
    return render_template("admin.html", query=query,result=result)

@app.route("/admin/junior_driver", methods=['GET', 'POST'])
def junior_driver():
    connection = getCursor()
    connection.execute("""SELECT d1.driver_id, CONCAT(d1.first_name,' ', d1.surname) AS driver_name, d1.date_of_birth, d1.age, 
                          CONCAT(d2.first_name,' ',d2.surname) AS caregiver_name
                          FROM driver d1 LEFT JOIN driver d2 ON d1.caregiver = d2.driver_id 
                          WHERE d1.age <= 25
                          ORDER BY d1.age DESC, d1.surname;""")
    junior_drivers = connection.fetchall()
    return render_template("junior_driver.html", junior_drivers=junior_drivers)

@app.route("/admin/edit_run", methods=['GET', 'POST'])
def edit_run():
    connection = getCursor()
    if request.method == "POST":
        driver_id = request.form.get("driver_id")
        driver_name = request.form.get("driver_name")
        course_id = request.form.get("course_id")
        run_num = request.form.get("run_num")
        times = request.form.get("times")
        cones = request.form.get("cones")
        wd = request.form.get("wd")
        connection.execute("""UPDATE run
                              SET seconds = %s, cones = %s, wd = %s
                              WHERE dr_id=%s AND crs_id=%s AND run_num=%s;""", 
                              (times if times else None, cones if cones else None, wd, driver_id,course_id,run_num,))
        # Check the number of affected rows
        affected_rows = connection.rowcount
        if affected_rows > 0:
            flash("Successfully updated runs data of {}-{} at Course {} run {}.".format(driver_id, driver_name, course_id, run_num), "success")
        else:
            flash("No rows were updated. Please check your enter and edit again.", "danger")
        return redirect(url_for('edit_run'))

    connection.execute("""SELECT d.driver_id, CONCAT(d.first_name, ' ' , d.surname) as driver_name, r.crs_id, r.run_num, 
                          r.seconds, r.cones, r.wd
                          FROM driver d 
                          JOIN (SELECT * FROM run r JOIN course c ON r.crs_id = c.course_id) r 
                          ON d.driver_id = r.dr_id ORDER BY d.driver_id, r.crs_id, run_num;""")
    drivers_list = connection.fetchall()
    driver = request.args.get('driver')
    driver_id, driver_name = None, None
    if driver:
        driver_id, driver_name = driver.split('-', 1)
    return render_template("edit_run.html", drivers_list=drivers_list, driver_id=driver_id, driver_name=driver_name)

@app.route("/admin/add_driver", methods=['GET', 'POST'])
def add_driver():
    connection = getCursor()
    # Get all driver names for the dropdown
    connection.execute("SELECT * FROM car;")
    all_cars = connection.fetchall()
    selected_car = request.args.get('car')

    connection.execute("SELECT * FROM driver WHERE age >25 or ISNULL(age);")
    all_drivers = connection.fetchall()
    selected_caregiver = request.args.get('caregiver')

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        check_junior = request.form.get("check_junior")
        date_birth = request.form.get("date_birth")
        caregiver = request.form.get("caregiver")
        car = request.form.get("car")
        print(first_name, last_name, check_junior, date_birth, caregiver, car)

        age = calculate_age(date_birth)
        if check_junior == "0":
            if age is None:
                flash("As driver is under 25 years old, the date of birth must be entered!", "danger")
                return redirect(url_for('add_driver'))
            elif age < 12 or age == 0:
                flash("The driver must be over 12 years old!", "danger")
                return redirect(url_for('add_driver'))
            elif 12 <= age <= 16 and caregiver is None:
                flash("As driver is under 16 years old, a caregiver is required!", "danger")
                return redirect(url_for('add_driver'))
        else:
            if age and age < 25:
                flash("As driver is under 25 years old, please make sure select a right option!", "danger")
                return redirect(url_for('add_driver'))

        connection.execute("""INSERT INTO driver (first_name, surname, date_of_birth, age, caregiver, car)
                              VALUES(%s, %s, %s, %s, %s, %s)""", 
                              (first_name, last_name, date_birth if date_birth != "" else None, age, caregiver, car))
        new_id = connection.lastrowid
        affected_rows = connection.rowcount
        if new_id and affected_rows > 0:
            for course in ['A', 'B', 'C', 'D', 'E', 'F']:
                for run_num in [1, 2]:
                    connection.execute("""INSERT INTO run (dr_id, crs_id, run_num, seconds, cones, wd) 
                                          VALUES (%s, %s, %s, NULL, NULL, 0)""", (new_id, course, run_num))
            flash("Successfully add a new driver, driver id is {}!".format(new_id), "success")
        else:
            flash("No rows were added. Please check your enter and add again.", "danger")
        return redirect(url_for('add_driver'))
    return render_template("add_driver.html", all_cars=all_cars, selected_car=selected_car, 
                           all_drivers=all_drivers,selected_caregiver=selected_caregiver)

def calculate_age(date_birth):
    if date_birth:
        birth_date = datetime.strptime(date_birth, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    return None
