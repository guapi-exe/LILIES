import struct


class DataStream:
    def __init__(self, length):
        self._pos = 0
        self._buf = bytearray(length)
        self._lim = length

    @staticmethod
    def allocate(length):
        return DataStream(length)

    @staticmethod
    def from_buffer(buffer):
        obj = DataStream(len(buffer))
        obj.put(buffer)
        obj.position(0)
        return obj

    def clear(self):
        self._pos = 0
        self._lim = len(self._buf)
        return self

    def get(self, bytes=None, offset=None, length=None):
        if isinstance(bytes, bytearray):
            self._buf[self._pos:self._pos + length] = bytes[offset:offset + length]
            self._pos += length
        else:
            o = self._pos
            self._pos = o + (bytes if bytes else 1)
            return self._buf[o:o + bytes] if bytes else self._buf[o]

    def limit(self, limit=None):
        if limit is not None:
            self._lim = limit
            self._pos = min(self._pos, limit)
            return self
        else:
            return self._lim

    def remaining(self):
        return self._lim - self._pos

    def get_short(self):
        return struct.unpack('>h', self.get(2))[0]

    def get_ushort(self):
        return struct.unpack('>H', self.get(2))[0]

    def position(self, pos=None):
        if pos is not None:
            self._pos = pos
            return self
        else:
            return self._pos

    def flip(self):
        self._lim = self._pos
        self._pos = 0
        return self

    def put(self, data):
        if isinstance(data, bytearray):
            write_bytes = min(self.remaining(), len(data))
            self._buf[self._pos:self._pos + write_bytes] = data[:write_bytes]
            self._pos += write_bytes
            return write_bytes
        elif isinstance(data, str):
            return self.put(bytearray(data, 'utf-8'))
        elif isinstance(data, list):
            return self.put(bytearray(data))
        elif isinstance(data, DataStream):
            data.position(data.position() + self.put(data._get_buffer(data.position())))
            return self
        else:
            self._buf[self._pos] = data
            self._pos += 1
            return self

    def has_remaining(self):
        return self.remaining() != 0

    def capacity(self):
        return len(self._buf)

    def put_short(self, data):
        self._buf[self._pos:self._pos + 2] = struct.pack('>h', data)
        self._pos += 2
        return self

    def put_ushort(self, data):
        self._buf[self._pos:self._pos + 2] = struct.pack('>H', data)
        self._pos += 2
        return self

    def array(self):
        return list(self._buf)

    def put_int(self, data):
        self._buf[self._pos:self._pos + 4] = struct.pack('>i', data)
        self._pos += 4
        return self

    def getInt(self):
        o = self._pos if self._pos else 0
        self._pos = o + 4
        return struct.unpack('>i', self._buf[o:o + 4])[0]

    def __str__(self):
        return f'DataStream[pos={self._pos},lim={self._lim},cap={len(self._buf)}]'

    def _get_buffer(self, offset=None):
        return self._buf[offset if offset is not None else 0:self._lim]

    def put_long(self, data):
        self._buf[self._pos:self._pos + 8] = struct.pack('>q', data)
        self._pos += 8
        return self

    def put_float(self, data):
        self._buf[self._pos:self._pos + 4] = struct.pack('>f', data)
        self._pos += 4
        return self

    def get_float(self):
        o = self._pos if self._pos else 0
        self._pos = o + 4
        return struct.unpack('>f', self._buf[o:o + 4])[0]

    def get_double(self):
        o = self._pos if self._pos else 0
        self._pos = o + 8
        return struct.unpack('>d', self._buf[o:o + 8])[0]

    def get_long(self):
        o = self._pos if self._pos else 0
        self._pos = o + 8
        value = struct.unpack('>q', self._buf[o:o + 8])[0]
        return value

    def read_string(self):
        return self.get(self.get_ushort()).decode('utf-8')

    def write_string(self, buf):
        if isinstance(buf, bytearray):
            self.put_ushort(len(buf))
            self.put(buf)
        else:
            self.write_string(bytearray(buf, 'utf-8'))
