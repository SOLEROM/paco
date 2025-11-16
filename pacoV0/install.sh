#!/bin/bash
# PACO Installation Script

set -e

echo "🚀 Installing PACO - Personal AI Assistant"
echo ""

# Determine installation directory
INSTALL_DIR="${HOME}/paco-bin"
echo "📁 Installation directory: ${INSTALL_DIR}"

# Create directory
mkdir -p "${INSTALL_DIR}"

# Copy files
echo "📦 Copying files..."
cp paco-* "${INSTALL_DIR}/" 2>/dev/null || true
cp paco_lib.py "${INSTALL_DIR}/"
chmod +x "${INSTALL_DIR}"/paco-*

echo "✅ Files copied"

# Check for Ollama
echo ""
echo "🔍 Checking for Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    
    # Check if llama3.2 is available
    if ollama list | grep -q "llama3.2"; then
        echo "✅ llama3.2 model is available"
    else
        echo "⚠️  llama3.2 model not found"
        echo "   Run: ollama pull llama3.2"
    fi
else
    echo "❌ Ollama not found"
    echo ""
    echo "Please install Ollama:"
    echo "  curl -fsSL https://ollama.com/install.sh | sh"
    echo "  ollama pull llama3.2"
fi

# Check shell configuration
echo ""
echo "🔧 Configuring PATH..."

SHELL_RC=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="${HOME}/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="${HOME}/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
    # Check if already in PATH
    if grep -q "paco-bin" "$SHELL_RC" 2>/dev/null; then
        echo "✅ PATH already configured in $SHELL_RC"
    else
        echo "Adding PACO to PATH in $SHELL_RC"
        echo "" >> "$SHELL_RC"
        echo "# PACO - Personal AI Assistant" >> "$SHELL_RC"
        echo "export PATH=\"\${HOME}/paco-bin:\${PATH}\"" >> "$SHELL_RC"
        echo "export PYTHONPATH=\"\${HOME}/paco-bin:\${PYTHONPATH}\"" >> "$SHELL_RC"
        echo "✅ PATH configured"
        echo "   Run: source $SHELL_RC"
    fi
else
    echo "⚠️  Could not detect shell config file"
    echo "   Please manually add to your shell config:"
    echo "   export PATH=\"\${HOME}/paco-bin:\${PATH}\""
    echo "   export PYTHONPATH=\"\${HOME}/paco-bin:\${PYTHONPATH}\""
fi

echo ""
echo "✨ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Source your shell config: source ~/.bashrc  (or ~/.zshrc)"
echo "  2. Try it out: paco-add-task demo 'Get things done' --priority high"
echo "  3. Read the docs: cat ${INSTALL_DIR}/README.md"
echo ""
echo "Quick start:"
echo "  paco-add-task myproject 'First task' --priority high"
echo "  paco-list projects"
echo "  paco-next myproject"
