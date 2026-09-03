import os
from uuid import uuid4


def generateId():
    return str(uuid4())


def Color(r, g, b, a=1):
    return {"r": r, "g": g, "b": b, "a": a}


def Position3(x, y, z=0):
    return {"x": x, "y": y, "z": z}


def Position2(x, y):
    return {"x": x, "y": y}


def GetSurvivalSavePath(
    filename: str,
    company: str = "Unicorn One",
    product: str = "AIComp",
) -> str:
    """
    Returns the full path for a Survival save file, matching Unity's persistentDataPath.
    Use this so Python-generated saves appear where the AIComp game loads them from.
    Example: GetSurvivalSavePath("AIApy.txt") -> .../AppData/LocalLow/Unicorn One/AIComp/Saves/Survival/AIApy.txt
    """
    if not filename.endswith(".txt"):
        filename = filename + ".txt"
    base = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    return os.path.join(base, "AppData", "LocalLow", company, product, "Saves", "Survival", filename)


def GetTennisSavePath(
    filename: str,
    company: str = "Unicorn One",
    product: str = "AIComp",
) -> str:
    """
    Returns the full path for a Tennis save file, matching Unity's persistentDataPath.
    Example: GetTennisSavePath("Away.txt") -> .../AppData/LocalLow/Unicorn One/AIComp/Saves/Tennis/Away.txt
    """
    if not filename.endswith(".txt"):
        filename = filename + ".txt"
    base = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    return os.path.join(base, "AppData", "LocalLow", company, product, "Saves", "Tennis", filename)
