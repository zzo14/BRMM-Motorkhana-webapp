from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
import re
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)
app.secret_key = 'key'

dbconn = None
connection = None

COURSES = ['A', 'B', 'C', 'D', 'E', 'F']

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

@app.route("/listdrivers")
def listdrivers():
    """Fetch and display a list of all drivers with details."""
    connection = getCursor()
    connection.execute("""SELECT d1.driver_id, d1.first_name, d1.surname, d1.date_of_birth, d1.age, 
                          CONCAT(d2.first_name,' ',d2.surname) AS caregiver_name, d1.model, d1.drive_class 
                          FROM (SELECT * FROM driver d JOIN car c ON d.car = c.car_num) d1 LEFT JOIN driver d2 ON d1.caregiver = d2.driver_id 
                          ORDER BY d1.surname, d1.first_name;""")
    driver_list = connection.fetchall()
    print(driver_list)
    return render_template("listdrivers.html", driver_list = driver_list)    

@app.route("/driversrun")
def driversrun():
    """Fetch and display driver run data based on selected driver."""
    connection = getCursor()
    # Fetching all driver names for the dropdown
    connection.execute("SELECT DISTINCT d.driver_id, CONCAT(d.first_name, ' ' , d.surname) as driver_name, d.age FROM driver d;")
    all_drivers = connection.fetchall()

    # Fetching selected driver's data
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
    """Fetch and display the result of all drivers across all courses."""
    connection = getCursor()
    connection.execute("""SELECT d.driver_id, CONCAT(d.first_name, ' ' , d.surname) as driver_name, d.age, d.model, 
                          r.crs_id, IF(ISNULL(MIN(r.seconds+IFNULL(r.cones,0)*5+r.wd*10)), 'dnf', FORMAT(MIN(r.seconds+(IFNULL(r.cones,0))*5+r.wd*10), 2)) AS best_time
                          FROM (SELECT * FROM driver d JOIN car c ON d.car = c.car_num) d 
                          JOIN (SELECT * FROM run r JOIN course c ON r.crs_id = c.course_id) r 
                          ON d.driver_id = r.dr_id GROUP BY d.driver_id, r.crs_id ORDER BY d.driver_id, r.crs_id; """)
    all_result = connection.fetchall()
    print(all_result)
    sorted_drivers = mod_allresult(all_result)
    return render_template("allresult.html", all_result=sorted_drivers)

@app.route("/graph")
def showgraph():
    """Fetch and display a graph of the top 5 drivers overall."""
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

@app.route("/listcourses")
def listcourses():
    """Fetch and display a list of all courses."""
    connection = getCursor()
    connection.execute("SELECT * FROM course;")
    course_list = connection.fetchall()
    return render_template("listcourses.html", course_list = course_list)

def mod_allresult(allresult):
    """Process and sort driver run data for display."""
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
                "name": driver_name + (' (J)' if age and age <= 25 else ''),
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
    """Handle searches for drivers and display results."""
    connection = getCursor()
    result = []
    query = []
    # Handling POST request for new adult driver
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        name_list = query.split()
        if len(name_list) == 2:
            first_name, last_name = name_list[0], name_list[1]
            connection.execute("""SELECT * FROM driver WHERE first_name LIKE %s and surname LIKE %s;""", 
                           (f"%{first_name}%" if query else None,f"%{last_name}%" if query else None,))
            result = connection.fetchall()
            print(result)
        elif len(name_list) == 1:
            first_name, last_name= name_list[0], name_list[0]
            connection.execute("""SELECT * FROM driver WHERE first_name LIKE %s or surname LIKE %s;""", 
                           (f"%{first_name}%" if query else None,f"%{last_name}%" if query else None,))
            result = connection.fetchall()
            print(result)
        else:
            first_name, last_name = None, None
            return redirect(url_for('admin'))
        print(first_name, last_name)

        modified_result = []
        for item in result:
            # Convert each tuple to a list, modify the date, then convert it back to a tuple
            item_list = list(item)
            if item_list[3]:
                item_list[3] = item[3].strftime('%d/%m/%Y')
            modified_result.append(tuple(item_list))

        session['result'] = modified_result
        session['query'] = query
        return redirect(url_for('admin'))
    result = session.pop('result', None)
    query = session.pop('query', None)  # Retrieve the data from the session and clear
    print(result)
    return render_template("admin.html", query=query,result=result)

@app.route("/admin/junior_driver")
def junior_driver():
    """Fetch all junior drivers (age <= 25) details"""
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
    """Handle the editing of run data for drivers."""
    connection = getCursor()
    # If the request method is POST, update the driver's run data in the database
    if request.method == "POST":
        # Fetch data form template
        driver_id = request.form.get("driver_id")
        driver_name = request.form.get("driver_name")
        course_id = request.form.get("course_id")
        run_num = request.form.get("run_num")
        times = round(float(request.form.get("times") if request.form.get("times") != '0' else None), 2)
        cones = request.form.get("cones") if request.form.get("cones") != '0' else None
        wd = request.form.get("wd")
        if times == None:
            if cones != None:
                flash("Runs data of {}-{} at Course {} run {} doesn't have Time data. No updates were made. Please check your enter and edit again.".format(driver_id, driver_name, course_id, run_num), "danger")
            return redirect(url_for('edit_run'))

        connection.execute("""UPDATE run
                              SET seconds = %s, cones = %s, wd = %s
                              WHERE dr_id=%s AND crs_id=%s AND run_num=%s;""", 
                              (times, cones, wd, driver_id,course_id,run_num,))
        # Check the number of affected rows
        affected_rows = connection.rowcount
        # Provide feedback based on the result of the update
        if affected_rows > 0:
            flash("Successfully updated runs data of {}-{} at Course {} run {}.".format(driver_id, driver_name, course_id, run_num), "success")
        else:
            flash("No rows were updated. Please check your enter and edit again.", "danger")
        return redirect(url_for('edit_run'))
    
    # Fetch and display existing run data for editing
    connection.execute("""SELECT d.driver_id, CONCAT(d.first_name, ' ' , d.surname) as driver_name, r.crs_id, r.run_num, 
                          r.seconds, r.cones, r.wd, d.age
                          FROM driver d 
                          JOIN (SELECT * FROM run r JOIN course c ON r.crs_id = c.course_id) r 
                          ON d.driver_id = r.dr_id ORDER BY d.driver_id, r.crs_id, run_num;""")
    drivers_list = connection.fetchall()
    driver = request.args.get('driver')
    driver_id, driver_name = None, None
    if driver:
        driver_id, driver_name = driver.split('-', 1)
    return render_template("edit_run.html", drivers_list=drivers_list, driver_id=driver_id, driver_name=driver_name)

