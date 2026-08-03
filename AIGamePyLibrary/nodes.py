import numbers
from typing import Literal

from .data import colorNames, countryNames
from .lib import AddNode, ConnectPorts, Node, SaveData, data
from .utils import Color, GetSurvivalSavePath, Position3


def parseLiteral(value):
    if isinstance(value, Node):
        return value

    elif isinstance(value, bool):
        return Bool(value)

    elif isinstance(value, numbers.Number):
        return Float(value)

    elif isinstance(value, str):
        if value in colorNames.__args__:
            return Color(value)
        elif value in countryNames.__args__:
            return Country(value)
        else:
            return String(value)

    return value


def cache(function):
    cachedNodes = {}

    def wrapper(*args, **kwargs):
        disableCache = kwargs.pop("disableCache", False)
        # Include both args and kwargs in cache key (kwargs sorted for determinism)
        cacheArgs = (
            tuple(hash(arg) for arg in args),
            tuple((k, hash(v)) for k, v in sorted(kwargs.items())),
        )

        if disableCache:
            return function(*args, **kwargs)

        if cacheArgs not in cachedNodes:
            cachedNodes[cacheArgs] = function(*args, **kwargs)

        return cachedNodes[cacheArgs]

    wrapper.cacheStore = cachedNodes
    return wrapper


class GameEntity:
    def __init__(self, entityType: str):
        self.entityType = entityType

    @property
    def Position(self) -> Node:
        return VolleyballGetVector3(f"{self.entityType} Position")

    @property
    def Velocity(self) -> Node:
        return VolleyballGetVector3(f"{self.entityType} Velocity")

    @property
    def Transform(self) -> Node:
        return VolleyballGetTransform(self.entityType)


class PlayerEntity(GameEntity):
    @property
    def CanJump(self) -> Node:
        return VolleyballGetBool(f"{self.entityType} Can Jump")

    @property
    def TeamSpawn(self) -> Node:
        return VolleyballGetTransform(f"{self.entityType} Team Spawn")

    @property
    def Score(self) -> Node:
        if self.entityType == "Self":
            return VolleyballGetFloat("Team score")
        if self.entityType == "Opponent":
            return VolleyballGetFloat("Opponent score")


class BallClass(GameEntity):
    def __init__(self):
        super().__init__("Ball")

    @property
    def IsSelfSide(self) -> Node:
        return VolleyballGetBool("Ball Is Self Side")

    @property
    def TouchesRemaining(self) -> Node:
        return VolleyballGetFloat("Ball touches remaining")


class GameClass:
    @property
    def DeltaTime(self) -> Node:
        return VolleyballGetFloat("Delta time")

    @property
    def FixedDeltaTime(self) -> Node:
        return VolleyballGetFloat("Fixed delta time")

    @property
    def Gravity(self) -> Node:
        return VolleyballGetFloat("Gravity")

    @property
    def Pi(self) -> Node:
        return VolleyballGetFloat("Pi")

    @property
    def SimulationDuration(self) -> Node:
        return VolleyballGetFloat("Simulation duration")


Self = PlayerEntity("Self")
Opponent = PlayerEntity("Opponent")
Ball = BallClass()
Game = GameClass()


def And(node0: Node, node1: Node) -> Node:
    return CompareBool(node0, node1, "and")


def Or(node0: Node, node1: Node) -> Node:
    return CompareBool(node0, node1, "or")


def Xor(node0: Node, node1: Node) -> Node:
    return CompareBool(node0, node1, "xor")


def Equal(node0: Node, node1: Node) -> Node:
    """Bool comparison"""
    return CompareBool(node0, node1, "equal to")


def Abs(node: Node) -> Node:
    return Operation(node, "abs")


def AbsFloat(node: Node) -> Node:
    """Alias for Abs - converts a number to its absolute value."""
    return Abs(node)


def Round(node: Node) -> Node:
    return Operation(node, "round")


def Floor(node: Node) -> Node:
    return Operation(node, "floor")


def Ceil(node: Node) -> Node:
    return Operation(node, "ceil")


def Sin(node: Node) -> Node:
    return Operation(node, "sin")


def Cos(node: Node) -> Node:
    return Operation(node, "cos")


def Tan(node: Node) -> Node:
    return Operation(node, "tan")


def Asin(node: Node) -> Node:
    return Operation(node, "asin")


def Acos(node: Node) -> Node:
    return Operation(node, "acos")


def Atan(node: Node) -> Node:
    return Operation(node, "atan")


def Sqrt(node: Node) -> Node:
    return Operation(node, "sqrt")


def Sign(node: Node) -> Node:
    return Operation(node, "sign")


def Ln(node: Node) -> Node:
    return Operation(node, "ln")


def Log10(node: Node) -> Node:
    return Operation(node, "log10")


def Exp(node: Node) -> Node:
    """e^x"""
    return Operation(node, "e^")


def Pow10(node: Node) -> Node:
    """10^x"""
    return Operation(node, "10^")


@cache
def InitializeSlime(
    name, color: colorNames, country: countryNames, speed, acceleration, jump
):
    speedNode = Stat(speed)
    accelerationNode = Stat(acceleration)
    jumpNode = Stat(jump)

    ConstructSlimeProperties(
        name, color, country, speedNode, accelerationNode, jumpNode
    )


@cache
def InitializeSurvival(
    name: str,
    country: countryNames,
    skin: colorNames,
    body_style: int | float,
    hair_style: int | float,
    hair_color: colorNames,
    facial_hair: int | float,
    custom_texture: str,
):
    """Initialize survival character with cosmetic properties. Sets up an Aialander for the Survival game. All parameters are required."""
    ConstructSurvivalProperties(
        String(name),
        Country(country),
        Color(skin),
        Float(body_style),
        Float(hair_style),
        Color(hair_color),
        Float(facial_hair),
        String(custom_texture),
    )


