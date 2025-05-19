from flask import Flask, request, render_template_string

app = Flask(__name__)

# Formulaire HTML
login_form = """
<!DOCTYPE html>
<html>
<head><title>Connexion</title></head>
<body>
  <h2>Connexion</h2>
  <form method="POST">
    Nom d'utilisateur: <input type="text" name="username"><br>
    Mot de passe: <input type="password" name="password"><br>
    <input type="submit" value="Se connecter">
  </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # RÉCUPÉRATION CÔTÉ SERVEUR
        username = request.form["username"]
        password = request.form["password"]

        # Tu peux maintenant utiliser ces valeurs comme tu veux :
        print(f"Nom d'utilisateur reçu : {username}")
        print(f"Mot de passe reçu : {password}")

        # Par exemple, vérification basique :
        if username == "admin" and password == "1234":
            return f"<h3>Bienvenue, {username} !</h3>"
        else:
            return "<h3>Identifiants incorrects</h3>"

    return render_template_string(login_form)

if __name__ == "__main__":
    app.run(debug=True)
