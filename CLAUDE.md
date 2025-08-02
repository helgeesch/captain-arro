# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Captain Arro is a Python library for generating animated SVG arrows for web interfaces. It provides four distinct arrow generator types with customizable animations, colors, speeds, and directions. The library is zero-dependency and generates clean SVG code suitable for direct HTML embedding.

## Development Commands

### Installation and Setup
```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install just the package
pip install -e .
```

### Testing
```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_moving_flow_arrow_generator.py

# Run single test method
pytest tests/test_base.py::TestAnimatedArrowGeneratorBase::test_generate_svg_template_method

# Run tests without coverage output
pytest --no-cov
```

### Code Quality
```bash
# Format code (line length: 100)
black captain_arro tests examples

# Sort imports 
isort captain_arro tests examples

# Type checking
mypy captain_arro

# Linting
flake8 captain_arro tests examples
```

### Package Building
```bash
# Build distribution packages
python -m build

# Install build tool if needed
pip install build
```

### Running Examples
```bash
# Generate all example SVGs
python examples/basic_usage.py

# Run individual generator scripts (creates _tmp/ outputs)
python captain_arro/generators/flow/moving_flow_arrow_generator.py
python captain_arro/generators/flow/spotlight_flow_arrow_generator.py
python captain_arro/generators/spread/bouncing_spread_arrow_generator.py
python captain_arro/generators/spread/spotlight_spread_arrow_generator.py
```

## Architecture Overview

### Core Design Pattern
The library follows a template method pattern with an abstract base class (`AnimatedArrowGeneratorBase`) defining the SVG generation workflow, and concrete subclasses implementing specific arrow behaviors.

### Generator Hierarchy
```
AnimatedArrowGeneratorBase (abstract)
├── MovingFlowArrowGenerator - Continuous flowing arrows in one direction
├── SpotlightFlowArrowGenerator - Flow arrows with moving spotlight effects
├── BouncingSpreadArrowGenerator - Arrows spreading from center with bounce animation
└── SpotlightSpreadArrowGenerator - Spread arrows with spotlight effects
```

### Key Architectural Concepts

**Speed Configuration**: All generators require either `speed_in_px_per_second` OR `speed_in_duration_seconds` (never both, never neither). The base class calculates the missing value automatically.

**Unique ID Management**: All generators support `unique_id` parameter in `generate_svg()` to prevent CSS/SVG ID collisions when multiple arrows are used on the same page. This is implemented via regex-based ID suffix replacement.

**Two-Category System**:
- **Flow generators** (`flow/`): Arrows move in cardinal directions (`FLOW_DIRECTIONS`: right, left, up, down)
- **Spread generators** (`spread/`): Arrows emanate from center (`SPREAD_DIRECTIONS`: horizontal, vertical)

**Template Method Implementation**: Each generator must implement:
- `_generate_arrow_elements()` - Creates the SVG arrow shapes and positioning
- `_generate_animations()` - Defines CSS keyframe animations
- `_get_transform_distance()` - Calculates animation movement distance
- `_get_unique_id_keys()` - Lists CSS/SVG IDs that need uniqueness suffixes

### Type Safety
The library uses TypeScript-style Literal types for parameters:
- `ANIMATION_TYPES`: CSS animation timing functions
- `FLOW_DIRECTIONS`: Cardinal directions for flow arrows  
- `SPREAD_DIRECTIONS`: Layout orientations for spread arrows

### File Structure Logic
- `constants.py`: Type definitions and literal types
- `generators/base.py`: Abstract base class with common SVG generation logic
- `generators/flow/`: Directional movement generators
- `generators/spread/`: Center-emanating generators
- `examples/`: Demonstration scripts that generate SVG files
- `_tmp/`: Temporary output directory for individual generator scripts

### Testing Architecture
Tests are organized by component with a `ConcreteArrowGenerator` test implementation in `test_base.py` that provides minimal implementations of abstract methods for testing the base class functionality.

### Package Structure
Zero-dependency library targeting Python 3.8+. Uses `py.typed` marker for type hint support. Examples generate actual SVG files in `examples/output/` for documentation and verification.