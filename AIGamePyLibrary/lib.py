import json
import math
import numbers
import random
from collections import deque
from typing import Literal

from .data import (
    outputs,
    ports,
    NODE_SIZES,
    DEFAULT_NODE_SIZE,
    DEFAULT_NODE_COLOR,
    DEFAULT_CONNECTION_COLOR,
    CAP_COLOR,
    SERIALIZE_SIZE_DELTA_NODES,
    SERIALIZE_COLOR_NODES,
    DROPDOWN_OPTIONS,
)

from .utils import Position2, Position3, generateId

data = {"serializableNodes": [], "serializableConnections": []}


def isNumber(value):
    return isinstance(value, numbers.Number) and not isinstance(value, bool)


class Node:
    def __init__(self, data: dict, outputIndex=1):
        self.data = data
        self.outputIndex = outputIndex
        self.type = outputs[data["id"]]
        self.inputPorts = {}
        self.outputPorts = {}
        for port in data["serializablePorts"]:
            if port["polarity"] == 0:
                self.inputPorts[port["id"]] = port
            else:
                self.outputPorts[port["id"]] = port

    @property
    def x(self):
        if self.type == "Vector3":
            from .nodes import Vector3Split

            return Vector3Split(self).x
        raise AttributeError("'Node' object has no attribute 'x'")

    @property
    def y(self):
        if self.type == "Vector3":
            from .nodes import Vector3Split

            return Vector3Split(self).y
        raise AttributeError("'Node' object has no attribute 'y'")

    @property
    def z(self):
        if self.type == "Vector3":
            from .nodes import Vector3Split

            return Vector3Split(self).z
        raise AttributeError("'Node' object has no attribute 'z'")

    def __repr__(self):
        return f"Node(type='{self.type}', id='{self.data['sID']}')"

    def __hash__(self):
        return int(self.data["sID"].replace("-", ""), 16) + self.outputIndex

    def __add__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import AddFloats

                return AddFloats(self, other)
            if self.type == "Vector3" and other.type == "Vector3":
                from .nodes import AddVector3

                return AddVector3(self, other)

        elif isNumber(other) and self.type == float:
            from .nodes import AddFloats

            return AddFloats(self, other)

        return NotImplemented

    def __radd__(self, other) -> "Node":
        return self.__add__(other)

    def __sub__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import SubtractFloats

                return SubtractFloats(self, other)
            if self.type == "Vector3" and other.type == "Vector3":
                from .nodes import SubtractVector3

                return SubtractVector3(self, other)

        elif isNumber(other) and self.type == float:
            from .nodes import SubtractFloats

            return SubtractFloats(self, other)

        return NotImplemented

    def __rsub__(self, other) -> "Node":
        if isNumber(other) and self.type == float:
            from .nodes import SubtractFloats

            return SubtractFloats(other, self)

        return NotImplemented

    def __mul__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import MultiplyFloats

                return MultiplyFloats(self, other)
            if self.type == "Vector3" and other.type == float:
                from .nodes import ScaleVector3

                return ScaleVector3(self, other)
            if self.type == float and other.type == "Vector3":
                from .nodes import ScaleVector3

                return ScaleVector3(other, self)

        elif isNumber(other):
            if self.type == float:
                from .nodes import MultiplyFloats

                return MultiplyFloats(self, other)
            if self.type == "Vector3":
                from .nodes import ScaleVector3

                return ScaleVector3(self, other)

        return NotImplemented

    def __rmul__(self, other) -> "Node":
        return self.__mul__(other)

    def __truediv__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import DivideFloats

                return DivideFloats(self, other)

        elif isNumber(other) and self.type == float:
            from .nodes import DivideFloats

            return DivideFloats(self, other)

        return NotImplemented

    def __rtruediv__(self, other) -> "Node":
        if isNumber(other) and self.type == float:
            from .nodes import DivideFloats

            return DivideFloats(other, self)

        return NotImplemented

    def __floordiv__(self, other) -> "Node":
        result = self.__truediv__(other)
        if result is NotImplemented:
            return result
        from .nodes import Operation

        return Operation(result, "floor")

    def __rfloordiv__(self, other) -> "Node":
        if isNumber(other) and self.type == float:
            from .nodes import DivideFloats

            div_result = DivideFloats(other, self)
            from .nodes import Operation

            return Operation(div_result, "floor")

        return NotImplemented

    def __mod__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import Modulo

                return Modulo(self, other)

        elif isNumber(other) and self.type == float:
            from .nodes import Modulo

            return Modulo(self, other)

        return NotImplemented

    def __rmod__(self, other) -> "Node":
        if isNumber(other) and self.type == float:
            from .nodes import Modulo

            return Modulo(other, self)

        return NotImplemented

    def __pow__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type in (float, "Any") and other.type in (float, "Any"):
                from .nodes import Power

                return Power(self, other)

        elif isNumber(other) and self.type in (float, "Any"):
            if other == 2 and self.type == float:
                from .nodes import MultiplyFloats

                return MultiplyFloats(self, self)

            from .nodes import Power

            return Power(self, other)

        return NotImplemented

    def __rpow__(self, other) -> "Node":
        if isNumber(other) and self.type in (float, "Any"):
            from .nodes import Power

            return Power(other, self)

        return NotImplemented

    def __neg__(self) -> "Node":
        if self.type == float:
            from .nodes import MultiplyFloats

            return MultiplyFloats(self, -1)

        return NotImplemented

    def __pos__(self) -> "Node":
        return self

    def __abs__(self) -> "Node":
        if self.type == float:
            from .nodes import Operation

            return Operation(self, "abs")

        return NotImplemented

    def __invert__(self) -> "Node":
        if self.type == bool:
            from .nodes import Not

            return Not(self)

        return NotImplemented

    def __eq__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import CompareFloats

                return CompareFloats(self, other)
            if self.type == bool and other.type == bool:
                from .nodes import CompareBool

                return CompareBool(self, other)

        elif isNumber(other) and self.type == float:
            from .nodes import CompareFloats

            return CompareFloats(self, other)

        elif isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(self, other)

        return NotImplemented

    def __ne__(self, other) -> "Node":
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        from .nodes import Not

        return Not(result)

    def __lt__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import CompareFloats

                return CompareFloats(self, other, "<")

        elif isNumber(other) and self.type == float:
            from .nodes import CompareFloats

            return CompareFloats(self, other, "<")

        return NotImplemented

    def __le__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import CompareFloats

                return CompareFloats(self, other, "<=")

        elif isNumber(other) and self.type == float:
            from .nodes import CompareFloats

            return CompareFloats(self, other, "<=")

        return NotImplemented

    def __gt__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import CompareFloats

                return CompareFloats(self, other, ">")

        elif isNumber(other) and self.type == float:
            from .nodes import CompareFloats

            return CompareFloats(self, other, ">")

        return NotImplemented

    def __ge__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import CompareFloats

                return CompareFloats(self, other, ">=")

        elif isNumber(other) and self.type == float:
            from .nodes import CompareFloats

            return CompareFloats(self, other, ">=")

        return NotImplemented

    def __and__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == bool and other.type == bool:
                from .nodes import CompareBool

                return CompareBool(self, other, "and")

        elif isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(self, other, "and")

        return NotImplemented

    def __rand__(self, other) -> "Node":
        if isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(other, self, "and")

        return NotImplemented

    def __or__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == bool and other.type == bool:
                from .nodes import CompareBool

                return CompareBool(self, other, "or")

        elif isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(self, other, "or")

        return NotImplemented

    def __ror__(self, other) -> "Node":
        if isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(other, self, "or")

        return NotImplemented

    def __xor__(self, other) -> "Node":
        if isinstance(other, Node):
            from .nodes import CompareBool

            if self.type == bool and other.type == bool:
                return CompareBool(self, other, "xor")

        elif isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(self, other, "xor")

        return NotImplemented

    def __rxor__(self, other) -> "Node":
        if isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(other, self, "xor")

        return NotImplemented

    def __matmul__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == "Vector3" and other.type == "Vector3":
                from .nodes import DotProduct

                return DotProduct(self, other)

        return NotImplemented

    def __rmatmul__(self, other) -> "Node":
        return self.__matmul__(other)


