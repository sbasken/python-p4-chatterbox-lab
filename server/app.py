from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():

    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at).all()
        messages_dict = [ message.to_dict() for message in messages]

        response = make_response(
            jsonify(messages_dict),
            200
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    
    elif request.method == 'POST':
        # new_message = Message(
        #     body = request.form.get('body'),
        #     username = request.form.get('username')
        # )
        data = request.get_json()
        new_message = Message(
            body=data['body'],
            username=data['username']
        )

        db.session.add(new_message)
        db.session.commit()

        response = make_response(
        jsonify(new_message.to_dict()),
        201
        )
        response.headers['Content-Type'] = 'application/json'
        return response



@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    
    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message, attr,data[attr])
            
            db.session.add(message)
            db.session.commit()

            response = make_response(
                jsonify(message.to_dict()),
                200
            )
            response.headers['Content-Type'] = 'application/json'
            return response

    elif request.method == 'DELETE':
        if request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Baked_goods deleted."
            }
            response = make_response(
                jsonify(response_body),
                200
            )
            response.headers['Content-Type'] = 'application/json'
            return response


if __name__ == '__main__':
    app.run(port=5555)
