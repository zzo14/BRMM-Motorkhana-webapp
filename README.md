# COMP636-BRMM-webapp
## Web Application Structure
### Routes & Functions
1. **@app.route("/") in app.py**
   - Renders the ***base.html*** template, serving as the application's homepage.

2. **@app.route("/listdrivers") in app.py**
   - Retrieves a list of all drivers from the database.
   - Passes the following data to the ***listdrivers.html*** template:
     - List of drivers' information

3. **@app.route("/driversrun") in app.py**
   - Retrieves a list of all drivers from the database.
   - Allows the user to select a driver from a dropdown.
   - Passes the following data to the ***driversrun.html*** template:
     - List of all drivers (for dropdown)
     - Selected driver's information (if chosen)

4. **@app.route("/allresult") in app.py**
   - Retrieves a list of all drivers and their best run times from the database.
   - Calculates the overall results for each driver using the *mod_allresult* function.
   - Passes the following data to the ***allresult.html*** template:
     - List of drivers and their overall results (processed by *mod_allresult*)

5. **@app.route("/graph") in app.py**
   - Retrieves driver and runs information from the database.
   - Calculates the top 5 drivers based on their overall results using the *mod_allresult* function.
   - Passes the following data to the ***top5graph.html*** template:
     - Names of the top 5 drivers
     - Their corresponding overall results (processed by *mod_allresult*)

6. **@app.route("/listcourses") in app.py**
   - Retrieves a list of all courses from the database.
   - Passes the following data to the ***listcourses.html*** template:
     - List of course information

7. **@app.route("/admin") in app.py**
   - Renders the ***admin.html*** template, serving as the admin interface's homepage.
   - Allows administrators to search for drivers.
   - Retrieves driver information based on search queries from the database.
   - Passes the following data to the ***admin.html*** template:
     - Search results (driver information)

8. **@app.route("/admin/junior_driver") in app.py**
   - Retrieves a list of junior drivers (drivers aged 25 or younger) from the database.
   - Passes the following data to the ***junior_driver.html*** template:
     - List of junior driver information

9. **@app.route("/admin/junior_driver") in app.py**
   - Retrieves a list of junior drivers (drivers aged 25 or younger) from the database.
   - Passes the following data to the ***junior_driver.html*** template:
     - List of junior driver information

10. **@app.route("/admin/edit_run") in app.py**
       - Allows administrators to edit run information for drivers.
       - Retrieves and passes the following data to the ***edit_run.html*** template:
         - Driver and run information
         - Updated run information (if modified)

11. **@app.route("/admin/add_driver") in app.py**
       - Renders the ***add_driver.html*** template, providing an option to choose between adding an adult or junior driver.

12. **@app.route("/admin/add_adult") in app.py**
       - Allows administrators to add new adult drivers.
       - Retrieves car information from the database to populate a dropdown.
       - Passes the following data to the ***add_adult.html*** template:
         - List of cars (for dropdown)

13. **@app.route("/admin/add_junior") in app.py**
       - Allows administrators to add new junior drivers.
       - Retrieves car and caregiver information from the database.
       - Passes the following data to the ***add_junior.html*** template:
         - List of cars (for dropdown)
         - List of caregivers (for dropdown)

### Additional Functions
1. **mod_allresult(allresult) in app.py**
   - Processes the driver and runs data to calculate overall results.
   - Returns a list of drivers with their overall results.

2. **calculate_age(date_birth) in app.py**
   - Calculates the age of a driver based on their date of birth.
   - Returns the driver's age or None if the date of birth is not provided.


## Assumptions and design decisions
### Assumptions:
1. **Desktop Focus:** The website is designed primarily for desktop displays, and mobile platforms are not a priority.
2. **Integration of Features:** Assume the driver search feature is on the home page of the admin interface and linked to other features, such as listing all drivers and editing runs.
3. **Flash Messages for Feedback:** Flash messages are used to provide real-time feedback to administrators regarding the success or failure of their actions, such as adding or editing driver information.

### Design Decisions
#### Public Interface
1. **Design a Home Page for Introducing the Motorkhana Event:**
     - The home page serves as the gateway to the application, introducing users to the Motorkhana event. It provides an initial impression and context for the application's purpose.
       
2. **Fixed Navigation Bar:**
     - The decision to fix the navigation bar at the top of the page, even during scrolling, ensures that users have constant access to essential navigation options. This design choice enhances the user experience by offering quick and convenient access to various parts of the application.
       
3. **Display Full Names in Separate Columns:**
     - Full names of drivers are consistently displayed in separate columns to optimise page space and improve the overall user experience. This design decision enhances readability and allows users to easily scan and compare driver information.
       
4. **Indicating Junior Drivers with "(J)":**
     - To provide clear and immediate identification, the application consistently appends "(J)" to the names of junior drivers. This design choice ensures that users can easily distinguish between junior and adult drivers, improving user understanding.
       
5. **Bootstrap Modals for Viewing Images:**
     - Bootstrap modals were employed on the courselist page to implement a user-friendly feature that allows users to click on images to view them in a larger format. This design decision enhances the user experience by providing an interactive and space-efficient way to examine course images without navigating to separate pages.
       
6. **Using .table-hover for Table Rows:**
     - The table-hover feature creates a user-friendly interaction by highlighting table rows when users hover their mouse over them. This provides a visual cue for interactive elements within the table, making it easier for users to identify and engage with data.
       
7. **Using Bootstrap Container for Centered Page Display:**
     - By wrapping the application's content within a container, ensure that it is displayed in a visually pleasing and organised manner. This design decision contributes to better aesthetics and readability, making it easier for users to navigate and engage with the application's content. Centering the content also maintains a consistent and balanced layout, which is visually appealing and user-friendly.

