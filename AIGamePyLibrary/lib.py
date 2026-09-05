import inspect
import json
import math
import numbers
import os
import random
import re
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
    DROPDOWN_MODIFIER_AS_LABEL,
    DROPDOWN_ALIASES,
)
from .utils import Position2, Position3, generateId

data = {"serializableNodes": [], "serializableConnections": []}

# Visual Region frames: members are node sIDs created inside `with Region("…")`
# or inferred from `# region` comments in the user script.
_region_stack = []
_region_records = []
_node_source_lines = {}
_REGION_PAD_X = 28
_REGION_PAD_BOTTOM = 28
_REGION_HEADER = 40
_REGION_COLORS = (
    {"r": 0.35, "g": 0.62, "b": 0.95, "a": 1},
    {"r": 0.40, "g": 0.78, "b": 0.55, "a": 1},
    {"r": 0.95, "g": 0.72, "b": 0.28, "a": 1},
    {"r": 0.93, "g": 0.40, "b": 0.55, "a": 1},
    {"r": 0.55, "g": 0.45, "b": 0.90, "a": 1},
    {"r": 0.30, "g": 0.80, "b": 0.85, "a": 1},
)
_COMMENT_REGION_END = re.compile(r"^\s*#\s*end\s*-?\s*region\b", re.I)
_COMMENT_REGION_START = re.compile(r"^\s*#\s*region(?:\s*:|\s+)\s*(.+?)\s*$", re.I)
_COMMENT_REGION_BANNER = re.compile(r"^\s*#\s*-{3,}\s+(.+?)\s+-{3,}\s*$")


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

    - `int` (not `bool`) → dropdown index, wrapped with ``% len(options)``.
    - `str` → label lookup only (casefold); never parsed as an index.
    - Most nodes emit a stringified index; label-storage nodes
      (`DROPDOWN_MODIFIER_AS_LABEL`) emit the option text Unity matches on.
    """
    options = DROPDOWN_OPTIONS.get(node_name)
    if not options:
        return node_value

    if isinstance(node_value, bool):
        # Avoid treating bool as int.
        return node_value

    n = len(options)
    idx = None

    if isinstance(node_value, int):
        idx = node_value % n
    elif isinstance(node_value, str):
        value_str = node_value.strip()
        alias = DROPDOWN_ALIASES.get(node_name, {}).get(value_str.casefold())
        if alias:
            value_str = alias
        lowered = value_str.casefold()
        for i, opt in enumerate(options):
            if opt.casefold() == lowered:
                idx = i
                break
        if idx is None:
            raise ValueError(
                f"{node_name} invalid selection: {node_value!r}. "
                f"Valid selections: {', '.join(options)}"
            )
    else:
        return node_value

    if node_name in DROPDOWN_MODIFIER_AS_LABEL:
        return options[idx]
    return str(idx)


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
    _record_node_source(nodeId)
    _attach_to_open_regions(nodeId)

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


def _user_caller():
    """First stack frame outside this package (the bot script)."""
    pkg = os.path.dirname(os.path.abspath(__file__))
    frame = inspect.currentframe()
    while frame:
        path = os.path.abspath(frame.f_code.co_filename)
        if not path.startswith(pkg) and path.endswith(".py"):
            return path, frame.f_lineno
        frame = frame.f_back
    return None, None


def _record_node_source(node_sid):
    path, lineno = _user_caller()
    if path and lineno:
        _node_source_lines[node_sid] = (path, lineno)


def _attach_to_open_regions(node_sid):
    for rec in _region_stack:
        rec["members"].add(node_sid)


def _region_label(label):
    text = str(label or "").strip()
    if text.startswith("//"):
        text = text[2:].strip()
    if not text:
        text = "Region"
    return "//" + text


def _region_color(color, index=0):
    if isinstance(color, dict) and "r" in color:
        return {
            "r": float(color.get("r", 0.35)),
            "g": float(color.get("g", 0.62)),
            "b": float(color.get("b", 0.95)),
            "a": float(color.get("a", 1)),
        }
    return _REGION_COLORS[index % len(_REGION_COLORS)]


def begin_region(label="", color=None):
    """Start a labeled visual Region; nodes created until end_region() are members."""
    node = AddNode("Region", _region_label(label), includePorts=True)
    rec = {"sid": node.data["sID"], "members": set()}
    node.data["serializableDefaultColor"] = _region_color(color, len(_region_records))
    _region_records.append(rec)
    _region_stack.append(rec)
    return node


def end_region():
    if _region_stack:
        _region_stack.pop()


def _parse_comment_regions(source_path):
    try:
        with open(source_path, encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return []
    blocks = []
    current = None
    for i, line in enumerate(lines, start=1):
        if _COMMENT_REGION_END.match(line):
            if current:
                current["end"] = i
                blocks.append(current)
                current = None
            continue
        start = _COMMENT_REGION_START.match(line) or _COMMENT_REGION_BANNER.match(line)
        if start:
            if current:
                current["end"] = i - 1
                blocks.append(current)
            current = {"label": start.group(1).strip(), "start": i, "end": len(lines)}
    if current:
        blocks.append(current)
    return [b for b in blocks if b["label"] and b["end"] > b["start"]]


def _apply_comment_regions():
    """Turn `# region Title` / `# --- Title ---` comments into Unity Region frames."""
    if not _node_source_lines:
        return
    already = set()
    for rec in _region_records:
        already.update(rec["members"])
        already.add(rec["sid"])

    by_path = {}
    for sid, (path, lineno) in _node_source_lines.items():
        by_path.setdefault(path, []).append((sid, lineno))

    for path, entries in by_path.items():
        for block in _parse_comment_regions(path):
            members = [
                sid
                for sid, lineno in entries
                if block["start"] < lineno < block["end"] and sid not in already
            ]
            if not members:
                continue
            begin_region(block["label"])
            rec = _region_records[-1]
            rec["members"].update(members)
            already.update(members)
            already.add(rec["sid"])
            end_region()


def _fit_region_frames():
    """Size each Region box around the nodes created inside it (after layout)."""
    registry = {node["sID"]: node for node in data["serializableNodes"]}
    for rec in reversed(_region_records):
        region = registry.get(rec["sid"])
        if not region or region.get("id") != "Region":
            continue
        boxes = []
        for sid in rec["members"]:
            node = registry.get(sid)
            if not node or sid == rec["sid"]:
                continue
            transform = node.get("serializableRectTransform")
            if not transform:
                continue
            x, y = _get_layout_position(transform)
            if node.get("id") == "Region":
                size = transform.get("sizeDelta") or {}
                w = size.get("x", _node_size(node)[0])
                h = size.get("y", _node_size(node)[1])
            else:
                w, h = _node_size(node)
            boxes.append((x, y, w, h))
        transform = region["serializableRectTransform"]
        if not boxes:
            if _is_at_origin(transform):
                _set_layout_position(transform, _LAYOUT_ORIGIN_X - 80, _LAYOUT_ORIGIN_Y + 80)
            continue
        min_x = min(x for x, y, w, h in boxes) - _REGION_PAD_X
        max_x = max(x + w for x, y, w, h in boxes) + _REGION_PAD_X
        max_y = max(y for x, y, w, h in boxes) + _REGION_HEADER
        min_y = min(y - h for x, y, w, h in boxes) - _REGION_PAD_BOTTOM
        _set_layout_position(transform, min_x, max_y)
        transform["localPosition"] = Position3(min_x, max_y, 0)
        transform["anchorMin"] = {"x": 0, "y": 1}
        transform["anchorMax"] = {"x": 0, "y": 1}
        transform["sizeDelta"] = {"x": max(160.0, max_x - min_x), "y": max(96.0, max_y - min_y)}


_LAYOUT_ORIGIN_X = 1263
_LAYOUT_ORIGIN_Y = -278
_LAYOUT_ROOT_IDS = frozenset(
    {
        "CreateFunction",
        "Float",
        "String",
        "Bool",
        "Color",
        "Country",
        "GetVariable",
        "Region",
    }
)


def _node_size(node):
    return NODE_SIZES.get(node.get("id", ""), DEFAULT_NODE_SIZE)


def _wired_pairs():
    pairs = []
    for conn in data["serializableConnections"]:
        source = findNodeByPortSID(conn["port0SID"])
        dest = findNodeByPortSID(conn["port1SID"])
        if source and dest and source["sID"] != dest["sID"]:
            pairs.append((source, dest))
    return pairs


def _graph_maps(nodes):
    sids = [node["sID"] for node in nodes]
    sid_set = set(sids)
    registry = {node["sID"]: node for node in nodes}
    succ = {sid: [] for sid in sids}
    pred = {sid: [] for sid in sids}
    for source, dest in _wired_pairs():
        src, dst = source["sID"], dest["sID"]
        if src in sid_set and dst in sid_set:
            succ[src].append(dst)
            pred[dst].append(src)
    return registry, succ, pred


def _feedback_edges(sids, succ, start_order=None):
    """DFS back-edges so cyclic graphs (CreateFunction ↔ body) still layer."""
    white, gray, black = 0, 1, 2
    color = {sid: white for sid in sids}
    back = set()

    def dfs(u):
        color[u] = gray
        for v in succ[u]:
            if v not in color:
                continue
            if color[v] == gray:
                back.add((u, v))
            elif color[v] == white:
                dfs(v)
        color[u] = black

    for sid in start_order or sids:
        if color.get(sid) == white:
            dfs(sid)
    return back


def _assign_levels(registry, succ, pred):
    sids = list(registry)
    start_order = sorted(
        sids,
        key=lambda sid: 0 if registry[sid].get("id") in _LAYOUT_ROOT_IDS else 1,
    )
    back = _feedback_edges(sids, succ, start_order)
    dag_succ = {sid: [v for v in succ[sid] if (sid, v) not in back] for sid in sids}
    dag_pred = {sid: [u for u in pred[sid] if (u, sid) not in back] for sid in sids}

    in_degree = {sid: len(dag_pred[sid]) for sid in sids}
    queue = deque(sid for sid in sids if in_degree[sid] == 0)
    if not queue:
        roots = [sid for sid in sids if registry[sid].get("id") in _LAYOUT_ROOT_IDS]
        queue.extend(roots or sids[:1])
        for sid in list(queue):
            in_degree[sid] = 0

    levels = {}
    while queue:
        u = queue.popleft()
        if u in levels:
            continue
        pred_lv = [levels[p] for p in dag_pred[u] if p in levels]
        levels[u] = max(pred_lv) + 1 if pred_lv else 0
        for v in dag_succ[u]:
            in_degree[v] -= 1
            if in_degree[v] <= 0 and v not in levels:
                queue.append(v)

    remaining = [sid for sid in sids if sid not in levels]
    remaining.sort(key=lambda sid: 0 if registry[sid].get("id") in _LAYOUT_ROOT_IDS else 1)
    while remaining:
        progressed = False
        still = []
        for sid in remaining:
            pred_lv = [levels[p] for p in pred[sid] if p in levels]
            if pred_lv:
                levels[sid] = max(pred_lv) + 1
                progressed = True
            else:
                still.append(sid)
        if not progressed:
            nxt = (max(levels.values()) + 1) if levels else 0
            for sid in still:
                levels[sid] = nxt
            break
        remaining = still
    return levels


def _barycenter_order(columns, succ, pred, passes=4):
    if len(columns) < 2:
        return columns
    for i in range(passes):
        if i % 2 == 0:
            for c in range(1, len(columns)):
                index_of = {sid: n for n, sid in enumerate(columns[c - 1])}

                def key(sid, index_of=index_of, pred=pred):
                    vals = [index_of[p] for p in pred[sid] if p in index_of]
                    return (sum(vals) / len(vals) if vals else len(index_of), sid)

                columns[c].sort(key=key)
        else:
            for c in range(len(columns) - 2, -1, -1):
                index_of = {sid: n for n, sid in enumerate(columns[c + 1])}

                def key(sid, index_of=index_of, succ=succ):
                    vals = [index_of[v] for v in succ[sid] if v in index_of]
                    return (sum(vals) / len(vals) if vals else len(index_of), sid)

                columns[c].sort(key=key)
    return columns


def _place_columns(columns, registry, gap_x, gap_y, origin_x, origin_y, force=False):
    """Place layered columns using real node sizes. Y grows downward (negative)."""
    current_x = origin_x
    for sids in columns:
        widths = [_node_size(registry[sid])[0] for sid in sids]
        heights = [_node_size(registry[sid])[1] for sid in sids]
        col_width = max(widths, default=DEFAULT_NODE_SIZE[0])
        total_h = sum(heights) + gap_y * max(0, len(sids) - 1)
        current_y = origin_y + total_h / 2.0
        for sid, height in zip(sids, heights):
            node = registry[sid]
            transform = node["serializableRectTransform"]
            if force or _is_at_origin(transform):
                _set_layout_position(transform, current_x, current_y)
            current_y -= height + gap_y
        current_x += col_width + gap_x


def _hierarchical_layout(nodes, origin_x, origin_y, gap_x, gap_y, force=False):
    if not nodes:
        return
    registry, succ, pred = _graph_maps(nodes)
    levels = _assign_levels(registry, succ, pred)
    by_level = {}
    for sid, level in levels.items():
        by_level.setdefault(level, []).append(sid)
    columns = [by_level[level] for level in sorted(by_level)]
    _barycenter_order(columns, succ, pred)
    _place_columns(columns, registry, gap_x, gap_y, origin_x, origin_y, force=force)


def _layout_node_groups():
    main = []
    owned = {}
    for node in data["serializableNodes"]:
        if node.get("id") == "Region":
            continue
        owner = node.get("ownerFunctionSID")
        if owner:
            owned.setdefault(owner, []).append(node)
        else:
            main.append(node)
    return main, owned


def _apply_hierarchical_layout(gap_x=96, gap_y=40):
    """Size-aware Sugiyama layout. Function bodies sit to the right of the main graph."""
    main, owned = _layout_node_groups()
    _hierarchical_layout(main, _LAYOUT_ORIGIN_X, _LAYOUT_ORIGIN_Y, gap_x, gap_y)

    body_x = _LAYOUT_ORIGIN_X
    for node in main:
        x, _ = _get_layout_position(node["serializableRectTransform"])
        w, _ = _node_size(node)
        body_x = max(body_x, x + w)
    body_x += gap_x

    registry = {node["sID"]: node for node in data["serializableNodes"]}
    for owner_sid, body in owned.items():
        owner = registry.get(owner_sid)
        if owner:
            _, origin_y = _get_layout_position(owner["serializableRectTransform"])
        else:
            origin_y = _LAYOUT_ORIGIN_Y
        _hierarchical_layout(body, body_x, origin_y, gap_x, gap_y)
        for node in body:
            x, _ = _get_layout_position(node["serializableRectTransform"])
            w, _ = _node_size(node)
            body_x = max(body_x, x + w + gap_x)

    _repack_region_clusters(gap_x, gap_y)


def _innermost_region_ids():
    inner = {}
    for rec in _region_records:
        for sid in rec["members"]:
            inner[sid] = rec["sid"]
    return inner


def _repack_region_clusters(gap_x, gap_y):
    """Keep data-flow placement, then pack each Region's nodes into a tight block."""
    inner = _innermost_region_ids()
    if not inner:
        return
    clusters = {}
    for node in data["serializableNodes"]:
        if node.get("id") == "Region":
            continue
        rid = inner.get(node["sID"])
        if rid:
            clusters.setdefault(rid, []).append(node)
    for nodes in clusters.values():
        if len(nodes) < 2:
            continue
        xs, ys = [], []
        for node in nodes:
            x, y = _get_layout_position(node["serializableRectTransform"])
            xs.append(x)
            ys.append(y)
        _hierarchical_layout(
            nodes, min(xs), sum(ys) / len(ys), gap_x, gap_y, force=True
        )


