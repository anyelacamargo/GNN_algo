
set -e

echo "Setting up environment..."

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Upgrade pip + install deps
pip install --upgrade pip
pip install -r requirements.txt

echo "Running pipeline..."
python src/main.py
