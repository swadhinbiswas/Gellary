# Gellary

This project aims to create an image gallery website that fetches images from copyright-free sources, stores them in a database, and displays them on the website. We'll prioritize ethical considerations and legal compliance throughout the process.

[![wakatime](https://wakatime.com/badge/github/swadhinbiswas/Gellary.svg)](https://wakatime.com/badge/github/swadhinbiswas/Gellary)

## `project code name: project Art`

# project details:

1. **Programming Language & Framework:** We'll use **Python** as it is beginner-friendly and widely used. Popular frameworks Fast API and React simplify web development. Choose the one you find more comfortable.
2. **Libraries:**

   - **requests**: Downloads images from the internet.
   - **Database library**: Choose one based on your chosen database (e.g., `psycopg2` for PostgreSQL, `MySQLdb` for MySQL).
   - **PIL (Python Imaging Library)**: Manipulates and displays images in Python.

   **Building the Backend (Server-side)**

   1. **Database Setup:**
      - Create a database table to store image data. Include columns for:
        - **Image ID (unique identifier for each image)**
        - **Image Data (byte string representing the image)**
        - **Image Source URL (link to the original image source)**
        - **Description (optional, a brief description of the image)**
        - **License (optional, the specific license under which the image is available)**
   2. **Develop functionalities:**
      - **Image fetching:** Write code using `requests` to download images from chosen URLs with proper error handling.
      - **Image conversion:** Convert downloaded images to a byte string format using libraries like `PIL` before storing them in the database.
      - **Data storage:** Use your chosen database library to establish a connection and store the image data and related information in the table you created.

**Building the Front end (Website)**

- We will use React to build our front end.
- front-end Design sample given blew

**Why Vite & React?**

- **Vite:** This build tool offers lightning-fast development server starts and super-efficient Hot Module Replacement (HMR), making your work feel incredibly smooth and responsive.
- **React:** This component-based JavaScript library empowers you to build modular, reusable, and interactive user interfaces, which fits perfectly with the dynamic nature of an image gallery.

# Sample for Start Project With Vite

`git clone  [https://github.com/swadhinbiswas/Gellary](https://github.com/swadhinbiswas/Gellary)`

[https://github.com/swadhinbiswas/Gellary](https://github.com/swadhinbiswas/Gellary)

`cd Gellary/frontend`

`npm create vite@latest {project name} --template react
  cd {project name}`

`npm install axios`

`npm install`

`npm run dev`

# **Resource**

## for visual chats

1.Chart.js

[Chart.js](https://www.chartjs.org/)

## database

PostgreSQL

[Set up hosted PostgreSQL® database for FREE](https://aiven.io/free-postgresql-database)

API Fetching

[GraphQL | A query language for your API](https://graphql.org/)

UI for React

[MUI: The React component library you always wanted](https://mui.com/)

Caching

[Redis](https://redis.io/)

## Auth Provider

[Auth0: Secure access for everyone. But not just anyone.](https://auth0.com/)

# Design
