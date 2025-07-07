# app/utils/chat/personality_loader.py

import json
from pathlib import Path

def load_character_prompt(character: str, mode: str) -> str:
    """
    Carga y combina el perfil base y las instrucciones de comportamiento para un personaje.
    """
    base_path = Path(__file__).resolve().parent.parent.parent / "characters" / character
    profile_file = base_path / "base.json"
    mode_file = base_path / "modes" / f"{mode}.txt"

    if not profile_file.is_file():
        raise FileNotFoundError(f"Profile not found for {character}: {profile_file}")
    if not mode_file.is_file():
        raise FileNotFoundError(f"Mode '{mode}' not found for {character}: {mode_file}")

    with profile_file.open(encoding="utf-8") as f:
        profile = json.load(f)
    profile_json = json.dumps(profile, ensure_ascii=False, indent=2)

    with mode_file.open(encoding="utf-8") as f:
        instructions = f.read().strip()

    return (
        f"You are {character.capitalize()}, a unique persona with the following profile:\n{profile_json}\n\n"
        f"Behavioral instructions:\n{instructions}\n"
        "Always reply embodying this personality."
    )