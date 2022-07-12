import subprocess
import sys



# Help to install packages form python file (this was made to works with replit)
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# Install every package needed
# Package name should be used

install("psycopg2")
install("dnspython")
install("Flask")
install("Flask-Cors")

import apiHandler
if __name__ == "__main__":
    apiHandler.app.run(host='0.0.0.0', port=5000, debug=True)