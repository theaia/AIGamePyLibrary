"""
Simple Soccer team bot — 4 roles (Grok)

  Player 1 — Striker: shoot when on ball; otherwise get CLEAR of the carrier
  Player 2 — Striker: shoot when on ball; otherwise get FORWARD of the carrier
  Player 3 — Defender: win the ball, pass toward a striker
  Player 4 — Goalie: triangle cover; steal if ball within 1.5; rush if opponent
               carrier is closer (in X) to our goal; clear when they have it

Loose ball: whichever teammate is closest sprints to it (overrides role move).

Interact (Bool2): True only when the player has the ball or is near it.
With ball: hold to charge, release when charged (shoots along move-to).
Near without ball: True to tackle / pickup. Otherwise False.
"""

from AIGamePyLibrary import *

# Faceoff spots (team space: +X toward attack). Strikers high, defender mid, GK deep.
faceoff_p1 = Vector3(Float(10), Float(0), Float(4))   # striker
faceoff_p2 = Vector3(Float(10), Float(0), Float(-4))  # striker
faceoff_p3 = Vector3(Float(-4), Float(0), Float(0))   # defender
faceoff_p4 = Vector3(Float(-14), Float(0), Float(0))  # goalie

InitializeSoccer(
    "Grok",
    "Grok",
    faceoff_p1,
    faceoff_p2,
    faceoff_p3,
    faceoff_p4,
)

# Shared landmarks / reads
ball_pos = RelativePosition(SoccerGetTransform("Ball"), "Self")
opp_goal = RelativePosition(SoccerGetTransform("Opponent Goal Center"), "Self")
team_goal = RelativePosition(SoccerGetTransform("Team Goal Center"), "Self")
striker1_pos = RelativePosition(SoccerGetTransform("Team Player 1"), "Self")
striker2_pos = RelativePosition(SoccerGetTransform("Team Player 2"), "Self")
goalie_pos = RelativePosition(SoccerGetTransform("Team Player 4"), "Self")
upper_team_corner = SoccerGetVector3("Upper Corner Team Side")
lower_team_corner = SoccerGetVector3("Lower Corner Team Side")
team_has_ball = SoccerGetBool("Team Has Ball")
opponent_has_ball = SoccerGetBool("Opponent Has Ball")
ball_is_loose = SoccerGetBool("Is Ball Loose")

# Goalie cover spot: centroid of triangle (ball, upper team corner, lower team corner)
goalie_triangle = (ball_pos + upper_team_corner + lower_team_corner) * Float(1.0 / 3.0)

# Support spots relative to ball carrier (ball ≈ carrier while team has possession)
clear_dir = SoccerGetVector3("Clear direction from team carrier")
clear_of_carrier = ball_pos + Normalize(clear_dir) * Float(10)
clear_of_carrier = ConditionalSetVector3(IsNull(clear_dir), upper_team_corner, clear_of_carrier)

forward_of_carrier = ball_pos + Normalize(opp_goal - ball_pos) * Float(12)

# Goalie clear kick: move along a clear ray from GK so release sends the ball that way
gk_clear_dir = SoccerGetVector3("Clear direction from Teammate 4")
gk_clear_spot = goalie_pos + Normalize(gk_clear_dir) * Float(12)
gk_clear_spot = ConditionalSetVector3(IsNull(gk_clear_dir), striker2_pos, gk_clear_spot)


def player_interact(player: int, has_ball: Node, shot_charge: Node) -> Node:
    """Interact is True only when this player has the ball or is near it.
    With ball: hold to charge, release when charged. Near without ball: tackle/pickup.
    Otherwise False."""
    near_ball = SoccerGetBool(f"Is Ball Nearby Team Player {player}")
    allowed = CompareBool(has_ball, near_ball, "or")

    charged = CompareFloats(shot_charge, 0.55, ">")
    with_ball_interact = ConditionalSetBool(charged, Bool(False), Bool(True))
    # has ball → charge/release; near only → True (tackle)
    active = ConditionalSetBool(has_ball, with_ball_interact, Bool(True))
    return ConditionalSetBool(allowed, active, Bool(False))


