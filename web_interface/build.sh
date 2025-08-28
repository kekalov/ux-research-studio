#!/usr/bin/env bash
# Build script for Render deployment

echo "🚀 Starting build process..."

# Check if we're on Render
if [ "$RENDER" = "true" ]; then
    echo "🌐 Running on Render - minimal setup..."
    
    # For now, we'll skip Chrome installation on Render
    # as it requires root privileges and can cause issues
    echo "⚠️ Skipping Chrome installation (requires root)"
    echo "💡 Will use headless mode without browser automation"
else
    echo "💻 Running locally - skipping Chrome installation"
fi

echo "✅ Build completed successfully!"