def _rect_transform(local_pos, size, node_id, anchor_x=0, anchor_y=1):
    """Build serializableRectTransform. New minimal format: only position+anchoredPosition for layout.
    Region nodes include sizeDelta/anchors (SerializeSizeDelta per NodeTypeDataSO)."""
    x, y, z = local_pos.get("x", 0), local_pos.get("y", 0), local_pos.get("z", 0)
    w, h = size
    rect = {
        "position": {"x": 0, "y": 0, "z": 0},
        "anchoredPosition": {"x": x, "y": y},
    }
    if node_id in SERIALIZE_SIZE_DELTA_NODES:
        rect["localPosition"] = local_pos
        rect["anchorMin"] = {"x": anchor_x, "y": anchor_y}
        rect["anchorMax"] = {"x": anchor_x, "y": anchor_y}
        rect["sizeDelta"] = {"x": w, "y": h}
    return rect


def _get_layout_position(transform):
    """Get (x, y) from transform. Prefers anchoredPosition, falls back to localPosition for old JSON."""
    ap = transform.get("anchoredPosition")
    if ap is not None:
        return (ap.get("x", 0), ap.get("y", 0))
    lp = transform.get("localPosition", {})
    return (lp.get("x", 0), lp.get("y", 0))


def _is_at_origin(transform):
    """True if node is at default (0,0) and should receive auto layout."""
    x, y = _get_layout_position(transform)
    return x == 0 and y == 0