def _neighbor_sets():
    neighbors = {}
    for source, dest in _wired_pairs():
        src, dst = source["sID"], dest["sID"]
        neighbors.setdefault(src, set()).add(dst)
        neighbors.setdefault(dst, set()).add(src)
    return neighbors


def _tighten_layout_to_neighbors(
    iterations=3, blend=0.4, max_step=280.0, movable_sids=None
):
    """Pull nodes toward wired neighbors (titaniummachine1 spatial visualizer)."""
    neighbors = _neighbor_sets()
    for _ in range(iterations):
        positions = {}
        movable = []
        for node in data["serializableNodes"]:
            transform = node.get("serializableRectTransform")
            if not transform:
                continue
            positions[node["sID"]] = _get_layout_position(transform)
            if node.get("id") == "Region":
                continue
            if movable_sids is None or node["sID"] in movable_sids:
                movable.append(node)
        if len(positions) < 2:
            return
        updated = dict(positions)
        for node in movable:
            sid = node["sID"]
            nbrs = [positions[n] for n in neighbors.get(sid, ()) if n in positions]
            if not nbrs:
                continue
            cx = sum(p[0] for p in nbrs) / len(nbrs)
            cy = sum(p[1] for p in nbrs) / len(nbrs)
            ox, oy = positions[sid]
            nx = ox + blend * (cx - ox)
            ny = oy + blend * (cy - oy)
            dx, dy = nx - ox, ny - oy
            step = math.hypot(dx, dy)
            if step > max_step:
                scale = max_step / step
                nx = ox + dx * scale
                ny = oy + dy * scale
            updated[sid] = (nx, ny)
        for node in movable:
            x, y = updated[node["sID"]]
            _set_layout_position(node["serializableRectTransform"], x, y)


