from flask_restful import Resource, reqparse
from models import db, Service, Appointment
from datetime import datetime

class ServiceResource(Resource):
    def get(self, service_id):
        service = Service.query.get_or_404(service_id)
        return {
            'id': service.id,
            'medspa_id': service.medspa_id,
            'name': service.name,
            'description': service.description,
            'price': float(service.price),
            'duration': service.duration,
            'category': service.category,
            'type': service.type,
            'product': service.product,
            'supplier': service.supplier
        }

    def put(self, service_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('price', type=float)
        parser.add_argument('duration', type=int)
        args = parser.parse_args()

        service = Service.query.get_or_404(service_id)
        for key, value in args.items():
            if value is not None:
                setattr(service, key, value)
        db.session.commit()
        return {'message': 'Service updated successfully'}

class ServiceListResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('medspa_id', type=int, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str)
        parser.add_argument('price', type=float, required=True)
        parser.add_argument('duration', type=int, required=True)
        parser.add_argument('category', type=str, required=True)
        parser.add_argument('type', type=str, required=True)
        parser.add_argument('product', type=str, required=True)
        parser.add_argument('supplier', type=str)
        args = parser.parse_args()

        new_service = Service(**args)
        db.session.add(new_service)
        db.session.commit()
        return {'message': 'Service created successfully', 'id': new_service.id}, 201

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('medspa_id', type=int, required=True)
        args = parser.parse_args()

        services = Service.query.filter_by(medspa_id=args['medspa_id']).all()
        return [{
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'price': float(service.price),
            'duration': service.duration,
            'category': service.category,
            'type': service.type,
            'product': service.product,
            'supplier': service.supplier
        } for service in services]

class AppointmentResource(Resource):
    def get(self, appointment_id):
        appointment = Appointment.query.get_or_404(appointment_id)
        return {
            'id': appointment.id,
            'medspa_id': appointment.medspa_id,
            'start_time': appointment.start_time.isoformat(),
            'total_duration': appointment.total_duration,
            'total_price': float(appointment.total_price),
            'status': appointment.status,
            'services': [{'id': service.id, 'name': service.name} for service in appointment.services]
        }

    def put(self, appointment_id):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True)
        args = parser.parse_args()

        appointment = Appointment.query.get_or_404(appointment_id)
        if args['status'] not in ['scheduled', 'completed', 'canceled']:
            return {'message': 'Invalid status'}, 400
        appointment.status = args['status']
        db.session.commit()
        return {'message': 'Appointment status updated successfully'}

class AppointmentListResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('medspa_id', type=int, required=True)
        parser.add_argument('start_time', type=str, required=True)
        parser.add_argument('service_ids', type=int, action='append', required=True)
        args = parser.parse_args()

        services = Service.query.filter(Service.id.in_(args['service_ids'])).all()
        if len(services) != len(args['service_ids']):
            return {'message': 'One or more invalid service IDs'}, 400

        total_duration = sum(service.duration for service in services)
        total_price = sum(service.price for service in services)

        new_appointment = Appointment(
            medspa_id=args['medspa_id'],
            start_time=datetime.fromisoformat(args['start_time']),
            total_duration=total_duration,
            total_price=total_price,
            status='scheduled',
            services=services
        )
        db.session.add(new_appointment)
        db.session.commit()
        return {'message': 'Appointment created successfully', 'id': new_appointment.id}, 201

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str)
        parser.add_argument('date', type=str)
        args = parser.parse_args()

        query = Appointment.query
        if args['status']:
            query = query.filter_by(status=args['status'])
        if args['date']:
            date = datetime.strptime(args['date'], '%Y-%m-%d').date()
            query = query.filter(db.func.date(Appointment.start_time) == date)

        appointments = query.all()
        return [{
            'id': appointment.id,
            'medspa_id': appointment.medspa_id,
            'start_time': appointment.start_time.isoformat(),
            'total_duration': appointment.total_duration,
            'total_price': float(appointment.total_price),
            'status': appointment.status
        } for appointment in appointments]