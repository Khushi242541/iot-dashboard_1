import os
import subprocess
import sys

# Step 1: Create virtual environment
subprocess.run([sys.executable, "-m", "venv", "venv"])
print("✅ Virtual environment created.")

# Step 2: Install packages inside venv
pip_path = "venv\\Scripts\\pip" if os.name == "nt" else "venv/bin/pip"
subprocess.run([pip_path, "install", "flask", "pymongo"])
print("✅ Installed Flask and PyMongo.")

# Step 3: Write .gitignore
with open(".gitignore", "w") as f:
    f.write("""\
__pycache__/
*.py[cod]
venv/
.env
*.log
.vscode/
.idea/
.DS_Store
""")
print("✅ .gitignore created.")

# Step 4: Git init
subprocess.run(["git", "init"])
print("✅ Git initialized.")

# Step 5: Freeze requirements
subprocess.run([pip_path, "freeze"], stdout=open("requirements.txt", "w"))
print("✅ requirements.txt generated.")
