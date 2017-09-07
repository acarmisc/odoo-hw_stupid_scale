# -*- coding: utf-8 -*-
import logging
import os
import re
import time

import serial

from collections import namedtuple

import openerp.addons.hw_proxy.controllers.main as hw_proxy
from openerp import http

_logger = logging.getLogger(__name__)

DRIVER_NAME = 'scale'


ScaleProtocol = namedtuple(
    'ScaleProtocol',
    "name baudrate bytesize stopbits parity timeout writeTimeout weightRegexp statusRegexp "
    "statusParse commandTerminator commandDelay weightDelay newWeightDelay "
    "weightCommand zeroCommand tareCommand clearCommand emptyAnswerValid autoResetWeight")

EchoProtocol = ScaleProtocol(
    name='EchoProtocol',
    baudrate=9600,
    bytesize=serial.SEVENBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_EVEN,
    timeout=1,
    writeTimeout=1,
    weightRegexp="\x02\\s*([0-9.]+)N?\\r",
    statusRegexp=None,
    statusParse=None,
    commandDelay=1,
    weightDelay=2,
    newWeightDelay=1,
    commandTerminator='',
    weightCommand='W',
    zeroCommand='Z',
    tareCommand='T',
    clearCommand='C',
    emptyAnswerValid=False,
    autoResetWeight=False,
)

SCALE_PROTOCOLS = (
    EchoProtocol,
)

class StupidScale(object):

    def __init__(self):
        self.status = {'status': 'connecting', 'messages': []}
        self.weight = 9.9
        self.weight_info = 'ok'
        self.device = None
        self.protocol = None

    def set_status(self, status, message):
        self.status = dict(status=status, messages=[message])

    def get_weight(self):
        connection = serial.Serial('/dev/ttyUSB0')
        response = connection.readline()
        _logger.debug(response)
        self.weight = float(response.replace('kg', '').strip())
        connection.close()
        return self.weight

    def get_weight_info(self):
        return self.weight_info

    def get_status(self):
        return self.status

    def get_device(self):
        self.set_status('connected', 'connected to EchoProtocol')
        self.protocol = EchoProtocol

stupid_scale = StupidScale()
stupid_scale.get_device()

hw_proxy.drivers[DRIVER_NAME] = stupid_scale


class ScaleDriver(hw_proxy.Proxy):
    @http.route('/hw_proxy/scale_read/', type='json', auth='none', cors='*')
    def scale_read(self):
        return dict(weight=stupid_scale.get_weight(), unit='kg', info=stupid_scale.get_weight_info())

