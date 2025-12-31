from uuid import uuid4


def generateId():
    return str(uuid4())


def Color(r, g, b, a=1):
    return {"r": r, "g": g, "b": b, "a": a}


def Position3(x, y, z=0):
    return {"x": x, "y": y, "z": z}


def Position2(x, y):
    return {"x": x, "y": y}