def InitializeDemoDerby(
    name: str,
    country: countryNames,
    skin_color: colorNames,
    body_style: int | float,
    hair_style: int | float,
    hair_color: colorNames,
    facial_hair_style: int | float,
    car_color: colorNames,
    custom_texture: str,
):
    """Initialize modular car and driver cosmetics for the Demo Derby simulation (delegates to `InitializeParking`). Returns the `UniformModularCarProperties` node so callers can set `node.data["modifier"] = "True"` to mark the car as LLM-driven."""
    return InitializeParking(
        name,
        country,
        skin_color,
        body_style,
        hair_style,
        hair_color,
        facial_hair_style,
        car_color,
        custom_texture,
    )


@cache
def InitializeParking(
    name: str,
    country: countryNames,
    skin_color: colorNames,
    body_style: int | float,
    hair_style: int | float,
    hair_color: colorNames,
    facial_hair_style: int | float,
    car_color: colorNames,
    custom_texture: str,
):
    """Initialize parking car and driver cosmetics for the Parking simulation. Returns the `UniformModularCarProperties` node so callers can set `node.data["modifier"] = "True"` to mark the car as LLM-driven."""
    return ConstructModularUniformProperties(
        String(name),
        Country(country),
        Color(skin_color),
        Float(body_style),
        Float(hair_style),
        Color(hair_color),
        Float(facial_hair_style),
        Color(car_color),
        String(custom_texture),
    )


@cache
def AddVector3(node0: Node, node1: Node):
    baseNode = AddNode("AddVector3")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def AddFloats(node0: Node, node1: Node):
    baseNode = AddNode("AddFloats")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def Bool(value: bool):
    return AddNode("Bool", "0" if value else "1")


