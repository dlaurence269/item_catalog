from main import app

app.secret_key = 'super_secret_key'
if __name__ == "__main__":
    app.run()
