import json
import uuid
import random
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from flask_heroku import Heroku
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cs490_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    sales_order = db.Column(db.String(120), unique=False)
    order_id = db.Column(db.String(120), unique=False)
    sku_number = db.Column(db.String(120), unique=False)
    quantity = db.Column(db.Integer, unique=False)
    quantity_completed = db.Column(db.Integer, unique=False)
    expected_start = db.Column(db.String(120), unique=False)
    expected_completion = db.Column(db.String(120), unique=False)
    status = db.Column(db.String(120), unique=False)

    def __init__(self, sales_order, order_id, sku_number, quantity, quantity_completed, expected_start, expected_completion, status):
        self.sales_order = sales_order
        self.order_id = order_id
        self.sku_number = sku_number
        self.quantity = quantity
        self.quantity_completed = quantity_completed
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
@cross_origin()
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
            ret = Schedule(data['salesOrder'], data['orderId'], data['skuNumber'], data['quantity'], 
                data['quantityCompleted'], data['expectedStart'], data['expectedCompletion'], data['status'])
        else:
            return json.dumps({"result": "Cannot add to table: " + table})
        db.session.add(ret)
        db.session.commit()
        db.session.close()
        return json.dumps({"result": "Added to table: " + table})
    except:
        raise
        return json.dumps({"result": "Failed to add data to table: " + table})

@app.route('/delete', methods=['DELETE'])
@cross_origin()
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
            return json.dumps({"result": "Cannot delete from table: " + table})
        db.session.commit()
        db.session.close()
        return json.dumps({"result": "Deleted row from table: " + table})
    except:
        return json.dumps({"result": "Failed to delete data from table: " + table})

@app.route('/delete_all', methods=['DELETE'])
@cross_origin()
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
            return json.dumps({"result": "Cannot delete rows from table: " + table})
        db.session.commit()
        db.session.close()
        return json.dumps({"result": "Deleted all rows from table: " + table})
    except:
        return json.dumps({"result": "Failed to delete all data from table: " + table})

@app.route('/parts_inventory_all', methods=['GET'])
@cross_origin()
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
@cross_origin()
def get_all_finished_goods_inventory():
    q = db.session.query(FinishedGoodsInventory)
    ret = {}
    for item in q.all():
        ret[item.sku_number] = {'skuName': item.sku_name,
                                'quantityInProduction': item.quantity_in_production,
                                'quantityOnHand': item.quantity_on_hand}
    return json.dumps(ret)

@app.route('/floor_control_all', methods=['GET'])
@cross_origin()
def get_all_floor_control():
    q = db.session.query(FloorControl)
    ret = {}
    for item in q.all():
        ret[item.serial_number] = {'orderId': item.order_id, 'stage': item.stage, 'status': item.status}
    return json.dumps(ret)

@app.route('/quality_assurance_all', methods=['GET'])
@cross_origin()
def get_all_quality_assurance():
    q = db.session.query(QualityAssurance)
    ret = {}
    for item in q.all():
        ret[item.serial_number] = {'orderId': item.order_id, 'stage0': item.stage0, 'stage1': item.stage1, 'stage2': item.stage2, 
                                    'stage3': item.stage3, 'stage4': item.stage4}
    return json.dumps(ret)

@app.route('/schedule_internal_all', methods=['GET'])
@cross_origin()
def get_all_schedule_internal():
    q = db.session.query(Schedule)
    ret = {}
    for item in q.all():
        ret[item.order_id] = {'salesOrder': item.sales_order,
                            'skuNumber': item.sku_number,
                            'quantity': item.quantity,
                            'quantityCompleted': item.quantity_completed, 
                            'expectedStart': item.expected_start,
                            'expectedCompletion': item.expected_completion,
                            'status': item.status}
    return json.dumps(ret)

product_names = {
    "250": "Enduro 250",
    "550": "Enduro 550",
    "300": "Moto 300",
    "450": "Moto 450"
}

@app.route('/doneQA', methods=['POST'])
@cross_origin()
def doneQA():
    try:
        data = request.get_json()
        qa_obj = QualityAssurance.query.filter_by(serial_number=data['serialNumber']).first()
        ps_obj = Schedule.query.filter_by(order_id=qa_obj.order_id).first() # this order id must exist
        ps_obj.quantity_completed += 1
        fg_obj = FinishedGoodsInventory.query.filter_by(sku_number=ps_obj.sku_number).first()

        if fg_obj is None:
            ret = FinishedGoodsInventory(ps_obj.sku_number, product_names[ps_obj.sku_number[-3:]], ps_obj.quantity-1, 1)
            db.session.add(ret)
        else:
            fg_obj.quantity_in_production -= 1
            fg_obj.quantity_on_hand += 1

        if ps_obj.quantity == ps_obj.quantity_completed:
            ps_obj.status = "Completed"
        else:
            ps_obj.status = "In Production"

        QualityAssurance.query.filter_by(serial_number=data['serialNumber']).delete()
        db.session.commit()
        db.session.close()
        return json.dumps({"result": "doneQA passed"})
    except:
        return json.dumps({"result": "doneQA failed"})

