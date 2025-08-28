#!/usr/bin/env bash
# Build script for Render deployment

echo "🚀 Starting build process..."

# Update package list
apt-get update

# Install Chrome dependencies
apt-get install -y wget gnupg2

# Add Google Chrome repository
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
apt-get update
apt-get install -y google-chrome-stable

# Install additional dependencies for Chrome
apt-get install -y xvfb

# Verify Chrome installation
google-chrome --version

echo "✅ Build completed successfully!"