def _resolve_overlaps(padding=16, passes=20, movable_sids=None):
    """Separate overlapping nodes after neighbor tightening."""
    items = []
    for node in data["serializableNodes"]:
        transform = node.get("serializableRectTransform")
        if not transform:
            continue
        if node.get("id") == "Region":
            continue
        if movable_sids is not None and node["sID"] not in movable_sids:
            continue
        w, h = _node_size(node)
        items.append((node, w, h))
    if len(items) < 2:
        return
    for _ in range(passes):
        moved = False
        for i in range(len(items)):
            node_a, wa, ha = items[i]
            ax, ay = _get_layout_position(node_a["serializableRectTransform"])
            for j in range(i + 1, len(items)):
                node_b, wb, hb = items[j]
                bx, by = _get_layout_position(node_b["serializableRectTransform"])
                overlap_x = min(ax + wa, bx + wb) - max(ax, bx) + padding
                overlap_y = min(ay, by) - max(ay - ha, by - hb) + padding
                if overlap_x <= 0 or overlap_y <= 0:
                    continue
                if overlap_x < overlap_y:
                    if bx >= ax:
                        bx = ax + wa + padding
                    else:
                        ax = bx + wb + padding
                else:
                    if ay >= by:
                        by = ay - ha - padding
                    else:
                        ay = by - hb - padding
                _set_layout_position(node_a["serializableRectTransform"], ax, ay)
                _set_layout_position(node_b["serializableRectTransform"], bx, by)
                moved = True
        if not moved:
            break


