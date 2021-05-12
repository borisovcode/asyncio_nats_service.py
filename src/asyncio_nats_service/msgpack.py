import msgpack


class MsgPackMixin(object):
    """Примесь для работы с сообщениями в формате MsgPack"""
    def packb(self, data, use_bin_type=True):
        return msgpack.packb(data, use_bin_type=use_bin_type)

    def unpackb(self, data, raw=False):
        return msgpack.unpackb(data, raw=raw)