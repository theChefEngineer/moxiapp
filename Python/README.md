# Moxie Medspa Management System

This is a simple RESTful CRUD application for managing medspa services and appointments.

## Setup Instructions

1. Clone this repository:
   ```
   git clone https://github.com/your-username/moxie-project.git
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

- The `supplier`