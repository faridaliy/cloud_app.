Farid Aliyev 48213
Abai Dyldaev
 


ser Management System with Docker Compose

Project Overview

This project is a simple User Management System where users can register, log in, and manage user profiles. After logging in, users can edit or delete their profiles. We wanted to make the setup as easy as possible, so everything runs with just one command using Docker Compose.

Key Features

User Registration: Users can sign up with basic details like name, email, and password.

User Login: A secure login feature that checks user credentials.

User Management: Logged-in users can update their profiles or delete accounts.

Set Location: Users can choose or update their location, making their profile more personalized.

Tools We Used

Python: For writing the backend logic and handling requests.

SQL Shell: To manage and interact with the database.

Visual Studio Code 2019: As our main code editor, making it easy to develop and debug.

How It Works

The project has a simple frontend that connects to a backend API, which handles all the user management tasks. The data is stored in a database, and everything is linked together with Docker.

Steps to Run the Project


Run It:
Just run this command to build and start everything:

docker-compose up --build

Access the App:
Open your browser and go to http://localhost:8000 (or the port mentioned in the Docker Compose file).

What's Inside

Frontend: A basic interface for user registration, login, and profile management.

Backend: Handles all the data processing, authentication, and API endpoints.

Database: Stores user info securely.

Docker Compose: Brings it all together and makes it easy to run.

What We Could Improve

Adding multi-factor authentication for better security.

Creating admin roles for more control over the system.

Adding analytics to track usage and improve features.

Why This Project?

We wanted to build something that’s useful and easy to set up. By using Docker Compose, our professor can run everything with one command. It’s simple, straightforward, and helps us learn how different parts of an application work together.