#### Admin Interface
1. **Driver Search Interface on Home Page:**
     - Placing the driver search interface on the home page of the admin interface streamlines the administrator's workflow. It allows administrators to quickly query driver information and quickly link to the target driver page to view or modify driver results on demand, contributing to a cohesive user experience.
       
2. **Modal for Editing Runs:**
     - The use of modals for editing run data offers a convenient and space-efficient method for administrators to update run information. Modals provide a seamless user experience by allowing data editing without the need to navigate to separate pages.
       
3. **Radio Button Group for Age Rank Selection on the add driver page:**
     - A radio button group is utilised to enable users to select the age rank of new drivers (over 25 or not). This design choice offers clear options and categorises drivers correctly, simplifying the data entry process.
       
4. **Dropdown Selections with Dynamic Generation on the add driver page:**
     - Dropdown select inputs are implemented for caregiver and car selection, ensuring simplified user input. Dynamic generation of options based on available data enhances the user experience by reducing input errors and providing relevant choices.
       
5. **Validation for Data Accuracy:**
     - Form validation is integrated to ensure data accuracy. This includes validating fields like date of birth using a date picker, times and cones cannot be negative, to confirm that users enter valid information.
       
6. **Clear Buttons for Form Reset:**
     - Clear buttons are added to forms to facilitate user interactions by allowing quick and effortless resetting of form fields. This design choice enhances user convenience during data entry.
       
7. **Flash Messages for Immediate Feedback:**
     - Flash messages are implemented to provide immediate feedback to administrators during actions such as adding or editing driver information. This design decision enhances user-friendliness by offering clear and informative error messages when issues arise.
       
8. **Method Selection for Data Transmission:**
     - The application employs the POST method for form submissions, ensuring secure data transmission and alignment with actions that could alter the server's state. For data retrieval tasks, like fetching search results, the GET method is utilised. This approach optimally leverages GET's suitability for data retrieval without side effects and its visibility in URLs, while POST provides enhanced security for data submissions.

## Database questions
**1.	What SQL statement creates the car table and defines its three fields/columns?**
```
CREATE TABLE IF NOT EXISTS car
(
car_num INT PRIMARY KEY NOT NULL,
model VARCHAR(20) NOT NULL,
drive_class VARCHAR(3) NOT NULL
);
```

**2.	Which line of SQL code sets up the relationship between the car and driver tables?**
```
FOREIGN KEY (car) REFERENCES car(car_num) ON UPDATE CASCADE ON DELETE CASCADE
```

**3.	Which 3 lines of SQL code insert the Mini and GR Yaris details into the car table?**
```
INSERT INTO car VALUES
(11,'Mini','FWD'),
(17,'GR Yaris','4WD'),
```

**4.	Suppose the club wanted to set a default value of ‘RWD’ for the driver_class field. What specific change would you need to make to the SQL to do this?**
```
drive_class VARCHAR(3) NOT NULL DEFAULT 'RWD'
```

**5.	Suppose logins were implemented. Why is it important for drivers and the club admin to access different routes?**
 - **Data Integrity and Security:** Not all users should have the ability to modify or delete data. By limiting the routes and features available to drivers, the club can prevent accidental or malicious changes to critical data.
 - **Role-based Responsibilities:** Different roles have different responsibilities. The club admin may need to access management tools, such as adding/deleting courses, updating run times, or managing drivers' information. Meanwhile, drivers might only need to view their stats, upcoming events, or personal data. By creating distinct routes, the application can cater to these specific needs.
 - **Privacy:** Some data should remain confidential. For instance, while an admin might have access to all drivers' personal details and performance stats, a driver should only see their own information. By segregating routes, you ensure that users only access data they're authorized to view.
 - **Minimizing Errors:** By restricting access to certain functionalities, the system minimizes the chance of users making mistakes. For example, a driver accidentally deletes or modifies their records.
   
 - **Example:**
    - (1) Drivers might unintentionally or maliciously manipulate essential data, such as driver details or run results. This could compromise the integrity of the event's data and results.
    - (2) If drivers and the club admin have access to all features, the user interface could become cluttered and complex. Drivers may find it challenging to locate the functions they need, leading to frustration and reduced efficiency.

## Image Sources
- **American Muscle Whitianga. (n.d.).** [american-muscle-whitianga-75-1681772520 used as background]. All About Whitianga. [https://allaboutwhitianga.co.nz/community/clubs-groups/hobbies/car-clubs/american-muscle-whitianga](https://allaboutwhitianga.co.nz/community/clubs-groups/hobbies/car-clubs/american-muscle-whitianga)

- **Canterbury Car Club. (n.d.).** [motorkhana1 saved as motorkhana1]. Canterbury Car Club. 
\r\n[https://www.canterburycarclub.co.nz/club-racing/motorkhana/](https://www.canterburycarclub.co.nz/club-racing/motorkhana/)

- **Canterbury Car Club. (n.d.).** [IMG_7780SMALL saved as motorkhana2]. Canterbury Car Club. 
[https://www.canterburycarclub.co.nz/club-racing/motorkhana/](https://www.canterburycarclub.co.nz/club-racing/motorkhana/)

- **Canterbury Car Club. (n.d.).** [clubsport-05 saved as motorkhana3]. Canterbury Car Club. 
[https://www.canterburycarclub.co.nz/club-racing/motorkhana/](https://www.canterburycarclub.co.nz/club-racing/motorkhana/)

