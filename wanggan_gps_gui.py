"""
Wanggan GPS Device - EasyGUI Interface

A user-friendly graphical interface for downloading GPS data from Wanggan handheld devices.
Designed for non-technical users with simple, intuitive controls.

Author: Hélio Teixeira
License: MIT
"""

import easygui
import os
import sys
from pathlib import Path
from typing import Optional, List
import subprocess
import platform

# Import serial port detection
try:
    import serial.tools.list_ports
except ImportError:
    easygui.msgbox(
        "Missing required library 'pyserial'.\n\n"
        "Please install it using:\npip install pyserial",
        "Installation Required"
    )
    sys.exit(1)

# Import the main GPS library
try:
    from wanggan_gps import WangganGPS, DownloadMode, OutputFormat
except ImportError:
    easygui.msgbox(
        "Could not import wanggan_gps.py\n\n"
        "Please ensure wanggan_gps.py is in the same directory as this GUI.",
        "Import Error"
    )
    sys.exit(1)


class WangganGPSGUI:
    """
    Main GUI application class for Wanggan GPS device interface.
    Manages the user interaction flow from connection to data export.
    """
    
    def __init__(self):
        """Initialize the GUI application with default settings."""
        self.gps: Optional[WangganGPS] = None
        self.connected = False
        
        # Default settings (sensible defaults for most users)
        self.port = "COM5"
        self.baudrate = 115200
        self.timeout = 1.0
        self.output_dir = "downloads"
        self.auto_create_dir = True
        
        # Application metadata
        self.app_title = "Wanggan GPS Data Downloader"
        self.version = "1.0.0"
    
    def get_available_ports(self) -> List[str]:
        """
        Detect all available serial ports on the system.
        
        Returns:
            List of port names (e.g., ['COM1', 'COM5', '/dev/ttyUSB0'])
        """
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        
        if not port_list:
            # If no ports detected, provide common defaults
            if platform.system() == "Windows":
                port_list = ["COM1", "COM3", "COM5", "COM7"]
            else:
                port_list = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyACM0"]
        
        return port_list
    
    def show_welcome_screen(self) -> bool:
        """
        Display welcome message and initial instructions.
        
        Returns:
            True if user wants to continue, False to exit
        """
        message = (
            "Welcome to Wanggan GPS Data Downloader!\n\n"
            "This application helps you download GPS data from your Wanggan device "
            "and convert it to popular formats like GPX, KML, and CSV.\n\n"
            "✅ Tested on: Wanggan D6E GNSS Handheld Navigator\n"
            "⚠️  May work with other Wanggan GPS models\n\n"
            "Before starting:\n"
            "1. Connect your GPS device to your computer via USB\n"
            "2. Make sure the device is powered on\n"
            "3. Know which COM port the device is using\n\n"
            "Click 'Continue' to connect to your device."
        )
        
        choice = easygui.buttonbox(
            message,
            self.app_title,
            choices=["Continue", "Settings", "Exit"]
        )
        
        if choice == "Exit":
            return False
        elif choice == "Settings":
            self.show_settings()
        
        return True
    
    def show_settings(self) -> None:
        """
        Display settings dialog for advanced users.
        Allows customization of baudrate, timeouts, and output directory.
        """
        message = "Advanced Settings\n\nAdjust these only if you know what you're doing."
        title = "Settings"
        
        field_names = [
            "Baudrate (default: 115200)",
            "Timeout in seconds (default: 1.0)",
            "Output directory (default: downloads)",
            "Auto-create output directory? (yes/no)"
        ]
        
        field_values = [
            str(self.baudrate),
            str(self.timeout),
            self.output_dir,
            "yes" if self.auto_create_dir else "no"
        ]
        
        new_values = easygui.multenterbox(message, title, field_names, field_values)
        
        if new_values:
            try:
                self.baudrate = int(new_values[0])
                self.timeout = float(new_values[1])
                self.output_dir = new_values[2]
                self.auto_create_dir = new_values[3].lower() in ['yes', 'y', 'true', '1']
                
                easygui.msgbox("Settings saved successfully!", "Settings")
            except ValueError:
                easygui.msgbox(
                    "Invalid values entered. Settings not changed.",
                    "Error"
                )
    
    def show_connection_screen(self) -> bool:
        """
        Display connection setup screen with port selection and refresh capability.
        
        Returns:
            True if connection successful, False otherwise
        """
        while True:  # Loop to allow refresh
            # Get available ports with details
            available_ports = self.get_available_ports()
            
            # Get detailed port information
            ports_with_details = []
            try:
                import serial.tools.list_ports
                port_objects = serial.tools.list_ports.comports()
                for port in port_objects:
                    # Create detailed description
                    detail = f"{port.device}"
                    if port.description and port.description != port.device:
                        detail += f" - {port.description}"
                    if port.manufacturer:
                        detail += f" ({port.manufacturer})"
                    ports_with_details.append(detail)
            except:
                # Fallback to simple list
                ports_with_details = available_ports
            
            if not ports_with_details:
                ports_with_details = ["No ports detected - Enter manually..."]
            
            # Add refresh and manual entry options
            ports_with_details.append("🔄 Refresh port list")
            ports_with_details.append("✏️ Enter manually...")
            
            message = (
                "Select your GPS device's COM port:\n\n"
                "📌 Tip: If your device doesn't appear, try:\n"
                "   • Reconnecting the USB cable\n"
                "   • Clicking 'Refresh port list'\n"
                "   • Entering the port manually\n\n"
                f"Current setting: {self.port}\n"
            )
            
            selected_port = easygui.choicebox(
                message,
                "Connect to GPS Device",
                ports_with_details
            )
            
            if not selected_port:
                return False  # User cancelled
            
            # Handle refresh
            if "Refresh" in selected_port:
                continue  # Loop back to refresh
            
            # Handle manual entry
            if "manually" in selected_port:
                selected_port = easygui.enterbox(
                    "Enter the COM port name:\n\n"
                    "Examples:\n"
                    "  Windows: COM3, COM5, COM7\n"
                    "  Linux: /dev/ttyUSB0, /dev/ttyACM0\n"
                    "  Mac: /dev/cu.usbserial",
                    "Manual Port Entry",
                    default=self.port
                )
                if not selected_port:
                    continue  # Go back to port list
            else:
                # Extract just the port name from the detailed description
                selected_port = selected_port.split(" - ")[0].split(" (")[0]
            
            self.port = selected_port
            
            # Attempt to connect
            if self.connect_to_device():
                return True
            else:
                # Ask if user wants to try another port
                retry = easygui.ccbox(
                    "Connection failed. Would you like to try another port?",
                    "Connection Failed",
                    choices=["Try Again", "Cancel"]
                )
                if not retry:
                    return False
                # Loop back to show port selection again
    
    def connect_to_device(self) -> bool:
        """
        Establish connection to the GPS device.
        Shows progress and error messages.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Create GPS instance
            self.gps = WangganGPS(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                output_dir=self.output_dir,
                auto_create_dir=self.auto_create_dir
            )
            
            # Try to connect
            if self.gps.connect():
                self.connected = True
                easygui.msgbox(
                    f"✅ Successfully connected to GPS device on {self.port}!",
                    "Connection Successful"
                )
                return True
            else:
                easygui.msgbox(
                    f"❌ Could not connect to GPS device on {self.port}.\n\n"
                    "Please check:\n"
                    "• Device is connected and powered on\n"
                    "• Correct COM port is selected\n"
                    "• No other application is using the port\n"
                    "• USB drivers are installed",
                    "Connection Failed"
                )
                return False
                
        except Exception as e:
            easygui.msgbox(
                f"❌ Connection error:\n\n{str(e)}\n\n"
                "Please check your device connection and try again.",
                "Connection Error"
            )
            return False
    
    def show_download_mode_screen(self) -> Optional[DownloadMode]:
        """
        Display download mode selection screen with simplified options.
        
        Returns:
            Selected DownloadMode or None if cancelled
        """
        message = (
            "How do you want to download your GPS data?\n\n"
            "📋 Full Download is recommended for most users.\n"
            "It includes all track details, timestamps, and coordinates."
        )
        
        # Simplified to only show Full Download for now
        choices = [
            "� Full Download (Recommended)",
        ]
        
        choice = easygui.buttonbox(
            message, 
            "Download Mode", 
            choices=choices + ["◀️ Back", "❌ Cancel"]
        )
        
        if not choice or "Cancel" in choice:
            return None
        
        if "Back" in choice:
            return None
        
        # Always return TILDE mode (Full Download)
        return DownloadMode.TILDE
    
    def show_export_options_screen(self) -> Optional[dict]:
        """
        Display export format and options selection screen with simplified interface.
        
        Returns:
            Dictionary with export settings or None if cancelled
        """
        # Simplified format selection with checkboxes
        format_message = (
            "Choose how to save your GPS data:\n\n"
            "💡 Tip: You can select multiple formats.\n"
            "   Each format works with different software."
        )
        
        format_choices = [
            "✅ GPX - Works with most GPS apps",
            "🌍 KML - For Google Earth",
            "📊 CSV - For Excel spreadsheets",
        ]
        
        selected_formats = easygui.multchoicebox(
            format_message,
            "Choose Export Format(s)",
            format_choices
        )
        
        if not selected_formats:
            return None
        
        # Parse selected formats
        formats = []
        if any("GPX" in f for f in selected_formats):
            formats.append(OutputFormat.GPX)
        if any("KML" in f for f in selected_formats):
            formats.append(OutputFormat.KML)
        if any("CSV" in f for f in selected_formats):
            formats.append(OutputFormat.CSV)
        
        # Add RAW format by default (for backup)
        formats.append(OutputFormat.RAW)
        
        # Simplified options - only show output directory option
        option_message = (
            "Export Settings:\n\n"
            f"📁 Files will be saved to: {self.output_dir}\n\n"
            "Each track/waypoint will be saved as a separate file.\n"
            "This makes it easier to manage individual GPS records."
        )
        
        option_choices = [
            "✅ Continue with these settings",
            "📁 Change output folder",
            "◀️ Back"
        ]
        
        option = easygui.buttonbox(option_message, "Export Settings", option_choices)
        
        if not option or "Back" in option:
            return None
        
        if "Change output" in option:
            new_dir = easygui.diropenbox(
                "Select where to save your GPS files:",
                "Choose Output Folder",
                default=self.output_dir
            )
            if new_dir:
                self.output_dir = new_dir
                if self.gps:
                    self.gps.output_dir = Path(new_dir)
        
        # Always split by track (removed the combine option)
        return {
            'formats': formats,
            'split_by_track': True
        }
    
    def show_action_screen(self, download_mode: DownloadMode, export_options: dict) -> bool:
        """
        Display final action screen with download/export buttons.
        
        Args:
            download_mode: Selected download mode
            export_options: Dictionary with export settings
        
        Returns:
            True if operation completed successfully
        """
        mode_names = {
            DownloadMode.TILDE: "Full Download",
            DownloadMode.EXCLAMATION: "Quick Download",
            DownloadMode.CARET: "Debug Mode"
        }
        
        # Create user-friendly format list
        format_display = []
        for fmt in export_options['formats']:
            if fmt == OutputFormat.GPX:
                format_display.append("GPX")
            elif fmt == OutputFormat.KML:
                format_display.append("KML")
            elif fmt == OutputFormat.CSV:
                format_display.append("CSV")
            elif fmt == OutputFormat.RAW:
                format_display.append("RAW (backup)")
        
        format_names = ", ".join(format_display)
        
        message = (
            "✅ Ready to download your GPS data!\n\n"
            f"📋 Mode: {mode_names[download_mode]}\n"
            f"💾 Formats: {format_names}\n"
            f"📁 Save to: {self.output_dir}\n\n"
            "⏱️ This will take 10-60 seconds.\n"
            "Progress will be shown in the console window."
        )
        
        choices = [
            "⬇️ Start Download",
            "◀️ Back",
            "❌ Cancel"
        ]
        
        choice = easygui.buttonbox(message, "Ready to Download", choices)
        
        if not choice or "Cancel" in choice:
            return False
        
        if "Back" in choice:
            return False
        
        # Perform the download operation
        if "Start Download" in choice:
            return self.perform_download_and_export(download_mode, export_options)
        
        return False
    
    def perform_download_only(self, download_mode: DownloadMode) -> bool:
        """
        Download data and save only the raw output.
        
        Args:
            download_mode: Download mode to use
        
        Returns:
            True if successful
        """
        try:
            # Show brief info message (non-blocking would be better but easygui limitation)
            print("Starting download...")
            print("Sending download trigger to GPS device...")
            print("Please wait while data is being received...")
            
            # Perform download (this is where the actual work happens)
            data = self.gps.download(mode=download_mode, save_raw=True)
            
            if data:
                easygui.msgbox(
                    f"✅ Download complete!\n\n"
                    f"Downloaded {len(data)} bytes\n"
                    f"Data saved to: {self.output_dir}",
                    "Download Complete"
                )
                
                # Ask if user wants to open output folder
                if easygui.ccbox(
                    "Would you like to open the output folder?",
                    "Open Folder"
                ):
                    self.open_output_folder()
                
                return True
            else:
                easygui.msgbox(
                    "❌ No data received from device.\n\n"
                    "Please try again or check device settings.",
                    "No Data Received"
                )
                return False
                
        except Exception as e:
            easygui.msgbox(
                f"❌ Download error:\n\n{str(e)}",
                "Error"
            )
            return False
    
    def perform_download_and_export(self, download_mode: DownloadMode, export_options: dict) -> bool:
        """
        Download data and export to selected formats.
        
        Args:
            download_mode: Download mode to use
            export_options: Dictionary with export settings
        
        Returns:
            True if successful
        """
        try:
            # Print to console for progress feedback
            print("\n" + "="*50)
            print("DOWNLOAD STARTED")
            print("="*50)
            print("Sending download trigger to GPS device...")
            print("Waiting for data from device...")
            print("This may take 10-60 seconds depending on data size...")
            print("="*50 + "\n")
            
            # Download data (this is where the actual work happens)
            data = self.gps.download(mode=download_mode, save_raw=True)
            
            if not data:
                easygui.msgbox(
                    "❌ No data received from device.\n\n"
                    "Please try again or check device settings.",
                    "No Data Received"
                )
                return False
            
            print(f"\n✓ Download complete! Received {len(data)} bytes")
            print("Now converting to selected formats...")
            
            # Export to each selected format
            all_files = []
            
            for format_type in export_options['formats']:
                try:
                    print(f"  • Exporting to {format_type.value.upper()}...")
                    files = self.gps.export_tracks(
                        data,
                        format=format_type,
                        split_by_track=export_options['split_by_track']
                    )
                    if files:
                        all_files.extend(files)
                        print(f"    ✓ Created {len(files)} file(s)")
                except Exception as e:
                    print(f"    ✗ Error: {str(e)}")
                    easygui.msgbox(
                        f"⚠️ Warning: Could not export to {format_type.value.upper()}\n\n"
                        f"Error: {str(e)}\n\n"
                        "Other formats may have succeeded.",
                        "Export Warning"
                    )
            
            # Show results
            if all_files:
                file_list = "\n".join([f"  • {f}" for f in all_files[:10]])  # Show first 10
                if len(all_files) > 10:
                    file_list += f"\n  ... and {len(all_files) - 10} more files"
                
                easygui.msgbox(
                    f"✅ Export complete!\n\n"
                    f"Created {len(all_files)} file(s):\n\n{file_list}",
                    "Export Complete"
                )
                
                # Ask if user wants to open output folder
                if easygui.ccbox(
                    "Would you like to open the output folder?",
                    "Open Folder"
                ):
                    self.open_output_folder()
                
                return True
            else:
                easygui.msgbox(
                    "⚠️ Download completed but no files were created.\n\n"
                    "The data may not be in a recognized format.",
                    "Warning"
                )
                return False
                
        except Exception as e:
            easygui.msgbox(
                f"❌ Error during download/export:\n\n{str(e)}",
                "Error"
            )
            return False
    
    def open_output_folder(self) -> None:
        """Open the output directory in the system file explorer."""
        try:
            output_path = Path(self.output_dir).resolve()
            
            if platform.system() == "Windows":
                os.startfile(output_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", output_path])
            else:  # Linux
                subprocess.run(["xdg-open", output_path])
        except Exception as e:
            easygui.msgbox(
                f"Could not open folder:\n\n{str(e)}",
                "Error"
            )
    
    def show_help_about(self) -> None:
        """Display about dialog with device compatibility information."""
        message = (
            f"Wanggan GPS Data Downloader\n"
            f"Version {self.version}\n\n"
            "A user-friendly tool for downloading GPS data from Wanggan devices.\n\n"
            "✅ Tested Device:\n"
            "   Wanggan D6E GNSS Handheld Navigator\n\n"
            "⚠️  Compatibility:\n"
            "   Protocol may work with other Wanggan GPS models (untested)\n\n"
            "Author: Hélio Teixeira\n"
            "License: MIT\n"
            "Repository: github.com/heliobteixeira/wanggan-gps-python"
        )
        
        easygui.msgbox(message, "About")
    
    def show_help_guide(self) -> None:
        """Display usage guide with step-by-step instructions."""
        message = (
            "Quick Start Guide\n\n"
            "1️⃣  Connect Your Device\n"
            "   • Plug GPS device into USB port\n"
            "   • Turn device on\n"
            "   • Note the COM port (Windows) or /dev/tty* (Linux/Mac)\n\n"
            "2️⃣  Select Download Mode\n"
            "   • Full Download: Best for most users, includes all details\n"
            "   • Quick Download: Faster, just coordinates\n"
            "   • Debug Mode: For troubleshooting\n\n"
            "3️⃣  Choose Export Formats\n"
            "   • GPX: Works with most GPS software\n"
            "   • KML: For Google Earth\n"
            "   • CSV: For Excel\n"
            "   • RAW: Keep original data\n\n"
            "4️⃣  Download & Export\n"
            "   • Click 'Download & Export'\n"
            "   • Wait for completion\n"
            "   • Open output folder to view files\n\n"
            "💡 Tips:\n"
            "   • Use 'Full Download' mode for complete records\n"
            "   • Export to multiple formats at once\n"
            "   • Check 'downloads' folder for output files"
        )
        
        easygui.msgbox(message, "Usage Guide")
    
    def main_menu(self) -> None:
        """
        Display main menu after successful connection.
        Allows performing multiple operations without reconnecting.
        """
        while True:
            choices = [
                "📥 Download GPS Data",
                "⚙️  Settings",
                "❓ Help",
                "ℹ️  About",
                "🔌 Disconnect & Exit"
            ]
            
            choice = easygui.buttonbox(
                f"Connected to: {self.port}\n\n"
                "What would you like to do?",
                self.app_title,
                choices
            )
            
            if not choice or "Disconnect" in choice:
                break
            
            if "Download GPS" in choice:
                # Start download workflow
                download_mode = self.show_download_mode_screen()
                if download_mode:
                    export_options = self.show_export_options_screen()
                    if export_options:
                        self.show_action_screen(download_mode, export_options)
            
            elif "Settings" in choice:
                self.show_settings()
            
            elif "Help" in choice:
                self.show_help_guide()
            
            elif "About" in choice:
                self.show_help_about()
    
    def cleanup(self) -> None:
        """Clean up resources and disconnect from device."""
        if self.gps and self.connected:
            self.gps.disconnect()
            self.connected = False
    
    def run(self) -> None:
        """
        Main application entry point.
        Manages the complete user flow from welcome to exit.
        """
        try:
            # Show welcome screen
            if not self.show_welcome_screen():
                return
            
            # Connection loop (allow retry)
            while not self.connected:
                if not self.show_connection_screen():
                    # User cancelled connection
                    return
            
            # Main menu loop
            self.main_menu()
            
            # Cleanup
            self.cleanup()
            
            # Goodbye message
            easygui.msgbox(
                "Thank you for using Wanggan GPS Data Downloader!\n\n"
                "Your GPS data has been saved to:\n"
                f"{self.output_dir}",
                "Goodbye"
            )
            
        except KeyboardInterrupt:
            self.cleanup()
        except Exception as e:
            easygui.msgbox(
                f"An unexpected error occurred:\n\n{str(e)}\n\n"
                "The application will now close.",
                "Error"
            )
            self.cleanup()


def main():
    """Application entry point."""
    try:
        app = WangganGPSGUI()
        app.run()
    except Exception as e:
        easygui.msgbox(
            f"Failed to start application:\n\n{str(e)}",
            "Startup Error"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
