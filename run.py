from WebApp import create_app

app = create_app()

    # Run Server
if __name__== "__main__":
    #app.run(debug=True)
    #app.run(host="GRE-L-20408", port='80')
    app.run(host='0.0.0.0', debug=True)
    