def apply_loose_ball_override(player: int, role_move: Node, role_sprint: Node):
    """If the ball is loose and this player is the nearest teammate, sprint to it."""
    is_closest = SoccerGetBool(f"Is Team Player {player} Closest Teammate to Ball")
    chase = CompareBool(ball_is_loose, is_closest, "and")
    move = ConditionalSetVector3(chase, ball_pos, role_move)
    sprint = ConditionalSetBool(chase, Bool(True), role_sprint)
    return move, sprint


def striker_brain(player: int, support_move: Node):
    """On ball → attack net. Off ball while team has it → support run. Else chase ball."""
    has_ball = SoccerGetBool(f"Team Player {player} Has Ball")
    charge = SoccerGetFloat(f"Teammate {player} Shot Charge")
    supporting = CompareBool(team_has_ball, Not(has_ball), "and")

    off_ball = ConditionalSetVector3(supporting, support_move, ball_pos)
    role_move = ConditionalSetVector3(has_ball, opp_goal, off_ball)
    role_sprint = Bool(True)

    move_to, sprint = apply_loose_ball_override(player, role_move, role_sprint)
    interact = player_interact(player, has_ball, charge)
    SoccerController(player, move_to, sprint, interact)


def defender_brain(player: int = 3):
    """Win the ball, then pass toward a striker."""
    has_ball = SoccerGetBool(f"Team Player {player} Has Ball")
    charge = SoccerGetFloat(f"Teammate {player} Shot Charge")

    open_teammate = SoccerGetVector3("Get nearest open teammate")
    pass_target = ConditionalSetVector3(IsNull(open_teammate), striker1_pos, open_teammate)

    role_move = ConditionalSetVector3(has_ball, pass_target, ball_pos)
    role_sprint = Bool(True)

    move_to, sprint = apply_loose_ball_override(player, role_move, role_sprint)
    interact = player_interact(player, has_ball, charge)
    SoccerController(player, move_to, sprint, interact)


def goalie_brain(player: int = 4):
    """Triangle cover; steal if ball within 1.5; rush if opponent carrier is closer
    in X to our goal; with ball sprint to a clear spot and kick clear."""
    has_ball = SoccerGetBool(f"Team Player {player} Has Ball")
    charge = SoccerGetFloat(f"Teammate {player} Shot Charge")

    # --- Steal: ball within 1.5 and GK doesn't have it ---
    dist_to_ball = Distance(goalie_pos, ball_pos)
    ball_in_reach = CompareFloats(dist_to_ball, 1.5, "<=")
    want_steal = CompareBool(ball_in_reach, Not(has_ball), "and")

    # --- Rush: opponent has ball and is closer (in X) to our goal than the GK ---
    ball_goal_x = Abs(ball_pos.x - team_goal.x)
    goalie_goal_x = Abs(goalie_pos.x - team_goal.x)
    opp_closer_to_goal = CompareFloats(ball_goal_x, goalie_goal_x, "<")
    rush_tackle = CompareBool(opponent_has_ball, opp_closer_to_goal, "and")

    # Priority (high → low): has ball → clear kick; steal; rush tackle; triangle
    move = goalie_triangle
    move = ConditionalSetVector3(rush_tackle, ball_pos, move)
    move = ConditionalSetVector3(want_steal, ball_pos, move)
    # With ball: sprint into a clear position (release shoots along that move dir)
    move = ConditionalSetVector3(has_ball, gk_clear_spot, move)

    urgent = CompareBool(want_steal, rush_tackle, "or")
    sprint = ConditionalSetBool(has_ball, Bool(True), urgent)

    move_to, sprint = apply_loose_ball_override(player, move, sprint)
    interact = player_interact(player, has_ball, charge)
    SoccerController(player, move_to, sprint, interact)


# --- Assign roles -----------------------------------------------------------
striker_brain(1, clear_of_carrier)
striker_brain(2, forward_of_carrier)
defender_brain(3)
goalie_brain(4)

SaveData("Soccer/Grok_roles.txt", "grid")
print("Wrote Soccer/Grok_roles.txt")
