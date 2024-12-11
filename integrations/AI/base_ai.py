from abc import ABC, abstractmethod

class BaseAI(ABC):
    @abstractmethod
    def load_model(self):
        """Cargar el modelo en memoria."""
        pass

    @abstractmethod
    def generate_response(self, messages: list) -> str:
        """
        Dada una lista de mensajes [{"role":"user"|"assistant"|"system","content":"..."}]
        retorna la respuesta del modelo.
        """
        pass

    @abstractmethod
    def get_model_code(self) -> str:
        """Retorna el code del modelo."""
        pass
