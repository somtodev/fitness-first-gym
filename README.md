# Fitness First Gym

---
[Live Website](http://fitness-first-gym.onrender.com/): We deployed our project lived for easy access.

---

Below are login details for the admin

**Email Address**: admin@mail.com
**Password**: admin_aptech_2023

---


## Contents
1. [Introduction](#introduction)
2. [Project File Structure](#project-file-structure)
3. [Program Routes](#program-routes)
4. [Program Middlwares](#program-middlewares)
5. [Web App Usuage](#how-to-use-web-app)
5. [How To Install & Run](#how-to-install--run)

## Introduction

The Fitness First GYM project aims to develop a comprehensive website for a local gym facility to improve membership management, online booking, and member communication. The project targets three main user groups: Guest Users, Registered Users, and Admin Users. Guest Users can browse information and make inquiries, while Registered Users can register, book packages, and manage their profiles. Admin Users have full control over system management.

FOR MODEL STRUCTURE: [Click Here](./BreakDown.md)
FOR MORE INFO: [Click Here](./Documentation.pdf)

The proposed solution involves building a dynamic website with the following core features:

1. **User Management:**
   - Registration and login for Registered Users.
   - Admin dashboard for system control.

2. **Membership Packages:**
   - Various gym membership packages, including categories and package types.

3. **Booking System:**
   - Booking fitness classes and trainers.
   - Viewing booking history and payment details.

4. **Communication:**
   - Member notifications and updates.
   - Inquiry and contact forms for Guest Users.

5. **Admin Control:**
   - Dashboard with overview statistics.
   - Package, category, and package type management.
   - Booking and payment tracking.
   - Report generation.

6. **Security:**
   - User authentication and authorization.
   - Encryption of sensitive data.
   
7. **Responsive Design:**
   - Ensuring the website functions well on various devices.

## Project File Structure

* **instance**: contains database file (database.sqlite)

* **app**: contains all web app templates, routes and third party libs like bootstrap and js
   * **models**: contains all models used in development of this application
   * **static**: contains images, css and js files used in the development of the project.
   * **templates**: contains all the web pages for the web app.
      * **admin**: contains all the web pages an admin can acces
      * **user**: contains the web app pages accessible by both the admin and user.
      * **components**: contains some components which were been used in the project. I.E (base.html and other core components).

## Program Routes
> **NOTE**: Some routes are protected by middlewares, click [here for info](#program-middlewares)
- Users 
    - All Users
        - /: Homepage
        - /contact-us: Contact Us Page
        - /auth/login: Login Page
        - /auth/register: Register User Page
        - /auth/logout: Logout the User
    - Registered Users
        - /profile: Profile Page (Edit)
        - /user/classes: User Classes Page
        - /user/bookings: User Booked Classes Page
- Admin
> **NOTE**: All admin route is protected by an **@authorize_request** middleware that protects them from normal users.
   - /admin/dashboard: The Admin Dashboard
   - /admin/categories: Manage categories page
   - /admin/booking/memberships: Shows all membership bookings
   - /admin/booking/classes: Shows all the class bookings
   - /admin/package/all: Shows all the current packages available for members
   - /admin/trainer/all: Shows all the gym trainers
   - /admin/class/all: Show all created classes



## Program Middlewares
Below are three middleware created to security integrity in fitness first gym.

* **@login_required**: protects a route by making sure any user who tries to access this route is logged in.

* **@membership_validator**: protects a route by making sure before the user access a route, he or she must be a member of a package.

* **@authorize_request**: protects a route by making sure any user who tries to access this route is an ***administrator***.

## How to use web app

> AS A USER

You can login in as user by creating a new account then logining into that new account.

> AS AN ADMIN

Below are login details for the admin

**Email Address**: admin@mail.com
**Password**: admin_aptech_2023


## How To Install & Run

**Requirements:**
Below are the requirements to proceed
* Python 
* Pip

> NOTE: A requirements.txt file is provided, it contains all the dependecies to run the project.

To Install Dependencies, Run:
```
pip3 install -r requirements.txt
```
or
```
python -m pip3 install -r requirements.txt
```
Once All Packages are downloaded
THEN RUN,
```
gunicorn app:app
```