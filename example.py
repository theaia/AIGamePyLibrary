from AIGameLibrary import *

# 1 to 1 recreation of the default AIA bot

InitializeSlime("AIA", "Yellow", "United States of America", 5, 3, 2)

positionSign = RelativePosition(Self.TeamSpawn, "Backward")

moveTo = Ball.Position + positionSign * 0.4

distanceToBall = Distance(Ball.Position, Self.Position)
jumpCondition = distanceToBall < 2.25

SlimeController(moveTo, jumpCondition)

SaveData("SlimeVolleyball/AIComp_Data/Saves/AIA python.txt", "grid")
