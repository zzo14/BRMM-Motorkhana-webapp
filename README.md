# COMP636-BRMM-webapp
## Web Application Structure
### 1. Routes & Functions
  #### @app.route("/") in app.py
  - Renders the ***base.html*** template, serving as the application's homepage.
  #### @app.route("/listdrivers") in app.py:
  - Retrieves a list of all drivers from the database.
  - Passes the following data to the ***listdrivers.html*** template:
    - List of drivers' information
  #### @app.route("/driversrun") in app.py:
  - Retrieves a list of all drivers from the database.
  - Allows the user to select a driver from a dropdown.
  - Retrieves and passes the following data to the ***driversrun.html*** template:
    - List of all drivers (for dropdown)
    - Selected driver's information (if chosen)
  #### @app.route("/allresult") in app.py:
  - Retrieves a list of all drivers and their best run times from the database.
  - Calculates the overall results for each driver.
  - Passes the following data to the ***allresult.html*** template:
    - List of drivers and their overall results
  #### @app.route("/graph") in app.py:
  - Retrieves driver and run information from the database.
  - Calculates the top 5 drivers based on their overall results.
  - Passes the following data to the ***top5graph.html*** template:
    - Names of the top 5 drivers
    - Their corresponding overall results
  #### @app.route("/listcourses") in app.py:
  - Retrieves a list of all courses from the database.
  - Passes the following data to the ***listcourses.html*** template:
    - List of course information
  #### @app.route("/admin") in app.py:
  - Renders the ***admin.html*** template, serving as the admin interface's homepage.
  - Allows administrators to search for drivers.
  - Retrieves driver information based on search queries from the database.
  - Passes the following data to the ***admin.html*** template:
    - Search results (driver information)
  #### @app.route("/admin/junior_driver") in app.py:
  - Retrieves a list of junior drivers (drivers aged 25 or younger) from the database.
  - Passes the following data to the junior_driver.html template:
    - List of junior driver information
  #### @app.route("/admin/edit_run") in app.py:
  - Allows administrators to edit run information for drivers.
  - Retrieves and passes the following data to the edit_run.html template:
    - Driver and run information
    - Updated run information (if modified)
  #### @app.route("/admin/add_driver") in app.py:
  - Renders the add_driver.html template, providing an option to choose between adding an adult or junior driver.
  #### @app.route("/admin/add_adult") in app.py:
  - Allows administrators to add new adult drivers.
  - Retrieves car information from the database to populate a dropdown.
  - Passes the following data to the add_adult.html template:
    - List of cars (for dropdown)
  #### @app.route("/admin/add_junior") in app.py:
  - Allows administrators to add new junior drivers.
  - Retrieves car and caregiver information from the database.
  - Passes the following data to the add_junior.html template:
    - List of cars (for dropdown)
    - List of caregivers (for dropdown)

