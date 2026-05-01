from AIGamePyLibrary import *

# 1 to 1 recreation of the AIA survival bot from the visual graph
# - Eat when hunger < 50%
# - Sprint when stamina > 50%
# - Default state: Gather
# - Auto-position based on state (Eat/Gather)

InitializeSurvival(
    name="AIA",
    country="United States of America",
    skin="White",
    body_style=0,
    hair_style=3,
    hair_color="Dark Brown",
    facial_hair=1,
    custom_texture="https://i.imgur.com/CvucGD8.png",
)

# Eat when below 50% hunger
hungerPct = SurvivalGetFloat(1)  # Hunger Percentage
hungerBelow50 = CompareFloats(hungerPct, Float(0.5), "<")
state = ConditionalSetSurvivalState(
    hungerBelow50,
    SurvivalState("Eat"),
    SurvivalState("Gather"),
)

# Auto-position based on state (goes to fruit/container for Eat, trees for Gather)
moveTo = SurvivalAutoPosition(state)

# Only run if stamina above 50%
staminaPct = SurvivalGetFloat(2)  # Stamina Percentage
sprint = CompareFloats(staminaPct, Float(0.5), ">")

# No emote
emote = SurvivalEmote(0)

SurvivalController(moveTo, state, sprint, emote)

SaveData(GetSurvivalSavePath("AIApy.txt"), "grid")
