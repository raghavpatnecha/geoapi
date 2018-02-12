from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, VARCHAR, NUMERIC, text, func, BIGINT, TEXT, JSON
import decimal
import json, datetime
from operator import is_not
from functools import partial
from math import radians, cos, sin, asin, sqrt


app = Flask(__name__)
POSTGRES = {
    'user': 'postgres',
    'pw': 'qwerty12345',
    'db': 'In',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = 'In'

    key = Column(VARCHAR, primary_key=True)
    place_name = Column(VARCHAR(100))
    admin_name1 = Column(VARCHAR(100))
    latitude = Column(NUMERIC(9, 6))
    longitude = Column(NUMERIC(9, 6))

    def __init__(self, key, place_name, admin_name1, latitude, longitude):
        self.key = key
        self.place_name = place_name
        self.admin_name1 = admin_name1
        self.latitude = latitude
        self.longitude = longitude


    def __repr__(self):
        """"""
        return "<User - '%s': '%s' - '%s'>" % (self.key, self.place_name,
                                                 self.admin_name1)



class Places(db.Model):

    __tablename__ = 'locations'

    gid = Column(BIGINT , primary_key=True)
    geom = Column(TEXT)
    properties = Column(JSON(100))


    def __init__(self, gid , geom, properties):
        self.gid = gid
        self.geom = geom
        self.properties = properties


    def __repr__(self):

        return "<Places - '%s'>" % (self.properties)


class UserSchem(ma.ModelSchema):
    class Meta:
        model = Places


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


@app.route('/')
def index():
    #users = User.query.all()
    # users = db.session.query(User).from_statement(text(
    #     '''SELECT key, place_name FROM Public."In" WHERE earth_box(ll_to_earth(28.616700,77.216700), 5000) @> ll_to_earth(latitude, longitude);''')).all()
    #
    # user_schema = UserSchema(many = True)
    # print user_schema
    # output = user_schema.dump(users).data
    # print output
    # output = json.dumps({'user': output}, default=alchemyencoder)
    # j = output.replace('"[', '[').replace(']"', ']')
    #
    # return (json.dumps(json.loads(j), indent=2))


@app.route('/post_location', methods = ['POST'])
def post_location():
    user = User(request.json['key'], request.json['place_name'], request.json['admin_name1'],
                  request.json['latitude'], request.json['longitude'])
    db.session.add(user)
    db.session.commit()
    #print user.key

    new_framework = db.session.query(User).filter_by(key =user.key, place_name = user.place_name, admin_name1 = user.admin_name1 ).all()
    user_schema = UserSchema(many= True)
    #print user_schema
    output = user_schema.dump(new_framework).data

    output = json.dumps({'user': output}, default=alchemyencoder)
    j = output.replace('"[', '[').replace(']"', ']')

    return (json.dumps(json.loads(j), indent=2))


@app.route('/get_using_self',methods = ['GET'])
def distance():
    q = db.session.query(User.key, User.place_name, User.latitude, User.longitude).all()
    lat1 =  float(request.args.get('latitude'))                     #28.616700
    lon1 =  float(request.args.get('longitude'))                      #77.216700
    lat = []
    lon = []
    for i in range(len(q)):
        x = q[i][2]
        y = q[i][3]
        lat.append(alchemyencoder(x))
        lon.append(alchemyencoder(y))
    # print lat
    # print lon
    lat = filter(partial(is_not, None), lat)
    lon = filter(partial(is_not, None), lon)
    lat_ = map(lambda i: radians(i), lat)
    lon_ = map(lambda i: radians(i), lon)
    lon1, lat1 = map(radians, [lon1, lat1])
    res = []
    for i in range(len(lat_)):
        dlon = lon1 - lon_[i]
        dlat = lat1 - lat_[i]
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat_[i]) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))
        r = 6371.00  # Radius of earth in kilometers. Use 3956 for miles
        y = c * r

        res.append(y)

    radius = 5.00  # in kilometer
    # print len(res)
    # print len(lat_), len(lon_)

    # print('Distance (km) : ', res)
    yy = []
    for i in res:

        if i <= radius:
            iy = 'Inside the area'
        else:
            iy = 'Outside the area'

        yy.append(iy)

    res = [lati for a, lati in zip(yy, lat) if a.startswith("Inside")]
    res1 = [lati for a, lati in zip(yy, lon) if a.startswith("Inside")]
    #print len(res), len(res1)

    uo = db.session.query(User).filter(User.latitude.in_(res), User.longitude.in_(res1)).all()
    #print uo
    #print len(uo)
    user_schema = UserSchema(many=True)
    # print user_schema
    output = user_schema.dump(uo).data

    output = json.dumps({'user': output}, default=alchemyencoder)
    j = output.replace('"[', '[').replace(']"', ']')

    return (json.dumps(json.loads(j), indent=2))



@app.route('/get_using_postgres' , methods = ['GET'])
def get_location():
    lat1 = float(request.args.get('latitude'))  # 28.616700
    lon1 = float(request.args.get('longitude')) #77.216700
    loc_amsterdam = func.earth_box(func.ll_to_earth(lat1, lon1 ), 5000)
    loc_company = func.ll_to_earth(User.latitude, User.longitude)
    print loc_company
    result = User.query.filter(loc_amsterdam.op("@>")(loc_company))

    print result
    # Resultset is no longer list of Company, but a list of tuples.

    user_schema = UserSchema(many=True)
    print user_schema
    output = user_schema.dump(result).data
    print output
    output = json.dumps({'user': output}, default=alchemyencoder)
    j = output.replace('"[', '[').replace(']"', ']')

    return (json.dumps(json.loads(j), indent=2))


@app.route('/get_geo' ,methods = ['GET'])
def geoj():
    lat = float(request.args.get('latitude'))  # 28.616700
    lon = float(request.args.get('longitude'))  # 77.216700
    Point = 'POINT('+ str(lon) + ' ' +str(lat) + ')'
    #print Point
    #Point = 'POINT(77.216700 28.616700)'
    query = db.session.query(Places.properties).filter(func.ST_Contains(Places.geom, Point)).all()
    print query
    user_schema = UserSchem(many=True)
    print user_schema
    output = user_schema.dump(query).data
    print output
    output = json.dumps({'result': output}, default=alchemyencoder)
    j = output.replace('"[', '[').replace(']"', ']')

    return (json.dumps(json.loads(j), indent=2))


if __name__ == '__main__':
    app.run(debug=True)
