"""
Client and server using classes
"""

import logging
import socket

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab


# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.sol.sol_clientserver.Server")
    _serving = True
    _data = dict()

    def __init__(self, dict=None):
        if dict:
            self._data = dict
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info('Server created')
        self._logger.info("Server bound to socket " + str(self.sock))


    def serve(self):
        """ Serve """
        self.sock.listen(1)
        self._logger.info('Server started')
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                while True:
                    data = connection.recv(1024)  # receive request from client
                    if not data:
                        break  # stop if client stopped
                    decoded_data = data.decode('utf-8')
                    msg_out = str('')
                    if decoded_data.startswith('GET:'): # client requests one entry: GET:name
                        self._logger.info(f'GET:{decoded_data[4:]} requested via {str(self.sock)}')
                        msg_out = str(self._data.get(decoded_data[4:], 'unknown key'))
                        self._logger.info(f'Sent entry: {decoded_data[4:]} : {msg_out}')
                    elif decoded_data.__eq__('GET_ALL'):  # client requests all entries: GET_ALL
                        self._logger.info(f'GET_ALL requested via {str(self.sock)}')
                        for d in self._data:
                            msg_out += f'{d} : {self._data[d]}\n'
                        self._logger.info(f'Sent {len(self._data)} entries')
                    elif decoded_data.__eq__('GET_NUM_OF_ENTRIES'): # client requests the number of entries
                        self._logger.info(f'GET_NUM_OF_ENTRIES requested via {str(self.sock)}')
                        msg_out = str(len(self._data))
                        self._logger.info(f'Sent number of entries ({str(len(self._data))})')
                    else:
                        self._logger.info(f'unknown request via {str(self.sock)}')
                        msg_out = 'unknown operation'
                    connection.send(msg_out.encode('utf-8'))
                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")

    def add_entry(self, name, number):
        """ add entry to dictionary """
        self._data.update({name: number})
        self._logger.info(f'added entry ({name}, {number})')


class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.sol.sol_clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info('Client created')
        self.logger.info("Client connected to socket " + str(self.sock))

    def __call(self, msg_in, buffer_size=1024):
        """ Call server """
        self.sock.send(msg_in.encode('utf-8'))  # send encoded string as data
        self.logger.info(f'Call {msg_in} via {str(self.sock)}')
        try:
            data = self.sock.recv(buffer_size)  # receive the response
        except socket.timeout:
            return None
        msg_out = data.decode('utf-8')
        print(msg_out)  # print the result
        return msg_out

    def get(self, name):
        """ retrieve number of the given name """
        return self.__call(f'GET:{name}')

    def get_all(self):
        """ retrieve all numbers """
        num = self.__call('GET_NUM_OF_ENTRIES')
        if num:
            num_of_entries = int(num)
            return self.__call('GET_ALL', buffer_size=32 * num_of_entries)
        else:
            return None


    def close(self):
        """ Close socket """
        self.sock.close()
        self.logger.info("Client down.")
