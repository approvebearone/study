# CLAUDE.md

This file provides guidance for AI assistants working on this repository.

## Project Overview

This is a Python study/learning repository containing two independent modules:

1. **`barcode_system/`** - A CLI-based inventory management system using barcodes as keys
2. **`sky/`** - A Raspberry Pi hardware controller for motors and sensors

The project is intentionally lightweight (no formal packaging, no CI/CD) and serves as a learning/prototyping environment.

---

## Repository Structure

```
study/
├── CLAUDE.md                    # This file
├── study_test.py                # Root-level test placeholder
├── barcode_system/
│   ├── __init__.py
│   ├── inventory.py             # Core Inventory class
│   └── main.py                  # Interactive CLI entry point
└── sky/
    ├── __init__.py
    ├── controller.py            # Raspberry Pi controller (motors + sensors)
    └── README.md                # Hardware setup and pin mapping docs
```

---

## Modules

### `barcode_system/`

A simple in-memory inventory management system operated via a REPL CLI.

**Key file:** `barcode_system/inventory.py`
- `Inventory` class: stores stock as `{barcode: quantity}` dict
- Methods: `add(barcode, qty)`, `remove(barcode, qty)`, `get_quantity(barcode)`, `all_items()`
- Raises `ValueError` for invalid operations (negative qty, barcode not found, insufficient stock)

**Entry point:** `barcode_system/main.py`
- Run with: `python barcode_system/main.py` (from repo root) or `python main.py` (from `barcode_system/`)
- Commands: `a` = add, `r` = remove, `q` = quit
- Note: imports `from inventory import Inventory` so must be run from within the `barcode_system/` directory

### `sky/`

A Raspberry Pi controller for a winch + stepper motor system with sensor feedback.

**Key file:** `sky/controller.py`
- **Classes:**
  - `WinchMotor(cw_pin, ccw_pin)`: DC motor with CW/CCW rotation and stop
  - `StepperMotor(a_pin, b_pin)`: Stepper motor with two positions (A and B)
  - `Sensor(pin)`: Generic sensor wrapper with state tracking (`.detected()`, `.set_state()`, `.reset()`)
  - `PowerRelay(pin)`: Relay for cutting power
  - `Controller`: Orchestrates all hardware; `run()` executes the main control loop

**Run:** `python sky/controller.py`

**GPIO Pin Mapping (BCM mode):**

| Pin | Function |
|-----|----------|
| 5   | Winch Motor CW (시계 방향) |
| 6   | Winch Motor CCW (반시계 방향) |
| 13  | Stepper Motor Position A |
| 19  | Stepper Motor Position B |
| 17  | Metal Detection Sensor |
| 27  | Safety Proximity Sensor |
| 22  | Descent Detection Sensor |
| 26  | Power Relay |

**GPIO fallback:** When `RPi.GPIO` is not available (non-Raspberry Pi machines), the module substitutes a mock GPIO that prints output calls, allowing logic testing without hardware.

**Control loop sequence (`Controller.run()`):**
1. If safety proximity sensor fires → cut power and exit
2. Rotate winch CW; if metal sensor detects → move stepper to position A
3. Wait 0.5s, rotate winch CCW
4. If descent sensor detects → move stepper to position B, reset both sensors
5. Wait 0.1s, repeat

---

## Development Conventions

### Language
- Code and docstrings are in **English**
- Inline comments include **Korean** translations for hardware-specific concepts (for educational clarity)

### Code Style
- No linting or formatting tools are configured; follow PEP 8 conventions
- Use type hints on function signatures where practical (see `inventory.py` and `controller.py`)
- Raise `ValueError` for domain-level input errors; do not use bare `except`

### No Formal Package Management
- No `requirements.txt` or `pyproject.toml`
- Only stdlib and optional `RPi.GPIO` (hardware-only, gracefully handled)
- Do not add unnecessary dependencies

---

## Testing

Currently minimal — `study_test.py` at the repo root is a placeholder (`print("hi")`).

- No test runner is configured (no pytest, unittest, etc.)
- To test inventory logic manually: run `python main.py` from `barcode_system/`
- To test sky controller without hardware: run `python sky/controller.py` from repo root — GPIO mock will activate automatically

**If adding tests:** pytest is the recommended framework. Place tests in a `tests/` directory mirroring the module structure.

---

## Running the Code

```bash
# Inventory system (run from barcode_system/ directory)
cd barcode_system
python main.py

# Sky controller (run from repo root)
python sky/controller.py
```

---

## Git Workflow

- Main branch: `master`
- Feature branches follow the pattern: `<username>/codex/<description>` or `claude/<task-id>`
- PRs are used to merge features into `master`
- Commits are small and descriptive (see git log for style reference)
