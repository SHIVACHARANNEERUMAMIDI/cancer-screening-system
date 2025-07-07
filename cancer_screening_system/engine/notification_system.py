from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from dataclasses import dataclass
import logging
import threading
import time

# === Logging === #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NotificationSystem")

# === Notification DTO === #
@dataclass(frozen=True)
class Notification:
    patient_id: int
    message: str

# === Strategy Interface === #
class NotificationChannel(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> bool:
        pass

# === Channel Implementations === #
class ConsoleNotifier(NotificationChannel):
    def send(self, notification: Notification) -> bool:
        print(f"[REMINDER] Patient {notification.patient_id}: {notification.message}")
        return True

class LoggerNotifier(NotificationChannel):
    def send(self, notification: Notification) -> bool:
        logger.info(f"Patient {notification.patient_id} - {notification.message}")
        return True

class NullNotifier(NotificationChannel):  # For testing/mocking
    def send(self, notification: Notification) -> bool:
        return True

# === Notification Engine === #
class NotificationSystem:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._channels: Dict[str, NotificationChannel] = {
            "console": ConsoleNotifier(),
            "log": LoggerNotifier(),
            "null": NullNotifier(),
        }
        self._default_channel = "console"

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def register_channel(self, name: str, channel: NotificationChannel):
        self._channels[name] = channel

    def send_reminder(
        self,
        patient_id: int,
        message: str,
        preferred_channels: Optional[List[str]] = None
    ) -> bool:
        preferred_channels = preferred_channels or [self._default_channel]
        notification = Notification(patient_id, message)

        for channel_name in preferred_channels:
            channel = self._channels.get(channel_name)
            if not channel:
                logger.warning(f"Channel {channel_name} not registered.")
                continue
            try:
                if channel.send(notification):
                    return True
            except Exception as e:
                logger.error(f"Failed to send via {channel_name}: {e}")
                continue
        return False

# === Singleton Wrapper === #
def send_reminder(patient_id: int, message: str, channels: Optional[List[str]] = None):
    notifier = NotificationSystem.get_instance()
    return notifier.send_reminder(patient_id, message, channels)
