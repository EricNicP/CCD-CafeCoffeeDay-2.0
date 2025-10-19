"""
CCD 2.0 - Application Runner
Coffee Shop Management System

This file is the entry point to run the backend server.
"""

from backend.app import app, init_db

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    # This will run the full-featured app from backend/app.py
    app.run(debug=True, host='0.0.0.0', port=5000)

    # Ensure we're in the right directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run the Flask application
    print("Starting CCD 2.0 Coffee Shop Management System...")
    print("Backend API: http://localhost:5000")
    print("API Documentation: http://localhost:5000/api/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
