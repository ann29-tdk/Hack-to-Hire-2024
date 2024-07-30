# Flight Tracker Application

## Flow of Application

### User View
**Register**

![User Register](https://i.imgur.com/O8cagWN.png)


**Login**

![User Login](https://i.imgur.com/vGbRgCe.png)

**User Dashboard**

In User Dashboard, the left half of the page is where users can search their respective flights, and right half of the page is where they will receive the live updates/notifications about their flights.

![User Dashboard](https://i.imgur.com/W4BPwQo.png)

### Admin View
**Admin Login**

- Admins have been assigned special credentials to access the Admin Panel. These credentials are to be used exclusively by admins.
- After logging in, the admin will see the panel where they can enter the flight number they wish to update. A modal will pop up with the respective details that need to be updated.

![Admin Login](https://i.imgur.com/CqGDe9t.png)

### Role of Sockets.io
**Let us see how push in app push notifications works**

- The screen has been divided into three sections: the left section belongs to the admin, while the right section is divided between two users, Anurag and Siddharth, both traveling on Flight **FL123** having **latest arrival time 15:00**.
 
![User](https://i.imgur.com/uneROXq.png)

- The admin decided to update the **latest arrival time** from **15:00** to **18:00**. Both passengers of the same flight received a notification in the top right corner as well as on their notification board, indicating the time and date they received this notification.
 
![Notifications](https://i.imgur.com/5Xc3vMf.png)





## Introduction

The Flight Tracker Application is designed to help users track their flights and stay updated with real-time information. It features user authentication, flight status tracking, and notifications for flight updates.

## Features

- User registration and login
- Real-time flight status updates
- Push notifications for flight changes
- Integration with MongoDB for data storage
- Responsive design using React and React Bootstrap

## Technologies

- Frontend: React, React Bootstrap
- Backend: Flask, Flask-SocketIO, MongoEngine
- Database: MongoDB
- Real-time updates: Socket.IO

## Getting Started

### Prerequisites

- Node.js
- npm or yarn
- Python
- Flask
- MongoDB

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/flight-tracker.git
   cd flight-tracker
   
2. **Install frontend dependencies:**
    ```bash
    cd frontend
    npm install
3. **Install backend dependencies:**
   
    ```bash
   cd backend
   pip install -r requirements.txt
   
### Running the Application
1. **Start the backend server:**
    ```bash
    cd backend
    python app.py
2. ***Start the frontend server:***
    ```bash
    cd frontend
    npm start
    
## Frontend Components
**HomePage**

The main landing page of the application that provides an overview and options to log in or register.

**Login**

A component that handles user authentication.

**Register**

A component that allows new users to create an account.

**CustomNavbar**

A navigation bar component that provides links to different sections of the application.

**UserDashboard**

A component where users can view and manage their flight information.

# Backend

**Models**

Define the data structure and schema for the application using MongoEngine.

**Routes**

Define the API endpoints for user registration, login, and flight tracking.

**SocketIO**

Handles real-time communication between the client and server for live flight updates.

**Configuration**

Contains configuration settings for the Flask application, including database connections and secret keys.

