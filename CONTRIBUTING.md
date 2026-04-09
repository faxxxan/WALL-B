# Contributing to WALL-B

Thank you for your interest in contributing to WALL-B! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Report Bugs](#how-to-report-bugs)
- [How to Suggest Features](#how-to-suggest-features)
- [Pull Request Process](#pull-request-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Development Setup](#development-setup)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)

---

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Examples of behavior that contributes to a positive environment:**

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Examples of unacceptable behavior:**

- The use of sexualized language or imagery and unwelcome sexual attention
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances.

---

## How to Report Bugs

### Before Submitting a Bug Report

1. **Search existing issues:**
   - Check if the bug has already been reported
   - Look for closed issues with similar descriptions

2. **Verify the bug:**
   - Try to reproduce the bug with the latest version
   - Test with default configurations

3. **Collect information:**
   - Your hardware configuration
   - Software versions (Python, ROS2, Arduino)
   - Error messages and logs
   - Steps to reproduce

### Bug Report Template

When submitting a bug report, please include:

```markdown
**Bug Description:**
A clear description of the bug.

**Steps to Reproduce:**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior:**
What you expected to happen.

**Actual Behavior:**
What actually happened.

**Environment:**
- Hardware: [e.g., Raspberry Pi 5, Arduino Mega 2560]
- Software: [e.g., Raspberry Pi OS 64-bit, ROS2 Humble]
- Python Version: [e.g., 3.10.11]
- Branch/Commit: [e.g., main, a1b2c3d]

**Logs:**
```
[Paste relevant error messages or logs here]
```

**Additional Context:**
Any other context about the problem.
```

### Where to Submit

Submit bugs to our [GitHub Issues](https://github.com/faxxxan/WALL-B/issues) with the label `bug`.

---

## How to Suggest Features

We welcome feature suggestions that improve the WALL-B robot project!

### Before Submitting a Feature Request

1. **Check existing feature requests:**
   - Review open and closed feature requests
   - Consider if the feature aligns with project goals

2. **Consider the scope:**
   - Is the feature feasible with current hardware?
   - Will it benefit the broader community?

### Feature Request Template

```markdown
**Feature Summary:**
A brief summary of the feature.

**Problem Statement:**
What problem does this feature solve?

**Proposed Solution:**
Describe your proposed solution.

**Alternatives Considered:**
Describe alternative solutions you've considered.

**Use Cases:**
List specific use cases for this feature.

**Additional Context:**
Any other context, mockups, or examples.
```

### Where to Submit

Submit feature requests to our [GitHub Issues](https://github.com/faxxxan/WALL-B/issues) with the label `enhancement`.

---

## Pull Request Process

### Development Workflow

1. **Fork the repository:**
   ```bash
   # Click "Fork" on GitHub
   # Clone your fork
   git clone https://github.com/YOUR_USERNAME/WALL-B.git
   cd WALL-B
   ```

2. **Create a feature branch:**
   ```bash
   # Create and switch to new branch
   git checkout -b feature/your-feature-name
   # Or for bug fixes:
   git checkout -b fix/issue-description
   ```

3. **Make your changes:**
   - Follow the code style guidelines
   - Write tests for new functionality
   - Update documentation as needed

4. **Commit your changes:**
   ```bash
   # Stage changes
   git add .

   # Commit with descriptive message
   git commit -m "Add: feature description"

   # Follow commit message format:
   # Add: - new feature
   # Fix: - bug fix
   # Update: - update existing feature
   # Refactor: - code refactoring
   # Docs: - documentation changes
   # Test: - adding or updating tests
   ```

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request:**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template

### Pull Request Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature)
- [ ] Documentation update

## Testing
Describe testing performed.

## Checklist
- [ ] Code follows style guidelines
- [ ] Code has been linted
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No console errors in normal operation

## Related Issues
Link any related issues: Fixes #123
```

### Review Process

1. **Automated checks:**
   - CI/CD pipeline must pass
   - All tests must pass
   - Code style must conform

2. **Code review:**
   - Maintainer review within 1 week
   - Address feedback constructively
   - Make requested changes

3. **Merge criteria:**
   - At least one maintainer approval
   - All checks passing
   - No unresolved discussions

---

## Code Style Guidelines

### Python Code Style

We follow PEP 8 with some modifications:

```bash
# Install linting tools
pip install flake8 black isort

# Format code before committing
black python/
isort python/
flake8 python/
```

**Key guidelines:**

- Line length: 100 characters (Black default)
- Use 4 spaces for indentation
- Use descriptive variable names
- Add docstrings to all functions and classes
- Type hints encouraged for function signatures

**Example:**

```python
from typing import List, Optional


class ServoController:
    """Controller for managing servo motors.

    Handles PWM signal generation and position tracking
    for the WALL-B robot's servo motors.
    """

    def __init__(self, port: str, baud_rate: int = 115200) -> None:
        """Initialize servo controller.

        Args:
            port: Serial port for communication
            baud_rate: Communication speed (default: 115200)
        """
        self._port = port
        self._baud_rate = baud_rate
        self._servos: List[int] = []

    def add_servo(self, servo_id: int) -> None:
        """Add a servo to the controller.

        Args:
            servo_id: Unique identifier for servo
        """
        if servo_id not in self._servos:
            self._servos.append(servo_id)

    def set_position(self, servo_id: int, position: int) -> bool:
        """Set servo to target position.

        Args:
            servo_id: Servo identifier
            position: Target position in microseconds

        Returns:
            True if command sent successfully
        """
        if servo_id not in self._servos:
            return False
        return self._send_command(servo_id, position)
```

### Arduino/C++ Code Style

```cpp
// Use meaningful names
const int SERVO_PIN_LEFT_KNEE = 45;
const int NEUTRAL_POSITION = 1500;

// Functions should have clear purposes
void initializeServos() {
    // Initialize all servo pins
}

void setServoPosition(int servoId, int position) {
    // Set servo to position
}

// Use namespaces for organization
namespace WallB {
    namespace Config {
        constexpr uint16_t BAUD_RATE = 115200;
        constexpr uint8_t SERVO_COUNT = 22;
    }
}
```

### ROS2 Code Style

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class ServoController(Node):
    """ROS2 node for servo control."""

    def __init__(self) -> None:
        """Initialize servo controller node."""
        super().__init__('servo_controller')
        self._publisher = self.create_publisher(
            JointState,
            'joint_states',
            10
        )
        self._timer = self.create_timer(
            0.1,
            self._timer_callback
        )

    def _timer_callback(self) -> None:
        """Timer callback for publishing states."""
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        self._publisher.publish(msg)
```

---

## Development Setup

### Prerequisites

```bash
# Required software
- Python 3.10+
- ROS2 Humble or Iron
- Arduino CLI or Arduino IDE
- Git
```

### Clone and Install

```bash
# Clone repository
git clone https://github.com/faxxxan/WALL-B.git
cd WALL-B

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_servo.py -v

# Run with coverage
pytest --cov=python tests/

# Run ROS2 tests
colcon test --event-handler console_direct
```

### Pre-commit Hooks

We use pre-commit hooks to ensure code quality:

```bash
# Run manually
pre-commit run --all-files

# Update hooks
pre-commit autoupdate
```

---

## Testing Guidelines

### Test Structure

```
tests/
├── unit/           # Unit tests
│   ├── test_servo.py
│   └── test_serial.py
├── integration/    # Integration tests
│   └── test_robot.py
└── fixtures/       # Test fixtures
    └── robot.yaml
```

### Writing Tests

```python
import pytest
from wallb.servo import ServoController


class TestServoController:
    """Tests for ServoController class."""

    @pytest.fixture
    def controller(self, mock_serial):
        """Create controller with mocked serial."""
        return ServoController('/dev/ttyUSB0')

    def test_initialization(self, controller):
        """Test controller initializes correctly."""
        assert controller.is_connected()
        assert len(controller.servos) == 0

    def test_add_servo(self, controller):
        """Test adding a servo."""
        controller.add_servo(0)
        assert 0 in controller.servos

    def test_set_position(self, controller):
        """Test setting servo position."""
        controller.add_servo(0)
        result = controller.set_position(0, 1500)
        assert result is True

    def test_invalid_servo_id(self, controller):
        """Test setting invalid servo ID."""
        result = controller.set_position(999, 1500)
        assert result is False
```

### Test Coverage Requirements

- Minimum 80% code coverage for new code
- All bug fixes must include a regression test
- Integration tests for all major features

---

## Documentation Standards

### Code Documentation

Every function and class must have:

1. **Docstrings** in Google style format
2. **Type hints** for parameters and return values
3. **Examples** for complex functions

```python
def calculate_inverse_kinematics(
    target_x: float,
    target_y: float,
    target_z: float
) -> List[float]:
    """Calculate joint angles for target position.

    Uses inverse kinematics to determine the joint angles
    required to reach a target position in 3D space.

    Args:
        target_x: X coordinate in millimeters
        target_y: Y coordinate in millimeters
        target_z: Z coordinate in millimeters

    Returns:
        List of joint angles in degrees [hip, knee, ankle]

    Raises:
        ValueError: If target is out of reach

    Example:
        >>> angles = calculate_inverse_kinematics(50, 0, 100)
        >>> print(angles)
        [15.2, -30.5, 15.3]
    """
    pass
```

### README Updates

When adding new features, update relevant documentation:

- Update README.md with new features
- Add new module documentation
- Include usage examples
- Document any new dependencies

### API Documentation

For public APIs:

```markdown
## API Reference

### ServoController

#### Methods

##### `set_position(servo_id: int, position: int) -> bool`
Set servo to target position.

**Parameters:**
- `servo_id` (int): Unique servo identifier
- `position` (int): Target position in microseconds (500-2500)

**Returns:** `bool` - True if successful

**Raises:** `SerialException` if communication fails
```

---

## Recognition

Contributors who have significant impact will be recognized in:

- README.md contributors section
- Release notes
- Project documentation

---

## Questions?

If you have questions about contributing:

1. Check the [GitHub Discussions](https://github.com/faxxxan/WALL-B/discussions)
2. Search existing issues
3. Create a new issue with the `question` label

---

Thank you for contributing to WALL-B!
