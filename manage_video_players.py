import subprocess
import shutil
import sys
import platform
import os
import distro  # We'll need to add this package for better Linux distro detection

# ANSI escape codes for color and styling
COLORS = {
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "bold": "\033[1m",
    "underline": "\033[4m",
    "reset": "\033[0m"
}

# Development Information
DEV_INFO = {
    "name": "Video Player Manager",
    "version": "2.0.0",
    "author": "HAMNA TEC",
    "license": "MIT",
    "description": "Universal Video Player Manager for Linux Systems"
}

video_players = {
    "1": {"name": "VLC Media Player", "pkg": "vlc"},
    "2": {"name": "MPV Media Player", "pkg": "mpv"},
    "3": {"name": "SMPlayer", "pkg": "smplayer"},
    "4": {"name": "MPlayer", "pkg": "mplayer"},
    "5": {"name": "Celluloid", "pkg": "celluloid"},
    "6": {"name": "Xine Player", "pkg": "xine-ui"}
}

def get_system_info():
    """Get detailed system information"""
    try:
        system_info = {
            "OS": f"{platform.system()} {platform.release()}",
            "Distribution": f"{distro.name()} {distro.version()}",
            "Architecture": platform.machine(),
            "Processor": platform.processor(),
            "Python Version": platform.python_version(),
            "Memory": get_memory_info()
        }
        return system_info
    except Exception as e:
        return {"Error": f"Could not retrieve full system information: {str(e)}"}

def get_memory_info():
    """Get system memory information"""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
            total = [l for l in lines if 'MemTotal' in l][0]
            return total.split()[1:][0] + ' ' + total.split()[1:][1]
    except:
        return "Unknown"

def print_header():
    """Print a professional header with development and system information"""
    width = 80
    print("╔" + "═" * (width-2) + "╗")
    print_centered(f"{DEV_INFO['name']} v{DEV_INFO['version']}", width)
    print_centered(f"by {DEV_INFO['author']}", width)
    print("╠" + "═" * (width-2) + "╣")
    
    # System Information
    sys_info = get_system_info()
    for key, value in sys_info.items():
        print_centered(f"{key}: {value}", width)
    
    print("╠" + "═" * (width-2) + "╣")
    print_centered("Package Manager: " + (get_package_manager() or "Not detected"), width)
    print("╚" + "═" * (width-2) + "╝\n")

def print_centered(text, width):
    """Print text centered within the given width"""
    padding = (width - len(text) - 2) // 2
    print("║" + " " * padding + text + " " * (width - padding - len(text) - 2) + "║")

def get_package_manager():
    """Detect the package manager based on the Linux distribution."""
    if shutil.which("apt"):
        return "apt"
    elif shutil.which("dnf"):
        return "dnf"
    elif shutil.which("pacman"):
        return "pacman"
    elif shutil.which("zypper"):
        return "zypper"
    else:
        return None

def color(text, c):
    return f"{COLORS[c]}{text}{COLORS['reset']}"

def is_installed(pkg_name, package_manager):
    """Check if a package is installed using the detected package manager."""
    if package_manager == "apt":
        command = ["dpkg", "-s", pkg_name]
    elif package_manager == "dnf":
        command = ["dnf", "list", "installed", pkg_name]
    elif package_manager == "pacman":
        command = ["pacman", "-Q", pkg_name]
    elif package_manager == "zypper":
        command = ["zypper", "search", "--installed-only", pkg_name]
    else:
        print(color("Error: Could not determine package manager.", "red"))
        return False

    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def print_menu():
    """Print the main menu"""
    print(color("\n╔════ Available Video Players ════╗", "cyan"))
    for num, player in video_players.items():
        status = is_installed(player['pkg'], get_package_manager())
        status_text = color("✓ Installed", "green") if status else color("✗ Not Installed", "red")
        print(f"║ {color(num, 'yellow')}. {player['name']:<20} {status_text:<15} ║")
    print(color("╚════════════════════════════════╝", "cyan"))
    print(f"\nEnter {color('1-6', 'yellow')} to manage a player, or {color('q', 'red')} to quit\n")

