from app import app

if __name__ == "__main__":
    print("App is running")
    
    app.run(debug=True,host='0.0.0.0', port=8000)