import serial
from collections import namedtuple
import time


ScaleProtocol = namedtuple(
    'ScaleProtocol',
    "name baudrate bytesize stopbits parity timeout writeTimeout weightRegexp statusRegexp "
    "statusParse commandTerminator commandDelay weightDelay newWeightDelay "
    "weightCommand zeroCommand tareCommand clearCommand emptyAnswerValid autoResetWeight")

HelmacProtocol = ScaleProtocol(
    name='Helmac',
    baudrate=9600,
    bytesize=serial.SEVENBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_EVEN,
    timeout=1,
    writeTimeout=1,
    weightRegexp="\x02\\s*([0-9.]+)N?\\r",
    statusRegexp=None,
    statusParse=None,
    commandDelay=0.2,
    weightDelay=0.5,
    newWeightDelay=0.2,
    commandTerminator='\r',
    weightCommand='2',
    zeroCommand='Z',
    tareCommand='T',
    clearCommand='C',
    emptyAnswerValid=False,
    autoResetWeight=False,
)

protocol = HelmacProtocol

def _get_raw_response(connection):
    answer = []
    while True:
        char = connection.read(1) # may return `bytes` or `str`
        if not char:
            break
        else:
            answer.append(char)

    return ''.join(answer)

connection = serial.Serial('/dev/ttyUSB0',
    baudrate=protocol.baudrate,
    bytesize=protocol.bytesize,
    stopbits=protocol.stopbits,
    parity=protocol.parity,
    timeout=1,      # longer timeouts for probing
    writeTimeout=1) # longer timeouts for probing

while True:
    print connection.readline()

#connection.write(protocol.weightCommand + protocol.commandTerminator)
#time.sleep(protocol.commandDelay)
#answer = _get_raw_response(connection)
#weight, weight_info, status = self._parse_weight_answer(protocol, answer)

