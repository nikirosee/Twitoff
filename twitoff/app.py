"""
Main app/ routing file for Twitoff

The file that holds the functions create_app
to collect our modules
"""



from flask import Flask, render_template

def create_app():
    """Creating and configuring an instance of the Flask applicaton"""
    app = Flask(__name__)

    #TODO : Make rest of application
    @app.route('/')
    def root():
        return render_template("base.html", title="Home")

    return app

