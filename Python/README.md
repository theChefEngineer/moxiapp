# Moxie Medspa Management System

This is a simple RESTful CRUD application for managing medspa services and appointments.

## Setup Instructions

1. Clone this repository:
   ```
   git clone https://github.com/your-username/moxie-project.git](https://github.com/theChefEngineer/moxiapp)
   cd moxie-project
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your PostgreSQL database and update the `SQLALCHEMY_DATABASE_URI` in `app.py` with your database credentials.

5. Initialize the database:
   ```
   python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

6. Run the application:
   ```
   python app.py
   ```

The API will now be available at `http://localhost:5000`.

## API Endpoints

### Services

- Create a service: `POST /services`
  ```json
  {
    "medspa_id": 1,
    "name": "Botox",
    "description": "Botox injection",
    "price": 300.00,
    "duration": 30,
    "category": "Injectables",
    "type": "Neuromodulator",
    "product": "Botox",
    "supplier": "Allergan"
  }
  ```

- Update a service: `PUT /services/{service_id}`
  ```json
  {
    "name": "Updated Botox",
    "price": 350.00
  }
  ```

- Get a service: `GET /services/{service_id}`

- List services for a medspa: `GET /services?medspa_id={medspa_id}`

### Appointments

- Create an appointment: `POST /appointments`
  ```json
  {
    "medspa_id": 1,
    "start_time": "2024-02-01T10:00:00",
    "service_ids": [1, 2, 3]
  }
  ```

- Update appointment status: `PUT /appointments/{appointment_id}`
  ```json
  {
    "status": "completed"
  }
  ```

- Get an appointment: `GET /appointments/{appointment_id}`

- List appointments: `GET /appointments`
  - Filter by status: `GET /appointments?status=scheduled`
  - Filter by date: `GET /appointments?date=2024-02-01`

## Notes on Implementation

- This implementation assumes that the Medspa records are pre-existing in the database.
- The total duration and price for appointments are calculated based on the associated services.
- The application uses SQLAlchemy as an ORM, which allows for easy switching between different SQL databases if needed in the future.
- Error handling and input validation are implemented, but could be further improved for production use.
- Due to the two-hour time constraint, this implementation focuses on core functionality and may lack some advanced features or extensive error handling.

## Assumptions and Design Decisions

- The `supplier` field for services is optional, as specified in the assignment.
- The `total_duration` and `total_price` fields for appointments are calculated and stored, rather than being computed on-the-fly. This decision was made to improve read performance at the cost of some additional storage.
- The application doesn't include authentication or authorization mechanisms due to time constraints. In a production environment, these would be crucial additions.
- The API doesn't include endpoints for managing medspas. It's assumed that medspas are created through another process or directly in the database.
- The status of an appointment can only be 'scheduled', 'completed', or 'canceled'. Any attempt to set a different status will result in an error.
- When creating an appointment, all specified services must exist and be associated with the same medspa as the appointment.
- The application uses UTC timestamps. In a production environment, time zone handling would need to be considered more carefully.
- Error messages are kept simple for this prototype. In a production environment, more detailed error responses would be beneficial.
- The database schema includes indexes on frequently queried fields to improve performance. In a production environment, these indexes should be reviewed and optimized based on actual query patterns.

## Conclusion

This implementation provides a basic foundation for a medspa management system, fulfilling the core requirements of the assignment within the given two-hour time constraint. It demonstrates the ability to design a sensible database schema and implement RESTful CRUD functionality. The chosen technologies (Flask, SQLAlchemy, PostgreSQL) provide a solid, scalable foundation that can be built upon for a more comprehensive system.
