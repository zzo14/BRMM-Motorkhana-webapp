# Motorkhana Web Application Project
## Introduction
Welcome to the GitHub repository for our COMP636 project, a web application designed for managing Motorkhana events organized by the BRMM car club.  This application aims to streamline the management of drivers, cars, courses, and run results, enhancing the event experience through efficient data handling and intuitive user interfaces.

## Key Features:
 + **Driver and Car Management**: Seamlessly manage driver entries and associate them with specific cars.
 + **Course and Run Handling**: Efficiently organize courses and track driver run details.
 + **Result Calculation**: Automated calculation of best run times and overall results, including penalties.
 + **Junior Driver Support**: Special attention to junior drivers, ensuring proper age and caregiver record management.

## Live Demo
Check out our live application here: [Motorkhana Web App](https://patzou.pythonanywhere.com/)

## Installation
Follow these steps to install and run the BRMM-Motorkhana webapp:

1. Clone the repository to your local machine:
   `git clone https://github.com/your-username/BRMM-Motorkhana-webapp`
2. Change the directory to the cloned repository:
   `cd BRMM-Motorkhana-webapp`
3. Install the required dependencies:
   `pip install -r requirements.txt`
4. Run the webapp using Flask:
   `flask run`

## Web Application Structure
### Routes & Functions
1. **@app.route("/"), Function: home()**
   - Renders the ***base.html*** template, acting as the application's homepage.

2. **@app.route("/listdrivers"), Function: listdrivers()**
   - Fetches a list of all drivers from the database.
   - Passes the following data to the ***listdrivers.html*** template:
     - List of drivers' information

3. **@app.route("/driversrun"), Function: driversrun()**
   - Fetches a list of all drivers from the database.
   - Allows the user to select a driver from a dropdown.
   - Passes the following data to the ***driversrun.html*** template:
     - List of all drivers (for dropdown)
     - Selected driver's information (if chosen)

4. **@app.route("/allresult"), Function: allresult()**
   - Fetches a list of all drivers and their best run times from the database.
   - Calculates the overall results for each driver using the ***mod_allresult()*** function.
   - Passes the following data to the ***allresult.html*** template:
     - List of drivers and their overall results (processed by ***mod_allresult()***)

5. **@app.route("/graph"), Function: showgraph()**
   - Fetches driver and runs information from the database.
   - Calculates the top 5 drivers based on their overall results using the ***mod_allresult()*** function.
   - Passes the following data to the ***top5graph.html*** template:
     - Names of the top 5 drivers
     - Their corresponding overall results (processed by ***mod_allresult()***)

6. **@app.route("/listcourses"), Function: listcourses()**
   - Fetches a list of all courses from the database.
   - Passes the following data to the ***listcourses.html*** template:
     - List of course information

7. **@app.route("/admin"), Function: admin()**
   - Renders the ***admin.html*** template, serving as the admin interface's homepage.
   - Allows administrators to search for drivers.
   - Fetches driver information based on search queries from the database.
   - Passes the following data to the ***admin.html*** template:
     - Search results (driver information)

8. **@app.route("/admin/junior_driver"), Function: junior_driver()**
    - Fetches a list of junior drivers (drivers aged 25 or younger) from the database.
   - Passes the following data to the ***junior_driver.html*** template:
     - List of junior driver information

9. **@app.route("/admin/edit_run"), Function: edit_run()**
      - Allows administrators to edit run information for drivers.
      - Fetches and passes the following data to the ***edit_run.html*** template:
        - Driver and run information
        - If modified, updated run info is sent back to the server

10. **@app.route("/admin/add_driver"), Function: add_driver()**
       - Renders the ***add_driver.html*** template, providing an option to choose between adding an adult or junior driver.
       - Redirects to the "/admin/add_adult" or "/admin/add_junior".

11. **@app.route("/admin/add_adult"), Function: add_adult()**
       - Allows administrators to add new adult drivers.
       - Fetches car information from the database to populate a dropdown.
       - Passes the following data to the ***add_adult.html*** template:
         - List of cars (for dropdown)
       - Redirects back to the "/admin/add_driver" after successful adding.

12. **@app.route("/admin/add_junior"), Function: add_junior()**
       - Allows administrators to add new junior drivers.
       - Fetches car and caregiver information from the database.
       - Passes the following data to the ***add_junior.html*** template:
         - List of cars (for dropdown)
         - List of caregivers (for dropdown)
       - Redirects back to the "/admin/add_driver" after successful adding.

### Additional Functions
1. **mod_allresult(allresult)**
   - Processes the driver and runs data to calculate overall results.
   - Returns a list of drivers with their overall results.

2. **calculate_age(date_birth)**
   - Calculates the age of a driver based on their date of birth.
   - Returns the driver's age or None if the date of birth is not provided.
 
## Image Sources
- **American Muscle Whitianga. (n.d.).** [american-muscle-whitianga-75-1681772520 used as background]. All About Whitianga.  
[https://allaboutwhitianga.co.nz/community/clubs-groups/hobbies/car-clubs/american-muscle-whitianga](https://allaboutwhitianga.co.nz/community/clubs-groups/hobbies/car-clubs/american-muscle-whitianga)

- **Canterbury Car Club. (n.d.).** [motorkhana1 saved as motorkhana1]. Canterbury Car Club.  
[https://www.canterburycarclub.co.nz/club-racing/motorkhana/](https://www.canterburycarclub.co.nz/club-racing/motorkhana/)

- **Canterbury Car Club. (n.d.).** [IMG_7780SMALL saved as motorkhana2]. Canterbury Car Club.  
[https://www.canterburycarclub.co.nz/club-racing/motorkhana/](https://www.canterburycarclub.co.nz/club-racing/motorkhana/)

- **Canterbury Car Club. (n.d.).** [clubsport-05 saved as motorkhana3]. Canterbury Car Club.  
[https://www.canterburycarclub.co.nz/club-racing/motorkhana/](https://www.canterburycarclub.co.nz/club-racing/motorkhana/)

