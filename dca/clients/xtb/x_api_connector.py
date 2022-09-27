import logging
import socket
import ssl
import time

import simplejson as json

from dca.models.xtb import Symbol, TradeTransInfo

# set to true on debug environment only
DEBUG = True

# default connection properites
DEFAULT_XAPI_ADDRESS = "xapi.xtb.com"
DEFAULT_XAPI_PORT = 5124
DEFUALT_XAPI_STREAMING_PORT = 5125

# wrapper name and version
WRAPPER_NAME = "python"
WRAPPER_VERSION = "2.5.0"

# API inter-command timeout (in ms)
API_SEND_TIMEOUT = 100

# max connection tries
API_MAX_CONN_TRIES = 3

# logger properties
logger = logging.getLogger("jsonSocket")
FORMAT = "[%(asctime)-15s][%(funcName)s:%(lineno)d] %(message)s"
logging.basicConfig(format=FORMAT)

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.CRITICAL)


class JsonSocket:  # pylint: disable=too-many-instance-attributes
    def __init__(self, address, port, encrypt=False):
        self._ssl = encrypt
        if self._ssl is not True:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = ssl.wrap_socket(sock)  # pylint: disable=deprecated-method
        self.conn = self.socket
        self._timeout = None
        self._address = address
        self._port = port
        self._decoder = json.JSONDecoder()
        self._received_data = ""

    def connect(self):
        for _ in range(API_MAX_CONN_TRIES):
            try:
                self.socket.connect((self.address, self.port))
            except socket.error as msg:
                logger.error("SockThread Error: %s", msg)
                time.sleep(0.25)
                continue
            logger.info("Socket connected")
            return True
        return False

    def _send_obj(self, obj):
        msg = json.dumps(obj)
        self._waiting_send(msg)

    def _waiting_send(self, msg):
        if self.socket:
            sent = 0
            msg = msg.encode("utf-8")
            while sent < len(msg):
                sent += self.conn.send(msg[sent:])
                logger.info("Sent: %s", str(msg))
                time.sleep(API_SEND_TIMEOUT / 1000)

    def _read(self, bytes_size=4096):
        if not self.socket:
            raise RuntimeError("socket connection broken")
        while True:
            char = self.conn.recv(bytes_size).decode()
            self._received_data += char
            try:
                (resp, size) = self._decoder.raw_decode(self._received_data)
                if size == len(self._received_data):
                    self._received_data = ""
                    break
                if size < len(self._received_data):
                    self._received_data = self._received_data[size:].strip()
                    break
            except ValueError:
                continue
        logger.info("Received: %s", str(resp))
        return resp

    def _read_obj(self):
        msg = self._read()
        return msg

    def close(self):
        logger.debug("Closing socket")
        self._close_socket()
        if self.socket is not self.conn:
            logger.debug("Closing connection socket")
            self._close_connection()

    def _close_socket(self):
        self.socket.close()

    def _close_connection(self):
        self.conn.close()

    def _get_timeout(self):
        return self._timeout

    def _set_timeout(self, timeout):
        self._timeout = timeout
        self.socket.settimeout(timeout)

    def _get_address(self):
        return self._address

    def _set_address(self, address):
        pass

    def _get_port(self):
        return self._port

    def _set_port(self, port):
        pass

    def _get_encrypt(self):
        return self._ssl

    def _set_encrypt(self, encrypt):
        pass

    timeout = property(_get_timeout, _set_timeout, doc="Get/set the socket timeout")
    address = property(_get_address, _set_address, doc="read only property socket address")
    port = property(_get_port, _set_port, doc="read only property socket port")
    encrypt = property(_get_encrypt, _set_encrypt, doc="read only property socket port")


class APIClient(JsonSocket):
    def __init__(self, address=DEFAULT_XAPI_ADDRESS, port=DEFAULT_XAPI_PORT, encrypt=True):
        super().__init__(address, port, encrypt)
        if not self.connect():
            raise Exception(
                "Cannot connect to "
                + address
                + ":"
                + str(port)
                + " after "
                + str(API_MAX_CONN_TRIES)
                + " retries"
            )

    def execute(self, dictionary):
        self._send_obj(dictionary)
        return self._read_obj()

    def disconnect(self):
        self.close()

    def command_execute(self, command_name, arguments=None):
        return self.execute(base_command(command_name, arguments))


# Command templates
def base_command(command_name, arguments=None):
    if arguments is None:
        arguments = {}
    return dict([("command", command_name), ("arguments", arguments)])


def login_command(user_id, password, app_name=""):
    return base_command("login", dict(userId=user_id, password=password, appName=app_name))


def trade_transaction_command(trade: TradeTransInfo):
    print(trade)
    return base_command("tradeTransaction", dict(tradeTransInfo=trade.dict()))


def get_symbol_command(symbol: Symbol):
    return base_command("getSymbol", dict(symbol=symbol.value))
