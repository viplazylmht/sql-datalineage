from typing import TypeVar, Generic
import pickle

T = TypeVar("T")


class Serializer(Generic[T]):
    """Serializer interface for serializing and deserializing data using
    Python’s highest available pickle protocol."""

    def serialize(self, data: T) -> bytes:
        """Serialize data to bytes"""
        return pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)

    def deserialize(self, data: bytes) -> T:
        """Deserialize data from bytes"""
        return pickle.loads(data)
