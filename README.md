# Comprehensive Data Analysis of a Music Streaming Platform

## Description
This project provides analytical tools for analyzing streaming data stored in a MySQL database.<br><br>
It includes such as behavior analysis, track and artists popularity, trends and clustering patterns using python.

## Installation

### Prerequisites
- MySQL 8.0+
- MySQL Workbench (For GUI managment)
- Python 3.10+
- Required Python packages


### Setup the database

1. Open MySQL Workbench
2. Create a new schema 'your_database_name'
3. Open and run schema.sql
4. For each table:
    - Right click on table
    - Select "Table data import wizard"
    - Import the corresponding CSV file from "/Seed_data/"

## Usage

1. Create and configure a `passwords.env` file with your database credentials:
```bash
DB_HOST=localhost
DB_PORT=PORT
DB_PASSWORD=PASSWORD
DB_USER=USER
DB_NAME=your_database_name
```

2. Run the main.py
```
python main.py
```

## License
This project is licensed under the MIT License. See LICENSE file for details