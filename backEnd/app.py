from main import create_app, db
import os

app = create_app()
#permite acceder a las porpiedades de la app en cualquier parte del sistema
app.app_context().push()

if __name__ == '__main__':
    db.create_all()

    app.run(port=os.getenv("PORT"),debug=True)