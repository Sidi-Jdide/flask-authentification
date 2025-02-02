from app import create_app

# Créer l'application Flask
app = create_app()

if __name__ == '__main__':
    # Démarrer le serveur de développement Flask
    app.run(debug=True, host='0.0.0.0', port=8080)