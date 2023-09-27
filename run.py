from flaskblog import create_app
# from flaskblog import app
app = create_app()
# app.app_context()

if __name__ == "__main__":
    app.run(debug=True,port=5050)
