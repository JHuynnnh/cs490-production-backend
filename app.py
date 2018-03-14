import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from flask_heroku import Heroku

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cs490_test'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

# Create our database models
class PartsInventory(db.Model):
    __tablename__ = "parts_inventory"

    id = db.Column(db.Integer, primary_key=True)
    sku_number = db.Column(db.String(120), unique=False)
    sku_name = db.Column(db.String(120), unique=False)
    dimensions = db.Column(db.String(120), unique=False)
    price = db.Column(db.Integer, unique=False)
    quantity_on_order = db.Column(db.Integer, unique=False)
    quantity_on_hand = db.Column(db.Integer, unique=False)

    def __init__(self, sku_number, sku_name, dimensions, price, quantity_on_order, quantity_on_hand):
        self.sku_number = sku_number
        self.sku_name = sku_name
        self.dimensions = dimensions
        self.price = price
        self.quantity_on_order = quantity_on_order
        self.quantity_on_hand = quantity_on_hand

class FinishedGoodsInventory(db.Model):
    __tablename__ = "finished_goods_inventory"

    id = db.Column(db.Integer, primary_key=True)
    sku_number = db.Column(db.String(120), unique=False)
    sku_name = db.Column(db.String(120), unique=False)
    quantity_in_production = db.Column(db.Integer, unique=False)
    quantity_on_hand = db.Column(db.Integer, unique=False)

    def __init__(self, sku_number, sku_name, quantity_in_production, quantity_on_hand):
        self.sku_number = sku_number
        self.sku_name = sku_name
        self.quantity_in_production = quantity_in_production
        self.quantity_on_hand = quantity_on_hand

class FloorControl(db.Model):
    __tablename__ = "floor_control"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(120), unique=False)
    serial_number = db.Column(db.String(120), unique=False)
    stage = db.Column(db.Integer, unique=False)
    status = db.Column(db.Integer, unique=False)

    def __init__(self, order_id, serial_number, stage, status):
        self.order_id = order_id
        self.serial_number = serial_number
        self.stage = stage
        self.status = status

class QualityAssurance(db.Model):
    __tablename__ = "quality_assurance"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(120), unique=False)
    serial_number = db.Column(db.String(120), unique=False)
    stage0 = db.Column(db.Integer, unique=False)
    stage1 = db.Column(db.Integer, unique=False)
    stage2 = db.Column(db.Integer, unique=False)
    stage3 = db.Column(db.Integer, unique=False)
    stage4 = db.Column(db.Integer, unique=False)

    def __init__(self, order_id, serial_number, stage0, stage1, stage2, stage3, stage4):
        self.order_id = order_id
        self.serial_number = serial_number
        self.stage0 = stage0
        self.stage1 = stage1
        self.stage2 = stage2
        self.stage3 = stage3
        self.stage4 = stage4

class Schedule(db.Model):
    __tablename__ = "schedule"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(120), unique=False)
    sku_number = db.Column(db.String(120), unique=False)
    quantity = db.Column(db.Integer, unique=False)
    expected_start = db.Column(db.String(120), unique=False)
    expected_completion = db.Column(db.String(120), unique=False)
    status = db.Column(db.String(120), unique=False)

    def __init__(self, order_id, sku_number, quantity, expected_start, expected_completion, status):
        self.order_id = order_id
        self.sku_number = sku_number
        self.quantity = quantity
        self.expected_start = expected_start
        self.expected_completion = expected_completion
        self.status = status

# TODO WHEN PRODUCTION SCHEDULE IS READY
#class Metrics(db.Model):
#    __tablename__ = "Metrics"

class Orders(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(120), unique=False)
    sku = db.Column(db.String(120), unique=False)
    price = db.Column(db.Integer, unique=False)
    quantity = db.Column(db.Integer, unique=False)

    def __init__(self, order_id, sku, price, quantity):
        self.order_id = order_id
        self.sku = sku
        self.price = price
        self.quantity = quantity

class EmployeeSchedule(db.Model):
    __tablename__ = "employee_schedule"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(120), unique=True)
    availability = db.Column(db.String(120), unique=False)

    def __init__(self, employee_id, availability):
        self.employee_id = employee_id
        self.availability = availability

class BillOfMaterials(db.Model):
    __tablename__ = "bill_of_materials"

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(120), unique=False)
    list_of_parts = db.Column(db.String(120), unique=False)

    def __init__(self, sku, list_of_parts):
        self.sku = sku
        self.list_of_parts = list_of_parts

#########################################################################################
# FOR FRONTEND