def gridLayout(offsetX=350, offsetY=-215):
    x = _LAYOUT_ORIGIN_X
    y = _LAYOUT_ORIGIN_Y
    nodesPerRow = max(1, int(math.sqrt(len(data["serializableNodes"]))))

    for i, node in enumerate(data["serializableNodes"]):
        if node.get("id") == "Region":
            continue
        transform = node["serializableRectTransform"]
        if not _is_at_origin(transform):
            continue
        _set_layout_position(transform, x, y)
        x += offsetX
        if (i + 1) % nodesPerRow == 0:
            x = _LAYOUT_ORIGIN_X
            y += offsetY


def autoLayout(offsetX=350, offsetY=-215):
    """Default visualizer: size-aware hierarchical layout with crossing reduction."""
    movable = {
        node["sID"]
        for node in data["serializableNodes"]
        if _is_at_origin(node["serializableRectTransform"])
    }
    gap_x = max(48, offsetX - DEFAULT_NODE_SIZE[0])
    gap_y = max(24, abs(offsetY) - DEFAULT_NODE_SIZE[1])
    _apply_hierarchical_layout(gap_x=gap_x, gap_y=gap_y)
    _resolve_overlaps(movable_sids=movable)


def terminatorLayout(offsetX=280, offsetY=-140):
    """Compact neighbor-tightened layout (titaniummachine1 spatial visualizer)."""
    movable = {
        node["sID"]
        for node in data["serializableNodes"]
        if _is_at_origin(node["serializableRectTransform"])
    }
    gap_x = max(28, offsetX - DEFAULT_NODE_SIZE[0])
    gap_y = max(12, abs(offsetY) - DEFAULT_NODE_SIZE[1])
    _apply_hierarchical_layout(gap_x=gap_x, gap_y=gap_y)
    _tighten_layout_to_neighbors(
        iterations=3, blend=0.32, max_step=220.0, movable_sids=movable
    )
    _resolve_overlaps(movable_sids=movable)


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


def SaveData(
    filePath,
    layout: Literal["auto", "terminator", "grid", "single", None] = "auto",
    pruneUnusedNodes=True,
    keepPosition=True,
):
    _apply_comment_regions()

    if pruneUnusedNodes:
        removeUnusedNodes()

    match layout:
        case "auto":
            autoLayout()
        case "terminator":
            terminatorLayout()
        case "grid":
            gridLayout()
        case "single":
            for node in data["serializableNodes"]:
                transform = node["serializableRectTransform"]
                if not _is_at_origin(transform) and keepPosition:
                    continue
                _set_layout_position(transform, 0, 0)

    _fit_region_frames()
    updateConnectionLinePoints()
    _prepare_for_unity_format()

    with open(filePath, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
