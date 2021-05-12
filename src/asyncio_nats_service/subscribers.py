from asyncio import AbstractEventLoop

from nats.aio.client import Client as NATS


class NatsSubscriberBase(object):
    """
    Base class for NATS subscribe handlers as object

    NatsService using `message_handler` from a instance of this class as callback function
    """

    nats_client: NATS  #: nats_client from NatsService

    async_loop: AbstractEventLoop = None  #: async loop from NatsService

    def __init__(self, nats_client: NATS, async_loop: AbstractEventLoop):
        self.async_loop = async_loop
        self.nats_client = nats_client

    async def message_handler(self, msg):
        """Method as callback subscriber function"""
        raise NotImplementedError('subclasses of NatsSubscriber must provide a message_handler() method')
