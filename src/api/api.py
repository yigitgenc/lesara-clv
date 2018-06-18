from flask import Flask
from flask_restful import Api, Resource
from redis import Redis, ConnectionPool

redis_pool = ConnectionPool(host='redis', decode_responses=True)
r = Redis(connection_pool=redis_pool)


class CustomerResource(Resource):
    """
    Customer Resource
    """
    def get(self, id):
        predicted_clv = r.get(id)

        if not predicted_clv:
            return {'error': 'Customer not found.'}, 404

        return {'customer_id': id, 'predicted_clv': predicted_clv}


app = Flask(__name__)
api = Api(app)

api.add_resource(CustomerResource, '/api/customers/<string:id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
