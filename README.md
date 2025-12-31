# AIA Game Library

A Python library for creating AI bots for AIA's game collection. This library allows you to programmatically create node-based AI logic that can be exported and used in Unity games.

## Installation

This library requires Python 3.7+. Simply place the `AIGameLibrary` folder in your project directory and import it:

```python
from AIGameLibrary import *
```

## Quick Start

Here's a simple example for Slime Volleyball:

```python
from AIGameLibrary import *

# Initialize the slime with name, color, country, and stats (speed, acceleration, jump)
InitializeSlime("AIA", "Yellow", "United States of America", 5, 3, 2)

# Calculate a position offset from the team spawn
positionSign = RelativePosition(Self.TeamSpawn, "Backward")

# Calculate where to move (ball position + offset)
moveTo = Ball.Position + positionSign * 0.4

# Calculate distance to ball and jump condition
distanceToBall = Distance(Ball.Position, Self.Position)
jumpCondition = distanceToBall < 2.25

# Control the slime (target position, jump condition)
SlimeController(moveTo, jumpCondition)

# Save the AI data to a file
SaveData("SlimeVolleyball/AIComp_Data/Saves/AIA python.txt", "grid")
```

## Core Concepts

### Nodes

The library uses a node-based system where operations return `Node` objects. Nodes can be combined using Python operators:

- **Arithmetic**: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- **Comparison**: `<`, `<=`, `>`, `>=`, `==`, `!=`
- **Boolean**: `&` (and), `|` (or), `^` (xor), `~` (not)

Example:
```python
distance = Distance(Ball.Position, Self.Position)
shouldJump = distance < 2.5  # Returns a Node representing the comparison
```

### Vector Operations

Vector3 nodes support component access and operations:

```python
# Access vector components
ballPos = Ball.Position
x = ballPos.x  # X component
y = ballPos.y  # Y component
z = ballPos.z  # Z component

# Vector arithmetic
offset = Ball.Position - Self.Position
scaled = offset * 0.5
```

## Complete Node Reference

### General Nodes (Available in All Games)

<details>
<summary><strong>Basic Types</strong></summary>

- **`Float(value)`** - Creates a float constant node
  - Input: `value` (int, float, or str)
  - Output: Float

- **`Bool(value)`** - Creates a boolean constant node
  - Input: `value` (bool)
  - Output: Bool

- **`String(value)`** - Creates a string constant node
  - Input: `value` (str)
  - Output: String

</details>

<details>
<summary><strong>Arithmetic Operations</strong></summary>

- **`AddFloats(a, b)`** or `a + b` - Adds two float values
  - Inputs: Float, Float
  - Output: Float

- **`SubtractFloats(a, b)`** or `a - b` - Subtracts two float values
  - Inputs: Float, Float
  - Output: Float

- **`MultiplyFloats(a, b)`** or `a * b` - Multiplies two float values
  - Inputs: Float, Float
  - Output: Float

- **`DivideFloats(a, b)`** or `a / b` - Divides two float values
  - Inputs: Float, Float
  - Output: Float

- **`Modulo(a, b)`** or `a % b` - Modulo operation
  - Inputs: Float, Float
  - Output: Float

- **`Power(a, b)`** or `a ** b` - Raises a to the power of b
  - Inputs: Float, Float
  - Output: Float

</details>

<details>
<summary><strong>Vector Operations</strong></summary>

- **`AddVector3(a, b)`** or `a + b` - Adds two Vector3 values
  - Inputs: Vector3, Vector3
  - Output: Vector3

- **`SubtractVector3(a, b)`** or `a - b` - Subtracts two Vector3 values
  - Inputs: Vector3, Vector3
  - Output: Vector3

- **`ScaleVector3(vec, scalar)`** or `vec * scalar` - Scales a vector by a float
  - Inputs: Vector3, Float
  - Output: Vector3

- **`DotProduct(a, b)`** or `a @ b` - Dot product of two vectors
  - Inputs: Vector3, Vector3
  - Output: Float

- **`CrossProduct(a, b)`** - Cross product of two vectors
  - Inputs: Vector3, Vector3
  - Output: Vector3

