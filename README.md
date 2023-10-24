# COMP636-BRMM-webapp
## Web Application Structure
### Routes & Functions
#### @app.route("/") in app.py
- Renders the **base.html** template, serving as the application's homepage.

#### @app.route("/listdrivers") in app.py:
- Retrieves a list of all drivers from the database.
- Passes the following data to the **listdrivers.html** template:
  - List of drivers' information

#### @app.route("/driversrun") in app.py:
- Retrieves a list of all drivers from the database.
- Allows the user to select a driver from a dropdown.
- Retrieves and passes the following data to the **driversrun.html** template:
  - List of all drivers (for dropdown)
  - Selected driver's information (if chosen)