@app.route("/admin/add_adult", methods=['GET', 'POST'])
def add_adult():
    """Handle the addition of new adult drivers to the database."""
    connection = getCursor()
    # Get all driver names for the dropdown
    connection.execute("SELECT * FROM car;")
    all_cars = connection.fetchall()
    selected_car = request.args.get('car')

    if request.method == "POST":
        # Fetch data form template
        first_name = request.form.get("first_name").strip()
        last_name = request.form.get("last_name").strip()
        car = request.form.get("car")
        print(first_name, last_name, car)

        connection.execute("""INSERT INTO driver (first_name, surname, date_of_birth, age, caregiver, car)
                              VALUES(%s, %s, %s, %s, %s, %s)""", 
                              (first_name, last_name, None, None, None, car))
        new_id = connection.lastrowid
        # Check the number of affected rows
        affected_rows = connection.rowcount
        # Add 12 blank runs for each course with null times and cones.
        if new_id and affected_rows > 0:
            for course in COURSES:
                for run_num in [1, 2]:
                    connection.execute("""INSERT INTO run (dr_id, crs_id, run_num, seconds, cones, wd) 
                                          VALUES (%s, %s, %s, NULL, NULL, 0)""", (new_id, course, run_num))
            # Provide feedback based on the result of the update
            flash("Successfully add a new adult driver, <a href='/listdrivers'>driver id is {}!</a>".format(new_id), "success")
            return redirect(url_for('add_driver'))
        else:
            flash("No rows were added. Please check your enter and add again.", "danger")
            return redirect(url_for('add_adult'))
    return render_template("add_adult.html", all_cars=all_cars, selected_car=selected_car)


@app.route("/admin/add_junior", methods=['GET', 'POST'])
def add_junior():
    """Handle the addition of new junior drivers to the database."""
    connection = getCursor()
    # Get all driver names for the dropdown
    connection.execute("SELECT * FROM car;")
    all_cars = connection.fetchall()
    selected_car = request.args.get('car')

    connection.execute("SELECT * FROM driver WHERE age >25 or ISNULL(age);")
    all_drivers = connection.fetchall()
    selected_caregiver = request.args.get('caregiver')

    if request.method == "POST":
        # Fetch data form template
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        date_birth = request.form.get("date_birth")
        caregiver = request.form.get("caregiver")
        car = request.form.get("car")
        print(first_name, last_name, date_birth, caregiver, car)

        age = calculate_age(date_birth)
        if 12 <= age <= 16 and caregiver is None:
            flash("As driver is under 16 years old, a caregiver is required!", "danger")
            return redirect(url_for('add_junior'))
        if age > 25:
            flash("As driver is over 25 years old, Please go to <a href='/admin/add_adult'>add adult page</a>!", "danger")
            return redirect(url_for('add_junior'))

        connection.execute("""INSERT INTO driver (first_name, surname, date_of_birth, age, caregiver, car)
                              VALUES(%s, %s, %s, %s, %s, %s)""", 
                              (first_name, last_name, date_birth if date_birth != "" else None, age, caregiver, car))
        new_id = connection.lastrowid
        # Check the number of affected rows
        affected_rows = connection.rowcount
        # Add 12 blank runs for each course with null times and cones.
        if new_id and affected_rows > 0:
            for course in COURSES:
                for run_num in [1, 2]:
                    connection.execute("""INSERT INTO run (dr_id, crs_id, run_num, seconds, cones, wd) 
                                          VALUES (%s, %s, %s, NULL, NULL, 0)""", (new_id, course, run_num))
            # Provide feedback based on the result of the update
            flash("Successfully add a new junior driver, <a href='/listdrivers'>driver id is {}!</a>".format(new_id), "success")
            return redirect(url_for('add_driver'))
        else:
            flash("No rows were added. Please check your enter and add again.", "danger")
            return redirect(url_for('add_junior'))
    
    max_time = (datetime.today() - timedelta(days=12*365)).strftime('%Y-%m-%d')
    return render_template("add_junior.html", all_cars=all_cars, selected_car=selected_car, 
                           all_drivers=all_drivers,selected_caregiver=selected_caregiver, max_time=max_time)

@app.route("/admin/add_driver", methods=['GET', 'POST'])
def add_driver():
    """Handle the choice between adding an adult or junior driver, then redirect to the page."""
    if request.method == "POST":
        age_choose = request.form.get("age_rank")
        if age_choose == "adult":
            return redirect(url_for('add_adult'))
        elif age_choose == "junior":
            return redirect(url_for('add_junior'))
    return render_template("add_driver.html")

def calculate_age(date_birth):
    """Calculate and return the age based on date of birth."""
    if date_birth:
        birth_date = datetime.strptime(date_birth, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    return None