- **`Magnitude(vec)`** - Magnitude (length) of a vector
  - Input: Vector3
  - Output: Float

- **`Normalize(vec)`** - Normalizes a vector to unit length
  - Input: Vector3
  - Output: Vector3

- **`Distance(pos1, pos2)`** - Distance between two Vector3 positions
  - Inputs: Vector3, Vector3
  - Output: Float

- **`Vector3Split(vec)`** - Splits a Vector3 into x, y, z components
  - Input: Vector3
  - Output: Vector3Components (access via `.x`, `.y`, `.z`)

- **`Vector3(x, y, z)`** or `ConstructVector3(x, y, z)` - Constructs a Vector3 from components
  - Inputs: Float, Float, Float
  - Output: Vector3

</details>

<details>
<summary><strong>Comparison Operations</strong></summary>

- **`CompareFloats(a, b, operator)`** or `a < b`, `a > b`, etc. - Compares two float values
  - Inputs: Float, Float
  - Operator: `"=="`, `"<"`, `">"`, `"<="`, `">="`
  - Output: Bool

- **`CompareBool(a, b, operator)`** - Compares two boolean values
  - Inputs: Bool, Bool
  - Operator: `"and"`, `"or"`, `"equal to"`, `"xor"`, `"nor"`, `"nand"`, `"xnor"`
  - Output: Bool

- **`Not(condition)`** or `~condition` - Boolean negation
  - Input: Bool
  - Output: Bool

- **`And(a, b)`** or `a & b` - Boolean AND
  - Inputs: Bool, Bool
  - Output: Bool

- **`Or(a, b)`** or `a | b` - Boolean OR
  - Inputs: Bool, Bool
  - Output: Bool

- **`Xor(a, b)`** or `a ^ b` - Boolean XOR
  - Inputs: Bool, Bool
  - Output: Bool

</details>

<details>
<summary><strong>Conditional Operations</strong></summary>

- **`ConditionalSetFloat(condition, trueValue, falseValue)`** - Returns one float based on condition
  - Inputs: Bool, Float, Float
  - Output: Float

- **`ConditionalSetVector3(condition, trueValue, falseValue)`** - Returns one Vector3 based on condition
  - Inputs: Bool, Vector3, Vector3
  - Output: Vector3

</details>

<details>
<summary><strong>Math Functions</strong></summary>

- **`Abs(x)`** - Absolute value
- **`Round(x)`** - Rounds to nearest integer
- **`Floor(x)`** - Floor (rounds down)
- **`Ceil(x)`** - Ceiling (rounds up)
- **`Sin(x)`** - Sine
- **`Cos(x)`** - Cosine
- **`Tan(x)`** - Tangent
- **`Asin(x)`** - Arc sine
- **`Acos(x)`** - Arc cosine
- **`Atan(x)`** - Arc tangent
- **`Sqrt(x)`** - Square root
- **`Sign(x)`** - Sign function (-1, 0, or 1)
- **`Ln(x)`** - Natural logarithm
- **`Log10(x)`** - Base-10 logarithm
- **`Exp(x)`** - e^x
- **`Pow10(x)`** - 10^x

All math functions:
- Input: Float
- Output: Float

</details>

<details>
<summary><strong>Utility Operations</strong></summary>

- **`ClampFloat(value, min, max)`** - Clamps a float between min and max
  - Inputs: Float, Float, Float
  - Output: Float

- **`RandomFloat(min, max)`** - Generates a random float between min and max
  - Inputs: Float, Float
  - Output: Float

</details>

<details>
<summary><strong>Debug Nodes</strong></summary>

- **`Debug(value, string=None, changePosition=True)`** - Debug output node
  - Input: Any node type
  - Output: None (side effect)

- **`DebugDrawLine(start, end, width, color)`** - Draws a debug line
  - Inputs: Vector3, Vector3, Float, Color
  - Output: None (side effect)

- **`DebugDrawDisc(center, radius, height, color)`** - Draws a debug disc
  - Inputs: Vector3, Float, Float, Color
  - Output: None (side effect)

</details>

