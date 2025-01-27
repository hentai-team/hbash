# HBash - Advanced Terminal Emulator

![HBash Logo](assets/hterm-logo.png)

## Overview
HBash is a feature-rich terminal emulator written in Python that provides a modern command-line interface with extensive functionality, user management, and customization options.

## Features

### Core Features
- User authentication and management
- Multi-language support (English, Russian)
- Colorful and customizable interface
- Command history
- Aliases support
- Cron-like task scheduling

### File Operations
- Basic file operations (cp, mv, rm, mkdir, touch)
- File content viewing and manipulation (cat, head, tail)
- File searching and comparison (find, grep, diff)
- Archive management (zip, unzip, tar, gzip)

### System Tools
- System monitoring (ps, top, df, free)
- Network utilities (ping, ifconfig, ssh, scp)
- Process management
- Resource monitoring

### Additional Tools
- Text editor with syntax highlighting
- Todo list manager
- Note-taking system
- Calendar
- Weather information
- Timer and stopwatch

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hterm.git
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting HTerm
```bash
python hterm.py
```

### Basic Commands
- `help` - Display available commands
- `quit` - Exit HTerm
- `clear` - Clear screen
- `ver` - Show version information

### User Management
- `login` - Log into the system
- `logout` - Log out current user
- `adduser` - Add new user (root only)
- `deluser` - Delete user (root only)

### Additional Documentation

Detailed documentation for commands is available in the docs folder in different languages:
[English](docs/COMMANDS-EN.md) | [Russian](docs/COMMANDS-RU.md) | [Japanese](docs/COMMANDS-JP.md) | [Chinese](docs/COMMANDS-CH.md)


## Configuration
- Default configuration stored in `config.json`
- Language settings in `localization` directory
- User data in `users.json`

## Customization
- Custom color schemes
- Configurable prompt
- Aliases for frequently used commands
- Personal settings per user

## Requirements
- Python 3.7+
- Required packages listed in requirements.txt

## Contributing
Contributions are welcome! Please feel free to submit pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support, please open an issue in the GitHub repository.