def _set_layout_position(transform, x, y):
    """Set layout position. Uses anchoredPosition (Unity's preferred field for placement)."""
    transform["anchoredPosition"] = Position2(x, y)
    transform["localPosition"] = Position3(x, y, 0)
    transform["position"] = {"x": 0, "y": 0, "z": 0}


def _default_line():
    """Line structure matching Unity UIC4 Line class. Points filled by UpdateLine at runtime."""
    return {
        "capStart": {
            "active": False,
            "shape": 3,  # Shape.Type.Diamond
            "size": 5,
            "color": CAP_COLOR,
            "angleOffset": 0,
        },
        "capEnd": {
            "active": False,
            "shape": 3,
            "size": 5,
            "color": CAP_COLOR,
            "angleOffset": 0,
        },
        "ID": "line",  # Match Unity Line default
        "startWidth": 3,
        "endWidth": 3,
        "dashDistance": 5,
        "color": DEFAULT_CONNECTION_COLOR,
        "points": [],
        "lineStyle": 0,  # LineStyle.Type.Solid
        "length": 0,
        "animation": {
            "isActive": False,
            "pointsDistance": 35,  # Match Unity LineAnimation default
            "size": 10,
            "color": {"r": 1, "g": 0.81, "b": 0.3, "a": 1},
            "shape": 1,  # Shape.Type.Diamond
            "speed": 20,
        },
    }


def _normalize_modifier(node_name: str, node_value):
    """
    Normalize `modifier` for nodes whose modifier is a dropdown selection.

    - Accepts either an int index or a string label.
    - Validates against `DROPDOWN_OPTIONS` when available.
    - Converts to a stringified index, because Unity nodes store dropdown
      selections in the `modifier` field as a string.
    """
    options = DROPDOWN_OPTIONS.get(node_name)
    if not options:
        return node_value

    if isinstance(node_value, bool):
        # Avoid treating bool as int.
        return node_value

    if isinstance(node_value, int):
        if 0 <= node_value < len(options):
            return str(node_value)
        raise ValueError(
            f"{node_name} dropdown index out of range: {node_value}. "
            f"Valid range: 0..{len(options) - 1} ({', '.join(options)})"
        )

    if isinstance(node_value, str):
        value_str = node_value.strip()
        if value_str.isdigit():
            idx = int(value_str)
            if 0 <= idx < len(options):
                return str(idx)
            raise ValueError(
                f"{node_name} dropdown index out of range: {value_str}. "
                f"Valid range: 0..{len(options) - 1} ({', '.join(options)})"
            )

        lowered = value_str.casefold()
        for i, opt in enumerate(options):
            if opt.casefold() == lowered:
                return str(i)

        raise ValueError(
            f"{node_name} invalid selection: {node_value!r}. "
            f"Valid selections: {', '.join(options)}"
        )

    return node_value