<details>
<summary><strong>Custom Nodes</strong></summary>

- **`QuadraticFormula(a, b, c)`** - Solves quadratic equation ax² + bx + c = 0
  - Inputs: Float, Float, Float
  - Output: Tuple of (solutionExists: Bool, root1: Float, root2: Float)

</details>

---

### Slime Volleyball Specific Nodes

<details>
<summary><strong>Game Entity Access</strong></summary>

The library provides pre-defined game entities for Slime Volleyball:

- **`Self`** - Your player entity
  - `Self.Position` - Current position (Vector3)
  - `Self.Velocity` - Current velocity (Vector3)
  - `Self.CanJump` - Whether the player can jump (Bool)
  - `Self.TeamSpawn` - Team spawn transform
  - `Self.Score` - Team score (Float)

- **`Opponent`** - The opponent player entity
  - Same properties as `Self`

- **`Ball`** - The ball entity
  - `Ball.Position` - Current position (Vector3)
  - `Ball.Velocity` - Current velocity (Vector3)
  - `Ball.IsSelfSide` - Whether ball is on your side (Bool)
  - `Ball.TouchesRemaining` - Remaining touches (Float)

- **`Game`** - Game state information
  - `Game.DeltaTime` - Time since last frame (Float)
  - `Game.FixedDeltaTime` - Fixed timestep (Float)
  - `Game.Gravity` - Gravity value (Float)
  - `Game.Pi` - Pi constant (Float)
  - `Game.SimulationDuration` - Simulation duration (Float)

</details>

<details>
<summary><strong>Slime Volleyball Specific Functions</strong></summary>

- **`InitializeSlime(name, color, country, speed, acceleration, jump)`**
  - Initializes your slime bot with the specified properties
  - `name`: String name for the bot
  - `color`: Color name (see available colors below)
  - `country`: Country name (see available countries below)
  - `speed`, `acceleration`, `jump`: Numeric stat values
  - Output: None (side effect)

- **`SlimeController(targetPosition, jumpCondition)`**
  - Controls the slime's movement
  - `targetPosition`: Vector3 Node representing where to move
  - `jumpCondition`: Bool Node representing when to jump
  - Output: None (side effect)

- **`ConstructSlimeProperties(name, color, country, speedStat, accelerationStat, jumpStat)`**
  - Low-level function to construct slime properties
  - Inputs: String, Color, Country, Stat, Stat, Stat
  - Output: None (side effect)

- **`GetVector3(value)`** - Gets Vector3 data from the game
  - Available values: `"Self Position"`, `"Self Velocity"`, `"Ball Position"`, `"Ball Velocity"`, `"Opponent Position"`, `"Opponent Velocity"`
  - Output: Vector3

- **`GetBool(value)`** - Gets boolean data from the game
  - Available values: `"Self Can Jump"`, `"Opponent Can Jump"`, `"Ball Is Self Side"`
  - Output: Bool

- **`GetFloat(value)`** - Gets float data from the game
  - Available values: `"Delta time"`, `"Fixed delta time"`, `"Gravity"`, `"Pi"`, `"Simulation duration"`, `"Team score"`, `"Opponent score"`, `"Ball touches remaining"`
  - Output: Float

- **`GetTransform(value)`** - Gets transform data from the game
  - Available values: `"Self"`, `"Opponent"`, `"Ball"`, `"Self Team Spawn"`, `"Opponent Team Spawn"`
  - Output: Transform

- **`RelativePosition(transform, direction)`** - Gets a relative position vector
  - `transform`: Transform node
  - `direction`: One of `"Self"`, `"Self + Forward"`, `"Self + Backward"`, `"Self + Left"`, `"Self + Right"`, `"Self + Up"`, `"Self + Down"`, `"Forward"`, `"Backward"`, `"Left"`, `"Right"`, `"Up"`, `"Down"`
  - Output: Vector3

- **`Stat(value)`** - Creates a stat node (used for slime stats)
  - Input: `value` (int or str)
  - Output: Stat

