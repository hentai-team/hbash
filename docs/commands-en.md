# hbash CLI Commands Documentation

## Overview
hbash is a powerful terminal emulator with extensive file management, system monitoring, and utility features. Here's a comprehensive list of available commands and their functionality.

## Basic Commands

### System & Navigation
- `quit` - Exit the terminal
- `help` - Display help information about commands
- `whoami` - Show current user name
- `clear` (or `cls`) - Clear terminal screen
- `ver` - Display HTerm version information
- `echo [options] <text>` - Print text to terminal
    - `-u` - Convert to uppercase
    - `-l` - Convert to lowercase
    - `-sc` - Swap case
    - `-r` - Reverse text
    - `-se` - Separate letters with spaces

### File Operations
- `ls` - List directory contents
- `cd <path>` - Change directory
- `pwd` - Print working directory
- `cp <source> <destination>` - Copy files/directories
- `mv <source> <destination>` - Move/rename files/directories
- `rm [-r] <path>` - Remove files/directories
    - `-r` - Remove recursively
- `mkdir <directory>` - Create new directory
- `touch <file>` - Create empty file or update timestamp
- `cat <file>` - Display file contents

### File Search & Analysis
- `find <pattern> [-d|-f]` - Search for files/directories
    - `-d` - Search directories only
    - `-f` - Search files only
- `grep <pattern> <file> [-i] [-n]` - Search text in files
    - `-i` - Case insensitive search
    - `-n` - Show line numbers
- `diff <file1> <file2>` - Compare two files
- `head [-n lines] <file>` - Show first lines of file
- `tail [-n lines] <file>` - Show last lines of file
- `wc <file> [-l|-w|-c]` - Count lines/words/bytes in file

### System Information
- `uname [options]` - Display system information
    - `-a` - All information
    - `-s` - Kernel name
    - `-n` - Network node hostname
    - `-r` - Kernel release
- `ps [-a]` - List processes
- `top` - Interactive process viewer
- `df [-h]` - Show disk space usage
- `free [-h]` - Display memory usage
- `uptime` - Show system uptime

### Network Tools
- `ping <host> [-c count]` - Test network connectivity
- `ifconfig` - Display network interfaces
- `netstat` - Show network connections
- `wget <url>` - Download files from web
- `curl` - Transfer data from/to servers
- `ssh <user>@<host>` - Secure shell connection
- `scp <source> <destination>` - Secure file copy

### Archive Management
- `zip <archive.zip> <files...> [-r]` - Create ZIP archive
- `unzip <archive.zip> [destination]` - Extract ZIP archive
- `tar [-c|-x] -f <archive.tar> [files...]` - Work with TAR archives
- `gzip <file>` - Compress files with GZIP
- `gunzip <file.gz>` - Decompress GZIP files

### User Management
- `adduser` - Add new user (root only)
- `deluser` - Delete user (root only)
- `login` - Log into system
- `logout` - Log out current user

### Utilities
- `calc <expression>` - Calculator
- `time` - Show current date/time
- `weather <city>` - Show weather forecast
- `todo` - Task management system
- `note` - Note-taking system
- `calendar [month] [year]` - Display calendar
- `timer <start|stop> [seconds]` - Countdown timer
- `stopwatch <start|stop|lap>` - Stopwatch function

### Text Editor
- `edit <filename>` - Open text editor
    - Commands within editor:
    - `^X` - Exit
    - `^O` - Save
    - `^W` - Show cursor position
    - `^K` - Cut line
    - `^U` - Paste

## Shell Features
- Command history
- Aliases
- Environment variables
- Color support
- Unicode support
- Multi-language support

## Additional Information
For detailed information about any command, use:
```bash
help <command>
# or
man <command>
```