def AddNode(nodeName, nodeValue="", includePorts=True, position=None, ownerFunctionSID=""):
    node = {}

    if position is None:
        position = Position3(0, 0)

    nodeId = generateId()
    size = NODE_SIZES.get(nodeName, DEFAULT_NODE_SIZE)

    node["serializableRectTransform"] = _rect_transform(position, size, nodeName)
    node["id"] = nodeName
    node["sID"] = nodeId
    node["modifier"] = _normalize_modifier(nodeName, nodeValue)
    if ownerFunctionSID:
        node["ownerFunctionSID"] = ownerFunctionSID
    if nodeName in SERIALIZE_COLOR_NODES:
        node["serializeColor"] = True
        node["serializeSizeDelta"] = True
        node["serializableDefaultColor"] = DEFAULT_NODE_COLOR
    elif nodeName in SERIALIZE_SIZE_DELTA_NODES:
        node["serializeSizeDelta"] = True
    node["serializablePorts"] = []
    if includePorts:
        for portData in ports[nodeName]:
            node["serializablePorts"].append(
                {
                    "id": portData["id"],
                    "sID": generateId(),
                    "polarity": portData["polarity"],
                    "nodeSID": nodeId,
                }
            )

    data["serializableNodes"].append(node)

    return Node(node)


def ConnectPorts(portType: tuple | str, node0: Node, node1: Node):
    if isinstance(portType, tuple):
        port0 = node0.outputPorts[portType[0]]
        port1 = node1.inputPorts[portType[1]]
    else:
        port0 = node0.outputPorts[portType]
        port1 = node1.inputPorts[portType]
    conn_id = generateId()
    connection = {
        "id": f"Connection ({node0.data['id']} - {node1.data['id']})",
        "sID": conn_id,
        "port0InstanceID": 0,
        "port1InstanceID": 0,
        "port0SID": port0["sID"],
        "port1SID": port1["sID"],
        "selectedColor": {"r": 1, "g": 0.58, "b": 0.04, "a": 1},
        "hoverColor": CAP_COLOR,
        "defaultColor": DEFAULT_CONNECTION_COLOR,
        "curveStyle": 2,  # Connection.CurveStyle.Soft_Z_Shape (Unity default)
        "label": "",
        "line": _default_line(),
        "enableDrag": True,
        "enableHover": True,
        "enableSelect": True,
        "disableClick": False,
    }
    data["serializableConnections"].append(connection)
    return connection


def findNodeByPortSID(portSID):
    for node in data["serializableNodes"]:
        for port in node["serializablePorts"]:
            if port["sID"] == portSID:
                return node
    return None


def gridLayout(offsetX=350, offsetY=-215):
    x = 1263
    y = -278
    nodesPerRow = max(1, int(math.sqrt(len(data["serializableNodes"]))))

    for i, node in enumerate(data["serializableNodes"]):
        transform = node["serializableRectTransform"]
        if not _is_at_origin(transform):
            continue
        _set_layout_position(transform, x, y)
        x += offsetX
        if (i + 1) % nodesPerRow == 0:
            x = 1263
            y += offsetY


def autoLayout(offsetX=350, offsetY=-215):
    adj = {}
    inDegree = {}

    for node in data["serializableNodes"]:
        adj[node["sID"]] = []
        inDegree[node["sID"]] = 0

    for conn in data["serializableConnections"]:
        sourceNode = findNodeByPortSID(conn["port0SID"])
        destNode = findNodeByPortSID(conn["port1SID"])

        if sourceNode and destNode and sourceNode["sID"] != destNode["sID"]:
            adj[sourceNode["sID"]].append(destNode["sID"])
            inDegree[destNode["sID"]] += 1

    queue = deque()
    for nodeSID, degree in inDegree.items():
        if degree == 0:
            queue.append(nodeSID)

    nodeRegistry = {node["sID"]: node for node in data["serializableNodes"]}

    nodeLevels = {nodeSID: 0 for nodeSID in nodeRegistry.keys()}
    visitedCount = 0

    while queue:
        u = queue.popleft()
        visitedCount += 1

        for v in adj[u]:
            nodeLevels[v] = max(nodeLevels[v], nodeLevels[u] + 1)
            inDegree[v] -= 1
            if inDegree[v] == 0:
                queue.append(v)

    if visitedCount < len(data["serializableNodes"]):
        gridLayout(offsetX, offsetY)
        return

    columns = {}
    for nodeSID, level in nodeLevels.items():
        if level not in columns:
            columns[level] = []
        columns[level].append(nodeRegistry[nodeSID])

    sortedColumns = sorted(columns.items())

    currentX = 1263
    for level, nodesInColumn in sortedColumns:
        totalHeight = (len(nodesInColumn) - 1) * offsetY
        currentY = -totalHeight / 2.0 - 278

        for node in nodesInColumn:
            transform = node["serializableRectTransform"]
            if not _is_at_origin(transform):
                continue
            _set_layout_position(transform, currentX, currentY)
            currentY += offsetY

        currentX += offsetX


def updateConnectionLinePoints():
    """No-op: minimal serialization format does not include connection line points."""
    pass


def _prepare_for_unity_format():
    """Ensure graph data matches new minimal format (NodeTypeDataSO).
    - Standard nodes: rect = position (0,0,0) + anchoredPosition only; no color/size (prefab provides)
    - Region: full rect + color (SerializeSizeDelta, SerializeColor)
    - Ports: id, sID, polarity, nodeSID only (position from prefab)
    """
    for node in data["serializableNodes"]:
        node_id = node.get("id", "")
        transform = node.get("serializableRectTransform", {})
        if transform:
            ap = transform.get("anchoredPosition")
            lp = transform.get("localPosition", {})
            if ap is None and lp:
                transform["anchoredPosition"] = {"x": lp.get("x", 0), "y": lp.get("y", 0)}
            transform["position"] = {"x": 0, "y": 0, "z": 0}
            if node_id not in SERIALIZE_SIZE_DELTA_NODES:
                for key in ("localPosition", "anchorMin", "anchorMax", "sizeDelta"):
                    transform.pop(key, None)
        if node_id not in SERIALIZE_COLOR_NODES:
            node.pop("defaultColor", None)
            node.pop("serializableDefaultColor", None)
        if node_id not in SERIALIZE_SIZE_DELTA_NODES:
            node.pop("serializeSizeDelta", None)
            node.pop("serializeColor", None)
        for port in node.get("serializablePorts", []):
            port.pop("serializableRectTransform", None)
            port.pop("controlPointSerializableRectTransform", None)


def removeUnreadVariables(verbose=False):
    """Delete SetVariable writes no GetVariable reads, and GetVariable reads
    whose output feeds nothing.

    `removeUnusedNodes` cannot do this: a SetVariable is a SINK, so it always
    looks used and its whole producing subgraph is kept alive with it. One
    real graph carried a 405-node service this way -- 29 of 31 variables were
    written and never read, and everything computing them came along.

    Runs to a fixpoint: dropping a write can orphan a read, and dropping a
    read can orphan a write. Bounded, since each round strictly removes nodes.

    A variable pair is a data edge with NO wire between the two nodes, so this
    is the one thing an optimiser can silently sever -- delete the write and
    the read still looks connected while reading nothing. Callers should check
    `assertVariablesIntact()` afterwards.
    """
    total_w = total_r = 0
    for _ in range(10):
        nodes = data["serializableNodes"]
        read = {n["modifier"] for n in nodes if n["id"] == "GetVariable"}
        doomed = {n["sID"] for n in nodes
                  if n["id"] == "SetVariable" and n["modifier"] not in read}
        wired = set()
        for c in data["serializableConnections"]:
            wired.add(c["port0SID"])
            wired.add(c["port1SID"])
        doomed |= {
            n["sID"] for n in nodes if n["id"] == "GetVariable"
            and not any(p["sID"] in wired for p in n.get("serializablePorts", []))
        }
        if not doomed:
            break
        dead_ports = {p["sID"] for n in nodes if n["sID"] in doomed
                      for p in n.get("serializablePorts", [])}
        data["serializableConnections"] = [
            c for c in data["serializableConnections"]
            if c["port0SID"] not in dead_ports and c["port1SID"] not in dead_ports
        ]
        data["serializableNodes"] = [n for n in nodes if n["sID"] not in doomed]
        total_w += len(doomed)
    if verbose and total_w:
        print(f"  removeUnreadVariables: dropped {total_w} unread variable node(s)")
    return total_w


def assertVariablesIntact():
    """Fail if any GetVariable lost the SetVariable that fed it.

    Variables link by NAME, not by wire, so no wire-based pruner can see the
    dependency. Severing one leaves a read that looks perfectly connected and
    silently returns nothing -- this turns that into a hard error instead.
    """
    nodes = data["serializableNodes"]
    written = {n["modifier"] for n in nodes if n["id"] == "SetVariable"}
    read = {n["modifier"] for n in nodes if n["id"] == "GetVariable"}
    orphaned = read - written
    if orphaned:
        raise RuntimeError(
            "GetVariable with no SetVariable feeding it: " + ", ".join(sorted(orphaned))
        )


def stripDebugSinks(verbose=False):
    """Delete Debug*/TimePlot sinks so the pruner can collect everything that
    existed only to feed them.

    Typically ~29% of a graph. Competition builds do not render debug output,
    and the save format costs ~2.4 KB per node. Safe only if drawing code
    never feeds a decision -- verify that, do not assume it.
    """
    nodes = data["serializableNodes"]
    sinks = {"DebugDrawLine", "DebugDrawDisc", "TimePlot", "Debug"}
    doomed = {n["sID"] for n in nodes if n["id"] in sinks}
    if not doomed:
        return 0
    dead_ports = {p["sID"] for n in nodes if n["sID"] in doomed
                  for p in n.get("serializablePorts", [])}
    data["serializableConnections"] = [
        c for c in data["serializableConnections"]
        if c["port0SID"] not in dead_ports and c["port1SID"] not in dead_ports
    ]
    data["serializableNodes"] = [n for n in nodes if n["sID"] not in doomed]
    if verbose:
        print(f"  stripDebugSinks: removed {len(doomed)} debug sink(s)")
    return len(doomed)


def removeUnusedNodes():
    portToNode = {}
    nodeToPorts = {}
    nodeIsString = {}

    for node in data["serializableNodes"]:
        node_sid = node["sID"]
        nodeIsString[node_sid] = node["id"] == "String"
        nodeToPorts[node_sid] = {"input": [], "output": []}

        for port in node["serializablePorts"]:
            portToNode[port["sID"]] = node_sid
            if port["polarity"] == 0:
                nodeToPorts[node_sid]["input"].append(port["sID"])
            else:
                nodeToPorts[node_sid]["output"].append(port["sID"])

    connectionGraph = {}
    portConnections = {}

    for node in data["serializableNodes"]:
        connectionGraph[node["sID"]] = {"inputs": set(), "outputs": set()}

    for connection in data["serializableConnections"]:
        sourceNode = portToNode.get(connection["port0SID"])
        destinationNode = portToNode.get(connection["port1SID"])

        if sourceNode and destinationNode and sourceNode != destinationNode:
            connectionGraph[sourceNode]["outputs"].add(destinationNode)
            connectionGraph[destinationNode]["inputs"].add(sourceNode)

            portConnections[connection["port0SID"]] = (
                portConnections.get(connection["port0SID"], 0) + 1
            )
            portConnections[connection["port1SID"]] = (
                portConnections.get(connection["port1SID"], 0) + 1
            )

    # nodesToRemove are the BFS starting points
    nodesToRemove = set()
    queue = deque()

    for node in data["serializableNodes"]:
        node_sid = node["sID"]

        if nodeIsString[node_sid]:
            continue

        hasInputPorts = len(nodeToPorts[node_sid]["input"]) > 0
        hasOutputPorts = len(nodeToPorts[node_sid]["output"]) > 0

        inputConnected = any(
            portConnections.get(pid, 0) > 0 for pid in nodeToPorts[node_sid]["input"]
        )

        outputConnected = any(
            portConnections.get(pid, 0) > 0 for pid in nodeToPorts[node_sid]["output"]
        )

        if (hasInputPorts and not inputConnected) or (
            hasOutputPorts and not outputConnected
        ):
            nodesToRemove.add(node_sid)
            queue.append(node_sid)

    # BFS to find all nodes that become disconnected
    while queue:
        currentNode = queue.popleft()

        for dependentNode in connectionGraph[currentNode]["outputs"]:
            if dependentNode in nodesToRemove or nodeIsString[dependentNode]:
                continue

            if all(
                src in nodesToRemove for src in connectionGraph[dependentNode]["inputs"]
            ):
                nodesToRemove.add(dependentNode)
                queue.append(dependentNode)

        for sourceNode in connectionGraph[currentNode]["inputs"]:
            if sourceNode in nodesToRemove or nodeIsString[sourceNode]:
                continue

            if all(
                dst in nodesToRemove for dst in connectionGraph[sourceNode]["outputs"]
            ):
                nodesToRemove.add(sourceNode)
                queue.append(sourceNode)

    activeConnections = []
    for connection in data["serializableConnections"]:
        sourceNode = portToNode.get(connection["port0SID"])
        destinationNode = portToNode.get(connection["port1SID"])

        if sourceNode not in nodesToRemove and destinationNode not in nodesToRemove:
            activeConnections.append(connection)
    data["serializableConnections"] = activeConnections

    activeNodes = []
    for node in data["serializableNodes"]:
        node_sid = node["sID"]
        if node_sid not in nodesToRemove or nodeIsString[node_sid]:
            activeNodes.append(node)
    data["serializableNodes"] = activeNodes


