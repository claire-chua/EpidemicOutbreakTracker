# README

##### Identification of the problem you are trying to solve by building this particular app.
Living through the COVID epidemic enabled us to see the destructive and exponential effects of infectious diseases. 
This app allows individuals to track their symptoms and log any past, current or suspected cases of any
infectious disease. 

Users are able to log their location, disease type and dates, which can help identify
and potentially help us avoid any huge outbreaks. e.g.by keeping track of the individuals
in locations experiencing particular infections in a given time period. 

#### Why is it a problem that needs solving?

Despite the highly destructive nature of COVID on the economy and multitudes of individuals' physical and mental health, 
not much has changed on an individual level. As individuals, we have power to document and share our collective
experiences, to help protect against future similar occurrences. 

This is similar to the COVID tracking app, but instead it is used for both preventative and countermeasures, and can be used for all forms of infectious diseases.

#### Why have you chosen this database system. What are the drawbacks compared to others?
For the database system, I utilised PostgreSQL primarily due to 1) familiarity and 2) the advantages heavily outweigh 
the disadvantages. 

Advantages: 
The database system is open-source, as such, it is free and widely customisable. As a student, it is more 
financially accessible than other paid database systems such as SAP HANA, and Google Cloud SQL.

Further, another advantage is its scalability. It is able to handle large amounts of data, which may not be necessary 
in the scope of this assignment but could be useful if the app is further developed for public use.

Next, it has an active community, which provides development and support for users. Hence, making it easier to receive
help and resolve issues.

It also supports a variety of data types, which enables users the flexibility in creating their database.

Disadvantages:

One of its disadvantages due to its flexibility and complexity, is the steep learning curve. This makes it harder for 
newer users to grasp the concepts. 

Another criticism is that it requires more computational power and storage than other
servers; however, this is a non issue for this assignment as we are not handling huge amounts of data.

#### Identify and discuss the key functionalities and benefits of an ORM
Object Relational Mapping enables developers to interact with a relational database with object-oriented programming, 
rather than raw SQL queries. 

One of the primary benefits include being able to write code in a familiar programming language, and does not require 
SQL knowledge. This is a huge time saver, as it converts the code into optimised SQL queries, thereby
simplifying the development process. Additionally, as the data is able to be manipulated like an object, this makes code easier to update and
maintain. Further, due to database abstraction, swapping databases is a non issue as the code does not have to be 
rewritten. Lastly, it is able to filter data to prevent SQL injection attaches, which allows the app to remain secure.

#### Document all endpoints for your API

Cases  
http://127.0.0.1:8080/cases/<id>: Enables cases to be retrieved via their id, with the get method.
http://127.0.0.1:8080/cases: Retrieves all cases.
http://127.0.0.1:8080/cases/add: Creates a new case, via JSON data provided with the post method.
http://127.0.0.1:8080/cases/<id>: Deletes a case via their id, with the delete method.
http://127.0.0.1:8080/cases/<int:id> :Updates a case via JSON data provided, with the update method.

Diseases  
http://127.0.0.1:8080/diseases/all: Retrieves all disease types, with get method.
http://127.0.0.1:8080/diseases/<id>: Retrieves one disease type via id, with the get method.
http://127.0.0.1:8080/diseases/<id>: Deletes disease type via id, with delete method.
http://127.0.0.1:8080//diseases/<id>: Updates disease type via id, with put or patch method.
http://127.0.0.1:8080/diseases/add: Creates a disease type, via JSON data provided with post method.

Symptom Tracking  
http://127.0.0.1:8080/symptom_trackings: Retrieves all symptom tracking data, with get method.
http://127.0.0.1:8080/symptom_trackings/<id>: Retrieves one symptom tracking via id, with get method.
http://127.0.0.1:8080/symptom_trackings/add : Creates a symptom tracking via JSON data, with post method.
http://127.0.0.1:8080/symptom_trackings/<id>: Deletes one symptom tracking via id, with delete method
http://127.0.0.1:8080/symptom_trackings/<int:id>: Updates one symptom tracking via id with JSON data provided, with put
or patch method.

CLI  
http://127.0.0.1:8080/create: Creates table parameters given by each of the other controllers.
http://127.0.0.1:8080/create: Drop all table parameters given by other controllers.
http://127.0.0.1:8080/seed: Seed data in tables, relevant to each model.


#### An ERD for your app
A screenshot of the ERD can be found in the root folder, alongside the readme file.

#### Detail any third party services that your app will use
Flask-Bcrypt==1.0.1: This exte  
nsion enables Flask users to utlise the bcrypt package, which enables passwords to be hashed, prior to being stored in the database via
via the bcrypt algorithm to provide adequate security.
Flask-JWT-Extended==4.5.2: JWT is used for authentication and authorisation, and this package enables Flask to use
this feature.
flask-marshmallow==0.15.0: This enables users to access Marshmallow libraries, which allows validation and conversion
of data into JSON.
Flask-SQLAlchemy==3.0.5: Combines SQLAlchemy, which enables easier database management, queries and database model 
interaction.
marshmallow-sqlalchemy==0.29.0: This integration of SQLAlchemy and Marshmallow enables the deserialisation of data,
declaring of models and generation of schemas.
psycopg2==2.9.6 and psycopg2-binary==2.9.6: Enables python code to interact with PostgreSQL databases.
python-dotenv==1.0.0: Sets key-value pairs as environment variables.
Werkzeug==2.3.6: A comprehensive WSGI web application library that includes features such as HTTP utilities, routing
system, a test client for HTTP requests and debugger.

#### Describe your projects models in terms of the relationships they have with each other
Cases model has a cascade to delete all if referenced user is deleted, and user id cannot be null.


#### Discuss the database relations to be implemented in your application
User has foreign key in Symptom tracking, and a one-and-only-one to many relationship with Symptom Tracking, where each user can have multiple symptom tracking data 
available. Where else, each symptom tracking may only have one user.

User has a Foreign key, and a one-and-only-one to zero-or-one relationship with Case. Each user may have zero or one case but each case
may only have one and only one user.

Case has a zero-or-many to one-and-only one relationship with Disease.Disease is a Foreign key in Case. Each case may only have one disease, but each
disease may have zero or multiple cases.  

#### Describe the way tasks are allocated and tracked in your project
Tasks are separated into critical files, such as init.py, main.py, controllers and models.
Detailed information is provided via this link:


