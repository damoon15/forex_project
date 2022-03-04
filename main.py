from app import app

if __name__ == "__main__":
    print("App is running on http://127.0.0.1:8000/")
    
    app.run(debug=False,host='0.0.0.0', port=8000) 