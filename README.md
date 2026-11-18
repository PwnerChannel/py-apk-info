# py-apk-info

A lightweight command-line Python script that scans the current directory for .apk files and displays detailed metadata from them.

### What it extracts:
- App name (Label) and package name
- Version name and code
- Min and Target SDKs (translated into actual Android names, like Android 14, 15, etc.)
- Supported CPU architectures (ARMv7, ARM64, x86, or marked as pure Java/Kotlin)
- File size, main activity class, icon path, and total permission count

### Setup

Just install the parser library:

```bash
pip install pyaxmlparser
```

### Usage

Drop scanner.py into the folder containing your APKs, open your terminal or command prompt right in that directory, and run:

```bash
python scanner.py
```
