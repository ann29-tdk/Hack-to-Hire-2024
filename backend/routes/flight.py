from flask import Blueprint, request, jsonify
from models.flight import Flight
from models.user import User
from models.user import Notification
from bson import ObjectId
from datetime import datetime
import logging
from dateutil.parser import isoparse

flight_bp = Blueprint('flight', __name__)

def format_delay(delay):
    if delay > 60:
        hours = delay // 60
        minutes = delay % 60
        return f"{hours} hour(s) {minutes} minute(s)"
    return f"{delay} minute(s)"

def convert_to_serializable(doc):
    if isinstance(doc, dict):
        return {k: convert_to_serializable(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [convert_to_serializable(v) for v in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    elif isinstance(doc, datetime):
        return doc.isoformat()  # Format datetime as ISO 8601 string
    return doc

@flight_bp.route('/<flightNumber>', methods=['GET'])
def get_flight(flightNumber):
    try:
        logging.info(f"Fetching flight with flight number: {flightNumber}")
        flight = Flight.objects(flightNumber=flightNumber).first()
        if flight:
            # Convert document to a serializable format
            flight_data = convert_to_serializable(flight.to_mongo().to_dict())

            # Format arrivalDate as ISO 8601 string
            flight_data['arrivalDate'] = flight.arrivalDate.isoformat()

            formatted_flight = {
                **flight_data,
                'latestArrivalTime': flight.arrivalTimes[-1] if flight.arrivalTimes else None,
                'latestDepartureTime': flight.departureTimes[-1] if flight.departureTimes else None,
                'latestArrivalDelay': format_delay(flight.arrivalDelays[-1] if flight.arrivalDelays else 0),
                'latestDepartureDelay': format_delay(flight.departureDelays[-1] if flight.departureDelays else 0)
            }
            logging.info(f"Flight found: {formatted_flight}")
            return jsonify(formatted_flight), 200
        logging.warning(f"Flight with flight number {flightNumber} not found")
        return jsonify(message='Flight not found'), 404
    except Exception as e:
        logging.error(f"Error fetching flight with flight number {flightNumber}: {e}")
        return jsonify(message='Internal server error', error=str(e)), 500

@flight_bp.route('/update', methods=['POST'])
def update_flight():
    try:
        data = request.get_json()
        flightNumber = data.get('flightNumber')
        arrivalDate = isoparse(data.get('arrivalDate'))
        arrivalTime = data.get('arrivalTime')
        departureTime = data.get('departureTime')
        isCancelled = data.get('isCancelled')
        destination = data.get('destination')

        flight = Flight.objects(flightNumber=flightNumber).first()
        if not flight:
            flight = Flight(
                flightNumber=flightNumber,
                arrivalDate=arrivalDate,
                arrivalTimes=[arrivalTime] if arrivalTime else [],
                departureTimes=[departureTime] if departureTime else [],
                isCancelled=isCancelled,
                destination=destination,
                arrivalDelays=[0],
                departureDelays=[0]
            )
        else:
            flight.update(
                arrivalDate=arrivalDate,
                isCancelled=isCancelled,
                destination=destination,
            )
            if arrivalTime:
                flight.arrivalTimes.append(arrivalTime)
                initialArrivalTime = datetime.strptime(flight.arrivalTimes[0], '%H:%M').time()
                currentArrivalTime = datetime.strptime(arrivalTime, '%H:%M').time()
                arrivalDelay = (datetime.combine(datetime.min, currentArrivalTime) - datetime.combine(datetime.min, initialArrivalTime)).seconds // 60
                flight.arrivalDelays.append(arrivalDelay)

            if departureTime:
                flight.departureTimes.append(departureTime)
                initialDepartureTime = datetime.strptime(flight.departureTimes[0], '%H:%M').time()
                currentDepartureTime = datetime.strptime(departureTime, '%H:%M').time()
                departureDelay = (datetime.combine(datetime.min, currentDepartureTime) - datetime.combine(datetime.min, initialDepartureTime)).seconds // 60
                flight.departureDelays.append(departureDelay)
        
        flight.save()

        users = User.objects(associatedFlights=flightNumber)
        for user in users:
            latestArrivalTime = flight.arrivalTimes[-1] if flight.arrivalTimes else None
            latestDepartureTime = flight.departureTimes[-1] if flight.departureTimes else None
            notification_message = f"The Flight {flightNumber} scheduled for {arrivalDate} will depart at {latestDepartureTime} and arrive at {latestArrivalTime} at {destination}. Thank you and have a safe flight."

            user.notifications.append(Notification(message=notification_message, date=datetime.utcnow()))
            user.save()

            flight_bp.socketio.emit('flightUpdate', {
                'message': notification_message, 
                'flight': convert_to_serializable(flight.to_mongo().to_dict())
            }, room=str(user.id))
        
        return jsonify(message='Flight updated successfully'), 200
    except Exception as e:
        logging.error(f"Error updating flight: {e}")
        return jsonify(message='Internal server error', error=str(e)), 500

@flight_bp.route('/add_test_flight', methods=['POST'])
def add_test_flight():
    try:
        logging.info("Attempting to add test flight...")
        flight = Flight(
            flightNumber="3",
            arrivalDate=datetime.utcnow(),  # Use datetime object
            arrivalTimes=["10:00"],
            departureTimes=["08:00"],
            isCancelled=False,
            destination="New York",
            arrivalDelays=[0],
            departureDelays=[0]
        )
        flight.save()
        logging.info("Test flight added successfully")
        return jsonify(message='Test flight added successfully'), 201
    except Exception as e:
        logging.error(f"Error adding test flight: {e}")
        return jsonify(message='Error adding test flight', error=str(e)), 500