@cache
def ClampFloat(node0: Node, node1: Node, node2: Node):
    baseNode = AddNode("ClampFloat")
    inputTypes = ["Float", "Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def Color(value: int | colorNames):
    """Color dropdown. Pass index (wraps) or color label."""
    return AddNode("Color", value)


@cache
def Vector3(node0: Node, node1: Node, node2: Node):
    baseNode = AddNode("ConstructVector3")
    inputTypes = ["Float", "Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def CompareBool(
    node0: Node,
    node1: Node,
    value: int
    | Literal["and", "or", "equal to", "xor", "nor", "nand", "xnor"] = "and",
):
    baseNode = AddNode("CompareBool", value)
    inputTypes = ["Bool", "Bool"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def CompareFloats(
    node0: Node,
    node1: Node,
    value: int | Literal["==", "<", ">", "<=", ">="] = "==",
):
    baseNode = AddNode("CompareFloats", value)
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def ConditionalSetBool(node0: Node, node1: Node, node2: Node, value: bool = True):
    baseNode = AddNode("ConditionalSetBool", "0" if value else "1")
    inputTypes = ["Bool", "Bool", "Bool"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def ConditionalSetFloat(node0: Node, node1: Node, node2: Node, value: bool = True):
    baseNode = AddNode("ConditionalSetFloatV2", "0" if value else "1")
    inputTypes = ["Bool", "Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def ConditionalSetSurvivalEmote(node0: Node, node1: Node, node2: Node, value: bool = True):
    baseNode = AddNode("ConditionalSetSurvivalEmote", "0" if value else "1")
    inputTypes = ["Bool", "SurvivalEmote", "SurvivalEmote"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def ConditionalSetSurvivalState(node0: Node, node1: Node, node2: Node, value: bool = True):
    baseNode = AddNode("ConditionalSetSurvivalState", "0" if value else "1")
    inputTypes = ["Bool", "SurvivalState", "SurvivalState"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def ConditionalSetVector3(node0: Node, node1: Node, node2: Node, value: bool = True):
    baseNode = AddNode("ConditionalSetVector3", "0" if value else "1")
    inputTypes = ["Bool", "Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def ConstructSlimeProperties(
    node0: Node,
    node1: colorNames,
    node2: countryNames,
    node3: Node,
    node4: Node,
    node5: Node,
):
    baseNode = AddNode("ConstructSlimeProperties")
    inputTypes = ["String", "Color", "Country", "Stat", "Stat", "Stat"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2, node3, node4, node5])
    return baseNode


@cache
def ConstructSurvivalProperties(
    node0: Node,
    node1: countryNames,
    node2: colorNames,
    node3: Node,
    node4: Node,
    node5: colorNames,
    node6: Node,
    node7: Node,
):
    """Sets cosmetic options for an Aialander. Inputs: name, country, skin color, body style, hair style, hair color, facial hair, outfit URL."""
    baseNode = AddNode("ConstructSurvivalProperties")
    inputTypes = ["String", "Country", "Color", "Float", "Float", "Color", "Float", "String"]
    connectInputNodes(
        baseNode,
        inputTypes,
        [node0, node1, node2, node3, node4, node5, node6, node7],
    )
    return baseNode


@cache
def SlimeController(node0: Node, node1: Node):
    baseNode = AddNode("SlimeController")
    inputTypes = ["Vector3", "Bool"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def Country(value: int | countryNames):
    """Country dropdown. Pass index (wraps) or country label."""
    return AddNode("Country", value)


@cache
def CrossProduct(node0: Node, node1: Node):
    baseNode = AddNode("CrossProduct")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


debugCounter = 0


def Debug(inputData, string: str = None, changePosition=True):
    global debugCounter

    if changePosition:
        # magic numbers for position gotten via
        # snappedX = (20 + x) * 64 - 17
        # snappedY = -(4 + y) * 64 - 22
        xPos = 1263 - 64 * 6
        yPos = -278 - 64 * 4 * debugCounter
        baseNode = AddNode("Debug", position=Position3(xPos, yPos - 55))
        if string is not None:
            AddNode(
                "String", string, includePorts=False, position=Position3(xPos, yPos)
            )

    else:
        baseNode = AddNode("Debug")
        if string is not None:
            AddNode("String", string, includePorts=False)

    debugCounter += 1

    if isinstance(inputData, tuple):
        inputNode = parseLiteral(inputData[0])
        num = inputData[1]
    else:
        inputNode = parseLiteral(inputData)
        num = inputNode.outputIndex

    ports = [
        port["id"]
        for port in inputNode.data["serializablePorts"]
        if port["polarity"] != 0
    ]
    portName = ports[num - 1]
    ConnectPorts((portName, "Any1"), inputNode, baseNode)
    data["serializableConnections"][-1]["line"]["startWidth"] = 0  # invisible line

    return baseNode


def DebugDrawLine(node0: Node, node1: Node, node2: Node, node3: colorNames):
    baseNode = AddNode("DebugDrawLine")
    inputTypes = ["Vector3", "Vector3", "Float", "Color"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2, node3])
    return baseNode


def DebugDrawDisc(node0: Node, node1: Node, node2: Node, node3: colorNames):
    baseNode = AddNode("DebugDrawDisc")
    inputTypes = ["Vector3", "Float", "Float", "Color"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2, node3])
    return baseNode


def TimePlot(
    node0: Node,
    node1: colorNames,
    node2: Node,
    node3: Node,
):
    """Adds a value to the time plot graph during a simulation (toggle with F1). Inputs: name, color, iconUrl, value."""
    baseNode = AddNode("TimePlot")
    inputTypes = ["String", "Color", "String", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2, node3])
    return baseNode


@cache
def Distance(node0: Node, node1: Node):
    baseNode = AddNode("Distance")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def DivideFloats(node0: Node, node1: Node):
    baseNode = AddNode("DivideFloats")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def DotProduct(node0: Node, node1: Node):
    baseNode = AddNode("DotProduct")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def Float(value: int | float | str):
    return AddNode("Float", str(value))


@cache
def GetVariable(name: str):
    """Outputs the value from the corresponding SetVariable node with the same variable name."""
    return AddNode("GetVariable", name)


@cache
def IsNull(node0: Node):
    """Checks if the input is a null value."""
    baseNode = AddNode("IsNull")
    inputTypes = ["Any"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def Keypress(value: int | str):
    """Whether the selected key is pressed. Pass dropdown index (int, wraps) or KeyCode name (str)."""
    return AddNode("Keypress", value)


@cache
def VolleyballGetBool(
    value: int
    | Literal["Self Can Jump", "Opponent Can Jump", "Ball Is Self Side"],
):
    """Volleyball bool accessor. Maps to the `VolleyballGetBool` Unity node
    (see `Assets/_Nodes/VolleyballGetBool.asset`). Only valid inside a
    Volleyball graph — other sims use `SurvivalGetBool` / `ParkingGetBool` /
    `DemoDerbyGetBool`."""
    return AddNode("VolleyballGetBool", value)


@cache
def VolleyballGetFloat(
    value: int
    | Literal[
        "Delta time",
        "Fixed delta time",
        "Gravity",
        "Pi",
        "Simulation duration",
        "Team score",
        "Opponent score",
        "Ball touches remaining",
    ],
):
    """Volleyball float accessor. Maps to the `VolleyballGetFloat` Unity
    node (see `Assets/_Nodes/VolleyballGetFloat.asset`). Only valid inside a
    Volleyball graph — other sims use `SurvivalGetFloat` /
    `ParkingGetFloat` / `DemoDerbyGetFloat`."""
    return AddNode("VolleyballGetFloat", value)


@cache
def VolleyballGetTransform(
    value: int
    | Literal[
        "Self", "Opponent", "Ball", "Self Team Spawn", "Opponent Team Spawn"
    ],
):
    """Volleyball transform accessor. Maps to the `VolleyballGetTransform`
    Unity node (see `Assets/_Nodes/VolleyballGetTransform.asset`). Only valid
    inside a Volleyball graph — other sims use `SurvivalGetTransform` /
    `ParkingGetTransform` / `DemoDerbyGetTransform`."""
    return AddNode("VolleyballGetTransform", value)


@cache
def VolleyballGetVector3(
    value: int
    | Literal[
        "Self Position",
        "Self Velocity",
        "Ball Position",
        "Ball Velocity",
        "Opponent Position",
        "Opponent Velocity",
    ],
):
    """Volleyball Vector3 accessor. Emits the Unity node type
    ``SlimeGetVector3`` (see `Assets/_Nodes/SlimeGetVector3.asset` — the
    on-disk / serialization name is historical). Only valid inside a Volleyball
    graph — other sims expose Vector3s via
    `RelativePosition(transform_node, "Self")` on sim-specific transform
    helpers (`SurvivalGetTransform`, `DemoDerbyGetTransform`,
    `CarGetPart(...).PartTransform`, etc.)."""
    return AddNode("SlimeGetVector3", value)


# ---------------------------------------------------------------------------
# Deprecated Volleyball / generic aliases.
# The generic names `GetBool` / `GetFloat` / `GetTransform` / `GetVector3` were
# originally Volleyball-specific but the unprefixed names led people to
# assume they worked across simulations (they don't — each sim has its own
# `Survival*` / `Parking*` / `DemoDerby*` helpers wired to its own Unity asset).
# `SlimeGetVector3` was renamed to `VolleyballGetVector3` so the public API
# does not mix "Slime" and "Volleyball" naming. Old scripts still work; new code
# should use the explicit Volleyball* names.
# ---------------------------------------------------------------------------
GetBool = VolleyballGetBool
GetFloat = VolleyballGetFloat
GetTransform = VolleyballGetTransform
GetVector3 = VolleyballGetVector3
SlimeGetVector3 = VolleyballGetVector3


@cache
def Magnitude(node0: Node):
    baseNode = AddNode("Magnitude")
    inputTypes = ["Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def Modulo(node0: Node, node1: Node):
    baseNode = AddNode("Modulo")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def Power(base: Node, exponent: Node):
    """Raises `base` to `exponent` (Unity `Power` / Mathf.Pow)."""
    baseNode = AddNode("Power")
    connectInputNodes(baseNode, ["Float", "Float"], [base, exponent])
    return baseNode


@cache
def Lerp(a: Node, b: Node, t: Node):
    """Linearly interpolates between `a` and `b` by `t` (Unity `Lerp` / Mathf.Lerp)."""
    baseNode = AddNode("Lerp")
    connectInputNodes(baseNode, ["Float", "Float", "Float"], [a, b, t])
    return baseNode


@cache
def MultiplyFloats(node0: Node, node1: Node):
    baseNode = AddNode("MultiplyFloats")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def Not(node0: Node):
    baseNode = AddNode("Not")
    inputTypes = ["Bool"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def Normalize(node0: Node):
    baseNode = AddNode("Normalize")
    inputTypes = ["Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def Operation(
    node0: Node,
    value: int
    | Literal[
        "abs",
        "round",
        "floor",
        "ceil",
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "sqrt",
        "sign",
        "ln",
        "log10",
        "e^",
        "10^",
    ],
):
    baseNode = AddNode("Operation", value)
    inputTypes = ["Float"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def RelativePosition(
    node0: Node,
    value: int
    | Literal[
        "Self",
        "Self + Forward",
        "Self + Backward",
        "Self + Left",
        "Self + Right",
        "Self + Up",
        "Self + Down",
        "Forward",
        "Backward",
        "Left",
        "Right",
        "Up",
        "Down",
        "World",
    ],
):
    baseNode = AddNode("RelativePosition", value)
    inputTypes = ["Transform"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


def RandomFloat(node0: Node, node1: Node):
    baseNode = AddNode("RandomFloat")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


def Region():
    """Groups nodes visually for organization. Does not affect logic."""
    return AddNode("Region", includePorts=True)


@cache
def Relay(node0: Node):
    """Passes through data from input to output. Useful for organizing connections."""
    baseNode = AddNode("Relay")
    inputTypes = ["Any"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def ScaleVector3(node0: Node, node1: Node):
    baseNode = AddNode("ScaleVector3")
    inputTypes = ["Vector3", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


class Vector3Components:
    def __init__(self, x: Node, y: Node, z: Node):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, index):
        return [self.x, self.y, self.z][index]


@cache
def Vector3Split(node0: Node):
    baseNode = AddNode("Vector3Split")
    inputTypes = ["Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return Vector3Components(baseNode, Node(baseNode.data, 2), Node(baseNode.data, 3))


@cache
def SetVariable(name: str, value: Node):
    """Saves the input value so that it can be used by GetVariable nodes with the same variable name."""
    baseNode = AddNode("SetVariable", name)
    inputTypes = ["Any"]
    connectInputNodes(baseNode, inputTypes, [value])
    return baseNode


@cache
def Stat(value: int | str):
    return AddNode("Stat", str(value))


@cache
def String(value: str):
    return AddNode("String", value)


@cache
def SubtractFloats(node0: Node, node1: Node):
    baseNode = AddNode("SubtractFloats")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def SubtractVector3(node0: Node, node1: Node):
    baseNode = AddNode("SubtractVector3")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def SurvivalAutoPosition(node0: Node):
    """Automatically decide where to move an Aialander based on predetermined rules for a given state."""
    baseNode = AddNode("SurvivalAutoPosition")
    inputTypes = ["SurvivalState"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def SurvivalController(node0: Node, node1: Node, node2: Node, node3: Node):
    """Controls an Aialander's brain. Inputs: targetPosition, state, sprint, emote. Use SurvivalEmote(0) for no emote."""
    baseNode = AddNode("SurvivalController")
    inputTypes = ["Vector3", "SurvivalState", "Bool", "SurvivalEmote"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2, node3])
    return baseNode


@cache
def SurvivalEmote(value: int | str):
    """Emote dropdown. Pass index (wraps) or label: None, Hi, Talk, Bored, Wave, Dance2."""
    return AddNode("SurvivalEmote", value)


@cache
def SurvivalGetBool(value: int | str):
    """Selection of bool options. Pass index or label (see README / DROPDOWN_OPTIONS)."""
    return AddNode("SurvivalGetBool", value)


@cache
def SurvivalGetFloat(value: int | str):
    """Selection of float options (Health %, Hunger %, Stamina %, etc.). Pass index or label."""
    return AddNode("SurvivalGetFloat", value)


@cache
def SurvivalGetTransform(value: int | str):
    """Selection of Transform options (Self, Player Nearest, etc.). Pass index or label."""
    return AddNode("SurvivalGetTransform", value)


@cache
def SurvivalState(value: int | str):
    """State dropdown. Pass index (wraps) or name: Passive, Gather, Eat, Attack, Steal, Dead."""
    return AddNode("SurvivalState", value)


class RaycastHitComponents:
    """Multi-output helper for `CarRaycasts` (RaycastHit1..RaycastHit8)."""

    def __init__(self, baseNode: Node):
        self._baseNode = baseNode

    @property
    def RaycastHit1(self) -> Node:
        return Node(self._baseNode.data, 1)

    @property
    def RaycastHit2(self) -> Node:
        return Node(self._baseNode.data, 2)

    @property
    def RaycastHit3(self) -> Node:
        return Node(self._baseNode.data, 3)

    @property
    def RaycastHit4(self) -> Node:
        return Node(self._baseNode.data, 4)

    @property
    def RaycastHit5(self) -> Node:
        return Node(self._baseNode.data, 5)

    @property
    def RaycastHit6(self) -> Node:
        return Node(self._baseNode.data, 6)

    @property
    def RaycastHit7(self) -> Node:
        return Node(self._baseNode.data, 7)

    @property
    def RaycastHit8(self) -> Node:
        return Node(self._baseNode.data, 8)

    def __iter__(self):
        """Allow tuple unpacking: ray1, ..., ray8 = CarRaycasts(sensor)."""
        yield self.RaycastHit1
        yield self.RaycastHit2
        yield self.RaycastHit3
        yield self.RaycastHit4
        yield self.RaycastHit5
        yield self.RaycastHit6
        yield self.RaycastHit7
        yield self.RaycastHit8

    def __len__(self):
        return 8

    def __getitem__(self, index):
        return [
            self.RaycastHit1,
            self.RaycastHit2,
            self.RaycastHit3,
            self.RaycastHit4,
            self.RaycastHit5,
            self.RaycastHit6,
            self.RaycastHit7,
            self.RaycastHit8,
        ][index]


class HitInfoComponents:
    """Multi-output helper for `HitInfo` (WasHit, Distance, Tag)."""

    def __init__(self, baseNode: Node):
        # We override `type` so Python operators work (==, <, arithmetic, etc.).
        # Port ids are typed (Bool1 / Float1 / String1), so each uses outputIndex 1.
        self._wasHit = Node(baseNode.data, 1)
        self._wasHit.type = bool

        self._distance = Node(baseNode.data, 1)
        self._distance.type = float

        self._tag = Node(baseNode.data, 1)
        self._tag.type = str

    @property
    def WasHit(self) -> Node:
        return self._wasHit

    @property
    def Distance(self) -> Node:
        return self._distance

    @property
    def Tag(self) -> Node:
        """Hit collider GameObject tag (`String1`); null/empty when no hit."""
        return self._tag

    def __iter__(self):
        """Allow tuple unpacking: was_hit, distance = HitInfo(raycast_hit). Use `.Tag` for the string."""
        yield self.WasHit
        yield self.Distance

    def __len__(self):
        return 2

    def __getitem__(self, index):
        return [self.WasHit, self.Distance][index]


class GetCarPartComponents:
    """Multi-output helper for `GetCarPart` (`Transform1` world location, `Float1` health 0–100 %)."""

    def __init__(self, baseNode: Node):
        self._baseNode = baseNode

    @property
    def PartTransform(self) -> Node:
        return Node(self._baseNode.data, 1)

    @property
    def HealthPercent(self) -> Node:
        return Node(self._baseNode.data, 2)

    def __iter__(self):
        yield self.PartTransform
        yield self.HealthPercent

    def __len__(self):
        return 2

    def __getitem__(self, index):
        return [self.PartTransform, self.HealthPercent][index]


class CarInfoComponents:
    """Multi-output helper for `CarInfo`. Exposes every port on the Unity
    `ModularCarInfoGate` / `CarInfo` node in the order they are declared on
    the `CarInfo` NodeTypeDataSO asset.

    Outputs:
      - `CarTransform` (Transform1): the input car's transform.
      - `Velocity` (Vector31): world-space linear velocity of the car.
      - `IsAI` (Bool1): true if the car was authored by AI (LLM or ML-Agent).
      - `IsImmobile` (Bool2): true if derby mobility tracking has flagged the car as immobile.
      - `Health` (Float1): summed current health across all non-detached damageable parts.
      - `Rank` (Float2): 1-based derby rank (1 = best), 0 when unknown.
    """

    def __init__(self, baseNode: Node):
        self._baseNode = baseNode

    @property
    def CarTransform(self) -> Node:
        return Node(self._baseNode.data, 1)

    @property
    def Velocity(self) -> Node:
        return Node(self._baseNode.data, 2)

    @property
    def IsAI(self) -> Node:
        return Node(self._baseNode.data, 3)

    @property
    def IsImmobile(self) -> Node:
        return Node(self._baseNode.data, 4)

    @property
    def Health(self) -> Node:
        return Node(self._baseNode.data, 5)

    @property
    def Rank(self) -> Node:
        return Node(self._baseNode.data, 6)

    def __iter__(self):
        """Allow tuple unpacking in declared asset order (Transform, Velocity, IsAI, IsImmobile, Health, Rank)."""
        yield self.CarTransform
        yield self.Velocity
        yield self.IsAI
        yield self.IsImmobile
        yield self.Health
        yield self.Rank

    def __len__(self):
        return 6

    def __getitem__(self, index):
        return [
            self.CarTransform,
            self.Velocity,
            self.IsAI,
            self.IsImmobile,
            self.Health,
            self.Rank,
        ][index]


@cache
def ModularUniformController(throttle: Node, steering: Node, brake: Node):
    """Destination node: sends throttle/steering/brake to the modular car (Parking, Demo Derby, and RacingV2)."""
    baseNode = AddNode("ModularCarController")
    inputTypes = ["Float", "Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [throttle, steering, brake])
    return baseNode


@cache
def ConstructModularUniformProperties(
    name: str,
    country: countryNames,
    skinColor: colorNames,
    bodyStyle: int | float,
    hairStyle: int | float,
    hairColor: colorNames,
    facialHairStyle: int | float,
    carColor: colorNames,
    outfitUrl: str,
):
    """Destination node: sets cosmetic options for the modular car (Parking and Demo Derby). RacingV2 uses `ConstructRacingV2Properties` (cosmetics + stats)."""
    baseNode = AddNode("UniformModularCarProperties")
    inputTypes = ["String", "Country", "Color", "Float", "Float", "Color", "Float", "Color", "String"]
    connectInputNodes(
        baseNode,
        inputTypes,
        [name, country, skinColor, bodyStyle, hairStyle, hairColor, facialHairStyle, carColor, outfitUrl],
    )
    return baseNode


@cache
def Spherecast(radius: Node, distance: Node):
    """Defines the Spherecast radius/distance used for `CarRaycasts` / soccer player sensors (Parking, Demo Derby, RacingV2, Soccer)."""
    baseNode = AddNode("Spherecast")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [radius, distance])
    return baseNode


@cache
def CarRaycasts(spherecast: Node) -> RaycastHitComponents:
    """Sends sensors out around the modular car and returns `RaycastHit1..8` (Parking, Demo Derby, and RacingV2)."""
    baseNode = AddNode("CarRaycasts")
    inputTypes = ["Spherecast"]
    connectInputNodes(baseNode, inputTypes, [spherecast])
    return RaycastHitComponents(baseNode)


@cache
def HitInfo(raycastHit: Node) -> HitInfoComponents:
    """Extracts bool+distance from a selected `RaycastHit` output."""
    baseNode = AddNode("HitInfo")
    inputTypes = ["RaycastHit"]
    connectInputNodes(baseNode, inputTypes, [raycastHit])
    return HitInfoComponents(baseNode)


@cache
def DemoDerbyGetTransform(value: int | str):
    """Demo Derby: `0` Self, `1` Fixed Reference, `2` Random Pathable Waypoint (index or label)."""
    return AddNode("DemoDerbyGetTransform", value)


@cache
def DemoDerbyGetCar(mode: int | str, index_float: Node | None = None):
    """Demo Derby: outputs a car reference by dropdown `mode` (`0`..`26` or label).

    Pass `index_float` when `mode` is `0` (by index, wrapped to vehicle count)
    or `1` (by rank, wrapped to ranked-vehicle count; ranking = DamageDealt desc,
    then HealthNormalized desc). `index_float` is ignored for all other modes.

    Mode reference (mirrors `DemoDerbyGetCarGate.cs`):
        0  By index (uses `index_float`)
        1  By rank (uses `index_float`)
        2  Self
        3  Nearest car
        4  Furthest car
        5  Lowest health car
        6  Highest health car
        7  Last damaged car
        8  Nearest active car
        9  Furthest active car
        10 Nearest disabled car
        11 Furthest disabled car
        12 Nearest car with disabled steering (rear may still drive)
        13 Furthest car with disabled steering (rear may still drive)
        14 Nearest AI-Authored (active)
        15 Lowest health AI-Authored (active)
        16 Highest health AI-Authored (active)
        17 Nearest Human-Authored (active)
        18 Lowest health Human-Authored (active)
        19 Highest health Human-Authored (active)
        20 Highest ranked car
        21 Lowest ranked car
        22 Nearest ranked car (rank neighbor of self)
        23 Highest ranked (not immobilized)
        24 Highest ranked (immobilized)
        25 Lowest ranked (not immobilized)
        26 Lowest ranked (immobilized)
    """
    baseNode = AddNode("DemoDerbyGetCar", mode)
    if index_float is not None:
        connectInputNodes(baseNode, ["Float"], [index_float])
    return baseNode


@cache
def CarGetPart(mode: int | str, car: Node) -> GetCarPartComponents:
    """Part world transform and health percent for a car; `mode` is dropdown index or label."""
    baseNode = AddNode("GetCarPart", mode)
    connectInputNodes(baseNode, ["Car"], [car])
    return GetCarPartComponents(baseNode)


@cache
def CarInfo(car: Node) -> CarInfoComponents:
    """Multi-output info about a car. Access `.CarTransform` (Transform), `.Velocity`
    (Vector3 world velocity), `.IsAI` (Bool — LLM / ML-Agent authored), `.IsImmobile`
    (Bool — derby mobility tracker flagged), `.Health` (Float — summed damageable part
    health), and `.Rank` (Float — 1-based derby rank, 0 when unknown)."""
    baseNode = AddNode("CarInfo")
    connectInputNodes(baseNode, ["Car"], [car])
    return CarInfoComponents(baseNode)


@cache
def Autosteer(goal: Node):
    """Steering float toward a world target (`Vector3`)."""
    baseNode = AddNode("Autosteer")
    connectInputNodes(baseNode, ["Vector3"], [goal])
    return Node(baseNode.data, 1)


@cache
def Autothrottle(goal: Node, desired_speed: Node):
    """Throttle float toward `goal` at `desired_speed` (obstacle-aware in Unity)."""
    baseNode = AddNode("Autothrottle")
    connectInputNodes(baseNode, ["Vector3", "Float"], [goal, desired_speed])
    return Node(baseNode.data, 1)


@cache
def GetCarFromTransform(transform: Node):
    """Resolves a car controller from an input Transform (Unity searches on the transform and parents)."""
    baseNode = AddNode("GetCarFromTransform")
    connectInputNodes(baseNode, ["Transform"], [transform])
    return baseNode


@cache
def ParkingGetTransform(value: int | str):
    """Selection of Transform options for the parking simulation. Pass index or label."""
    return AddNode("ParkingGetTransform", value)


@cache
def ParkingGetFloat(value: int | str):
    """Selection of Float options for the parking simulation. Pass index or label."""
    return AddNode("ParkingGetFloat", value)


@cache
def ParkingGetBool(value: int | str):
    """Selection of Bool options for the parking simulation. Pass index or label."""
    return AddNode("ParkingGetBool", value)


# ---------------------------------------------------------------------------
# Custom Functions (Unity CreateFunction / Function)
# ---------------------------------------------------------------------------

class CreateFunctionComponents:
    """Param outputs (Any1–Any4) for a `CreateFunction` definition. Use `.node` for AssignToFunction / Return wiring."""

    def __init__(self, baseNode: Node):
        self._baseNode = baseNode
        self.node = baseNode

    @property
    def Param1(self) -> Node:
        return Node(self._baseNode.data, 1)

    @property
    def Param2(self) -> Node:
        return Node(self._baseNode.data, 2)

    @property
    def Param3(self) -> Node:
        return Node(self._baseNode.data, 3)

    @property
    def Param4(self) -> Node:
        return Node(self._baseNode.data, 4)

    def __iter__(self):
        yield self.Param1
        yield self.Param2
        yield self.Param3
        yield self.Param4

    def __len__(self):
        return 4


@cache
def CreateFunction(name: str = "") -> CreateFunctionComponents:
    """Defines a named custom function body (Unity key `CreateFunction`).

    Typical pattern:
        fn = CreateFunction("PowerFn")
        powered = AssignToFunction(Power(fn.Param1, fn.Param2), fn)
        SetFunctionReturn(fn, powered)  # REQUIRED to expose Power.Float1 as the call result
        result = CustomFunction("PowerFn", Float(2), Float(3))
    """
    baseNode = AddNode("CreateFunction", name)
    return CreateFunctionComponents(baseNode)


def AssignToFunction(body_node: Node, create_function: Node | CreateFunctionComponents):
    """Marks `body_node` as belonging to a CreateFunction body (`ownerFunctionSID`).

    Every node used inside the function (e.g. `Power`) must be assigned, or Unity will
    solve it globally instead of only when the function is called.
    """
    create = create_function.node if isinstance(create_function, CreateFunctionComponents) else create_function
    body_node.data["ownerFunctionSID"] = create.data["sID"]
    return body_node


def SetFunctionReturn(
    create_function: Node | CreateFunctionComponents,
    body_output: Node,
    output_port: str | None = None,
):
    """Wire a body node's output to the CreateFunction **Return** input.

    This is what makes `CustomFunction(...)` yield a value. Without it, calls still run
    the body but the call-site output is null.

    Port mapping (critical for LLMs):
      - CreateFunction Return input: id ``Any1``, polarity **In** (0)
        (GameObject name is "Any - In"; same id as Param1 but Param1 is Out)
      - Typical body outs: ``Float1`` (Power, Lerp, AddFloats, …), ``Vector31``, ``Bool1``, …

    Example — Power.Float1 → function Return:
        powered = AssignToFunction(Power(fn.Param1, fn.Param2), fn)
        SetFunctionReturn(fn, powered)                 # connects Float1 → Any1 (In)
        # equivalent: SetFunctionReturn(fn, powered, "Float1")
    """
    create = create_function.node if isinstance(create_function, CreateFunctionComponents) else create_function
    src = parseLiteral(body_output)
    if output_port is None:
        out_ports = [pt["id"] for pt in src.data["serializablePorts"] if pt["polarity"] != 0]
        out_idx = (body_output.outputIndex if isinstance(body_output, Node) else 1) - 1
        output_port = out_ports[out_idx]
    # Return port id is Any1 with polarity In (see Prefabs/Ports/In/Any - In.prefab).
    ConnectPorts((output_port, "Any1"), src, create)
    return create


@cache
def CustomFunction(
    name: str,
    param1: Node | None = None,
    param2: Node | None = None,
    param3: Node | None = None,
    param4: Node | None = None,
):
    """Call site for a CreateFunction by `name` (Unity key `Function`).

    Passes up to 4 parameters into the definition's Param1–4. The returned Node is the
    definition's **Return** value — only non-null if you called `SetFunctionReturn(...)`
    when building the CreateFunction body.
    """
    baseNode = AddNode("Function", name)
    for i, p in enumerate((param1, param2, param3, param4)):
        if p is None:
            continue
        src = parseLiteral(p)
        out_ports = [pt["id"] for pt in src.data["serializablePorts"] if pt["polarity"] != 0]
        out_idx = (p.outputIndex if isinstance(p, Node) else 1) - 1
        out_id = out_ports[out_idx]
        ConnectPorts((out_id, f"Any{i + 1}"), src, baseNode)
    return Node(baseNode.data, 1)


# ---------------------------------------------------------------------------
# Soccer simulation
# ---------------------------------------------------------------------------

@cache
def SoccerController(player: int, move_to: Node, sprint: Node, interact: Node):
    """Controls soccer team player `player` (1–4). `interact` is Bool2: hold to charge
    shot / tackle; release while charged (with ball) shoots along that frame's move input."""
    if player not in (1, 2, 3, 4):
        raise ValueError(f"SoccerController player must be 1..4, got {player}")
    baseNode = AddNode(f"SoccerController{player}")
    connectInputNodes(baseNode, ["Vector3", "Bool", "Bool"], [move_to, sprint, interact])
    return baseNode


@cache
def SoccerPlayerSensors(player: int, spherecast: Node) -> RaycastHitComponents:
    """Eight-way spherecasts around team player `player` (1–4). Hits map to letters A–H
    on the Player Sensor node graphic (RaycastHit1=A … RaycastHit8=H)."""
    if player not in (1, 2, 3, 4):
        raise ValueError(f"SoccerPlayerSensors player must be 1..4, got {player}")
    baseNode = AddNode(f"SoccerPlayerSensors{player}")
    connectInputNodes(baseNode, ["Spherecast"], [spherecast])
    return RaycastHitComponents(baseNode)


@cache
def ConstructSoccerProperties(
    name: str | Node,
    country: countryNames | Node,
    faceoff1: Node,
    faceoff2: Node,
    faceoff3: Node,
    faceoff4: Node,
):
    """Sets team name, country, and faceoff positions for players 1–4."""
    baseNode = AddNode("ConstructSoccerProperties")
    connectInputNodes(
        baseNode,
        ["String", "Country", "Vector3", "Vector3", "Vector3", "Vector3"],
        [name, country, faceoff1, faceoff2, faceoff3, faceoff4],
    )
    return baseNode


def InitializeSoccer(
    name: str,
    country: countryNames,
    faceoff1: Node,
    faceoff2: Node,
    faceoff3: Node,
    faceoff4: Node,
):
    """Convenience wrapper around `ConstructSoccerProperties`."""
    return ConstructSoccerProperties(
        String(name),
        Country(country),
        faceoff1,
        faceoff2,
        faceoff3,
        faceoff4,
    )


@cache
def SoccerGetBool(value: int | str):
    """Soccer bool accessor. Pass dropdown index or label (see README / DROPDOWN_OPTIONS)."""
    return AddNode("SoccerGetBool", value)


@cache
def SoccerGetFloat(value: int | str):
    """Soccer float accessor. Pass dropdown index or label (see README / DROPDOWN_OPTIONS)."""
    return AddNode("SoccerGetFloat", value)


@cache
def SoccerGetTransform(value: int | str):
    """Soccer transform accessor. Pass dropdown index or label (see README / DROPDOWN_OPTIONS)."""
    return AddNode("SoccerGetTransform", value)


@cache
def SoccerGetVector3(value: int | str):
    """Soccer Vector3 accessor (clear directions, landmarks, open players, etc.).
    Pass dropdown index or label (see README / DROPDOWN_OPTIONS)."""
    return AddNode("SoccerGetVector3", value)


# ---------------------------------------------------------------------------
# RacingV2 simulation
# ---------------------------------------------------------------------------

@cache
def ConstructRacingV2Properties(
    name: str | Node,
    country: countryNames | Node,
    skinColor: colorNames | Node,
    bodyStyle: int | float | Node,
    hairStyle: int | float | Node,
    hairColor: colorNames | Node,
    facialHairStyle: int | float | Node,
    carColor: colorNames | Node,
    outfitUrl: str | Node,
    speed_stat: Node,
    turn_stat: Node,
    health_stat: Node,
):
    """RacingV2 cosmetics + 20-point Stat budget (Stat1 speed, Stat2 turn, Stat3 health)."""
    baseNode = AddNode("ConstructRacingV2Properties")
    connectInputNodes(
        baseNode,
        ["String", "Country", "Color", "Float", "Float", "Color", "Float", "Color", "String", "Stat", "Stat", "Stat"],
        [
            name,
            country,
            skinColor,
            bodyStyle,
            hairStyle,
            hairColor,
            facialHairStyle,
            carColor,
            outfitUrl,
            speed_stat,
            turn_stat,
            health_stat,
        ],
    )
    return baseNode


def InitializeRacingV2(
    name: str,
    country: countryNames,
    skin_color: colorNames,
    body_style: int | float,
    hair_style: int | float,
    hair_color: colorNames,
    facial_hair_style: int | float,
    car_color: colorNames,
    custom_texture: str,
    speed: int | str = 5,
    turn: int | str = 5,
    health: int | str = 5,
):
    """Convenience initializer for RacingV2 (cosmetics + Stat points). Returns the properties node."""
    return ConstructRacingV2Properties(
        String(name),
        Country(country),
        Color(skin_color),
        Float(body_style),
        Float(hair_style),
        Color(hair_color),
        Float(facial_hair_style),
        Color(car_color),
        String(custom_texture),
        Stat(speed),
        Stat(turn),
        Stat(health),
    )


@cache
def RacingV2GetFloat(value: int | str):
    """RacingV2 float accessor. Pass dropdown index or label."""
    return AddNode("RacingV2GetFloat", value)


@cache
def RacingV2GetBool(value: int | str):
    """RacingV2 bool accessor. Pass dropdown index or label."""
    return AddNode("RacingV2GetBool", value)


@cache
def RacingV2GetCar(mode: int | str, index_float: Node | None = None):
    """RacingV2 car selector (modes 0–26, same shape as DemoDerbyGetCar). Pass `index_float` for by-index / by-rank."""
    baseNode = AddNode("RacingV2GetCar", mode)
    if index_float is not None:
        connectInputNodes(baseNode, ["Float"], [index_float])
    return baseNode


@cache
def RacingV2GetWaypoint(value: int | str, index_float: Node | None = None):
    """RacingV2 waypoint selector: Next / Previous / By index / Start. Pass `index_float` for By index."""
    baseNode = AddNode("RacingV2GetWaypoint", value)
    if index_float is not None:
        connectInputNodes(baseNode, ["Float"], [index_float])
    return baseNode


class RacingV2WaypointComponents:
    """Vector3 + index outputs from `RacingV2Waypoint`."""

    def __init__(self, baseNode: Node):
        self._baseNode = baseNode

    @property
    def Position(self) -> Node:
        return Node(self._baseNode.data, 1)

    @property
    def Index(self) -> Node:
        return Node(self._baseNode.data, 2)

    def __iter__(self):
        yield self.Position
        yield self.Index

    def __len__(self):
        return 2


@cache
def RacingV2Waypoint(
    mode: int | str,
    waypoint: Node | None = None,
    reference_transform: Node | None = None,
) -> RacingV2WaypointComponents:
    """Resolves a waypoint to Center / Left / Right / Nearest point. Returns `.Position` and `.Index`."""
    baseNode = AddNode("RacingV2Waypoint", mode)
    if waypoint is not None:
        connectInputNodes(baseNode, ["Waypoint"], [waypoint])
    if reference_transform is not None:
        connectInputNodes(baseNode, ["Transform"], [reference_transform])
    return RacingV2WaypointComponents(baseNode)


def connectInputNodes(baseNode, inputTypes, inputs):
    counters = {}

    for inputType, inputData in zip(inputTypes, inputs):
        num1 = 1

        if isinstance(inputData, Node):
            num1 = inputData.outputIndex

        if isinstance(inputData, tuple):
            inputNode = inputData[0]
            num1 = inputData[1]
        else:
            inputNode = inputData

        inputNode = parseLiteral(inputNode)

        if inputType not in counters:
            counters[inputType] = 1
        num2 = counters[inputType]
        counters[inputType] += 1

        if inputType == "Any":
            # Get actual output port from input node (Float1, Vector31, Bool1, etc.)
            outputPorts = [
                p["id"]
                for p in inputNode.data["serializablePorts"]
                if p["polarity"] != 0
            ]
            portName1 = outputPorts[num1 - 1]
            portName2 = "Any1"
        else:
            portName1 = f"{inputType}{num1}"
            portName2 = f"{inputType}{num2}"
            if isinstance(inputType, tuple):
                portName1 = f"{inputType[0]}{num1}"
                portName2 = f"{inputType[1]}{num2}"
            # CreateFunction / Relay / GetVariable expose Any* outs that feed typed inputs.
            if portName1 not in inputNode.outputPorts:
                outputPorts = [
                    p["id"]
                    for p in inputNode.data["serializablePorts"]
                    if p["polarity"] != 0
                ]
                if 0 <= num1 - 1 < len(outputPorts):
                    portName1 = outputPorts[num1 - 1]

        if inputData is not None:
            ConnectPorts((portName1, portName2), inputNode, baseNode)
