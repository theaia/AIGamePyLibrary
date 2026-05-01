from AIGamePyLibrary import *

# 1 to 1 recreation of the default AIA bot

InitializeSlime("AIA", "Yellow", "United States of America", 5, 3, 2)

# Pull world state from node helpers. Each helper is Volleyball-specific
# and matches its Unity node type in `Assets/_Nodes/` (Vector3 uses
# `SlimeGetVector3` in Unity; Python name is `VolleyballGetVector3`). Other
# sims have their own (`SurvivalGetTransform`, `DemoDerbyGetTransform`, ...).
ball_position = VolleyballGetVector3("Ball Position")
self_position = VolleyballGetVector3("Self Position")
team_spawn    = VolleyballGetTransform("Self Team Spawn")

positionSign = RelativePosition(team_spawn, "Backward")

moveTo = ball_position + positionSign * 0.4

distanceToBall = Distance(ball_position, self_position)
jumpCondition  = distanceToBall < 2.25

SlimeController(moveTo, jumpCondition)

SaveData("AIA.txt", "grid")