def get_user_choice():
    """Get user's menu choice"""
    while True:
        choice = input(color("Your choice → ", "cyan")).lower().strip()
        if choice == 'q':
            print(color("\n👋 Thank you for using Video Player Manager!\n", "blue"))
            sys.exit(0)
        if choice in video_players:
            return video_players[choice]['pkg']
        print(color("⚠️  Invalid choice. Please enter a number between 1-6 or 'q' to quit.\n", "red"))

def install_package(pkg, package_manager):
    print(color(f"\n📥 Installing {pkg} using {package_manager}...\n", "blue"))
    if package_manager == "apt":
        subprocess.call(["sudo", "apt", "update"])
        subprocess.call(["sudo", "apt", "install", "-y", pkg])
    elif package_manager == "dnf":
        subprocess.call(["sudo", "dnf", "install", "-y", pkg])
    elif package_manager == "pacman":
        subprocess.call(["sudo", "pacman", "-Sy", "--noconfirm", pkg])
    elif package_manager == "zypper":
        subprocess.call(["sudo", "zypper", "install", "-y", pkg])
    else:
        print(color(f"❌ Cannot install: Unsupported package manager '{package_manager}'.", "red"))
        return

    if is_installed(pkg, package_manager):
        print(color(f"\n✅ {pkg} has been successfully installed.\n", "green"))
    else:
        print(color(f"\n⚠️ Installation of {pkg} may have failed. Please check manually.\n", "yellow"))

def uninstall_package(pkg, package_manager):
    print(color(f"\n🗑️  Uninstalling {pkg} using {package_manager}...\n", "blue"))
    if package_manager == "apt":
        subprocess.call(["sudo", "apt", "remove", "-y", pkg])
        subprocess.call(["sudo", "apt", "autoremove", "-y"])
    elif package_manager == "dnf":
        subprocess.call(["sudo", "dnf", "remove", "-y", pkg])
    elif package_manager == "pacman":
        subprocess.call(["sudo", "pacman", "-R", "--noconfirm", pkg])
    elif package_manager == "zypper":
        subprocess.call(["sudo", "zypper", "remove", "-y", pkg])
    else:
        print(color(f"❌ Cannot uninstall: Unsupported package manager '{package_manager}'.", "red"))
        return

    if not is_installed(pkg, package_manager):
        print(color(f"\n✅ {pkg} has been successfully removed.\n", "green"))
    else:
        print(color(f"\n⚠️ Uninstallation of {pkg} may have failed or requires manual intervention.\n", "yellow"))

def main():
    # Check if required package is installed
    try:
        import distro
    except ImportError:
        print(color("\n⚠️  Installing required package 'distro'...", "yellow"))
        subprocess.call([sys.executable, "-m", "pip", "install", "distro"])
        import distro

    print_header()
    
    package_manager = get_package_manager()
    if not package_manager:
        print(color("⚠️ Could not detect a supported package manager.", "red"))
        print(color("Supported package managers: apt, dnf, pacman, zypper", "yellow"))
        sys.exit(1)

    while True:
        print_menu()
        choice = get_user_choice()
        
        if is_installed(choice, package_manager):
            print(color(f"\n✓ {choice} is currently installed.", "green"))
            if input(color("Do you want to uninstall it? (y/N): ", "yellow")).lower() == 'y':
                uninstall_package(choice, package_manager)
        else:
            print(color(f"\n✗ {choice} is not installed.", "red"))
            if input(color("Do you want to install it? (y/N): ", "yellow")).lower() == 'y':
                install_package(choice, package_manager)
        
        if input(color("\nWould you like to perform another action? (y/N): ", "yellow")).lower() != 'y':
            print(color("\n👋 Thank you for using Video Player Manager!\n", "blue"))
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(color("\n\n👋 Program terminated by user. Goodbye!\n", "blue"))
        sys.exit(0)

