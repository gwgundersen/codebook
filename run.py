"""Dev deployment script.
"""

from codebook import app

app.run(debug=True, port=8080, host='0.0.0.0')