def _optimize_to_fixpoint(verbose=False, *, strip_debug=False, prune=True):
    """Interleave strip, variable prune and DCE until a full round is a no-op.

    One pass feeds the next: stripping a TimePlot can orphan the SetVariable
    that only fed it, dropping that write can orphan the subgraph behind it,
    and so on. A single pass of each leaves most of that on the table."""
    max_rounds = max(len(data["serializableNodes"]), 1)
    for round_idx in range(max_rounds):
        changed = 0
        if strip_debug:
            changed += stripDebugSinks(verbose and round_idx == 0)
        if prune:
            changed += removeUnreadVariables(verbose and round_idx == 0)
            before = len(data["serializableNodes"])
            removeUnusedNodes()
            changed += before - len(data["serializableNodes"])
            assertVariablesIntact()
        if changed == 0:
            break


def SaveData(
    filePath,
    layout: Literal["auto", "grid", "single", "hidden", None] = "auto",
    pruneUnusedNodes=True,
    keepPosition=True,
    optimize: Literal["normal", "release"] = "normal",
    verbose=False,
):
    """`optimize` selects how hard to compile the graph down:

      "normal"  (default) remove only what cannot be observed: unreachable
                nodes, and SetVariable writes that no GetVariable reads. Every
                Debug*/TimePlot sink is kept, so the graph stays observable.
      "release" additionally strips every Debug*/TimePlot sink, then re-prunes
                to a fixpoint, so anything that ONLY fed debug output goes
                with it. Smallest and fewest per-tick node evaluations.

    Every node evaluates every tick in-engine, so removing nodes removes real
    per-tick work, not just file size.

    The difference between the two is what they assume. "normal" assumes
    nothing: a node no output can reach, and a variable no one reads, cannot
    change a decision. "release" assumes debug output is not an input -- that
    no drawing or plotting code also feeds a controller. That holds for every
    graph I know of, but it is an assumption about YOUR graph, so verify it
    before shipping a release build.
    """
    if optimize == "release":
        _optimize_to_fixpoint(verbose, strip_debug=True, prune=pruneUnusedNodes)
    elif pruneUnusedNodes:
        removeUnreadVariables(verbose)
        removeUnusedNodes()
        assertVariablesIntact()

    match layout:
        case "auto":
            autoLayout()
        case "grid":
            gridLayout()
        case "single":
            for node in data["serializableNodes"]:
                transform = node["serializableRectTransform"]
                if not _is_at_origin(transform) and keepPosition:
                    continue
                _set_layout_position(transform, 0, 0)
        case "hidden":
            for node in data["serializableNodes"]:
                transform = node["serializableRectTransform"]
                if not _is_at_origin(transform) and keepPosition:
                    continue
                _set_layout_position(transform, 9999, 9999)
                transform["scale"] = Position3(0, 0)

    updateConnectionLinePoints()
    _prepare_for_unity_format()

    with open(filePath, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
