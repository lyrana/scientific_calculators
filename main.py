#!/usr/bin/env python3
"""
Scientific Calculators Application

A NiceGUI-based web application for physics calculations including
electromagnetic, plasma physics, beam physics, and atomic physics formulas.

Usage:
    python main.py

The application will start on http://localhost:8080
"""

from nicegui import ui, app
from pathlib import Path

from app.layout import AppLayout


def main():
    """Initialize and run the application."""
    # Get the directory containing this file
    app_dir = Path(__file__).parent

    # Serve static files (cross-section images)
    static_path = app_dir / "app" / "static"
    if static_path.exists():
        app.add_static_files("/static", str(static_path))

    @ui.page("/")
    def index():
        """Main page."""
        layout = AppLayout()
        layout.create_layout()

    # Run the application
    ui.run(
        title="Scientific Calculators",
        dark=True,
        reload=True,  # Enable auto-reload for development
        port=8080,
        show=False,  # Don't auto-open browser
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()
