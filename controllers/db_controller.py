from flask import Blueprint, jsonify, session, flash, redirect, request
from utils import build_message, rest_output
from services.db_service import intialise_contents, construct_database
from models.base import db

db_controller = Blueprint('db_controller', __name__)


@db_controller.route('/api/initdb')
def initialize_database():
    message_key = 'construct database'
    try:
        construct_database()
    except ValueError as err:
        return rest_output(err)

    return rest_output(message_key)


@db_controller.route('/api/filldb')
def fill_db():
    message_key = 'fill database'
    try:
        intialise_contents()
    except ValueError as err:
        return rest_output(err)

    return rest_output(message_key)
