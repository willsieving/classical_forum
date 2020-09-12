from flask_server import create_app

app = create_app()
# Creating app object

if __name__ == '__main__':
    app.run(debug=True)