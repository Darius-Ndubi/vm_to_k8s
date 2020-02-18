"""
    This is the apps entry point
"""
from app import app


#run the app
if __name__ == '__main__':
    app.run(debug=False)