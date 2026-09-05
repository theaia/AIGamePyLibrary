from AIGamePyLibrary import *

# 1 to 1 recreation of the default AIA bot

InitializeSlime("AIA", "Yellow", "United States of America", 5, 3, 2)

with Region("Read world state"):
    ball_position = VolleyballGetVector3("Ball Position")
    self_position = VolleyballGetVector3("Self Position")
    team_spawn = VolleyballGetTransform("Self Team Spawn")

with Region("Move under the ball"):
    positionSign = RelativePosition(team_spawn, "Backward")
    moveTo = ball_position + positionSign * 0.4

with Region("Jump when the ball is close"):
    distanceToBall = Distance(ball_position, self_position)
    jumpCondition = distanceToBall < 2.25

SlimeController(moveTo, jumpCondition)

SaveData("AIA.txt")
