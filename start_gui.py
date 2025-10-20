"""
CFPB Analysis Tool - GUI Launcher
Run this script to start the graphical interface
"""

import sys
import os
import subprocess

def main():
    """Launch the CFPB Analysis GUI"""
    print("🏛️ CFPB Consumer Complaint Analysis Tool")
    print("=" * 50)
    print("Starting GUI interface...")
    
    # Check if gui_app.py exists
    gui_script = "gui_app.py"
    if not os.path.exists(gui_script):
        print(f"❌ Error: {gui_script} not found in current directory")
        print("Make sure you're running this from the project root folder")
        input("Press Enter to exit...")
        return
    
    try:
        # Launch the GUI
        subprocess.run([sys.executable, gui_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching GUI: {e}")
        input("Press Enter to exit...")
    except KeyboardInterrupt:
        print("\n⏹️ GUI closed by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()