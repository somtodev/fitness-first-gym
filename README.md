# Fitness First Gym

## Contents
1. [Introduction](#introduction)
2. [Proposed Solution](#proposed-solution)
3. [Project File Structure](#project-file-structure)
4. [Program Routes](#program-routes)
5. [Web App Usuage](#how-to-use-web-app)

## Introduction

The Fitness First GYM project aims to develop a comprehensive website for a local gym facility to improve membership management, online booking, and member communication. The project targets three main user groups: Guest Users, Registered Users, and Admin Users. Guest Users can browse information and make inquiries, while Registered Users can register, book packages, and manage their profiles. Admin Users have full control over system management.

FOR MODEL STRUCTURE: [Click Here](./BreakDown.md)
FOR MORE INFO: [Click Here](./Documentation.pdf)

## Proposed Solution

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

## Program Routes

- Users 
    - All Users
        - /: Homepage
        - /contact-us: Contact Us Page
        - /auth/login: Login Page
        - /auth/register: Register User Page
    - Registered Users
        - /profile: Profile Page (Edit)
        - /classes: User Classes Page
        - /bookings: User Booked Classes Page

- Admin


## How to use web app

> AS A USER

You can login in as user by creating a new account then logining into that new account.

> AS AN ADMIN

Below are login details for the admin

**Email Address**: admin@mail.com

**Password**: admin
