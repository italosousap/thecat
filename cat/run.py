import time
from api import app

time.sleep(10)
app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
