# utils/chat/text_processor.py

import re
import random
from .personality_loader import load_character_prompt

class TextProcessor:
    """
    Proporciona utilidades para limpiar y postprocesar texto generado por el modelo.
    """

    @staticmethod
    def load_personality(character: str = "arelia", mode: str = "default") -> str:
        """
        Carga la personalidad completa del personaje.
        """
        return load_character_prompt(character, mode)

    @staticmethod
    def clean_input(output: str) -> str:
        """
        Limpieza básica del texto de entrada antes de enviarlo a la API.
        (Aquí puedes agregar reemplazos si lo necesitas)
        """
        return output

    @staticmethod
    def clean_output(output: str) -> str:
        """
        Limpia la respuesta generada por el modelo:
        - Quita etiquetas como 'Arelia:'
        - Elimina menciones peligrosas
        - Reemplaza emotes si hicieras uso de eso en un futuro
        """
        output = output.replace("Arelia:", "").replace("arelia:", "")
        # output = output.replace("@here", "@/here").replace("@everyone", "@/everyone")
        return output.strip()
    

    @staticmethod
    def format_history(history: list[dict]) -> str:
        """
        Convierte el historial en un texto legible para el prompt y para debug.
        """
        lines = ["Esta es la conversación reciente entre el usuario y Arelia:\n"]
        for i, msg in enumerate(history):
            role = "Usuario" if msg["role"] == "user" else "Arelia"
            lines.append(f"{role}: {msg['content']}")
        return "\n".join(lines).strip()