@app.route('/scrapQA', methods=['POST'])
@cross_origin()
def scrapQA():
    try:
        data = request.get_json()
        qa_obj = QualityAssurance.query.filter_by(serial_number=data['serialNumber']).first()
        ret = FloorControl(qa_obj.order_id, str(uuid.uuid4())[0:8].upper() + str(uuid.uuid4())[-1].upper(), 0, 0)
        db.session.add(ret)
        QualityAssurance.query.filter_by(serial_number=data['serialNumber']).delete()
        db.session.commit()
        db.session.close()
        return json.dumps({"result": "scrapQA passed"})
    except:
        return json.dumps({"result": "scrapQA failed"})

@app.route('/scrapFC', methods=['POST'])
@cross_origin()
def scrapFC():
    try:
        data = request.get_json()
        fc_obj = FloorControl.query.filter_by(serial_number=data['serialNumber']).first()
        fc_obj.serial_number = str(uuid.uuid4())[0:8].upper() + str(uuid.uuid4())[-1].upper()
        fc_obj.stage = 0
        fc_obj.status = 0
        db.session.commit()
        db.session.close()
        return json.dumps({"result": "scrapFC passed"})
    except:
        return json.dumps({"result": "scrapFC failed"})

@app.route('/incFG', methods=['POST'])
@cross_origin()
def incFG():
    try:
        data = request.get_json()
        fg_obj = FinishedGoodsInventory.query.filter_by(sku_number=data['skuNumber']).first()
        fg_obj.quantity_on_hand += int(data['amount'])
        db.session.commit()
        db.session.close()
        return json.dumps({"result": "incFG passed"})
    except:
        return json.dumps({"result": "incFG failed"})

@app.route('/incPI', methods=['POST'])
@cross_origin()
def incPI():
    try:
        data = request.get_json()
        pi_obj = PartsInventory.query.filter_by(sku_number=data['skuNumber']).first()
        pi_obj.quantity_on_hand += int(data['amount'])
        db.session.commit()
        db.session.close()
        return json.dumps({"result": "incPI passed"})
    except:
        return json.dumps({"result": "incPI failed"})

@app.route('/usePart', methods=['POST'])
@cross_origin()
def usePart():
    try:
        data = request.get_json()
        pi_obj = PartsInventory.query.filter_by(sku_number=data['skuNumber']).first()
        if pi_obj.quantity_on_hand == 0:
            pi_obj.quantity_on_hand = random.randint(5, 20)
        else:
            pi_obj.quantity_on_hand -= 1
        db.session.commit()
        db.session.close()
        return json.dumps({"result": "usePart passed"})
    except:
        return json.dumps({"result": "usePart failed"})
        
# FOR FRONTEND
#########################################################################################

year = 2018
month = 4
@app.route('/events', methods=['POST'])
@cross_origin()
def events():
    try:
        global month
        global year
        data = request.get_json()
        orderID = data['data']['orderID']
        items = data['data']['items']
        for item in items:
            new_month = month+(item['quantity']//2 + 1)
            if new_month > 12:
                completion_month = new_month % 12
            else:
                completion_month = new_month
            day = str(random.randint(10, 28))

            if month < 10:
                month = "0"+str(month)
            else:
                month = str(month)

            if completion_month < 10:
                completion_month = "0"+str(completion_month)
            else:
                completion_month = str(completion_month)

            ret = Schedule(str(orderID), str(orderID) + '-' + item['model'][-3:], "0000000" + item['model'][-3:],
                item['quantity'], 0, str(year)+"-"+month+"-"+day, str(year)+"-"+completion_month+"-"+day, "Not Started")
            db.session.add(ret)
            db.session.commit()
            ret = FloorControl(str(orderID) + '-' + item['model'][-3:], str(uuid.uuid4())[0:8].upper() + str(uuid.uuid4())[-1].upper(), 0, 0)
            db.session.add(ret)
            db.session.commit()
            if new_month > 12:
                month = new_month % 12
                year += 1
            else:
                month = new_month
        db.session.close()
        return json.dumps({"result": "successfully processed order"})
    except:
        return json.dumps({"result": "failed to process order"})

@app.route('/schedule_all', methods=['GET'])
@cross_origin()
def get_all_schedule():
    q = db.session.query(Schedule)
    ret = {}
    for item in q.all():
        if item.sales_order in ret:  
            ret[item.sales_order] += [{'skuNumber': item.sku_number,
                                'quantity': item.quantity,
                                'quantityCompleted': item.quantity_completed, 
                                'expectedStart': item.expected_start,
                                'expectedCompletion': item.expected_completion,
                                'status': item.status}]
        else:
            ret[item.sales_order] = [{'skuNumber': item.sku_number,
                                'quantity': item.quantity,
                                'quantityCompleted': item.quantity_completed, 
                                'expectedStart': item.expected_start,
                                'expectedCompletion': item.expected_completion,
                                'status': item.status}]
    return json.dumps(ret)

@app.route('/hr', methods=['POST'])
@cross_origin()
def hr():
    return json.dumps({"result": "received data"})

#########################################################################################

if __name__ == '__main__':
    app.debug = True
    app.run()
