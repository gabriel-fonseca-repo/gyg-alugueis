from flask import Flask, render_template, request

app = Flask(__name__)
with (app.app_context()):
    app.config.update(
        TEMPLATES_AUTO_RELOAD=True,
        DEBUG=True
    )

    @app.route("/")
    def index():
        return render_template("login.html")

    @app.route("/login", methods=['POST', 'GET'])
    def login():
        if request.method == 'GET':
            return render_template("login.html")
        if request.method == 'POST':
            print(request.form)
            return "Vc tentou logar!"
