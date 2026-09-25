# kiwi_mobile
## Python mobile application (calculator) using Kiwi

What has been improved since previous version.
1. Segregation of Concerns (SoC): Separate UI (Kivy) from mathematical business logic. Business logic should not know about buttons and vidgets.

2. Applied MVC / Strategy Pattern:

* Model: A calculator engine (CalculatorEngine) that works via an AST (abstract syntax tree) or a strict safe parser instead of eval().
* View: Pure Kivy-interface, that is responsible for the desplay and interception of user actions.

* Controller / Operations Strategy: Each arythmetical operation (+, -, %, +/-) can be implemented via unified interface of operators (pattern Strategy), this will allow to simplify addition of new modes
for example: Scintific Calculator, Progrrammers calculator.

3. Vulnurable eval() replaced with safe ast.literal_eval or AST-parcer: Protects code from running Frees code from arbitrary Python code execution vulnerabilities.

Project Structure: 
project_root/
│
├── src/
│   ├── __init__.py
│   ├── engine.py          # Calculator model and safe computing module
│   ├── strategies.py      # Strategies of arithmetical operations
│   └── ui.py              # Kivy UI (View)
│
├── tests/
│   ├── __init__.py
│   ├── test_engine.py     # Tests of logic
│   └── test_strategies.py # Tests for operators and  edge cases testing
│   └── test_ui.py         # Testing UI (kivi)  
├── main.py                # Entry point for the application
├── requirements.txt
└── pytest.ini


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

1. Install rquired libraries:
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

3. Create configuration file for buldozer building tool (will create buildozer.spec)
```bash
poetry run buildozer init
```

4. Open created buldozer.spec file and edit the following parameters:

* Name and package
```bash
title = Mobile Calculator
package.name = calcapp
package.domain = org.example
```

* Entry point and source code
```bash
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
```

* Dependencies (requirements). Define all needed dependencies
```bash
requirements = python3, kivy==2.3.1
```

* Screen orientation
```bash
orientation = portrait
```

5. Switch on developer options on the smarphone and USB debugging, and connect it with USB data cable to PC. Execute the follobing command to build and automatic update:

```bash
poetry run buildozer -v android debug deploy run
```

*Important Note:* During the first launch the Buldozer automatically loads Android SDK, NDK and Android NDK toolchain (it may take 10-20 minutes and will need additional space on the drive ~10-15Gb). Nex builds will need much less time.

Alternative: Testing via Kivy Launcher (without compilation)

1. Install Kivy launcher from the Google Play (Play Store)
2. Create a folder on your phone like /sdcard/kivy/calculator and copy main and /src files to the folder. Additionallly create android.txt file near main.py with the following contents:

```bash
title=Calculator
author=pm012
orientation=portrait
```



