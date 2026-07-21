# Aialander PyLib

A Python library for creating AI bots for AIA's game collection. This library allows you to programmatically create node-based AI logic that can be exported and used in Unity games.

> If you are an LLM writing a bot from this README, jump to **[Notes for LLM Authors](#notes-for-llm-authors)** at the bottom first. It explains the mental model, lists the mistakes we keep seeing, and shows a correct minimal script.

## Installation

This library requires Python 3.7+. Place the `AIGamePyLibrary` package folder in your project directory and import it:

```python
from AIGamePyLibrary import *
```

**Aialander PyLib** is the friendly name; the importable Python package matches the [GitHub](https://github.com/theaia/AIGamePyLibrary) repo: **`AIGamePyLibrary`** (one name, no separate “Library” / “PyLibrary” split).

## Quick Start

Here's a simple example for **Volleyball**. Everything you read here — positions, velocities, "the ball", "the opponent" — is a **node** you ask the graph for via a simulation-prefixed helper (`VolleyballGetVector3`, `VolleyballGetTransform`, `VolleyballGetBool`, `VolleyballGetFloat`). These match the `VolleyballGet*` / `SlimeGetVector3` node types in `Assets/_Nodes/` (the Vector3 node type id is still `SlimeGetVector3` in Unity; the Python API is `VolleyballGetVector3` so naming stays consistent). There are **no** Unity-style dotted accessors like `something.Position` / `something.Velocity` — always go through the helpers.

```python
from AIGamePyLibrary import *

# Initialize the slime with name, color, country, and stats (speed, acceleration, jump)
InitializeSlime("AIA", "Yellow", "United States of America", 5, 3, 2)

# Grab the world Vector3s from the graph. Every call returns a Node.
ball_position = VolleyballGetVector3("Ball Position")
self_position = VolleyballGetVector3("Self Position")

# Team spawn is a Transform; convert to a Vector3 via RelativePosition.
team_spawn    = VolleyballGetTransform("Self Team Spawn")
positionSign  = RelativePosition(team_spawn, "Backward")

# Calculate where to move (ball position + offset)
moveTo = ball_position + positionSign * 0.4

# Calculate distance to ball and jump condition
distanceToBall = Distance(ball_position, self_position)
jumpCondition  = distanceToBall < 2.25

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
ball_pos = VolleyballGetVector3("Ball Position")
self_pos = VolleyballGetVector3("Self Position")
distance   = Distance(ball_pos, self_pos)
shouldJump = distance < 2.5  # Returns a Node representing the comparison
```

### Vector Operations

Vector3 nodes support component access and operations. Always get the Vector3 from a simulation-prefixed helper (`VolleyballGetVector3(...)` in Volleyball, `RelativePosition(transform_node, "Self")` for any Transform node in other sims) — Transforms do **not** have a `.Position` / `.position` attribute.

```python
# Access vector components on a Vector3 Node
ballPos = VolleyballGetVector3("Ball Position")
x = ballPos.x  # X component
y = ballPos.y  # Y component
z = ballPos.z  # Z component

# Vector arithmetic between Vector3 Nodes
offset = VolleyballGetVector3("Ball Position") - VolleyballGetVector3("Self Position")
scaled = offset * 0.5
```

## Complete Node Reference

Node configurations determine which nodes are available in the Unity editor. Each configuration has a specific purpose. Expand the lists below to see nodes by configuration.

---

<details>
<summary><strong>Default Nodes</strong></summary>

**Description:** General purpose nodes for all simulations. Includes arithmetic, vectors, logic, variables, and debug tools.

<details>
<summary>Basic Types</summary>

<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
      <th align="left">Options</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>Float(value)</code></td>
      <td valign="top">Represents a real number</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The typed value</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>Bool(value)</code></td>
      <td valign="top">Represents a true/false or “boolean” value</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The selected value</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>String(value)</code></td>
      <td valign="top">Represents a text value</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-string"><code>String1</code></a> — <sub>The typed value</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>Color(value)</code></td>
      <td valign="top">Outputs the color value selected in the dropdown</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-color"><code>Color1</code></a> — <sub>The selected value</sub></li>
        </ul>
      </td>
      <td valign="top"><a href="#color-options">See <code>Color</code> options</a></td>
    </tr>
    <tr>
      <td valign="top"><code>Country(value)</code></td>
      <td valign="top">Outputs the country value selected in the dropdown</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-country"><code>Country1</code></a> — <sub>The selected value</sub></li>
        </ul>
      </td>
      <td valign="top"><a href="#country-options">See <code>Country</code> options</a></td>
    </tr>
  </tbody>
</table>

<details id="color-options">
<summary><strong>Color</strong> options</summary>

`"Auburn"`, `"Black"`, `"Blonde"`, `"Blue"`, `"Brown"`, `"Dark Brown"`, `"Dark Green"`, `"Green"`, `"Hot Pink"`, `"Light Blue"`, `"Light Grey"`, `"Medium Grey"`, `"Orange"`, `"Pink"`, `"Purple"`, `"Red"`, `"Tan"`, `"White"`, `"Yellow"`

</details>

<details id="country-options">
<summary><strong>Country</strong> options</summary>

`"Unknown"`, `"Afghanistan"`, `"Albania"`, `"Algeria"`, `"Andorra"`, `"Angola"`, `"Argentina"`, `"Armenia"`, `"Australia"`, `"Austria"`, `"Azerbaijan"`, `"Bahamas"`, `"Bahrain"`, `"Bangladesh"`, `"Barbados"`, `"Belarus"`, `"Belgium"`, `"Bermuda"`, `"Bohemia"`, `"Botswana"`, `"Brazil"`, `"Bulgaria"`, `"Burkina Faso"`, `"Burundi"`, `"Cameroon"`, `"Canada"`, `"Chile"`, `"China"`, `"Colombia"`, `"Costa Rica"`, `"Croatia"`, `"Cuba"`, `"Cyprus"`, `"Czechia"`, `"Côte d'Ivoire"`, `"Denmark"`, `"Djibouti"`, `"Dominican Republic"`, `"DR Congo"`, `"Ecuador"`, `"Egypt"`, `"Eritrea"`, `"Estonia"`, `"Ethiopia"`, `"Fiji"`, `"Finland"`, `"France"`, `"Gabon"`, `"Georgia"`, `"Germany"`, `"Ghana"`, `"Greece"`, `"Grenada"`, `"Guatemala"`, `"Guyana"`, `"Haiti"`, `"Hong Kong"`, `"Hungary"`, `"Iceland"`, `"India"`, `"Indonesia"`, `"Iran"`, `"Iraq"`, `"Ireland"`, `"Israel"`, `"Italy"`, `"Jamaica"`, `"Japan"`, `"Jordan"`, `"Kazakhstan"`, `"Kenya"`, `"Kosovo"`, `"Kuwait"`, `"Kyrgyzstan"`, `"Latvia"`, `"Lebanon"`, `"Lithuania"`, `"Luxembourg"`, `"Malaysia"`, `"Mauritius"`, `"Mexico"`, `"Moldova"`, `"Mongolia"`, `"Montenegro"`, `"Morocco"`, `"Mozambique"`, `"Myanmar"`, `"Namibia"`, `"Netherlands"`, `"New Zealand"`, `"Niger"`, `"Nigeria"`, `"North Korea"`, `"North Macedonia"`, `"Norway"`, `"Oman"`, `"Pakistan"`, `"Palestine"`, `"Panama"`, `"Paraguay"`, `"Peru"`, `"Philippines"`, `"Poland"`, `"Portugal"`, `"Puerto Rico"`, `"Qatar"`, `"Romania"`, `"Russia"`, `"Samoa"`, `"San Marino"`, `"Saudi Arabia"`, `"Scotland"`, `"Senegal"`, `"Serbia"`, `"Singapore"`, `"Slovakia"`, `"Slovenia"`, `"Somolia"`, `"South Africa"`, `"South Korea"`, `"Spain"`, `"Sri Lanka"`, `"Sudan"`, `"Suriname"`, `"Sweden"`, `"Switzerland"`, `"Syria"`, `"Taiwan"`, `"Tajikistan"`, `"Tanzania"`, `"Thailand"`, `"Togo"`, `"Tonga"`, `"Trinidad and Tobago"`, `"Tunisia"`, `"Turkey"`, `"Turkmenistan"`, `"Uganda"`, `"Ukraine"`, `"United Arab Emirates"`, `"United Kingdom"`, `"United States of America"`, `"Uruguay"`, `"Uzbekistan"`, `"Venezuela"`, `"Vietnam"`, `"Virgin Islands"`, `"Yemen"`, `"Zambia"`, `"Zimbabwe"`, `"ChatGPT"`, `"Claude"`, `"Deepseek"`, `"Gemini"`, `"Grok"`, `"Llama"`, `"Mistral"`, `"Perplexity"`, `"Qwen"`

</details>

</details>

<details>
<summary>Arithmetic Operations</summary>

<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Alias</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>AddFloats(a, b)</code></td>
      <td valign="top"><code>a + b</code></td>
      <td valign="top">Performs an addition operation between two numbers</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Left operand</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>Right operand</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Sum</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>SubtractFloats(a, b)</code></td>
      <td valign="top"><code>a - b</code></td>
      <td valign="top">Performs a subtract operation between two numbers</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Left operand</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>Right operand</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Difference</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>MultiplyFloats(a, b)</code></td>
      <td valign="top"><code>a * b</code></td>
      <td valign="top">Performs a multiplication operation between two numbers</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Left operand</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>Right operand</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Product</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>DivideFloats(a, b)</code></td>
      <td valign="top"><code>a / b</code></td>
      <td valign="top">Performs a divide operation between two numbers</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Numerator</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>Denominator</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Quotient</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>Modulo(a, b)</code></td>
      <td valign="top"><code>a % b</code></td>
      <td valign="top">Divides a number by another number and returns any remainder</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Dividend</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>Divisor</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Remainder</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>ClampFloat(value, min, max)</code></td>
      <td valign="top">—</td>
      <td valign="top">Limits (clamps) a number between a minimum and maximum value</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Value</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>Minimum</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float3</code></a> — <sub>Maximum</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Clamped value</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>RandomFloat(min, max)</code></td>
      <td valign="top">—</td>
      <td valign="top">Returns a random number value between two values (changes every Update)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Minimum</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>Maximum</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Random value</sub></li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

</details>

<details>
<summary>Math Functions</summary>

<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Alias</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
      <th align="left">Options</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>AbsFloat(x)</code></td>
      <td valign="top"><code>Abs(x)</code></td>
      <td valign="top">Convert a number to it’s unsigned / absolute value</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The number to perform the function on</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>Operation(x)</code></td>
      <td valign="top">—</td>
      <td valign="top">Performs the selected operation on the input number</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The number to perform the operation on</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
      <td valign="top"><a href="#operation-options">Operations</a></td>
    </tr>
    <tr>
      <td valign="top"><code>Power(base, exponent)</code></td>
      <td valign="top"><code>a ** b</code></td>
      <td valign="top">Raises base to the given power (<code>Mathf.Pow</code>)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Base</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>Exponent</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>Lerp(a, b, t)</code></td>
      <td valign="top">—</td>
      <td valign="top">Linearly interpolates between A and B by T (<code>Mathf.Lerp</code>)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Start (A)</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>End (B)</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float3</code></a> — <sub>Factor (T)</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
  </tbody>
</table>

<details id="operation-options">
<summary><strong>Operation</strong> options</summary>

`abs`, `round`, `floor`, `ceil`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sqrt`, `sign`, `ln`, `log10`, `e^`, `10^`

</details>

</details>

<details>
<summary>Vector Operations</summary>

<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Alias</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>AddVector3(a, b)</code></td>
      <td valign="top"><code>a + b</code></td>
      <td valign="top">Adds two three-dimensional vectors to each other</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The first Vector3 value</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector32</code></a> — <sub>The second Vector3 value to add to the first</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>SubtractVector3(a, b)</code></td>
      <td valign="top"><code>a - b</code></td>
      <td valign="top">Subtracts the second Vector3 from the first (component-wise)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The first input</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector32</code></a> — <sub>The second input</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>ScaleVector3(vec, scalar)</code></td>
      <td valign="top"><code>vec * scalar</code></td>
      <td valign="top">Multiplies a Vector3 by a number</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The value to scale</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The amount to uniformly scale by</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>DotProduct(a, b)</code></td>
      <td valign="top"><code>a @ b</code></td>
      <td valign="top">Returns the dot product between two vectors</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The first input vector</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector32</code></a> — <sub>The second input vector</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>CrossProduct(a, b)</code></td>
      <td valign="top">—</td>
      <td valign="top">Calculates the cross product (result perpendicular to both inputs)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The first input vector</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector32</code></a> — <sub>The second input vector</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>Magnitude(vec)</code></td>
      <td valign="top">—</td>
      <td valign="top">Returns the length of the input vector</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The input value</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>Normalize(vec)</code></td>
      <td valign="top">—</td>
      <td valign="top">Returns a vector with the same direction but magnitude 1</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The input value</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>Distance(pos1, pos2)</code></td>
      <td valign="top">—</td>
      <td valign="top">Calculates the distance between two points</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The first point</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector32</code></a> — <sub>The second point</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>Vector3Split(vec)</code></td>
      <td valign="top">—</td>
      <td valign="top">Splits a Vector3 into x, y, z components</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The Vector3 to be split into it’s components</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The x component of the input Vector3</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>The y component of the input Vector3</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float3</code></a> — <sub>The z component of the input Vector3</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>ConstructVector3(x, y, z)</code></td>
      <td valign="top"><code>Vector3(x, y, z)</code></td>
      <td valign="top">Creates a Vector3 from three numbers</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>x component</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>y component</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float3</code></a> — <sub>z component</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

</details>

<details>
<summary>Comparison & Logic Operations</summary>

<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Alias</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
      <th align="left">Options</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>CompareFloats(a, b, operator)</code></td>
      <td valign="top"><code>a &lt; b</code>, <code>a &gt; b</code>, …</td>
      <td valign="top">Evaluates two float values against the selected operator</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The number representing the left side of the comparison</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>The number representing the right side of the comparison</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
      <td valign="top"><a href="#comparefloats-operators">Operators</a></td>
    </tr>
    <tr>
      <td valign="top"><code>CompareBool(a, b, operator)</code></td>
      <td valign="top">—</td>
      <td valign="top">Evaluates two boolean values against the selected operator</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The first value</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool2</code></a> — <sub>The value to compare to the first</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
      <td valign="top"><a href="#comparebool-operators">Operators</a></td>
    </tr>
    <tr>
      <td valign="top"><code>Not(condition)</code></td>
      <td valign="top"><code>~condition</code></td>
      <td valign="top">Toggles the input boolean (TRUE↔FALSE)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The input value</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>ConditionalSetFloat(condition, trueValue, falseValue)</code></td>
      <td valign="top">—</td>
      <td valign="top">Selects between two Float values based on a condition</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The value to compare against the dropdown selection</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>If TRUE, this value will be set as the result</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>If FALSE, this value will be set as the result</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
      <td valign="top"><a href="#conditionalsetfloat-options">Dropdown</a></td>
    </tr>
    <tr>
      <td valign="top"><code>ConditionalSetVector3(condition, trueValue, falseValue)</code></td>
      <td valign="top">—</td>
      <td valign="top">Selects between two Vector3 values based on a condition</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The value to compare against the dropdown selection</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>If TRUE, this value will be set as the result</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector32</code></a> — <sub>If FALSE, this value will be set as the result</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
      <td valign="top"><a href="#conditionalset-options">Dropdown</a></td>
    </tr>
    <tr>
      <td valign="top"><code>ConditionalSetBool(condition, trueValue, falseValue)</code></td>
      <td valign="top">—</td>
      <td valign="top">Selects between two Bool values based on a condition</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The value to compare against the dropdown selection</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool2</code></a> — <sub>If TRUE, this value will be set as the result</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool3</code></a> — <sub>If FALSE, this value will be set as the result</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
      <td valign="top"><a href="#conditionalset-options">Dropdown</a></td>
    </tr>
  </tbody>
</table>

<details id="comparefloats-operators">
<summary><strong>CompareFloats</strong> operators</summary>

`==`, `<`, `>`, `<=`, `>=`

</details>

<details id="comparebool-operators">
<summary><strong>CompareBool</strong> operators</summary>

`AND`, `OR`, `EQUAL TO`, `XOR`, `NOR`, `NAND`, `XNOR`

</details>

<details id="conditionalsetfloat-options">
<summary><strong>ConditionalSetFloat</strong> dropdown</summary>

`True` (use trueValue when condition is true), `False` (use trueValue when condition is false)

</details>

<details id="conditionalset-options">
<summary><strong>ConditionalSetBool / ConditionalSetVector3</strong> dropdown</summary>

`True`, `False`

</details>

</details>

<details>
<summary>Variables & Utilities</summary>

<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
      <th align="left">Options</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>SetVariable(value)</code></td>
      <td valign="top">Saves the input value so it can be used by matching <code>GetVariable</code> nodes</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-any"><code>Any1</code></a> — <sub>An input of any data type</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
      <td valign="top">Destination node</td>
    </tr>
    <tr>
      <td valign="top"><code>GetVariable(name)</code></td>
      <td valign="top">Outputs the value from the corresponding <code>SetVariable</code> node with the same typed name</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-any"><code>Any1</code></a> — <sub>The result of the Set Variable matching the same typed name</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>Relay(value)</code></td>
      <td valign="top">Passes through data from input to output (useful for organization)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-any"><code>Any1</code></a> — <sub>Input of any data type to pass through</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-any"><code>Any1</code></a> — <sub>The passed-through value</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>IsNull(value)</code></td>
      <td valign="top">Checks if the input is null</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-any"><code>Any1</code></a> — <sub>A connection of any data type</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>Keypress(key)</code></td>
      <td valign="top">Indicates whether the selected key is currently pressed</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>Is the key pressed</sub></li>
        </ul>
      </td>
      <td valign="top">Key is selected in dropdown</td>
    </tr>
    <tr>
      <td valign="top"><code>RelativePosition(transform, direction)</code></td>
      <td valign="top">Gets a world-space position relative to the input Transform and selected direction</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-transform"><code>Transform1</code></a> — <sub>The transform to extract the position from</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The resulting value</sub></li>
        </ul>
      </td>
      <td valign="top"><code>Self</code>, <code>Self + Forward</code>, <code>Self + Backward</code>, <code>Self + Left</code>, <code>Self + Right</code>, <code>Self + Up</code>, <code>Self + Down</code>, <code>Forward</code>, <code>Backward</code>, <code>Left</code>, <code>Right</code>, <code>Up</code>, <code>Down</code>, <code>World</code></td>
    </tr>
  </tbody>
</table>

<details id="relativeposition-options">
<summary><strong>RelativePosition</strong> options</summary>

`Self`, `Self + Forward`, `Self + Backward`, `Self + Left`, `Self + Right`, `Self + Up`, `Self + Down`, `Forward`, `Backward`, `Left`, `Right`, `Up`, `Down`, `World`

Note: `World` exists in the Unity dropdown; currently it behaves the same as `Self` unless/until the Unity gate assigns it a distinct meaning.

</details>

</details>

<details>
<summary>Debug & Visualization</summary>

<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>Debug(value)</code></td>
      <td valign="top">Displays the real-time value of the connected output</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-any"><code>Any1</code></a> — <sub>An input of any data type</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>DebugDrawLine(start, end, width, color)</code></td>
      <td valign="top">Draws a 2D line in worldspace (debug visualization)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The start point of the line</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector32</code></a> — <sub>The end point of the line</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The thickness of the line</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-color"><code>Color1</code></a> — <sub>The color of the line</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>DebugDrawDisc(center, radius, height, color)</code></td>
      <td valign="top">Draws a 2D disc in worldspace on the XY plane (debug visualization)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The centerpoint of the drawn disc</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The radius of the drawn disc</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>The thickness of the drawn disc</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-color"><code>Color1</code></a> — <sub>The color to set the disc</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>TimePlot(name, color, iconUrl, value)</code></td>
      <td valign="top">Adds a value to the time plot graph during a simulation (toggle with F1)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-string"><code>String1</code></a> — <sub>The name to be assigned to the Aialander name tag</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-color"><code>Color1</code></a> — <sub>The color of the line to plot</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-string"><code>String2</code></a> — <sub>A URL of a custom icon to use for the graph</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The value to set on the graph for the current tick</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
  </tbody>
</table>

</details>

<details>
<summary>Organization</summary>

<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>Region</code></td>
      <td valign="top">Groups nodes visually for organization (does not affect logic)</td>
      <td valign="top">—</td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>CreateFunction(name)</code></td>
      <td valign="top">Defines a named custom function body (Unity: Construct Custom Function). Nodes assigned to its bounds run only when a matching <code>CustomFunction</code> call evaluates them — not during the global graph solve.</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-any"><code>Any1</code></a> (In) — <sub><strong>Return</strong> — wire body output here via <code>SetFunctionReturn</code> (same id as Param1 Out)</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-string"><code>String1</code></a>–<code>String4</code> — <sub>Optional parameter labels</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-any"><code>Any1</code></a>–<code>Any4</code> — <sub>Up to 4 parameters passed into the body (<code>fn.Param1</code>…)</sub></li>
        </ul>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>SetFunctionReturn(fn, body_output)</code></td>
      <td valign="top"><strong>Required for a call result.</strong> Connects a body output (e.g. <code>Power.Float1</code>) to CreateFunction Return port <code>Any1</code> (polarity In).</td>
      <td valign="top"><code>body_output</code> — any body node with an out port</td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>AssignToFunction(body_node, fn)</code></td>
      <td valign="top">Marks a node as owned by the CreateFunction body (<code>ownerFunctionSID</code>)</td>
      <td valign="top">—</td>
      <td valign="top">Returns the same body node</td>
    </tr>
    <tr>
      <td valign="top"><code>CustomFunction(name, param1=None, …)</code></td>
      <td valign="top">Call site for a CreateFunction by name (Unity key <code>Function</code>). Passes through used params; output is the definition’s Return value when <code>SetFunctionReturn</code> was used.</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-any"><code>Any1</code></a>–<code>Any4</code> — <sub>Arguments for connected params</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-any"><code>Any1</code></a> — <sub>Return value (null if definition has no Return)</sub></li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

<details>
<summary><strong>Custom Functions</strong> (how they differ from normal nodes)</summary>

- **Definition vs call:** `CreateFunction("MyFn")` defines a reusable body; `CustomFunction("MyFn", …)` calls it by name (`modifier`).
- **Parameters:** Up to **4** Param outputs on the definition (`Any1`–`Any4` → `fn.Param1`…`Param4`). Wire them into body nodes. Only params that are connected on the definition appear as inputs on call sites.
- **Return (required for a usable call result):** Call **`SetFunctionReturn(fn, body_output)`**. This connects the body node's output port to the CreateFunction **Return** input.
  - Return port id is **`Any1`**, polarity **In** (GameObject name `"Any - In"`). Param1 is also `Any1` but polarity **Out** — same id, different polarity.
  - For `Power` / `Lerp` / most float math, the body output port is **`Float1`** → wire to Return `Any1` (In).
  - Without `SetFunctionReturn`, `CustomFunction(...)` still runs the body but the call output is **null**.
- **Body bounds:** Mark every body node with `AssignToFunction(body_node, fn)` (`ownerFunctionSID`). Body nodes are skipped by the global solve and only run when a `Function` call evaluates them.
- **Isolation:** Body cannot wire to the outside world except via Param / Return. Banned in body: nested `CreateFunction` / `Function`, `SetVariable`, and most destination nodes (controllers / properties). Allowed destinations in body: `Debug`, `DebugDrawLine`, `DebugDrawDisc`. Max nested call depth: **8**.
- **Unlike `Region`:** Region is visual-only. CreateFunction bounds **change execution**.
- **Unlike Python helpers in `customNodes.py`:** those expand into ordinary nodes at compile time. Unity Custom Functions are the `CreateFunction` / `Function` pair. Native math nodes like `Power(...)` / `Lerp(...)` are normal graph nodes and are ideal **inside** a function body.

### Canonical example — Power inside a Custom Function (LLM copy/paste)

```python
from AIGamePyLibrary import *

fn = CreateFunction("PowerFn")

# Body: params → Power → Return
#   fn.Param1 (Any1) = base
#   fn.Param2 (Any2) = exponent
#   Power.Float1     = result  →  MUST go to CreateFunction Return (Any1 In)
powered = AssignToFunction(Power(fn.Param1, fn.Param2), fn)
SetFunctionReturn(fn, powered)   # Power.Float1 → Return Any1 (In)  ← do not omit

# Call with different variables; CustomFunction output IS the Return value
result = CustomFunction("PowerFn", Float(2), Float(3))  # → 8
Debug(result, "2^3", changePosition=False)

SaveData("PowerFunctionTest.txt", "grid")
```

Full three-call test: `Examples/CustomFunctionPowerExample.py`.

</details>

</details>

</details>

---

<details>
<summary><strong>Survival Simulation</strong></summary>

<div style="margin-left: 1em;">

<details>
<summary><strong>Overview</strong></summary>

Aialanders are trapped on a deserted island with apple trees and other inhabitants. Each Aialander has a storage container they can put food. Tree count and location can vary per simulation. The number of competitors and their strategies will vary per simulation. The maximum number of total players is 7.

**Objective:** Survive on the island given the available food. Other inhabitants may be friendly or aggressive — choose any personality you want.

</details>

<details>
<summary><strong>Requirements</strong></summary>

- The `SurvivalController(...)` node is the required destination to control a single 3D character.
- `ConstructSurvivalProperties(...)` sets that character’s aesthetic.

</details>

<details>
<summary><strong>Nodes</strong></summary>

<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
      <th align="left">Options / Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>SurvivalController(targetPosition, state, sprint, emote)</code></td>
      <td valign="top">Controls an Aialander’s brain (navigation uses pathfinding)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The target world position to move the character to</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-survivalstate"><code>SurvivalState1</code></a> — <sub>The current state of the character which will control its behavior</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>Whether the character should attempt to sprint (requires stamina)</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-survivalemote"><code>SurvivalEmote1</code></a> — <sub>Optional emote; performing an emote stops movement</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
      <td valign="top">Destination node</td>
    </tr>
    <tr>
      <td valign="top"><code>ConstructSurvivalProperties(...)</code></td>
      <td valign="top">Sets cosmetic options for this Aialander</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-string"><code>String1</code></a> — <sub>The name to be assigned to the Aialander name tag</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-country"><code>Country1</code></a> — <sub>The country this Aialander is representing</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-color"><code>Color1</code></a> — <sub>The color of the Aialander’s skin</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Body style (0 = male, 1 = female). Value wraps to prevent errors</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>Hair style. Value wraps to prevent errors</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-color"><code>Color2</code></a> — <sub>Hair color</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float3</code></a> — <sub>Facial hair style. Value wraps to prevent errors</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-string"><code>String2</code></a> — <sub>Optional outfit image URL</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
      <td valign="top">Customization options are documented under <a href="#survival-customization"><strong>Details → Customization</strong></a>.</td>
    </tr>
    <tr>
      <td valign="top"><code>SurvivalGetTransform(value)</code></td>
      <td valign="top">Select a Transform representing a current location / entity in the sim</td>
      <td valign="top">—</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-transform"><code>Transform1</code></a> — <sub>The selected value</sub></li></ul></td>
      <td valign="top"><a href="#survivalgettransform-options">Options</a></td>
    </tr>
    <tr>
      <td valign="top"><code>SurvivalGetFloat(value)</code></td>
      <td valign="top">Select a Float representing a current simulation parameter</td>
      <td valign="top">—</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The selected value</sub></li></ul></td>
      <td valign="top"><a href="#survivalgetfloat-options">Options</a></td>
    </tr>
    <tr>
      <td valign="top"><code>SurvivalGetBool(value)</code></td>
      <td valign="top">Select a Bool representing a current simulation parameter</td>
      <td valign="top">—</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The selected value</sub></li></ul></td>
      <td valign="top"><a href="#survivalgetbool-options">Options</a></td>
    </tr>
    <tr>
      <td valign="top"><code>SurvivalState(value)</code></td>
      <td valign="top">Select a SurvivalState value</td>
      <td valign="top">—</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-survivalstate"><code>SurvivalState1</code></a> — <sub>The selected value</sub></li></ul></td>
      <td valign="top"><code>Passive</code>, <code>Gather</code>, <code>Eat</code>, <code>Attack</code>, <code>Steal</code>, <code>Dead</code></td>
    </tr>
    <tr>
      <td valign="top"><code>SurvivalEmote(value)</code></td>
      <td valign="top">Select an emote</td>
      <td valign="top">—</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-survivalemote"><code>SurvivalEmote1</code></a> — <sub>The selected value</sub></li></ul></td>
      <td valign="top"><code>None</code>, <code>Hi</code>, <code>Talk</code>, <code>Bored</code>, <code>Wave</code></td>
    </tr>
    <tr>
      <td valign="top"><code>SurvivalAutoPosition(state)</code></td>
      <td valign="top">Automatically decide where to move based on a given state</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-survivalstate"><code>SurvivalState1</code></a> — <sub>The state from which the position will be determined</sub></li></ul></td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The resulting value</sub></li></ul></td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>ConditionalSetSurvivalState(condition, trueValue, falseValue)</code></td>
      <td valign="top">Select between two SurvivalState values based on a condition</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The value to compare against the dropdown selection</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-survivalstate"><code>SurvivalState1</code></a> — <sub>If TRUE, this value will be set as the result</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-survivalstate"><code>SurvivalState2</code></a> — <sub>If FALSE, this value will be set as the result</sub></li>
        </ul>
      </td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-survivalstate"><code>SurvivalState1</code></a> — <sub>The resulting value</sub></li></ul></td>
      <td valign="top"><code>True</code>, <code>False</code></td>
    </tr>
    <tr>
      <td valign="top"><code>ConditionalSetSurvivalEmote(condition, trueValue, falseValue)</code></td>
      <td valign="top">Select between two SurvivalEmote values based on a condition</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The value to compare against the dropdown selection</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-survivalemote"><code>SurvivalEmote1</code></a> — <sub>If TRUE, this value will be set as the result</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-survivalemote"><code>SurvivalEmote2</code></a> — <sub>If FALSE, this value will be set as the result</sub></li>
        </ul>
      </td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-survivalemote"><code>SurvivalEmote1</code></a> — <sub>The resulting value</sub></li></ul></td>
      <td valign="top"><code>True</code>, <code>False</code></td>
    </tr>
  </tbody>
</table>

</details>

<details>
<summary><strong>Details</strong></summary>

<a id="survival-customization"></a>

### Customization

**Body Type**
- `0` Pants and shorts
- `1` Dress
- `2` Robot

**Beard Styles**
- `0` None
- `1` Full trimmed beard

**Hair Styles**
- `0` Curtains
- `1` Caesar
- `2` Bob
- `3` Faux hawk
- `4` Long polytail
- `5` Pebbles
- `6` Side pony
- `7` Samurai side bun
- `8` Undercut
- `9` Medium polytail
- `10` Bowl
- `11` Space buns
- `12` Samurai bun
- `13` Bald

**Custom Outfit**
The properties node has a custom outfit at the bottom that can take a URL string to an image. You can upload the image to something like imgur and then copy the image URL.

If you want, here's the PSD to make a custom outfit texture for your character:
`https://github.com/theaia/AIGamePyLibrary/blob/main/CustomOutfit.psd`

### Container Information

**Health**
- Each player starts with a designated container with 250 health.
- Containers do not regenerate health.
- When a container's health reaches 0 it will be destroyed along with any food stored in it.

**Terrain**
- Terrain has an approximate diameter of 160.
- For the competition the seed will be random—you may be the closest one to a tree, or the furthest.
- I'll be running the sim with both abundant and scarce resources. Adjust your strategy appropriately.
- After being harvested, fruit respawn after 190 seconds. Each tree starts with and has a maximum of 3 fruit.

### Ranking

Players are sorted by Survival Time, then Most Health, then Hunger, then stored apple count. When a player dies, their survival time stops at the time they die.

### Player Information

**Abilities**
- Standard move speed is 5.
- Sprinting increases player speed 9. Players must have available stamina to sprint.
- Attacking deals 10 damage per hit and consumes 5 stamina. Players must have enough stamina to attack. Attack range is 2. Attack radius is 1 in the forward direction of the player. Attacking while holding food will drop the food.
- Players will drop food they are holding when they die.
- Emoting will stop all movement and cause the player to perform a looping animation until their emote state is set to "None".

**Health**
- Players all start with 100 health.
- Players will regenerate 1 health per Tick after they've not taken damage for 5 seconds.
- After a player has started regenerating health, their "last attacked by" player is reset.

**Hunger**
- Players start with 100 Hunger points.
- Every 5 seconds players lose 10 points. The 5 second timer is reset whenever a player eats.
- If the player does not have 10 hunger to be consumed, they will instead take 10 damage.
- Consuming food restores 25 points.

**Stamina**
- Players all start with 100 stamina.
- Sprinting consumes stamina at .15 per tick and Attacking consumes stamina at 5 per attack.
- After not consuming stamina for 3 seconds players will regenerate 2 stamina per Tick.

**Aggression**
- Players have an aggression level.
- Attacking a player with the same or lower aggression level will increase a player's aggression by 1.
- Attacking a player's container with the same or lower aggression level will increase a player's aggression by .5.
- Players can reference players based on aggression using the Get Transform and Get Float nodes.
- Stealing from an alive player's container will increase aggression by .25.
- Stealing from a dead player's inventory does not affect a player's aggression level.

### Player States

- **Passive** - The player will not perform any actions during this state.
- **Gathering** - If not carrying any food a player will search for nearby food to gather and automatically pick it from trees or off the ground. When carrying food the player will automatically deposit it into its own storage container if nearby.
- **Eating** - If not carrying any food a player will search for nearby food to gather and automatically pick it from trees, off of the ground, or from its own container. When carrying food the player will automatically consume it.
- **Attack** - If not carrying any food a player will search for nearby players and containers and will automatically attack them when in range. When carrying food the player will automatically drop it.
- **Steal** - If not carrying any food a player will search for nearby containers they do not own to steal from. When carrying food the player will automatically deposit it into its own storage container if nearby.
- **Dead** - The player will not perform any actions during this state.

<a id="survivalgettransform-options"></a>

### SurvivalGetTransform options

- `0` Self
- `1` Player Last Damaged By
- `2` Player Last Attacking (Global)
- `3` Player Nearest
- `4` Player 2nd Nearest
- `5` Player Farthest
- `6` Player with Highest Health
- `7` Player with Lowest Health
- `8` Player with Highest Hunger
- `9` Player with Lowest Hunger
- `10` Player with Highest Stamina
- `11` Player with Lowest Stamina
- `12` Player Last Stolen From Self Container
- `13` Player Last Stealing (Global)
- `14` Player with Highest Score
- `15` Player with Lowest Score
- `16` Player of Closest Score
- `17` Player with Most Aggression
- `18` Player with Lowest Aggression
- `19` Player Nearest with Aggression
- `20` Player Nearest with No Aggression
- `21` Player with Most Stored Fruit
- `22` Player with Least Stored Fruit
- `23` Container Self
- `24` Container Closest (excluding self)
- `25` Container Farthest (excluding self)
- `26` Container of Last Attacker
- `27` Container of Last Global Attacker
- `28` Container of Most Stored Fruit
- `29` Container of Nearest Dead Player
- `30` Container of Nearest Dead Player (with Food)
- `31` Container of Highest Aggression Player
- `32` Container of Lowest Aggression Player
- `33` Container of Player with Closest Rank
- `34` Fruit Nearest
- `35` Fruit Farthest
- `36` Fruit Nearest Self Container
- `37` Fruit (Random)
- `38` Tree Nearest

<a id="survivalgetfloat-options"></a>

### SurvivalGetFloat options

- `0` Health Percentage
- `1` Hunger Percentage
- `2` Stamina Percentage
- `3` Current Rank
- `4` Stored Food Count
- `5` Distance to Nearest Player
- `6` Distance to Nearest Aggressive Player
- `7` Distance to Last Attacker
- `8` Distance to Nearest Container
- `9` Distance to Nearest Fruit Tree
- `10` Player Count Remaining
- `11` Current Simulation Time
- `12` Max Simulation Time
- `13` Simulation Time Remaining
- `14` Delta time
- `15` Fixed delta time
- `16` Pi
- `17` Self Gathers
- `18` Self Food Consumed
- `19` Self Steals
- `20` Self Damage Dealt
- `21` Self Kills
- `22` Self Aggression Level
- `23` Available Fruit Count
- `24` Player Count Without Stored Food
- `25` Average Player Health
- `26` Average Player Hunger
- `27` Average Player Stamina
- `28` Average Player Aggression Level
- `29` Total Possible Fruit
- `30` Distance Traveled

<a id="survivalgetbool-options"></a>

### SurvivalGetBool options

- `0` Is Carrying Resource
- `1` Container has Health
- `2` Container Was Attacked
- `3` Container Was Stolen From
- `4` Self Was Attacked

</details>

</div>

</details>

---

<details>
<summary><strong>Parking Simulation</strong></summary>

<div style="margin-left: 1em;">

<details>
<summary><strong>Overview</strong></summary>

The goal of the simulation is to navigate the car to a target parking stall and have it sit inside the stall for 3 seconds. After that, the player progresses to a new level with the same goal but from a different local position and with a different target parking stall.

Alignment to the stall is encouraged but not required. Colliding with any objects will reset the player to the starting position.

</details>

<details>
<summary><strong>Requirements</strong></summary>

- You must drive your car via the destination node: `ModularUniformController(...)`
- Use `ConstructModularUniformProperties(...)` / `InitializeParking(...)` to set cosmetics
- Sensors are built from `Spherecast(...)` → `CarRaycasts(...)` → `HitInfo(...)`
- The same modular car stack (controller, sensors, Autosteer / Autothrottle) is shared with **Demo Derby** and **RacingV2**. RacingV2 adds race-specific getters and uses `ConstructRacingV2Properties` for cosmetics + stats — see **RacingV2 Simulation**.

</details>

<details>
<summary><strong>Nodes</strong></summary>

<!-- Single consolidated node table for Parking -->
<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
      <th align="left">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>ModularUniformController(throttle, steering, brake)</code></td>
      <td valign="top">Sends inputs to the car to control it</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Throttle (1 is forward, -1 is reverse)</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>Steering (-1 is left, 1 is right)</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float3</code></a> — <sub>Brake (any value over 0 will apply brake)</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
      <td valign="top">Destination node</td>
    </tr>
    <tr>
      <td valign="top"><code>ConstructModularUniformProperties(name, country, skinColor, bodyStyle, hairStyle, hairColor, facialHairStyle, carColor, outfitUrl)</code></td>
      <td valign="top">Sets cosmetic options for this car</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-string"><code>String1</code></a> — <sub>The name to be assigned to the Aialander name tag</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-country"><code>Country1</code></a> — <sub>The country this Aialander is representing</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-color"><code>Color1</code></a> — <sub>The color of the Aialander’s skin</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Body style (0 = male, 1 = female). Value wraps to prevent errors</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>Hair style. Value wraps to prevent errors</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-color"><code>Color2</code></a> — <sub>Hair color</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float3</code></a> — <sub>Facial hair style. Value wraps to prevent errors</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-color"><code>Color3</code></a> — <sub>Car color</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-string"><code>String2</code></a> — <sub>Optional image URL to download and apply to the outfit</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
      <td valign="top">Destination node</td>
    </tr>
    <tr>
      <td valign="top"><code>Spherecast(radius, distance)</code></td>
      <td valign="top">Defines the radius and travel distance used for spherecast sensors</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The radius of the spherecast to be sent out</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>The maximum distance to check for collisions from the origin</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-spherecast"><code>Spherecast1</code></a> — <sub>The spherecast that will check for collisions</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>CarRaycasts(spherecast)</code></td>
      <td valign="top">Sends 8 sensors out around the car (spherecasts)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-spherecast"><code>Spherecast1</code></a> — <sub>The length/size of spherecasts to send out as sensors</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-raycasthit"><code>RaycastHit1</code></a> — <sub>Data from the forward left spherecast</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-raycasthit"><code>RaycastHit2</code></a> — <sub>Data from the forward spherecast</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-raycasthit"><code>RaycastHit3</code></a> — <sub>Data from the forward right spherecast</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-raycasthit"><code>RaycastHit4</code></a> — <sub>Data from the left spherecast</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-raycasthit"><code>RaycastHit5</code></a> — <sub>Data from the right spherecast</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-raycasthit"><code>RaycastHit6</code></a> — <sub>Data from the rear left spherecast</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-raycasthit"><code>RaycastHit7</code></a> — <sub>Data from the rear spherecast</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-raycasthit"><code>RaycastHit8</code></a> — <sub>Data from the rear right spherecast</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>HitInfo(raycastHit)</code></td>
      <td valign="top">Extracts collision info from a RaycastHit</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-raycasthit"><code>RaycastHit1</code></a> — <sub>The raycast being checked</sub></li>
        </ul>
      </td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>Was a collision detected?</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The collision distance (infinity if no collision)</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>ParkingGetTransform(value)</code></td>
      <td valign="top">Selection of Transform options that represent a current location in the simulation. <code>value</code> may be a dropdown index (<code>0</code>, <code>1</code>, …) or one of the exact labels shown in the options column; the saved graph stores the dropdown <em>index</em> in the node’s <code>modifier</code> field.</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul><li style="margin: 0 0 8px 0;"><a href="#datatype-transform"><code>Transform1</code></a> — <sub>The selected value</sub></li></ul>
      </td>
      <td valign="top"><code>Self</code>, <code>Target Parking Stall</code></td>
    </tr>
    <tr>
      <td valign="top"><code>ParkingGetFloat(value)</code></td>
      <td valign="top">Selection of number-based options that represent a current simulation parameter</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul><li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The selected value</sub></li></ul>
      </td>
      <td valign="top"><code>Speed</code>, <code>Distance to Stall (based on pathfinding)</code>, <code>Target Stall Width</code>, <code>Target Stall Depth</code>, <code>Current Level</code>, <code>Fail Count</code>, <code>Current Simulation Time</code>, <code>Max Simulation Time</code>, <code>Delta Time</code>, <code>Fixed Delta Time</code>, <code>Pi</code>, <code>Signed Speed (forward +, reverse −)</code></td>
    </tr>
    <tr>
      <td valign="top"><code>ParkingGetBool(value)</code></td>
      <td valign="top">Selection of True/False options that represent a current simulation parameter</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul><li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The result of the selected value</sub></li></ul>
      </td>
      <td valign="top"><code>Is Partially in Target Parking Stall</code>, <code>Is Fully in Target Parking Stall</code></td>
    </tr>
  </tbody>
</table>

<details>
<summary><code>InitializeParking(...)</code> (convenience helper)</summary>

Same nine positional arguments as <code>ConstructModularUniformProperties(...)</code>, but applies them as a convenience initialization helper.

</details>

</details>

<details>
<summary><strong>Details</strong></summary>

<details>
<summary>Tips</summary>

- Raycasts originate from the car’s **center**. Approx width **6**, length **10.8**.
- Stepping on the **brake** while setting **throttle** to **`-1`** will almost instantly stop the car.
- Shared with Demo Derby and RacingV2: `ModularUniformController`, `Spherecast` → `CarRaycasts` → `HitInfo`, `Autosteer`, `Autothrottle`. Parking cosmetics use `ConstructModularUniformProperties` / `InitializeParking` (not RacingV2’s stat budget properties node).

</details>

<details>
<summary>Marking the bot as LLM-driven</summary>

See the top-level [Marking your bot as LLM-driven](#marking-your-bot-as-llm-driven) section. The same `props.data["modifier"] = "True"` recipe applies to `InitializeParking`, `InitializeDemoDerby`, and `ConstructModularUniformProperties` — they all return the same `UniformModularCarProperties` node.

</details>

</details>

</div>

</details>

---

<details>
<summary><strong>Demo Derby Simulation</strong></summary>

<div style="margin-left: 1em;">

<details>
<summary><strong>Overview</strong></summary>

Maximize damage to other cars. Collisions deal damage; vulnerable parts change handling (front wheels steering; rear wheels, engine, driveshaft acceleration). At **0** engine health a car **explodes** and damages nearby cars.

</details>

<details>
<summary><strong>Requirements</strong></summary>

- Same modular car stack as Parking / RacingV2:
  - Drive with `ModularUniformController(...)`
  - Cosmetics with `ConstructModularUniformProperties(...)` / `InitializeParking(...)` / `InitializeDemoDerby(...)`
  - Sensors via `Spherecast(...)` → `CarRaycasts(...)` → `HitInfo(...)`
  - Optional `Autosteer` / `Autothrottle` (also used by RacingV2)

</details>

<details>
<summary><strong>Nodes</strong></summary>

<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
      <th align="left">Options / Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>InitializeDemoDerby(name, country, skinColor, bodyStyle, hairStyle, hairColor, facialHairStyle, carColor, outfitUrl)</code></td>
      <td valign="top">Convenience helper to set derby cosmetics (delegates to <code>InitializeParking</code>)</td>
      <td valign="top">See <code>ConstructModularUniformProperties(...)</code> in <strong>Parking Simulation</strong></td>
      <td valign="top">—</td>
      <td valign="top">Returns <code>UniformModularCarProperties</code>; set <code>props.data["modifier"] = "True"</code> to mark as LLM-driven</td>
    </tr>
    <tr>
      <td valign="top"><code>DemoDerbyGetTransform(value)</code></td>
      <td valign="top">Get key transforms used in the derby sim</td>
      <td valign="top">—</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-transform"><code>Transform1</code></a> — <sub>The selected value</sub></li></ul></td>
      <td valign="top">
        <div><strong>Values</strong>:</div>
        <div><code>0</code> self</div>
        <div><code>1</code> fixed ref (inspector)</div>
        <div><code>2</code> random pathable waypoint</div>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>DemoDerbyGetCar(mode, index_float=None)</code></td>
      <td valign="top">Select a car reference by mode (nearest, ranked, etc.)</td>
      <td valign="top">—</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-car"><code>Car1</code></a> — <sub>The selected car</sub></li></ul></td>
      <td valign="top">
        <div><strong>Modes</strong>:</div>
        <div><code>0</code> by index</div>
        <div><code>1</code> by rank</div>
        <div><code>2</code> self</div>
        <div><code>3</code> nearest car</div>
        <div><code>4</code> furthest car</div>
        <div><code>5</code> lowest health car</div>
        <div><code>6</code> highest health car</div>
        <div><code>7</code> last damaged car</div>
        <div><code>8</code> nearest active</div>
        <div><code>9</code> furthest active</div>
        <div><code>10</code> nearest disabled</div>
        <div><code>11</code> furthest disabled</div>
        <div><code>12</code> nearest with disabled steering (rear may still drive)</div>
        <div><code>13</code> furthest with disabled steering</div>
        <div><code>14</code> nearest AI-authored (active)</div>
        <div><code>15</code> lowest health AI</div>
        <div><code>16</code> highest health AI</div>
        <div><code>17</code> nearest human-authored (active)</div>
        <div><code>18</code> lowest health human</div>
        <div><code>19</code> highest health human</div>
        <div><code>20</code> highest ranked</div>
        <div><code>21</code> lowest ranked</div>
        <div><code>22</code> nearest ranked (rank neighbor of self)</div>
        <div><code>23</code> highest ranked (not immobilized)</div>
        <div><code>24</code> highest ranked (immobilized)</div>
        <div><code>25</code> lowest ranked (not immobilized)</div>
        <div><code>26</code> lowest ranked (immobilized)</div>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>CarGetPart(mode, car)</code></td>
      <td valign="top">Pick a part of a car (aim point, weakpoint, etc.)</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-car"><code>Car1</code></a> — <sub>The car to query</sub></li></ul></td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-transform"><code>Transform1</code></a> — <sub>Part transform</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Health percent (0–100)</sub></li>
        </ul>
      </td>
      <td valign="top">
        <div><strong>Modes</strong>:</div>
        <div><code>0</code> average of all parts</div>
        <div><code>1</code> nearest part</div>
        <div><code>2</code> weakest part</div>
        <div><code>3</code> nearest crucial part</div>
        <div><code>4</code> WheelFL</div>
        <div><code>5</code> WheelFR</div>
        <div><code>6</code> WheelRL</div>
        <div><code>7</code> WheelRR</div>
        <div><code>8</code> AxleFL</div>
        <div><code>9</code> AxleFR</div>
        <div><code>10</code> AxleRL</div>
        <div><code>11</code> AxleRR</div>
        <div><code>12</code> Engine</div>
        <div><code>13</code> Driveshaft</div>
        <div><code>14</code> SuspensionFL</div>
        <div><code>15</code> SuspensionFR</div>
        <div><code>16</code> SuspensionRL</div>
        <div><code>17</code> SuspensionRR</div>
        <div><code>18</code> Hood</div>
        <div><code>19</code> Trunk</div>
        <div><code>20</code> BumperFront</div>
        <div><code>21</code> BumperRear</div>
        <div><code>22</code> LicensePlateFront</div>
        <div><code>23</code> LicensePlateRear</div>
        <div><code>24</code> FenderFL</div>
        <div><code>25</code> FenderFR</div>
        <div><code>26</code> DoorL</div>
        <div><code>27</code> DoorR</div>
        <div><code>28</code> DoorRL</div>
        <div><code>29</code> DoorRR</div>
        <div><code>30</code> TurnSignalFL</div>
        <div><code>31</code> TurnSignalFR</div>
        <div><code>32</code> HeadlightL</div>
        <div><code>33</code> HeadlightR</div>
        <div><code>34</code> TaillightL</div>
        <div><code>35</code> TaillightR</div>
        <div><code>36</code> WindshieldWipers</div>
      </td>
    </tr>
    <tr>
      <td valign="top"><code>CarInfo(car)</code></td>
      <td valign="top">Multi-output car info helper</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-car"><code>Car1</code></a> — <sub>The car to query</sub></li></ul></td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-transform"><code>Transform1</code></a> — <sub>Car transform</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>Velocity</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>Is AI-authored</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool2</code></a> — <sub>Is immobile</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Health</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>Rank</sub></li>
        </ul>
      </td>
      <td valign="top"><a href="#carinfo-accessor-warnings"><strong>Notes</strong></a></td>
    </tr>
    <tr>
      <td valign="top"><code>GetCarFromTransform(transform)</code></td>
      <td valign="top">Convert a Transform into a Car reference</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-transform"><code>Transform1</code></a> — <sub>The transform to resolve</sub></li></ul></td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-car"><code>Car1</code></a> — <sub>The resolved car</sub></li></ul></td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>Autosteer(goal)</code></td>
      <td valign="top">Steer toward a world-space goal</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>Target position</sub></li></ul></td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Steering output</sub></li></ul></td>
      <td valign="top">—</td>
    </tr>
    <tr>
      <td valign="top"><code>Autothrottle(goal, desired_speed)</code></td>
      <td valign="top">Throttle toward a goal with a target speed</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>Target position</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>Desired speed at goal</sub></li>
        </ul>
      </td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float2</code></a> — <sub>Throttle output</sub></li></ul></td>
      <td valign="top">—</td>
    </tr>
  </tbody>
</table>

</details>

<details>
<summary><strong>Details</strong></summary>

### Guardrails (common LLM pitfalls)

- **Transform vs Vector3**: Many helpers output a **Transform** (type `Transform`) which is *not* a Vector3 position. In this library, transforms are represented as `Node` objects and **do not** have Unity-style fields like `.Position` / `.position`.
- **How to get a position Vector3 from a Transform**: use **`RelativePosition(transform_node, "Self")`** (returns a `Vector3`).
- **Bad (will error)**: `goal = CarGetPart(0, car).PartTransform.Position`
- **Good**:
  - `part = CarGetPart(0, car)`
  - `part_tf, _health = CarGetPart(0, car)`
  - `goal = RelativePosition(part_tf, "Self")`

<a id="demoderbygetcar-modes"></a>

### DemoDerbyGetCar modes

- **`0`** by index · **`1`** by rank · **`2`** self
- **`3`** nearest car · **`4`** furthest car
- **`5`** lowest health car · **`6`** highest health car
- **`7`** last damaged car
- **`8`** nearest active · **`9`** furthest active
- **`10`** nearest disabled · **`11`** furthest disabled
- **`12`** nearest with disabled steering (rear may still drive) · **`13`** furthest with disabled steering
- **`14`** nearest AI-authored (active) · **`15`** lowest health AI · **`16`** highest health AI
- **`17`** nearest human-authored (active) · **`18`** lowest health human · **`19`** highest health human
- **`20`** highest ranked · **`21`** lowest ranked · **`22`** nearest ranked (rank neighbor of self)
- **`23`** highest ranked (not immobilized) · **`24`** highest ranked (immobilized)
- **`25`** lowest ranked (not immobilized) · **`26`** lowest ranked (immobilized)

<a id="cargetpart-modes"></a>

### CarGetPart modes

- Modes **`0`–`3`**: average of all parts; nearest part; weakest part; nearest crucial part
- Modes **`4`–`36`** select a specific part:
  - `4` WheelFL
  - `5` WheelFR
  - `6` WheelRL
  - `7` WheelRR
  - `8` AxleFL
  - `9` AxleFR
  - `10` AxleRL
  - `11` AxleRR
  - `12` Engine
  - `13` Driveshaft
  - `14` SuspensionFL
  - `15` SuspensionFR
  - `16` SuspensionRL
  - `17` SuspensionRR
  - `18` Hood
  - `19` Trunk
  - `20` BumperFront
  - `21` BumperRear
  - `22` LicensePlateFront
  - `23` LicensePlateRear
  - `24` FenderFL
  - `25` FenderFR
  - `26` DoorL
  - `27` DoorR
  - `28` DoorRL
  - `29` DoorRR
  - `30` TurnSignalFL
  - `31` TurnSignalFR
  - `32` HeadlightL
  - `33` HeadlightR
  - `34` TaillightL
  - `35` TaillightR
  - `36` WindshieldWipers

<a id="carinfo-accessor-warnings"></a>

### Multi-output accessor warnings (current limitation)

- **CarGetPart**: only output **`Transform1`** currently wires up correctly. Using the health output (published as `Float2`) in another node currently raises `KeyError: 'Float2'`.
- **CarInfo**: only output **`Transform1`** currently wires up correctly. Using `Vector32` / `Bool3` / `Bool4` / `Float5` / `Float6` in another node currently raises `KeyError` (commonly `Vector32` / `Bool3` / `Bool4` / `Float5` / `Float6`).
- The same limitation applies in **RacingV2** graphs that use `CarInfo` / `CarGetPart` — prefer `.CarTransform` / `.PartTransform` plus `RacingV2GetFloat` / sensors instead of multi-output component reads.

### Minimal complete Demo Derby example

This is the smallest end-to-end derby bot. It chases the nearest active car, aims for that car's nearest crucial part, commits to the throttle, and brakes if something is right in front of the bumper but the real target is still far away.

```python
from AIGamePyLibrary import *

# 1. Cosmetics + LLM flag (positional args; capture the returned node).
props = InitializeDemoDerby(
    "MyBot",                    # name
    "Gemini",                   # country (LLM persona names are valid)
    "Tan",                      # skin color
    0,                          # body style
    2,                          # hair style
    "Brown",                    # hair color
    0,                          # facial hair style
    "Blue",                     # car color
    "",                         # custom outfit URL (empty)
)
props.data["modifier"] = "True"   # mark this bot as LLM-driven

# 2. Self position (Vector3) for distance checks.
self_pos = RelativePosition(DemoDerbyGetTransform(0), "Self")

# 3. Pick a target: nearest active opponent, aim at its nearest crucial part.
target      = DemoDerbyGetCar(8)                     # 8 = nearest active
target_tf, _target_part_health = CarGetPart(3, target)  # 3 = nearest crucial part
goal                          = RelativePosition(target_tf, "Self")

# 4. Forward sensor for emergency braking against scenery.
sensor          = Spherecast(1.2, 12.0)
_, ray_f, *_    = CarRaycasts(sensor)
front_hit, front_dist = HitInfo(ray_f)

goal_dist = Distance(self_pos, goal)
panic     = front_hit & (front_dist < 2.5) & (goal_dist > 10.0)
brake     = ConditionalSetFloat(panic, 1.0, 0.0)

# 5. Drive: Autosteer / Autothrottle do the heavy lifting.
ModularUniformController(
    Autothrottle(goal, 25.0),   # throttle
    Autosteer(goal),            # steering
    brake,                      # brake
)

# 6. Save (without this, nothing is exported).
SaveData("MyBot", "auto")
```

### Tips

- Raycasts originate at the car **center** (rough width **6**, length **10.8**, same as Parking / RacingV2).
- JSON node id for auto throttle is **`Autothrottle`** (not `AutoThrottle`).
- Shared modular stack also powers **RacingV2**; use `RacingV2Get*` for race state and `InitializeRacingV2` for cosmetics + stats.

</details>

</div>

</details>

---

<details>
<summary><strong>Soccer Simulation</strong></summary>

<div style="margin-left: 1em;">

<details>
<summary><strong>Overview</strong></summary>

Team soccer (4 players per team graph). Control each player with move-to, sprint, and interact (shoot / tackle). Match flow includes kickoff, play, goals, overtime, and whistle (stale ball).

**Save folder:** `Soccer/`

</details>

<details>
<summary><strong>Requirements</strong></summary>

- Drive players with `SoccerController(player, moveTo, sprint, interact)` for players `1`–`4` (Unity keys `SoccerController1`…`4`)
- Optional sensors: `SoccerPlayerSensors(player, spherecast)` → eight RaycastHits labeled **A–H** on the Player Sensor node
- Team cosmetics / faceoff: `ConstructSoccerProperties(...)` / `InitializeSoccer(...)`
- World state: `SoccerGetBool` / `SoccerGetFloat` / `SoccerGetVector3` / `SoccerGetTransform`

</details>

<details>
<summary><strong>Nodes</strong></summary>

<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
      <th align="left">Options / Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>SoccerController(player, moveTo, sprint, interact)</code></td>
      <td valign="top">Controls team player <code>player</code> (1–4)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>Move-to world position</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>Sprint</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool2</code></a> — <sub>Interact (shoot / tackle)</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
      <td valign="top">Destination. Hold interact to charge a shot (with ball) or attempt tackle (without). See Details.</td>
    </tr>
    <tr>
      <td valign="top"><code>SoccerPlayerSensors(player, spherecast)</code></td>
      <td valign="top">Eight-way spherecasts around player <code>player</code> (1–4)</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-spherecast"><code>Spherecast1</code></a></li></ul></td>
      <td valign="top"><code>RaycastHit1</code>…<code>8</code> (letters <strong>A</strong>–<strong>H</strong>)</td>
      <td valign="top">Aligns with the Player Sensor graphic</td>
    </tr>
    <tr>
      <td valign="top"><code>ConstructSoccerProperties(name, country, faceoff1..4)</code></td>
      <td valign="top">Team name, country, and faceoff positions</td>
      <td valign="top">String, Country, Vector3 ×4</td>
      <td valign="top">—</td>
      <td valign="top">Destination. Or use <code>InitializeSoccer(...)</code></td>
    </tr>
    <tr>
      <td valign="top"><code>SoccerGetBool(value)</code></td>
      <td valign="top">Bool world state</td>
      <td valign="top">—</td>
      <td valign="top"><code>Bool1</code></td>
      <td valign="top">Index or label — see <a href="#soccergetbool-values">all values</a></td>
    </tr>
    <tr>
      <td valign="top"><code>SoccerGetFloat(value)</code></td>
      <td valign="top">Float world state</td>
      <td valign="top">—</td>
      <td valign="top"><code>Float1</code></td>
      <td valign="top">Index or label — see <a href="#soccergetfloat-values">all values</a></td>
    </tr>
    <tr>
      <td valign="top"><code>SoccerGetTransform(value)</code></td>
      <td valign="top">Key transforms</td>
      <td valign="top">—</td>
      <td valign="top"><code>Transform1</code></td>
      <td valign="top">Index or label — see <a href="#soccergettransform-values">all values</a></td>
    </tr>
    <tr>
      <td valign="top"><code>SoccerGetVector3(value)</code></td>
      <td valign="top">Directions, landmarks, open-player picks</td>
      <td valign="top">—</td>
      <td valign="top"><code>Vector31</code></td>
      <td valign="top">Index or label — see <a href="#soccergetvector3-values">all values</a></td>
    </tr>
  </tbody>
</table>

</details>

<details>
<summary><strong>Details</strong></summary>

### Tackles

A tackle contest subtracts the **stamina delta** between the tackling player and the ball carrier from both players. After that drain, if the tackling player has **more stamina** (or equal), they win the ball.

### Shooting (interact release)

If a player **has the ball** and there is **shot charge**, setting **interact** (`Bool2`) to **false** releases the shot — the ball is kicked in the direction of that frame’s **movement input**.

Hold interact while with the ball to charge; without the ball, interact attempts a tackle / pickup.

### Vector3 directional checks

`SoccerGetVector3` options that search clear / directional views check the **8** player spherecast directions and return the **first** valid direction meeting the criteria (or null if none). Letters match the Player Sensor graphic (**A**–**H**).

Search order prioritizes the team’s attacking direction:

- **Home:** E, C, H, B, G, A, F, D
- **Away:** D, F, A, G, B, H, C, E

### Kickoff

- Opening kickoff receiving team is **random**
- After a goal, the team that was **scored on** receives the next kickoff
- In **extra time**, the receiving team is the **opposite** of who kicked off at match start
- On **whistle** (stale ball / no meaningful movement after time), kickoff flips to the **opposite** of who last received a kickoff

Pass a dropdown **index** (`0`, `1`, …) or the exact Unity **label** string below. Order matches Unity and `DROPDOWN_OPTIONS` in `data.py`.

<a id="soccergetbool-values"></a>

### SoccerGetBool values

`"Team Has Ball"`, `"Opponent Has Ball"`, `"Is Ball Loose"`, `"Team Player 1 Has Ball"`, `"Team Player 2 Has Ball"`, `"Team Player 3 Has Ball"`, `"Team Player 4 Has Ball"`, `"Opponent Player 1 Has Ball"`, `"Opponent Player 2 Has Ball"`, `"Opponent Player 3 Has Ball"`, `"Opponent Player 4 Has Ball"`, `"Is Ball Nearby Team Player 1"`, `"Is Ball Nearby Team Player 2"`, `"Is Ball Nearby Team Player 3"`, `"Is Ball Nearby Team Player 4"`, `"Is Ball Nearby Opponent Player 1"`, `"Is Ball Nearby Opponent Player 2"`, `"Is Ball Nearby Opponent Player 3"`, `"Is Ball Nearby Opponent Player 4"`, `"Is Team Player 1 Closest Teammate to Ball"`, `"Is Team Player 2 Closest Teammate to Ball"`, `"Is Team Player 3 Closest Teammate to Ball"`, `"Is Team Player 4 Closest Teammate to Ball"`, `"Is Opponent Player 1 Closest Opponent to Ball"`, `"Is Opponent Player 2 Closest Opponent to Ball"`, `"Is Opponent Player 3 Closest Opponent to Ball"`, `"Is Opponent Player 4 Closest Opponent to Ball"`, `"Is Team Player 1 Open"`, `"Is Team Player 2 Open"`, `"Is Team Player 3 Open"`, `"Is Team Player 4 Open"`, `"Is Opponent Player 1 Open"`, `"Is Opponent Player 2 Open"`, `"Is Opponent Player 3 Open"`, `"Is Opponent Player 4 Open"`, `"Is Kickoff"`, `"Is Team Kicking off"`, `"Is Opponent Kicking off"`, `"Team Is Winning"`, `"Opponent Is Winning"`, `"Team Scored Last Point"`, `"Opponent Scored Last Point"`, `"Ball On Team Side"`, `"Ball On Opponent Side"`, `"Is Ball Headed Towards Team Goal"`, `"Is Ball Headed Towards Opponent Goal"`, `"Is Home Team"`, `"Is Away Team"`, `"Is Active Graph"`

<a id="soccergetfloat-values"></a>

### SoccerGetFloat values

`"Team Score"`, `"Opponent Score"`, `"Team Shots"`, `"Opponent Shots"`, `"Team Possession %"`, `"Opponent Possession %"`, `"Team Attacking %"`, `"Opponent Attacking %"`, `"Ball Speed"`, `"Player Interact Radius"`, `"Player With Ball Shot Charge %"`, `"Ball Carrier Stamina"`, `"Ball Carrier Shot Charge"`, `"Teammate 1 Shot Charge"`, `"Teammate 2 Shot Charge"`, `"Teammate 3 Shot Charge"`, `"Teammate 4 Shot Charge"`, `"Field Width"`, `"Field Depth"`, `"Kickoff Circle Radius"`, `"Goal Width"`, `"Goal Height"`, `"Team Player 1 Stamina"`, `"Team Player 2 Stamina"`, `"Team Player 3 Stamina"`, `"Team Player 4 Stamina"`, `"Distance from Team Player 1 to nearest Opponent"`, `"Distance from Team Player 2 to nearest Opponent"`, `"Distance from Team Player 3 to nearest Opponent"`, `"Distance from Team Player 4 to nearest Opponent"`, `"Opponent Player 1 Stamina"`, `"Opponent Player 2 Stamina"`, `"Opponent Player 3 Stamina"`, `"Opponent Player 4 Stamina"`, `"Opponent Nearest Teammate Player 1 Stamina"`, `"Opponent Nearest Teammate Player 2 Stamina"`, `"Opponent Nearest Teammate Player 3 Stamina"`, `"Opponent Nearest Teammate Player 4 Stamina"`, `"Stamina of last defending opponent"`, `"Current Simulation Time"`, `"Max Simulation Time"`, `"Simulation Time Remaining"`, `"Delta Time"`, `"Fixed Delta Time"`, `"Pi"`

<a id="soccergettransform-values"></a>

### SoccerGetTransform values

`"Ball"`, `"Team Player 1"`, `"Team Player 2"`, `"Team Player 3"`, `"Team Player 4"`, `"Opponent Player 1"`, `"Opponent Player 2"`, `"Opponent Player 3"`, `"Opponent Player 4"`, `"Teammate Nearest Team Player 1"`, `"Teammate Nearest Team Player 2"`, `"Teammate Nearest Team Player 3"`, `"Teammate Nearest Team Player 4"`, `"Opponent Nearest Team Player 1"`, `"Opponent Nearest Team Player 2"`, `"Opponent Nearest Team Player 3"`, `"Opponent Nearest Team Player 4"`, `"Team Goal Center"`, `"Team Goal Left Post"`, `"Team Goal Right Post"`, `"Opponent Goal Center"`, `"Opponent Goal Left Post"`, `"Opponent Goal Right Post"`, `"Opponent Nearest Team Goal"`, `"Opponent Nearest Opponent Goal"`, `"Teammate Nearest Team Goal"`, `"Teammate Nearest Opponent Goal"`

<a id="soccergetvector3-values"></a>

### SoccerGetVector3 values

`"Ball Velocity"`, `"Clear direction from team carrier"`, `"Backwards clear direction from team carrier"`, `"Clear direction from team carrier (avoid goal lines)"`, `"Clear direction from team carrier (avoid sidelines)"`, `"Clear direction from team carrier (avoid all walls)"`, `"Upper Corner Home Side"`, `"Lower Corner Home Side"`, `"Upper Midfield"`, `"Lower Midfield"`, `"Upper Corner Away Side"`, `"Lower Corner Away Side"`, `"Upper Corner Opposing Side"`, `"Lower Corner Opposing Side"`, `"Upper Corner Team Side"`, `"Lower Corner Team Side"`, `"Center Field"`, `"Get nearest open teammate"`, `"Get furthest open teammate"`, `"Get most open teammate"`, `"Get nearest open opponent"`, `"Get furthest open opponent"`, `"Get most open opponent"`, `"Direction of clear teammate from Teammate 1"`, `"Direction of clear teammate from Teammate 2"`, `"Direction of clear teammate from Teammate 3"`, `"Direction of clear teammate from Teammate 4"`, `"Direction of clear teammate from Opponent 1"`, `"Direction of clear teammate from Opponent 2"`, `"Direction of clear teammate from Opponent 3"`, `"Direction of clear teammate from Opponent 4"`, `"Direction of ball from Teammate 1"`, `"Direction of ball from Teammate 2"`, `"Direction of ball from Teammate 3"`, `"Direction of ball from Teammate 4"`, `"Direction of ball from Opponent 1"`, `"Direction of ball from Opponent 2"`, `"Direction of ball from Opponent 3"`, `"Direction of ball from Opponent 4"`, `"Direction of team goal from Teammate 1"`, `"Direction of team goal from Teammate 2"`, `"Direction of team goal from Teammate 3"`, `"Direction of team goal from Teammate 4"`, `"Direction of opponent goal from Teammate 1"`, `"Direction of opponent goal from Teammate 2"`, `"Direction of opponent goal from Teammate 3"`, `"Direction of opponent goal from Teammate 4"`, `"Clear direction from Teammate 1"`, `"Clear direction from Teammate 2"`, `"Clear direction from Teammate 3"`, `"Clear direction from Teammate 4"`, `"Direction of teammate from Team Player 1"`, `"Direction of teammate from Team Player 2"`, `"Direction of teammate from Team Player 3"`, `"Direction of teammate from Team Player 4"`

### Tips

- During kickoff restriction, only the kicking-off team gets graph control; non-kickoff players are kept outside the center circle until first touch / delay expires.
- Convert transforms to positions with `RelativePosition(transform, "Self")`.

</details>

</div>

</details>

---

<details>
<summary><strong>RacingV2 Simulation</strong></summary>

<div style="margin-left: 1em;">

<details>
<summary><strong>Overview</strong></summary>

Lap racing on additive **V2** tracks using the modular car stack. Default **3** laps; cars can DNF on no waypoint progress; modular part damage still applies.

**Save folder:** `RacingV2/`

</details>

<details>
<summary><strong>Requirements</strong></summary>

- Drive with `ModularUniformController(throttle, steering, brake)` (same as Parking / Demo Derby)
- Cosmetics + **20-point** stats: `ConstructRacingV2Properties(...)` / `InitializeRacingV2(...)` (not `UniformModularCarProperties`)
- Sensors: `Spherecast` → `CarRaycasts` → `HitInfo` (shared stack)
- Optional helpers: `Autosteer`, `Autothrottle`, `CarGetPart`, `CarInfo` (same multi-output wiring caveat as Demo Derby)
- Race state: `RacingV2GetFloat` / `RacingV2GetBool` / `RacingV2GetCar` / `RacingV2GetWaypoint` / `RacingV2Waypoint`

</details>

<details>
<summary><strong>Nodes</strong></summary>

<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
      <th align="left">Options / Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>InitializeRacingV2(..., speed, turn, health)</code></td>
      <td valign="top">Cosmetics + Stat1/2/3 (20-point budget → speed / turn / health)</td>
      <td valign="top">Same cosmetics as Parking, plus three <code>Stat</code> inputs</td>
      <td valign="top">—</td>
      <td valign="top">Unity key <code>ConstructRacingV2Properties</code></td>
    </tr>
    <tr>
      <td valign="top"><code>RacingV2GetFloat(value)</code></td>
      <td valign="top">Speed, waypoints, rank, laps, sim time, …</td>
      <td valign="top">—</td>
      <td valign="top"><code>Float1</code></td>
      <td valign="top">Index or label (see DROPDOWN_OPTIONS)</td>
    </tr>
    <tr>
      <td valign="top"><code>RacingV2GetBool(value)</code></td>
      <td valign="top">Grounded / disabled / sim started</td>
      <td valign="top">—</td>
      <td valign="top"><code>Bool1</code></td>
      <td valign="top"><code>Is Grounded</code>, <code>Is Disabled</code>, <code>Simulation started</code></td>
    </tr>
    <tr>
      <td valign="top"><code>RacingV2GetCar(mode, index_float=None)</code></td>
      <td valign="top">Select a car (modes 0–26, same shape as DemoDerbyGetCar)</td>
      <td valign="top">Optional Float for by-index / by-rank</td>
      <td valign="top"><code>Car1</code></td>
      <td valign="top">Rank uses race scoreboard</td>
    </tr>
    <tr>
      <td valign="top"><code>RacingV2GetWaypoint(value, index_float=None)</code></td>
      <td valign="top">Next / Previous / By index / Start waypoint</td>
      <td valign="top">Optional Float for By index</td>
      <td valign="top"><code>Waypoint1</code></td>
      <td valign="top">Feed into <code>RacingV2Waypoint</code></td>
    </tr>
    <tr>
      <td valign="top"><code>RacingV2Waypoint(mode, waypoint, ref=None)</code></td>
      <td valign="top">Resolve a waypoint to a world point</td>
      <td valign="top">Waypoint (+ optional Transform for Nearest)</td>
      <td valign="top"><code>.Position</code> (Vector3), <code>.Index</code> (Float)</td>
      <td valign="top">Center / Left / Right / Nearest point</td>
    </tr>
  </tbody>
</table>

Shared modular nodes are documented under **Parking Simulation** and **Demo Derby Simulation** (`ModularUniformController`, `CarRaycasts`, `Autosteer`, `Autothrottle`, …).

</details>

<details>
<summary><strong>Details</strong></summary>

### Stats

`ConstructRacingV2Properties` takes **Stat1** (speed), **Stat2** (turn), **Stat3** (health) with a sequential **20-point** budget (typical mapping: max speed ~20–60, turn ~0.5–2.0, health fraction of baseline).

### RacingV2GetFloat options

`Speed`, `Signed Speed (forward +, reverse −)`, waypoint indices/distances, `Current race rank`, `Number of competitors`, lap times, `Current lap` / `Total laps`, sim time, `Delta Time`, `Pi`, …

### Tips

- Prefer `Autosteer(goal)` + `Autothrottle(goal, speed)` toward `RacingV2Waypoint(...).Position`.
- Avoid `CarInfo` / `CarGetPart` non-Transform outputs (same KeyError limitation as Demo Derby).
- Older `Racing.unity` / Kart nodes are a different stack — use **RacingV2** helpers for this scene.

### Minimal RacingV2 sketch

```python
from AIGamePyLibrary import *

props = InitializeRacingV2(
    "Racer", "United States of America", "Tan", 0, 0, "Brown", 0, "Red", "",
    7, 7, 6,
)
wp = RacingV2GetWaypoint("Next waypoint")
goal = RacingV2Waypoint("Center", wp).Position
ModularUniformController(Autothrottle(goal, 30.0), Autosteer(goal), Float(0.0))
SaveData("RacingV2/AIComp_Data/Saves/racer.txt", "grid")
```

</details>

</div>

</details>

---

<details>
<summary><strong>Volleyball Simulation</strong></summary>

<blockquote>

<details>
<summary><strong>Overview</strong></summary>

Volleyball bots control a slime character to move and jump based on the current world state (self/opponent/ball positions and velocities, scores, etc.).

</details>

<details>
<summary><strong>Requirements</strong></summary>

- Drive the slime via the destination node: `SlimeController(targetPosition, jumpCondition)`
- Read world state via sim-prefixed helpers: `VolleyballGetVector3` / `VolleyballGetTransform` / `VolleyballGetBool` / `VolleyballGetFloat`

</details>

<details>
<summary><strong>Nodes</strong></summary>

<table>
  <thead>
    <tr>
      <th align="left">Node</th>
      <th align="left">Purpose</th>
      <th align="left">Inputs</th>
      <th align="left">Outputs</th>
      <th align="left">Options / Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="top"><code>VolleyballGetVector3(value)</code></td>
      <td valign="top">World-space vectors (Unity node type id: <code>SlimeGetVector3</code>)</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul><li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>The resulting value from the selection</sub></li></ul>
      </td>
      <td valign="top"><a href="#volleyballgetvector3-values">Values</a></td>
    </tr>
    <tr>
      <td valign="top"><code>VolleyballGetTransform(value)</code></td>
      <td valign="top">Transform references (convert to Vector3 via <code>RelativePosition(tf, \"Self\")</code>)</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul><li style="margin: 0 0 8px 0;"><a href="#datatype-transform"><code>Transform1</code></a> — <sub>The selected value</sub></li></ul>
      </td>
      <td valign="top"><a href="#volleyballgettransform-values">Values</a></td>
    </tr>
    <tr>
      <td valign="top"><code>VolleyballGetBool(value)</code></td>
      <td valign="top">Boolean state</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul><li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>The selected value</sub></li></ul>
      </td>
      <td valign="top"><a href="#volleyballgetbool-values">Values</a></td>
    </tr>
    <tr>
      <td valign="top"><code>VolleyballGetFloat(value)</code></td>
      <td valign="top">Scalar state</td>
      <td valign="top">—</td>
      <td valign="top">
        <ul><li style="margin: 0 0 8px 0;"><a href="#datatype-float"><code>Float1</code></a> — <sub>The selected value</sub></li></ul>
      </td>
      <td valign="top"><a href="#volleyballgetfloat-values">Values</a></td>
    </tr>
    <tr>
      <td valign="top"><code>InitializeSlime(name, color, country, speed, acceleration, jump)</code></td>
      <td valign="top">Initialize your slime bot with the specified properties</td>
      <td valign="top">See <code>ConstructSlimeProperties(...)</code> below</td>
      <td valign="top">—</td>
      <td valign="top">Convenience helper</td>
    </tr>
    <tr>
      <td valign="top"><code>SlimeController(targetPosition, jumpCondition)</code></td>
      <td valign="top">Drive the slime (movement + jump)</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>Target world position</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-bool"><code>Bool1</code></a> — <sub>Jump condition</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
      <td valign="top">Destination node</td>
    </tr>
    <tr>
      <td valign="top"><code>ConstructSlimeProperties(name, color, country, speedStat, accelerationStat, jumpStat)</code></td>
      <td valign="top">Low-level slime cosmetics + stat initialization</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-string"><code>String1</code></a> — <sub>Name tag</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-color"><code>Color1</code></a> — <sub>Slime color</sub></li>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-country"><code>Country1</code></a> — <sub>Country / persona</sub></li>
          <li style="margin: 0 0 8px 0;"><code>Stat1</code> — <sub>Speed stat</sub></li>
          <li style="margin: 0 0 8px 0;"><code>Stat2</code> — <sub>Acceleration stat</sub></li>
          <li style="margin: 0 0 8px 0;"><code>Stat3</code> — <sub>Jump stat</sub></li>
        </ul>
      </td>
      <td valign="top">—</td>
      <td valign="top">Destination node</td>
    </tr>
    <tr>
      <td valign="top"><code>RelativePosition(transform, direction)</code></td>
      <td valign="top">Convert a Transform reference into a world-space Vector3</td>
      <td valign="top">
        <ul>
          <li style="margin: 0 0 8px 0;"><a href="#datatype-transform"><code>Transform1</code></a> — <sub>Transform to query</sub></li>
        </ul>
      </td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-vector3"><code>Vector31</code></a> — <sub>World-space position</sub></li></ul></td>
      <td valign="top"><code>Self</code>, <code>Self + Forward</code>, <code>Self + Backward</code>, <code>Self + Left</code>, <code>Self + Right</code>, <code>Self + Up</code>, <code>Self + Down</code>, <code>Forward</code>, <code>Backward</code>, <code>Left</code>, <code>Right</code>, <code>Up</code>, <code>Down</code>, <code>World</code></td>
    </tr>
    <tr>
      <td valign="top"><code>Stat(value)</code></td>
      <td valign="top">Create a Stat node (used for slime properties)</td>
      <td valign="top">—</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><code>Stat1</code> — <sub>The stat</sub></li></ul></td>
      <td valign="top"><code>value</code> can be <code>int</code> or <code>str</code></td>
    </tr>
    <tr>
      <td valign="top"><code>Color(value)</code></td>
      <td valign="top">Create a Color node</td>
      <td valign="top">—</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-color"><code>Color1</code></a> — <sub>The selected color</sub></li></ul></td>
      <td valign="top">See <a href="#volleyball-color-values">values</a></td>
    </tr>
    <tr>
      <td valign="top"><code>Country(value)</code></td>
      <td valign="top">Create a Country node</td>
      <td valign="top">—</td>
      <td valign="top"><ul><li style="margin: 0 0 8px 0;"><a href="#datatype-country"><code>Country1</code></a> — <sub>The selected country / persona</sub></li></ul></td>
      <td valign="top">See <a href="#volleyball-country-values">values</a></td>
    </tr>
  </tbody>
</table>
 
</details>

<details>
<summary><strong>Details</strong></summary>

<a id="volleyballgetvector3-values"></a>

### VolleyballGetVector3 values

`"Self Position"`, `"Self Velocity"`, `"Opponent Position"`, `"Opponent Velocity"`, `"Ball Position"`, `"Ball Velocity"`

<a id="volleyballgettransform-values"></a>

### VolleyballGetTransform values

`"Self"`, `"Opponent"`, `"Ball"`, `"Self Team Spawn"`, `"Opponent Team Spawn"`

<a id="volleyballgetbool-values"></a>

### VolleyballGetBool values

`"Self Can Jump"`, `"Opponent Can Jump"`, `"Ball Is Self Side"`

<a id="volleyballgetfloat-values"></a>

### VolleyballGetFloat values

`"Delta time"`, `"Fixed delta time"`, `"Gravity"`, `"Pi"`, `"Simulation duration"`, `"Team score"`, `"Opponent score"`, `"Ball touches remaining"`

<a id="relativeposition-directions"></a>

### RelativePosition directions

`"Self"`, `"Self + Forward"`, `"Self + Backward"`, `"Self + Left"`, `"Self + Right"`, `"Self + Up"`, `"Self + Down"`, `"Forward"`, `"Backward"`, `"Left"`, `"Right"`, `"Up"`, `"Down"`, `"World"`

<a id="volleyball-color-values"></a>

### Color values

`"Auburn"`, `"Black"`, `"Blonde"`, `"Blue"`, `"Brown"`, `"Dark Brown"`, `"Dark Green"`, `"Green"`, `"Hot Pink"`, `"Light Blue"`, `"Light Grey"`, `"Medium Grey"`, `"Orange"`, `"Pink"`, `"Purple"`, `"Red"`, `"Tan"`, `"White"`, `"Yellow"`

<a id="volleyball-country-values"></a>

### Country values

See the full list in the Country node docs above (same list used across simulations).

### Access rules (important)

- There are **no** Unity-style dotted shortcuts. Always use the sim-prefixed helpers.
- The unprefixed aliases (`GetVector3` / `GetTransform` / `GetBool` / `GetFloat`) are Volleyball-only backward-compat; prefer the explicit `VolleyballGet*` names.
- Transform → world position: `RelativePosition(transform_node, "Self")`.

</details>

</blockquote>

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
from AIGamePyLibrary import *

# Initialize bot
InitializeSlime("MyBot", "Blue", "Canada", 6, 4, 3)

# Pull world state from the graph helpers (no dotted accessors anywhere).
ball_position = VolleyballGetVector3("Ball Position")
self_position = VolleyballGetVector3("Self Position")

# Calculate direction to ball
directionToBall = ball_position - self_position
distanceToBall  = Magnitude(directionToBall)

# Normalize direction and add offset
normalizedDir = Normalize(directionToBall)
targetOffset  = normalizedDir * 0.3
moveTo        = ball_position + targetOffset

# Jump when close to ball and ball is above us (component access on Vector3 Nodes)
ballAbove     = ball_position.y > self_position.y
closeToBall   = distanceToBall < 2.0
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

---

## Data types

This section is the “type dictionary” that port keys link to (for example: clicking `Float1` jumps you here).

<details>
<summary><strong>Float</strong></summary>

<a id="datatype-float"></a>

- **Type**: Float
- **Ports**: `Float1`, `Float2`, `Float3`, ...
- **Meaning**: A numeric scalar value.

</details>

<details>
<summary><strong>Bool</strong></summary>

<a id="datatype-bool"></a>

- **Type**: Bool
- **Ports**: `Bool1`, `Bool2`, ...
- **Meaning**: A true/false scalar value.

</details>

<details>
<summary><strong>String</strong></summary>

<a id="datatype-string"></a>

- **Type**: String
- **Ports**: `String1`, `String2`, ...
- **Meaning**: A text value.

</details>

<details>
<summary><strong>Color</strong></summary>

<a id="datatype-color"></a>

- **Type**: Color
- **Ports**: `Color1`, `Color2`, ...
- **Meaning**: A dropdown-selected color value.

</details>

<details>
<summary><strong>Country</strong></summary>

<a id="datatype-country"></a>

- **Type**: Country
- **Ports**: `Country1`, `Country2`, ...
- **Meaning**: A dropdown-selected country value.

</details>

<details>
<summary><strong>RaycastHit</strong></summary>

<a id="datatype-raycasthit"></a>

- **Type**: RaycastHit
- **Ports**: `RaycastHit1`, `RaycastHit2`, ...
- **Meaning**: A ray/spherecast hit result container (used by sensors).

</details>

<details>
<summary><strong>Spherecast</strong></summary>

<a id="datatype-spherecast"></a>

- **Type**: Spherecast
- **Ports**: `Spherecast1`, `Spherecast2`, ...
- **Meaning**: A sensor definition that configures the size/length of spherecast sensors.

</details>

<details>
<summary><strong>Any</strong></summary>

<a id="datatype-any"></a>

- **Type**: Any
- **Ports**: `Any1`, `Any2`, ...
- **Meaning**: Generic “wildcard” type. Carries through whatever concrete type you connect.

</details>

<details>
<summary><strong>Vector3</strong></summary>

<a id="datatype-vector3"></a>

- **Type**: Vector3
- **Ports**: `Vector31`, `Vector32`, ...
- **Meaning**: A 3D vector. Supports `.x`, `.y`, `.z` component access in the graph.

</details>

<details>
<summary><strong>Transform</strong></summary>

<a id="datatype-transform"></a>

- **Type**: Transform
- **Ports**: `Transform1`, `Transform2`, ...
- **Meaning**: A Unity Transform reference (position/rotation container). Use `RelativePosition(transform, "Self")` to convert to a world-space Vector3.

</details>

<details>
<summary><strong>SurvivalState</strong></summary>

<a id="datatype-survivalstate"></a>

- **Type**: SurvivalState
- **Ports**: `SurvivalState1`, `SurvivalState2`, ...
- **Meaning**: Survival simulation state enum.

</details>

<details>
<summary><strong>SurvivalEmote</strong></summary>

<a id="datatype-survivalemote"></a>

- **Type**: SurvivalEmote
- **Ports**: `SurvivalEmote1`, `SurvivalEmote2`, ...
- **Meaning**: Survival simulation emote enum.

</details>

<details>
<summary><strong>Car</strong></summary>

<a id="datatype-car"></a>

- **Type**: Car
- **Ports**: `Car1`, `Car2`, ...
- **Meaning**: Car reference for Demo Derby / RacingV2 (selected via `DemoDerbyGetCar(...)` / `RacingV2GetCar(...)` or derived from a Transform).

</details>

---

<details>
<summary><strong>Notes for LLM Authors</strong></summary>

## Marking your bot as LLM-driven

The car / kart Properties node carries an **`isLLM`** flag that is **not exposed in the Unity inspector** — it can only be set by the PyLib compiler. At runtime Unity reads it from the node's **`modifier`** field during `Initialize()`, writes it onto the resulting properties (`KartProperties` / modular car properties), and applies it to the spawned `Player` (`Player.IsLLM = true`).

To set it, **capture the Properties node** returned by any of the helpers and assign its `modifier` after construction. Accepted values: **`"True"` / `"False"`** or **`"1"` / `"0"`** (anything else falls back to `False`).

```python
from AIGamePyLibrary import *

# Works for InitializeDemoDerby, InitializeParking, and ConstructModularUniformProperties —
# they all return the same UniformModularCarProperties node.
# For RacingV2, use InitializeRacingV2 / ConstructRacingV2Properties the same way (modifier on the returned node).
props = InitializeDemoDerby(
    "MyBot", "United States of America", "Tan",
    0, 0, "Brown", 0, "Red", "",
)
props.data["modifier"] = "True"   # mark this car as LLM-driven
```

`isLLM` is persisted in the saved JSON through the standard `modifier` field, so the graph round-trips through Unity without losing the flag. Equivalent behavior is wired up on the C# side for `ConstructKartProperties` (Kart-style simulations) and RacingV2 properties — same `modifier` accepted values.

This section consolidates everything an LLM (or anyone new to the library) needs to avoid the most common mistakes. Read it in full before writing a script.

> 🛑 **Before you submit a bot, scan it for these six accessor patterns and delete every one of them** — they all currently crash in `ConnectPorts` with a `KeyError` and are the #1 thing we keep seeing LLMs burn on:
>
> - `CarInfo(...).Velocity` → `KeyError: 'Vector32'`
> - `CarInfo(...).IsAI` → `KeyError: 'Bool3'`
> - `CarInfo(...).IsImmobile` → `KeyError: 'Bool4'`
> - `CarInfo(...).Health` → `KeyError: 'Float5'`
> - `CarInfo(...).Rank` → `KeyError: 'Float6'`
> - `CarGetPart(...).HealthPercent` → `KeyError: 'Float2'`
>
> That includes the sneaky **tuple-unpacking** form (`car_tf, velocity, is_ai, is_immobile, health, rank = CarInfo(car)` — the unpacked vars are the same broken nodes) and any arithmetic/comparison that funnels them into another node (`Magnitude(v)`, `v * dt`, `health < 50`, `ConditionalSetFloat(is_immobile, ...)`, etc.). Only **`.CarTransform`** and **`.PartTransform`** are safe. See **[Multi-output component accessor bug](#multi-output-component-accessor-bug)** for replacements.

## The mental model

This is a **graph compiler**, not a runtime game SDK. Your script does **not** drive the car/slime/Aialander frame-by-frame. It builds a static node graph **once**, and `SaveData(...)` writes that graph to JSON. Unity loads the JSON and re-evaluates the graph every tick.

Concretely:

- Every value you compose (`VolleyballGetVector3("Self Position")`, `Distance(...)`, `props`, sensor outputs, etc.) is a **`Node` object**, not a number, string, list, or dict.
- Plain Python `if` / `while` / `for`, `min` / `max` / `sorted`, `lambda`, list/dict indexing, and `import math` calls **do not become nodes**. They run once at compile time and are gone. Use the graph equivalents: `ConditionalSetFloat` / `ConditionalSetVector3` / `ConditionalSetBool` for branching, `Operation(x)` for math, `DemoDerbyGetCar` / `SurvivalGetTransform` to "pick" entities, etc.
- **Nodes have no Unity-style dotted accessors.** There is no `something.Position` / `something.Velocity` / `something.Transform` / `something.DeltaTime` anywhere in this library. To read world state you always call a **simulation-prefixed** helper that matches the Unity asset for that sim:
  - Volleyball → `VolleyballGetVector3(...)` / `VolleyballGetTransform(...)` / `VolleyballGetBool(...)` / `VolleyballGetFloat(...)` (Vector3 node type in Unity: `SlimeGetVector3`; other nodes: `VolleyballGetTransform`, etc. — see `Assets/_Nodes/`).
  - Survival → `SurvivalGetTransform(...)` / `SurvivalGetFloat(...)` / `SurvivalGetBool(...)`.
  - Parking → `ParkingGetTransform(...)` / `ParkingGetFloat(...)` / `ParkingGetBool(...)`.
  - Demo Derby → `DemoDerbyGetTransform(...)` / `DemoDerbyGetCar(...)` / `CarGetPart(...).PartTransform` / `CarInfo(...).CarTransform`.
  - RacingV2 → `RacingV2GetFloat(...)` / `RacingV2GetBool(...)` / `RacingV2GetCar(...)` / `RacingV2GetWaypoint(...)` / `RacingV2Waypoint(...)` plus the shared modular car stack (`ModularUniformController`, `CarRaycasts`, …). Properties: `InitializeRacingV2` / `ConstructRacingV2Properties`.
  - Soccer → `SoccerGetBool(...)` / `SoccerGetFloat(...)` / `SoccerGetTransform(...)` / `SoccerGetVector3(...)`, with per-player `SoccerController(1..4, …)` and `SoccerPlayerSensors(1..4, …)`.
  - The unprefixed aliases (`GetVector3` / `GetTransform` / `GetBool` / `GetFloat`) are **Volleyball only** — they exist purely for backward-compat with old scripts. Using them in any other sim's graph produces the wrong Unity node and won't deserialize correctly.
  - **Custom Functions** (`CreateFunction` / `CustomFunction`) are reusable Unity subgraphs: params in, return out via **`SetFunctionReturn(fn, body_output)`** (e.g. `Power.Float1` → Return `Any1` In). Body nodes only run when called — not the same as Python `customNodes.py` helpers. See **Default Nodes → Organization → Custom Functions**.
  - To turn any `Transform` node into a world-space `Vector3`, wrap it in `RelativePosition(transform_node, "Self")`.
- Save folders by sim include `Soccer/`, `RacingV2/`, `DemoDerby/`, `Parking/`, etc.
- The `Initialize*` helpers take **positional arguments**, not keyword arguments. There is no `name=`, `country=`, `modifier_llm=`, `save_file=` etc. See each simulation's section for the exact signature.
- There is no `sim` object. Methods like `sim.is_active()`, `sim.get_self_data()`, `sim.get_opponents()`, `sim.set_controls()`, `sim.update()` **do not exist** — if you wrote any of those, you are hallucinating an SDK that isn't here.
- The **`AIGamePyLibrary`** import exposes helpers as **free functions**, not methods on a module object you treat like a `sim` runtime. (**Aialander PyLib** is the same project under that friendly name.)
- The LLM-driven flag is set on the **returned** Properties node: `props.data["modifier"] = "True"`. There is **no** `modifier_llm=`, `is_llm=`, `llm=`, or `isLLM=` keyword argument on any helper.
- Your script must end with a call to **`SaveData("YourBot", "auto")`** or nothing is exported.

## 🚨 CRITICAL: Multi-output Bug (KeyError: 'Bool4', 'Vector32', etc.)

**The most common error LLMs make** when writing Demo Derby or RacingV2 bots is using `CarInfo(...).IsImmobile`, `.Velocity`, `.Health`, `.Rank`, or `CarGetPart(...).HealthPercent` in `ConditionalSetFloat`, comparisons, arithmetic, etc.

```python
# These ALL fail with KeyError in ConnectPorts:
is_stuck = CarInfo(self_car).IsImmobile                    # → 'Bool4'
throttle = ConditionalSetFloat(is_stuck, -1.0, throttle_fwd)
# or: Magnitude(CarInfo(car).Velocity) → 'Vector32'
```

**Fix:** 
- Only use `.CarTransform` and `.PartTransform` from these helpers.
- For stuck detection use **forward raycast sensors** (`HitInfo(ray_f)`) as shown in `Grok.py`.
- See full details in [Multi-output component accessor bug](#multi-output-component-accessor-bug) below.

**`Grok.py` (and `Claude.py`) have been updated with a working sensor-based unstick workaround.** Older versions will hit this exact error.

## Common mistakes

These are the exact mistakes we keep seeing. If your draft does any of them, rewrite it before saving.

| ❌ Don't | ✅ Do |
|---|---|
| `import AIGamePyLibrary as aig` then `aig.InitializeDemoDerby(...)` (treats helpers as methods on a sim object) | `from AIGamePyLibrary import *` and call helpers as free functions |
| `InitializeDemoDerby(name="X", country="USA", modifier_llm=True, save_file="X")` | `props = InitializeDemoDerby("X", "United States of America", "Tan", 0, 0, "Brown", 0, "Red", "")` — positional only |
| `country="USA"` / `country="UK"` / `country="South-Korea"` | Use the exact strings from the Country list, e.g. `"United States of America"`, `"United Kingdom"`, `"South Korea"`. Bot personas: `"ChatGPT"`, `"Claude"`, `"Deepseek"`, `"Gemini"`, `"Grok"`, `"Llama"`, `"Mistral"`, `"Perplexity"`, `"Qwen"` |
| Pass `modifier_llm=True` / `is_llm=True` / `llm=True` to any helper | After init: `props.data["modifier"] = "True"` (see [Marking your bot as LLM-driven](#marking-your-bot-as-llm-driven)) |
| Pass `save_file="X"` to any helper | Saving is a separate call at the end of the script: `SaveData("X", "auto")` |
| `while sim.is_active(): sim.set_controls(...)` style runtime loop | Build the graph once. Unity runs it every tick. There is no loop in your script. |
| `sim.get_self_data()`, `sim.get_opponents()`, `sim.set_controls()`, `sim.update()`, `sim.is_active()` | None of these exist. Use `DemoDerbyGetTransform`, `DemoDerbyGetCar`, `CarInfo`, `CarRaycasts`, `ModularUniformController`, etc. |
| `if dist < 50: throttle = 1.0 else: throttle = 0.5` | `throttle = ConditionalSetFloat(dist < 50, 1.0, 0.5)` |
| `min(opponents, key=lambda o: ...)` / iterating Python lists of game entities | There is no Python-side list of opponents. Use selector nodes like `DemoDerbyGetCar(8)` (nearest active), `CarGetPart(3, car)` (nearest crucial part), `SurvivalGetTransform(3)` (player nearest), etc. |
| `math.atan2(...)`, `math.sqrt(...)`, `math.degrees(...)` | `Operation(x)` (`atan`, `sqrt`, etc.), `Magnitude`, `Distance`, `DotProduct`, `Normalize`, or just rely on `Autosteer(goal)` / `Autothrottle(goal, speed)` for car driving |
| 2D thinking: `pos[0]`, `pos[1]`, `heading` in degrees | Everything is 3D `Vector3`. Access components via `vec.x`, `vec.y`, `vec.z`. There is no scalar "heading". Use `Autosteer` for car aim. |
| `transform.Position` / `transform.position` on a Transform node | `RelativePosition(transform_node, "Self")` returns the world `Vector3` |
| `Self.Position` / `Ball.Position` / `entity.Velocity` / `Self.TeamSpawn` / `Game.DeltaTime` — dotted accessors on a game entity | **Use the simulation-prefixed node helpers everywhere.** Volleyball: `VolleyballGetVector3("Self Position")`, `VolleyballGetVector3("Ball Velocity")`, `VolleyballGetTransform("Self Team Spawn")`, `VolleyballGetBool("Self Can Jump")`, `VolleyballGetFloat("Delta time")`. Other sims have their own helpers (`DemoDerbyGetTransform`, `DemoDerbyGetCar`, `CarGetPart(...).PartTransform`, `SurvivalGetTransform`, `ParkingGetTransform`, etc.). Never assume `.Position` / `.Velocity` / `.Transform` exists on a Node — it does not, and examples that used to show that shortcut have been rewritten. |
| `GetTransform(...)` / `GetBool(...)` / `GetFloat(...)` / `GetVector3(...)` used in Survival / Parking / Demo Derby / Soccer / RacingV2 graphs | Those unprefixed names are **Volleyball-only** backward-compat aliases. In other sims you'll silently build the wrong Unity node. Use the sim prefix: `SurvivalGetTransform` / `ParkingGetTransform` / `DemoDerbyGetTransform` / `SoccerGetTransform` / `RacingV2GetFloat`, etc. |
| Treating `CreateFunction` like `Region`, or like Python `customNodes.py` | Custom Functions change execution: body nodes only run via `CustomFunction(...)` calls; params/optional return are the interface. `Region` is visual-only. |
| Building `Power` / math inside `CreateFunction` but forgetting the return wire | Always call `SetFunctionReturn(fn, powered)` so `Power.Float1` connects to CreateFunction Return (`Any1` In). Without it, `CustomFunction(...)` output is null. |
| Wiring Return to port id `Any` | Return is **`Any1` polarity In** (not `Any`). Param1 Out is also `Any1` — polarity distinguishes them. |
| One `SlimeController` / single controller for Soccer | Soccer needs `SoccerController(1..4, moveTo, sprint, interact)` per player on the team graph |
| `Magnitude(CarInfo(car).Velocity)`, `ClampFloat(CarInfo(car).Health, ...)`, `pos + CarInfo(car).Velocity * dt`, `ConditionalSetFloat(CarGetPart(3, car).HealthPercent < 50, ...)` | **Broken in the current library.** Only `.CarTransform` (on `CarInfo`) and `.PartTransform` (on `CarGetPart`) can be passed to another node — everything else raises `KeyError: 'Vector32'` / `'Bool3'` / `'Bool4'` / `'Float5'` / `'Float6'` / `'Float2'` in `ConnectPorts`. Plan your bot around `Autosteer` / `Autothrottle` + `DemoDerbyGetCar` / `CarGetPart(3, ...).PartTransform` + raycast sensors. See **[Multi-output component accessor bug](#multi-output-component-accessor-bug)**. |
| Forget to call `SaveData(...)` at the end | Always finish with `SaveData("YourBotName", "auto")` — without this the script does literally nothing |

## Side-by-side example

**Wrong (looks like a runtime loop, none of this works):**

```python
import AIGamePyLibrary as aig          # treats helpers as methods on a sim object
sim = aig.InitializeDemoDerby(name="Gemini", country="USA",
                              modifier_llm=True, save_file="Gemini")  # not real kwargs
while sim.is_active():                  # no such method
    me = sim.get_self_data()            # no such method
    for op in sim.get_opponents():      # no such method
        if dist(me, op) < 50:           # plain Python if won't compile to a node
            sim.set_controls(throttle=1.0, steer=0.2)  # no such method
    sim.update()                        # no such method
```

**Right (build a graph, mark it LLM-driven, save it):**

```python
from AIGamePyLibrary import *

props = InitializeDemoDerby(
    "Gemini", "Gemini", "Tan", 0, 2, "Brown", 0, "Blue", "",
)
props.data["modifier"] = "True"   # mark as LLM-driven (see "Marking your bot as LLM-driven")

self_pos = RelativePosition(DemoDerbyGetTransform(0), "Self")
target   = DemoDerbyGetCar(8)                                 # nearest active car
goal     = RelativePosition(CarGetPart(3, target).PartTransform, "Self")

ModularUniformController(Autothrottle(goal, 25.0), Autosteer(goal), Float(0.0))
SaveData("Gemini", "auto")
```

For a slightly fuller derby starter (with sensors and a panic brake) see the **[Minimal complete Demo Derby example](#demo-derby-simulation)**. `Grok.py` now demonstrates a safe, aggressive ramming strategy with sensor-based unsticking that avoids the `KeyError: 'Bool4'` (see the new warning at the top of Notes for LLM Authors).

## Multi-output component accessor bug

> This is a **known library bug**, not an LLM mistake. It's documented here so LLM authors stop writing scripts that hit it.

### What breaks

Any of these will raise a `KeyError` inside `AIGamePyLibrary/lib.py → ConnectPorts` at compile time (when `SaveData(...)` runs, or earlier if the consuming node is constructed first):

```python
# --- all of these crash ---
self_info = CarInfo(DemoDerbyGetCar(2))
self_speed = Magnitude(self_info.Velocity)                          # KeyError: 'Vector32'
is_alive   = self_info.Health > 0                                   # KeyError: 'Float5'
if_imm     = ConditionalSetFloat(self_info.IsImmobile, -1.0, 1.0)   # KeyError: 'Bool4'
rank_ok    = self_info.Rank < 3                                     # KeyError: 'Float6'

# unpacking doesn't save you — the unpacked Nodes are the same broken objects:
car_tf, velocity, is_ai, is_immobile, health, rank = CarInfo(car)
Magnitude(velocity)                                                 # still KeyError: 'Vector32'

# GetCarPart has the same shape of bug:
part = CarGetPart(3, target)
weak = part.HealthPercent < 30                                      # KeyError: 'Float2'
```

### Why it breaks

`CarInfoComponents` and `GetCarPartComponents` store each accessor's `outputIndex` as its **global position** in the node's port list, but `ConnectPorts` builds the Unity port name as `f"{inputType}{outputIndex}"` — which must be the **type-local** port number. Unity's `CarInfo` node publishes `Transform1, Vector31, Bool1, Bool2, Float1, Float2` (type-local), but the Python wrappers ask for `Transform1, Vector32, Bool3, Bool4, Float5, Float6`. Only the first port of each multi-output node (`Transform1`, position 1) lines up by accident.

For reference, here's what each accessor currently does and what port id it asks for:

| Accessor | `outputIndex` | Port name built | Actual Unity port | Status |
|---|---|---|---|---|
| `CarInfo(...).CarTransform` | 1 | `Transform1` | `Transform1` | ✅ works |
| `CarInfo(...).Velocity` | 2 | `Vector32` | `Vector31` | ❌ `KeyError` |
| `CarInfo(...).IsAI` | 3 | `Bool3` | `Bool1` | ❌ `KeyError` |
| `CarInfo(...).IsImmobile` | 4 | `Bool4` | `Bool2` | ❌ `KeyError` |
| `CarInfo(...).Health` | 5 | `Float5` | `Float1` | ❌ `KeyError` |
| `CarInfo(...).Rank` | 6 | `Float6` | `Float2` | ❌ `KeyError` |
| `CarGetPart(...).PartTransform` | 1 | `Transform1` | `Transform1` | ✅ works |
| `CarGetPart(...).HealthPercent` | 2 | `Float2` | `Float1` | ❌ `KeyError` |

`HitInfoComponents` sidesteps this by storing `outputIndex=1` for **both** `WasHit` and `Distance` and instead setting `node.type` to `bool` / `float` so the consumer prefixes the right port type — `CarInfoComponents` and `GetCarPartComponents` would need the same kind of fix.

### What to do until it's fixed

LLM authors: **plan your bot so you never pass the broken accessors into another node.** In practice that's easier than it sounds because the library already gives you graph-side alternatives:

- **Don't velocity-lead the aim.** Skip `target_pos + target_vel * dt`. Let **`Autosteer(goal)`** and **`Autothrottle(goal, speed)`** handle aim + speed management — they already compensate for relative motion and obstacles internally.
- **Don't check self-speed via `Magnitude(CarInfo(...).Velocity)`.** For stuck-recovery, gate on **`CarInfo(self).IsImmobile`**… wait, that's broken too — use `Spherecast` + `CarRaycasts` + `HitInfo` to detect "nose blocked" instead, and flip to reverse on that signal.
- **Don't branch on opponent `Health` or `Rank` from `CarInfo`.** Use the built-in target selectors that already bake those in: `DemoDerbyGetCar(5)` (lowest health), `DemoDerbyGetCar(8)` (nearest active), `DemoDerbyGetCar(12)` (nearest with disabled steering), `DemoDerbyGetCar(20)` (highest ranked), `DemoDerbyGetCar(21)` (lowest ranked), etc. Pick the target by mode, then aim at `CarGetPart(3, target).PartTransform` (nearest crucial part).
- **Don't branch on `CarGetPart(...).HealthPercent`.** `CarGetPart` mode `2` is "weakest part" — use that part's `PartTransform` directly and skip the health comparison.
- **Do keep using `.CarTransform` and `.PartTransform`.** Both resolve to `Transform1` (index 1) and compile correctly — pipe them through `RelativePosition(..., "Self")` to get a world `Vector3`.

#### Substitution cheat sheet

If you find yourself reaching for one of the broken accessors, swap in the pattern on the right instead. Every example on the right compiles against the current library.

| Broken pattern (crashes in `ConnectPorts`) | Safe replacement |
|---|---|
| `speed = Magnitude(CarInfo(self).Velocity)` — reason about own speed | **Skip it.** `Autothrottle(goal, desired_speed)` already manages cruise speed for you. If you absolutely need a "too slow" signal, use `HitInfo(ray_forward)` + `HitInfo(ray_back)` proximity — if the nose is pinned and the rear is clear, you're stuck. |
| `lead = target_pos + CarInfo(target).Velocity * dt` — predict the target | **Skip it.** `Autosteer(goal)` already tracks a moving `Vector3` goal reasonably well. |
| `is_stuck = CarInfo(self).IsImmobile` (then `ConditionalSetFloat(is_stuck, -1.0, throttle_fwd)`) | `front_hit, front_dist = HitInfo(ray_forward)`<br>`rear_hit, rear_dist = HitInfo(ray_back)`<br>`nose_wedged = front_hit & (front_dist < 2.0) & (goal_dist > 6.0)`<br>`rear_clear  = ~rear_hit \| (rear_dist > 4.0)`<br>`reverse_mode = nose_wedged & rear_clear` |
| `finish_them = CarInfo(target).Health < 50` | **Pre-select a weak target instead of branching on health.** `target = DemoDerbyGetCar(5)` (lowest health) or `DemoDerbyGetCar(12)` (nearest with disabled steering). |
| `winning = CarInfo(self).Rank < 3` | **No safe replacement right now.** Drop the rank-based branching — the built-in target selectors already keep you aggressive. |
| `is_ai = CarInfo(target).IsAI` (avoid human targets) | **No safe replacement right now.** Drop the filter — the derby is set up to only pit eligible cars against each other. |
| `weak = CarGetPart(3, target).HealthPercent < 30` | `target_part = CarGetPart(2, target)  # mode 2 = weakest part`<br>`goal = RelativePosition(target_part.PartTransform, "Self")` |

#### Worked example: "`is_stuck = CarInfo(self).IsImmobile`" done right

This is the exact pattern that crashed the reference `claude.py` with `KeyError: 'Bool4'`. Here's the broken version (do not ship) and the raycast-only version (compiles, does the same job):

```python
# ❌ CRASHES at SaveData time with KeyError: 'Bool4'
self_info    = CarInfo(DemoDerbyGetCar(2))
is_stuck     = self_info.IsImmobile                     # outputIndex=4 -> asks for Bool4
throttle_fwd = Autothrottle(goal, 28.0)
throttle     = ConditionalSetFloat(is_stuck, -1.0, throttle_fwd)  # boom
```

```python
# ✅ Same intent, raycast-only, compiles today
sensor = Spherecast(1.2, 12.0)
ray_fl, ray_f, ray_fr, ray_l, ray_r, ray_bl, ray_b, ray_br = CarRaycasts(sensor)
front_hit, front_dist = HitInfo(ray_f)
rear_hit,  rear_dist  = HitInfo(ray_b)

nose_wedged  = front_hit & (front_dist < 2.0) & (goal_dist > 6.0)
rear_clear   = ~rear_hit | (rear_dist > 4.0)
reverse_mode = nose_wedged & rear_clear

throttle_fwd = Autothrottle(goal, 28.0)
throttle     = ConditionalSetFloat(reverse_mode, -1.0, throttle_fwd)
```

Any bot that follows the [Minimal complete Demo Derby example](#demo-derby-simulation) pattern (target car → nearest crucial part → `Autosteer` + `Autothrottle` + a forward raycast for panic-brake, **no `CarInfo` component reads other than `.CarTransform`**) avoids this bug entirely.

</details>
