# Cafe Finder App

This Flask application is designed to help users discover cafes in their vicinity or a specified location. Leveraging the Google Places API, it allows for searching cafes based on various criteria such as location, type, and keyword. Additionally, users can save their favorite cafes to a SQLite database for future reference. The app incorporates Flask for backend logic, Flask-WTF for form handling, and Flask-Bootstrap for styling.

## Features

- **Search Functionality**: Users can search for cafes by location, type (e.g., cafe, restaurant, bar), keyword (e.g., Starbucks), and radius in meters.
- **Save Favorite Cafes**: Users can save their favorite cafes into a SQLite database, which allows for easy retrieval and management of their saved locations.
- **Dynamic Results**: Search results are dynamically displayed on the website, including cafe names, ratings, and locations.
- **Responsive Design**: Utilizes Flask-Bootstrap to ensure the app is responsive and provides a good user experience across various devices and screen sizes.

## Technologies Used

- **Flask**: A micro web framework written in Python for building web applications.
- **Flask-WTF**: An extension for Flask that integrates WTForms for form handling, including CSRF protection.
- **Flask-Bootstrap**: An extension for Flask that integrates Bootstrap for frontend layouts and components.
- **Flask-SQLAlchemy**: An extension for Flask that adds support for SQLAlchemy, a SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **SQLite**: A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
- **Google Places API**: Used for fetching information about places (like cafes) based on user-defined specifications.

## Setup and Installation

1. **Clone the Repository:**
2. ```bash
   git clone https://github.com/Kimchimantium/cafe_nearby_me
   cd your-project-folder
