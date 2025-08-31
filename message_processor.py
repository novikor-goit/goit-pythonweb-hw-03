import json
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Payload:
    username: str
    message: str


@dataclass(frozen=True)
class Message:
    datetime: datetime
    payload: Payload


class MessageFactory:
    @staticmethod
    def create(username: str, message: str) -> Message:
        return Message(datetime.now(), Payload(username=username, message=message))


class MessageProcessor:
    STORAGE_PATH = "storage/data.json"

    @staticmethod
    def load_messages() -> list[Message]:
        try:
            with open(MessageProcessor.STORAGE_PATH, "r") as file:
                data = json.load(file)
                return [
                    Message(datetime.fromisoformat(time), Payload(**payload))
                    for message in data
                    for time, payload in message.items()
                ]
        except FileNotFoundError:
            return []

    @staticmethod
    def append_message(message: Message) -> None:
        existing_messages = MessageProcessor.load_messages()

        with open(MessageProcessor.STORAGE_PATH, "w") as file:
            existing_messages.append(message)
            data = [
                {
                    msg.datetime.isoformat(): {
                        "username": msg.payload.username,
                        "message": msg.payload.message,
                    },
                }
                for msg in existing_messages
            ]
            json.dump(data, file, indent=4)