@app.route('/populate', methods=['POST'])
def populate():
    try:
        data = request.get_json()
        table = data['table']
        if table == 'parts_inventory':
            ret = PartsInventory(data['skuNumber'], data['skuName'], 
                    data['dimensions'], data['price'],
                    data['quantityOnOrder'], data['quantityOnHand'])
        elif table == 'finished_goods_inventory':
            ret = FinishedGoodsInventory(data['skuNumber'], data['skuName'],
                    data['quantityInProduction'], data['quantityOnHand'])
        elif table == 'floor_control':
            ret = FloorControl(data['orderId'], data['serialNumber'], data['stage'], data['status'])
        elif table == 'quality_assurance':
            ret = QualityAssurance(data['orderId'], data['serialNumber'], data['stage0'],
                    data['stage1'], data['stage2'], data['stage3'], data['stage4'])
        elif table == 'schedule':
            ret = Schedule(data['orderId'], data['skuNumber'], data['quantity'],
                    data['expectedStart'], data['expectedCompletion'], data['status'])
        else:
            return json.dumps({"Result": "Cannot add to table: " + table})
        db.session.add(ret)
        db.session.commit()
        db.session.close()
        return json.dumps({"Result": "Added to table: " + table})
    except:
        return json.dumps({"Result": "Failed to add data to table: " + table})

@app.route('/delete', methods=['DELETE'])
def delete():
    try:
        data = request.get_json()
        table = data['table']
        if table == 'parts_inventory':
            obj = PartsInventory.query.filter_by(sku_number=data['skuNumber']).delete()
        elif table == 'finished_goods_inventory':
            obj = FinishedGoodsInventory.query.filter_by(sku_number=data['skuNumber']).delete()
        elif table == 'floor_control':
            obj = FloorControl.query.filter_by(serial_number=data['serialNumber']).delete()
        elif table == 'quality_assurance':
            obj = QualityAssurance.query.filter_by(serial_number=data['serialNumber']).delete()
        elif table == 'schedule':
            obj = Schedule.query.filter_by(order_id=data['orderId']).delete()
        else:
            return json.dumps({"Result": "Cannot delete from table: " + table})
        db.session.commit()
        db.session.close()
        return json.dumps({"Result": "Deleted row from table: " + table})
    except:
        return json.dumps({"Result": "Failed to delete data from table: " + table})

@app.route('/delete_all', methods=['DELETE'])
def delete_all():
    try:
        data = request.get_json()
        table = data['table']
        if table == 'parts_inventory':
            db.session.query(PartsInventory).delete()
        elif table == 'finished_goods_inventory':
            db.session.query(FinishedGoodsInventory).delete()
        elif table == 'floor_control':
            db.session.query(FloorControl).delete()
        elif table == 'quality_assurance':
            db.session.query(QualityAssurance).delete()
        elif table == 'schedule':
            db.session.query(Schedule).delete()
        else:
            return json.dumps({"Result": "Cannot delete rows from table: " + table})
        db.session.commit()
        db.session.close()
        return json.dumps({"Result": "Deleted all rows from table: " + table})
    except:
        return json.dumps({"Result": "Failed to delete all data from table: " + table})

@app.route('/parts_inventory_all', methods=['GET'])
def get_all_parts_inventory():
    q = db.session.query(PartsInventory)
    ret = {}
    for item in q.all():
        ret[item.sku_number] = {'skuName': item.sku_name,
                                'dimensions': item.dimensions, 
                                'price': item.price,
                                'quantityOnOrder': item.quantity_on_order, 
                                'quantityOnHand': item.quantity_on_hand}
    return json.dumps(ret)

@app.route('/finished_goods_inventory_all', methods=['GET'])
def get_all_finished_goods_inventory():
    q = db.session.query(FinishedGoodsInventory)
    ret = {}
    for item in q.all():
        ret[item.sku_number] = {'skuName': item.sku_name,
                                'quantityInProduction': item.quantity_in_production,
                                'quantityOnHand': item.quantity_on_hand}
    return json.dumps(ret)

@app.route('/floor_control_all', methods=['GET'])
def get_all_floor_control():
    q = db.session.query(FloorControl)
    ret = {}
    for item in q.all():
        ret[item.serial_number] = {'stage': item.stage, 'status': item.status}
    return json.dumps(ret)

@app.route('/quality_assurance_all', methods=['GET'])
def get_all_quality_assurance():
    q = db.session.query(FloorControl)
    ret = {}
    for item in q.all():
        ret[item.serial_number] = {'stage0': item.stage0, 'stage1': item.stage1, 'stage2': item.stage2, 
                                    'stage3': item.stage3, 'stage4': item.stage4}
    return json.dumps(ret)

@app.route('/schedule_all', methods=['GET'])
def get_all_schedule():
    q = db.session.query(FloorControl)
    ret = {}
    for item in q.all():
        ret[item.order_id] = {'skuNumber': item.sku_number,
                            'quantity': item.quantity,
                            'expectedStart': item.expected_start,
                            'expectedCompletion': item.expected_completion,
                            'status': item.status}
    return json.dumps(ret)

# FOR FRONTEND
#########################################################################################

if __name__ == '__main__':
    app.debug = True
    app.run()
