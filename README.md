# kiwi_mobile

## Cross-Platform Mobile Calculator Application Built with Kivy

### Overview
**kiwi_mobile** is a modern, cross-platform mobile calculator application built using Python and the Kivy framework. Designed with modularity, security, and scalability in mind, it provides a seamless user experience across PC, Android, and iOS platforms. The app replaces unsafe dynamic evaluation with a custom AST (Abstract Syntax Tree) parser and employs the Strategy pattern to easily support advanced operational modes (e.g., Scientific and Programmer calculators).

---

### Key Improvements & Architectural Enhancements

1. **Separation of Concerns (SoC)**
   * Decoupled the graphical user interface (Kivy) from the mathematical business logic. 
   * The core computing engine operates completely independently of UI elements, layouts, and widgets.

2. **MVC Architecture & Strategy Pattern**
   * **Model:** A robust calculation engine (`CalculatorEngine`) that evaluates expressions safely via an AST-based parser instead of relying on native execution.
   * **View:** A clean, responsive Kivy interface responsible solely for rendering UI elements and capturing user inputs.
   * **Controller / Strategy Pattern:** Arithmetic operations (such as `+`, `-`, `%`, `+/-`) are encapsulated via a unified operator interface. This design allows straightforward expansion into specialized modes (e.g., Scientific or Programmer mode).

3. **Enhanced Security**
   * Replaced vulnerable `eval()` execution with safe evaluation mechanisms (`ast.literal_eval` / custom AST traversal).
   * Prevents arbitrary Python code execution vulnerabilities, ensuring secure expression processing.

---

### Project Structure

```text
kiwi_mobile/
│
├── src/
│   ├── __init__.py
│   ├── engine.py                   # Core calculator engine & safe AST evaluator
│   ├── ui.py                       # Kivy-based Graphical User Interface (View)
│   └── strategies/                 # Strategy pattern implementations for operations
│       ├── __init__.py
│       ├── base.py                 # Abstract base class for operation strategies
│       ├── basic.py                # Basic arithmetic (+, -, *, /, ^)
│       ├── programmer.py           # Bitwise logic (AND, OR, XOR, NOT, shifts, MOD)
│       └── scientific.py           # Scientific operations (sqrt, trig, logs, factorial)
│
├── tests/
│   ├── __init__.py
│   ├── test_engine.py              # Tests for AST parser, expression handling & edge cases
│   ├── test_basic_strategies.py    # Unit tests for basic arithmetic strategies
│   ├── test_programmer_strategies.py # Unit tests for bitwise & base-conversion logic
│   ├── test_scientific_strategies.py # Unit tests for trigonometric, logarithmic & root logic
│   └── test_ui.py                  # Kivy UI integration, user input & mode-switching tests
│
├── main.py                         # Application entry point
├── pyproject.toml                  # Poetry project configuration & dependencies
├── requirements.txt                # Exported dependencies
└── pytest.ini                      # Pytest configuration settings
```


# Launch and setup manual

## Usage on PC

1. Install poetry and run: 

```bash
poetry install 
```

2. Launch application on PC:

```bash
poetry run python main.py
```

3. To run tests for the application with comprehencive report do the following:

```bash
poetry run pytest
```

## Installation/launch on Android (iOS) device with specialized Boldozer tool
*Important:* To create the package you need to use Ubuntu 24.04 (or later) environment. Please use wsl if on Windows or VM on MacOS

1. Install system dependencies:
```bash
sudo apt update
sudo apt install -y build-essential ccache git libffi-dev libssl-dev \
    python3-dev python3-pip python3-setuptools zip unzip \
    openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev \
    libncurses5-dev libncursesw5-dev libtinfo5 cmake
```

2. Install buldozer to the poetry dependencies
```bash
poetry add --group dev buildozer cython
```

3. Initialize Buildozer Specification (will create buildozer.spec)
```bash
poetry run buildozer init
```

4. Open created buldozer.spec file and edit the following parameters:

* Application Details:
```bash
title = Mobile Calculator
package.name = calcapp
package.domain = org.example
```

* Source Files & Extentions:
```bash
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
```

* Application Dependencies:
```bash
requirements = python3, kivy==2.3.1
```

* Screen orientation
```bash
orientation = portrait
```

5. Build, Deploy and Run

Enable Developer Options and USB Debugging on your Android device, connect it to your PC via USB cable, and execute:

```bash
poetry run buildozer -v android debug deploy run
```

*Important Note:* On the initial build, Buildozer will automatically download the Android SDK, NDK, and necessary build toolchains. This process requires 10–15 GB of disk space and may take 10–20 minutes. Subsequent builds will be significantly faster.

Alternative: Testing via Kivy Launcher (without compilation)

1. Install Kivy launcher from the Google Play (Play Store)
2. Create a folder on your phone like /sdcard/kivy/calculator and copy main and /src files to the folder. Additionallly create android.txt file near main.py with the following contents:

```bash
title=Calculator
author=pm012
orientation=portrait
```



