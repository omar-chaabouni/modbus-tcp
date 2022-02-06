# import logging
# from socketserver import TCPServer
# from collections import defaultdict

# from umodbus import conf
# from umodbus.server.tcp import RequestHandler, get_server
# from umodbus.utils import log_to_stream

# # Add stream handler to logger 'uModbus'.
# log_to_stream(level=logging.DEBUG)

# # A very simple data store which maps addresses against their values.
# data_store = defaultdict(int)

# # Enable values to be signed (default is False).
# conf.SIGNED_VALUES = True

# TCPServer.allow_reuse_address = True
# app = get_server(TCPServer, ('localhost', 2001), RequestHandler)


# @app.route(slave_ids=list(range(1, 10)), function_codes=[1,4], addresses=list(range(0, 1000)))
# def read_data_store(slave_id, function_code, address):
#     """" Return value of address. """
#     print('Read : ',slave_id, function_code, address, 'Data : ', data_store)
#     return data_store[address]


# @app.route(slave_ids=list(range(1, 10)), function_codes=[15, 16], addresses=list(range(0, 1000)))
# def write_data_store(slave_id, function_code, address, value):
#     """" Set value for address. """
#     data_store[address] = value
#     print('Write : ', data_store)

import socket
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# hostname = socket.gethostname()    
# server_ip_address = socket.gethostbyname(hostname)
server_ip_address = '127.0.0.1'
server_port = 200

store = ModbusSlaveContext(zero_mode=True)
context = ModbusServerContext(slaves=store, single=True)

print("[+]Info : Server Started on IP : {I} and PORT : {P} ".format(I=server_ip_address,P=server_port))
server=StartTcpServer(context, address=(server_ip_address,server_port))

if __name__ == '__main__':
    try:
        print('Starting server ...')
        app.serve_forever()
    finally:
        print('Shutdown server ...')
        app.shutdown()
        app.server_close()
        print('Server is offline')
