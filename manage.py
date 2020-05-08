import sys
from WebApp import create_app
from waitress import serve


if len(sys.argv) == 3:
    command = sys.argv[1]
    param = sys.argv[2]

    # Run server
    if command == "runserver":
        app = create_app()

        # Check if running in dev or prod mode
        if param == "dev":
            if __name__ == "__main__":
                app.run(host="0.0.0.0", debug=True)
        elif param == "prod":
            serve(app, host="0.0.0.0", port="80")
    #Start Migration
    elif command == "migrate":
        print("attempt to migrate")
else:
    print("manage.py requires command and parameter.. example: python manage.py runserver dev")

