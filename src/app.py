from src.utilities.create_app import create_app

app = create_app(config_filename="")

if __name__ == '__main__':
    app.run()
