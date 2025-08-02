🧰 Step-by-Step Guide: Installing Visual Studio Code

🖥️ What is Visual Studio Code (VS Code)?

Visual Studio Code is a free, open-source code editor developed by Microsoft. It's lightweight yet powerful — and perfect for Python, web, AI, and research-based projects like NOVA.

📋 System Requirements

🪟 Windows
Windows 10 or later (64-bit recommended)
Minimum: 1.6 GHz CPU, 1 GB RAM

🍎 macOS
macOS 10.11 (El Capitan) or later
Intel or Apple Silicon (M1, M2, etc.)


🚀 Part 1: Downloading VS Code

🪟 Windows Instructions:
Go to the official VS Code website:
👉 https://code.visualstudio.com/
Click the green "Download for Windows" button.
Choose "User Installer" (x64) version for most users.
A .exe file will start downloading, named something like:
VSCodeUserSetup-x64-1.89.1.exe

🍎 macOS Instructions:
Visit:
👉 https://code.visualstudio.com/
Click the blue "Download for macOS" button.
The file will download as:
VSCode-darwin-universal.zip
Once downloaded:
Double-click the .zip file.
You’ll get a Visual Studio Code.app file.
Drag and drop it into your Applications folder.


🛠️ Part 2: Installing VS Code

✅ Windows Installation:
Double-click the downloaded .exe file.
The Setup Wizard will launch.
Follow the steps:
Accept license terms.
Choose installation location (default is fine).
On “Select Additional Tasks”, check these options:
✅ Add "Open with Code" to context menu
✅ Add to PATH (important for terminal use)
Click Install and wait for it to finish.
Click Finish and launch VS Code.

✅ macOS Installation:
After dragging Visual Studio Code.app into Applications:
Open Launchpad or Finder > Applications
Double-click Visual Studio Code
You may see a "Security" warning (because it’s downloaded from the internet):
Click Open.


🧪 Part 3: Add code Command to Terminal (Very Useful)

🪟 Windows:
VS Code adds the code command to terminal if you checked “Add to PATH.”
To verify:
Open Command Prompt or PowerShell.
Type:
code .
It should open VS Code in the current folder.

🍎 macOS:
Open VS Code.
Press Cmd+Shift+P (opens Command Palette).
Type:
Shell Command: Install 'code' command in PATH
Press Enter.
To test:
code .