- **`Color(value)`** - Creates a color node
  - Available colors: `"Black"`, `"Blue"`, `"Brown"`, `"Green"`, `"Hot Pink"`, `"Light Blue"`, `"Light Grey"`, `"Medium Grey"`, `"Orange"`, `"Pink"`, `"Purple"`, `"Red"`, `"White"`, `"Yellow"`
  - Output: Color

- **`Country(value)`** - Creates a country node
  - Available countries: `"Andorra"`, `"Argentina"`, `"Armenia"`, `"Australia"`, `"Austria"`, `"Bangladesh"`, `"Belarus"`, `"Belgium"`, `"Brazil"`, `"Canada"`, `"Chile"`, `"China"`, `"Colombia"`, `"Croatia"`, `"Cuba"`, `"Czechia"`, `"DR Congo"`, `"Denmark"`, `"Egypt"`, `"Ethiopia"`, `"Finland"`, `"France"`, `"Germany"`, `"Guatemala"`, `"India"`, `"Indonesia"`, `"Iran"`, `"Iraq"`, `"Ireland"`, `"Israel"`, `"Italy"`, `"Japan"`, `"Jordan"`, `"Kenya"`, `"Latvia"`, `"Malaysia"`, `"Mexico"`, `"Myanmar"`, `"Netherlands"`, `"New Zealand"`, `"Nigera"`, `"Norway"`, `"Oman"`, `"Pakistan"`, `"Palestine"`, `"Philippines"`, `"Poland"`, `"Portugal"`, `"Puerto Rico"`, `"Qatar"`, `"Romania"`, `"Russia"`, `"Slovakia"`, `"Slovenia"`, `"Somolia"`, `"South Africa"`, `"South Korea"`, `"Spain"`, `"Sweden"`, `"Switzerland"`, `"Syria"`, `"Tanzania"`, `"Thailand"`, `"Turkey"`, `"Ukraine"`, `"Unite Arab Emirates"`, `"United Kingdom"`, `"United States of America"`, `"Vietnam"`, `"Yemen"`
  - Output: Country

</details>

---

## Saving Your AI

<details>
<summary><strong>SaveData Function</strong></summary>

- **`SaveData(filePath, layout="auto", pruneUnusedNodes=True, keepPosition=True)`**
  - Saves the AI data to a JSON file that can be imported into Unity
  - `filePath`: Path to save the file
  - `layout`: Layout mode
    - `"auto"` - Topological layout (recommended)
    - `"grid"` - Grid-based layout
    - `"single"` - All nodes at origin
    - `"hidden"` - Nodes positioned off-screen
    - `None` - No layout changes
  - `pruneUnusedNodes`: Remove nodes that aren't connected (default: True)
  - `keepPosition`: Preserve manually set node positions (default: True)

</details>

## Example: Advanced Bot

```python
from AIGameLibrary import *

# Initialize bot
InitializeSlime("MyBot", "Blue", "Canada", 6, 4, 3)

# Calculate direction to ball
directionToBall = Ball.Position - Self.Position
distanceToBall = Magnitude(directionToBall)

# Normalize direction and add offset
normalizedDir = Normalize(directionToBall)
targetOffset = normalizedDir * 0.3
moveTo = Ball.Position + targetOffset

# Jump when close to ball and ball is above us
ballAbove = Ball.Position.y > Self.Position.y
closeToBall = distanceToBall < 2.0
jumpCondition = closeToBall & ballAbove

# Control the slime
SlimeController(moveTo, jumpCondition)

# Save with auto layout
SaveData("my_bot.txt", "auto")
```

## Tips

1. **Use Python operators**: Instead of calling `AddFloats(a, b)`, use `a + b` for cleaner code
2. **Node caching**: Functions automatically cache nodes with the same inputs for efficiency
3. **Layout options**: Use `"auto"` for clean topological layouts, `"grid"` for grid-based layouts
4. **Debugging**: Use `Debug(value)` to inspect node values during development
5. **Vector components**: Access vector components via `.x`, `.y`, `.z` properties on Vector3 nodes

## File Output

The `SaveData` function generates a JSON file that can be imported into Unity for use in AIA's games. The file contains all the node connections and logic you've defined in Python.
