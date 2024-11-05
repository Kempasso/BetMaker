import asyncio
import hashlib
import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from src.config import server
from src.domain.event.schemas import UpdateEvent
from src.infrastructure.db.dbrepo import DBStorage
from src.infrastructure.db.models import Bet
from src.infrastructure.db.session import make_session


async def event_update_listener():
    consumer = AIOKafkaConsumer(
        "events_changes",
        bootstrap_servers=server.conf.kafka.bootstrap_servers
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(message)
            decoded_data = message.value.decode()
            async with make_session() as session:
                try:
                    changes_info = UpdateEvent.model_validate_json(decoded_data)
                except Exception as e:
                    print("Something went wrong, but we will continue...") #noqa
                    continue
                bet_repo = DBStorage(Bet, session)
                whereclause = Bet.event_id == changes_info.event_id
                await bet_repo.update(
                    where=whereclause,
                    status=changes_info.status
                )
    finally:
        await consumer.stop()


class KafkaBroker:

    def __init__(self):
        self.bootstrap_servers = server.conf.kafka.bootstrap_servers

    async def remote_call(
        self,
        action: str,
        request: dict = dict(),
        wait_response: bool = True, ):
        service, action = action.split(".")
        request.update(service=service, action=action)
        if wait_response:
            task = asyncio.create_task(self._send_request(request))
            print(task)
            for tick in range(900):
                if task.done():
                    break
                await asyncio.sleep(0.1)
            else:
                task.cancel()
            print(task.result())
            return task.result()
        else:
            await self._send_request_nowait(request)

    async def _send_request(self, request):
        topic = await self._make_read_topic(request['service'])
        try:
            request_key = await self._send_request_nowait(request)
            print(f"{request_key=}")
        except Exception as e:
            print(e)
        consumer = AIOKafkaConsumer(
            topic, bootstrap_servers=self.bootstrap_servers
        )
        await consumer.start()
        try:
            print("before async for")
            async for message in consumer:

                key = message.key.decode()
                print(f"{key=}")
                if request_key == key:
                    data = json.loads(message.value.decode())
                    print(f"{data=}")
                    return data
        finally:
            await consumer.stop()

    async def _send_request_nowait(self, request):

        topic = await self._make_write_topic(request['service'])
        serialized_req = json.dumps(request).encode()
        request_key = hashlib.sha256(serialized_req).hexdigest()
        producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers
        )
        try:
            await producer.start()
            print("before send")
            await producer.send(
                topic, serialized_req, key=request_key.encode()
            )
            print("after send")
            return request_key
        except Exception as e:
            print("Error in _send_request_nowait")
            print(e)
        finally:
            await producer.stop()

    async def _make_read_topic(self, service_name) -> str:
        return f"{service_name}-to-server"

    async def _make_write_topic(self, service_name) -> str:
        return f"{service_name}-to-service"
