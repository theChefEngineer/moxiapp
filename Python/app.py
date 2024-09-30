from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/moxie_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

from resources import ServiceResource, ServiceListResource, AppointmentResource, AppointmentListResource

api.add_resource(ServiceResource, '/services/<int:service_id>')
api.add_resource(ServiceListResource, '/services')
api.add_resource(AppointmentResource, '/appointments/<int:appointment_id>')
api.add_resource(AppointmentListResource, '/appointments')

if __name__ == '__main__':
    app.run(debug=True)