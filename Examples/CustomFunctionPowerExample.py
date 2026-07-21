"""
Custom Function + Power — canonical LLM pattern
===============================================

Goal: reusable Power(base, exponent) whose Float1 result is the function Return,
so each CustomFunction call can pass different variables and read the result.

REQUIRED wiring (do not skip):
  1. CreateFunction("Name")                         # definition
  2. Power(fn.Param1, fn.Param2)                    # body uses param outs
  3. AssignToFunction(powered, fn)                  # mark Power as body-owned
  4. SetFunctionReturn(fn, powered)                 # Power.Float1 → Return (Any)
  5. CustomFunction("Name", base, exponent)         # call site; output = Return
"""

from AIGamePyLibrary import *

# --- 1) Define the function -------------------------------------------------
fn = CreateFunction("PowerFn")

# Optional human-readable labels for Param1 / Param2
ConnectPorts(("String1", "String1"), String("base"), fn.node)
ConnectPorts(("String1", "String2"), String("exponent"), fn.node)

# --- 2–4) Body: Power → assign to function → wire Float1 to Return ----------
# Param1 = base (Any1 Out), Param2 = exponent (Any2 Out)
# Power outputs Float1 — MUST connect to CreateFunction Return:
#   Return port id = "Any1", polarity In  (GameObject "Any - In")
powered = AssignToFunction(Power(fn.Param1, fn.Param2), fn)
SetFunctionReturn(fn, powered)  # Power.Float1 → CreateFunction.Any1 (In / Return)

# --- 5) Call with 3 different inputs; Debug the returned Float --------------
# Each CustomFunction output is the wired Return (Power result).
out_a = CustomFunction("PowerFn", Float(2), Float(3))       # 2^3 = 8
Debug(out_a, "2^3 (expect 8)", changePosition=False)

out_b = CustomFunction("PowerFn", Float(5), Float(2))       # 5^2 = 25
Debug(out_b, "5^2 (expect 25)", changePosition=False)

out_c = CustomFunction("PowerFn", Float(10), Float(0.5))    # 10^0.5 ≈ 3.16
Debug(out_c, "10^0.5 (expect ~3.16)", changePosition=False)

SaveData("PowerFunctionTest.txt", "grid")
print("Wrote PowerFunctionTest.txt")
