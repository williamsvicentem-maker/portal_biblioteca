from flask import Flask, render_template, request, redirect, url_for, session, make_response

app = Flask(__name__)
app.secret_key = "biblioteca123"

usuarios = {
    "carlos": "1111",
    "laura": "2222",
    "diego": "3333"
}

libros_lista = [
    {
        "titulo": "Python desde cero",
        "autor": "Juan Pérez",
        "disponibles": 4
    },
    {
        "titulo": "Desarrollo Web",
        "autor": "María López",
        "disponibles": 2
    },
    {
        "titulo": "Inteligencia Artificial",
        "autor": "Pedro García",
        "disponibles": 0
    }
]


@app.route("/")
def index():
    ultimo_usuario = request.cookies.get("ultimo_usuario")
    return render_template("index.html", ultimo_usuario=ultimo_usuario)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        contraseña = request.form["contraseña"]

        if usuario in usuarios and usuarios[usuario] == contraseña:

            session["usuario"] = usuario

            respuesta = make_response(
                redirect(url_for("libros"))
            )

            respuesta.set_cookie("ultimo_usuario", usuario)

            return respuesta

        return render_template(
            "login.html",
            mensaje="Usuario o contraseña incorrectos."
        )

    return render_template("login.html")


@app.route("/libros")
def libros():

    return render_template(
        "libros.html",
        libros=libros_lista
    )


@app.route("/perfil")
def perfil():

    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template(
        "perfil.html",
        usuario=session["usuario"]
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


@app.route("/eliminar_cookie")
def eliminar_cookie():

    respuesta = make_response(
        redirect(url_for("index"))
    )

    respuesta.set_cookie(
        "ultimo_usuario",
        "",
        expires=0
    )

    return respuesta


if __name__ == "__main__":
    app.run(debug=True)