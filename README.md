# jbl-chat

Let's set the stage, you are the founder of this exciting new messaging startup, you are tasked with building the first version of a product that is aimed to evolve with feedback from the team and users.

You're building the backend using Django, and your initial task is to expose a starting API while also leveraging HTMX for interactive front-end experiences. With this first release, we want to deliver the following user stories:

1. As a user, I want to see all other users on the platform.
2. As a user, I want to view my conversation with another user.
3. As a user, I want to be able to send messages to another user on the platform.

Given that this is your startup, you have the freedom to set up and utilize the practices that align with your goals. You can use any Python libraries or external tools that you prefer.

We have provided a Django skeleton project along with Docker setup for your convenience. Feel free to utilize Docker for development or Python virtual environments for your local setup. Since managing user registration isn’t required for this assessment, you can create dummy users directly using the shell and implement session authentication for the API.

Incorporating HTMX will allow you to create dynamic, interactive elements on the front end without needing to reload the page. We encourage you to think about how HTMX can enhance user interactions effectively.

Please submit your solution as a pull request to our public repository. Happy coding!


---

# LOCAL DEVELOPMENT SETUP

This guide explains how to set up and run the application locally using Docker and Docker Compose.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Building and Running the Application

1. **Build and start the containers:**

   ```bash
   docker compose build && docker compose up
   ```

2. **Connect to the running Docker container:**

   ```bash
   docker compose exec web bash
   ```

3. **Navigate to the application directory:**

   ```bash
   cd jbl_chat/
   ```

### Database Setup

1. **Run database migrations:**

   ```bash
   ./manage.py migrate
   ```

2. **Import fake users and set all their passwords to 'admin':**

   ```bash
   ./manage.py loaddata fixtures/local_development_users.json
   ./manage.py set_default_passwords
   ```

3. **Access the Django admin panel by opening:**

   http://0.0.0.0:8000/admin/


4. **Login with:**
   - **Username:** admin
   - **Password:** admin


### Local API docs and testing

In order to create new api documentation and to run it locally follow the instructions here: https://drf-spectacular.readthedocs.io/en/latest/readme.html#take-it-for-a-spin



# LIVE TEST APPLICATION

## Admin interface access

A default admin user has been created for assessment purposes.
- **Username:** admin
- **Password:** admin

Log in via the Django admin at:
   https://jbl-chat.onrender.com//admin/
   or 
   https://jbl-chat.onrender.com/

## API Documentation

Explore and test the API using:
- **Redoc:**   https://jbl-chat.onrender.com/api/docs/redoc/
- **Swagger:** https://jbl-chat.onrender.com/api/docs/swagger/

## Testing the system as different Users

For testing, you may first log in as admin, and then switch to another user.

Once logged in as a different user you can select a user to chat to.

In this way you can open two browsers and login as a different user in each and chat between users.


---