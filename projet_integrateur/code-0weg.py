from flask import Flask, render_template, request

app = Flask(__name__)

# Page pour l'administration (coordonnateurs)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Code pour éditer les emplois du temps
        pass
    else:
        return render_template('admin.html')

# Page pour les étudiants
@app.route('/')
def index():
   # Code pour afficher les emplois du temps hebdomadaires et autres informations relatives aux cours, enseignants et salles de cours 
   return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)