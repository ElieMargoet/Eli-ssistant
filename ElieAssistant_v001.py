import nuke
from PySide2 import QtWidgets, QtCore, QtGui
import os
import json
import functools

class ElieAssistantWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.buttons_info = {}  # Initialiser buttons_info comme un dictionnaire vide
        self.setWindowTitle("Eli-ssistant")
        self.setGeometry(100, 100, 350, 700)  # Position et taille de la fenêtre
        self.setMinimumSize(350, 300)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, False)

        # Création d'un widget central et d'un layout pour organiser les widgets
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(self.layout)

        # Réduction des marges et de l'espacement
        self.layout.setContentsMargins(10, 5, 10, 5)  # Marge autour du layout
        self.layout.setSpacing(5)  # Espacement entre les widgets

        # Ajouter l'image en haut de la fenêtre
        self.add_header_image(r'D:\Templates_Nuke\imageElieAssistant_03.png')

        # Création du label pour le nom du projet
        self.project_label = QtWidgets.QLabel("Pirates")
        self.project_label.setAlignment(QtCore.Qt.AlignLeft)
        self.project_label.setStyleSheet("font-size: 25px; font-weight: bold;")

        # Création du label pour le titre de la section templates
        self.templates_section_label = QtWidgets.QLabel("Templates")
        self.templates_section_label.setAlignment(QtCore.Qt.AlignLeft)
        self.templates_section_label.setStyleSheet("font-size: 15px; font-weight: bold;")

        # Création du champ de texte pour le nom du projet et le bouton pour changer le nom
        self.new_project_name_field = QtWidgets.QLineEdit()
        self.new_project_name_field.setPlaceholderText("Entrez le nouveau nom du projet...")

        self.change_name_button = QtWidgets.QPushButton("Ajouter")
        self.change_name_button.clicked.connect(self.change_project_name)  # Connexion du signal click à un slot

        # Creation d'une QListWidget pour les dossiers
        self.nukeScript_list = QtWidgets.QListWidget()

        # Creation d'un QComboBox pour les presets de projets
        self.project_preset = QtWidgets.QComboBox()
        self.read_project_preset()

        # Creation d'un bouton pour sauver les presets de projets
        self.project_preset_saveButton = QtWidgets.QPushButton("Save project preset")
        self.project_preset_saveButton.clicked.connect(self.on_save_preset_clicked)

        # Création du séparateur
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)

        # Création du deuxieme séparateur
        separator2 = QtWidgets.QFrame()
        separator2.setFrameShape(QtWidgets.QFrame.HLine)
        separator2.setFrameShadow(QtWidgets.QFrame.Sunken)
  
        # Création du troisieme séparateur
        separator3 = QtWidgets.QFrame()
        separator3.setFrameShape(QtWidgets.QFrame.HLine)
        separator3.setFrameShadow(QtWidgets.QFrame.Sunken)

        # Creation du quatrieme separateur
        separator4 = QtWidgets.QFrame()
        separator4.setFrameShape(QtWidgets.QFrame.HLine)
        separator4.setFrameShadow(QtWidgets.QFrame.Sunken)

        # Création du label pour changer le path du projet
        self.change_path_label = QtWidgets.QLabel("Ajouter le path du projet")
        self.change_path_label.setAlignment(QtCore.Qt.AlignLeft)

        # Création du champ de texte pour le chemin du projet
        self.text_field = QtWidgets.QLineEdit()
        self.text_field.setPlaceholderText("Entrez le chemin du répertoire...")

        # Création du bouton pour afficher les dossiers
        self.button = QtWidgets.QPushButton("Ajouter")
        self.button.clicked.connect(self.load_folders)  # Connexion du signal click à un slot

        # Création d'un layout horizontal pour le champ de texte et le bouton
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self.text_field)
        h_layout.addWidget(self.button)
        h_layout.setSpacing(5)

        # Création d'un layout horizontal pour le champ de texte et le bouton de changement de nom
        name_change_layout = QtWidgets.QHBoxLayout()
        name_change_layout.addWidget(self.new_project_name_field)
        name_change_layout.addWidget(self.change_name_button)
        name_change_layout.setSpacing(5)

        # Ajout des widgets au layout principal
        self.layout.addWidget(self.project_label)
        # Label et champs pour modifier le nom du projet
        self.layout.addWidget(QtWidgets.QLabel("Ajouter un nom de projet :"))
        self.layout.addLayout(name_change_layout)
        self.layout.addWidget(separator)
        self.layout.addWidget(self.change_path_label)
        self.layout.addLayout(h_layout)

        # Ajouter la section pour les presets
        self.layout.addWidget(separator4)
        self.layout.addWidget(self.project_preset_saveButton)
        self.layout.addWidget(self.project_preset)

        # Ajouter la liste des plans
        self.layout.addWidget(self.nukeScript_list)



        # Ajouter la section pour les templates
        self.templates_label = QtWidgets.QLabel("Templates Nuke")
        self.templates_label.setAlignment(QtCore.Qt.AlignLeft)
        self.templates_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Charger les boutons existants depuis un fichier
        self.layout.addWidget(separator2)
        self.load_buttons()
        self.layout.addWidget(separator3)
        self.layout.addWidget(self.templates_section_label)
        self.load_templates()



    def add_header_image(self, image_path):
        if os.path.exists(image_path):
            pixmap = QtGui.QPixmap(image_path)
            image_label = QtWidgets.QLabel()
            image_label.setPixmap(pixmap)
            image_label.setScaledContents(True)  # Assure que l'image s'ajuste à l'espace disponible
            self.layout.addWidget(image_label)
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", "L'image spécifiée n'existe pas.")



    def load_folders(self):

        # Obtenir le chemin du répertoire depuis le champ de texte
        directory_path = self.text_field.text()

        # Vérifier si le répertoire existe
        if not os.path.isdir(directory_path):
            QtWidgets.QMessageBox.warning(self, "Erreur", "Le chemin spécifié n'est pas un répertoire valide.")
            return
        
        # Clear la liste
        self.nukeScript_list.clear()

        # Lister les sous-dossiers
        try:
            folders = [f for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))]
            # Enregistrer les chemins complets des dossiers
            self.buttons_info = {folder: os.path.join(directory_path, folder) for folder in folders}
            
            # Loader le nom des fichiers dans la liste
            for folder_name, folder_path in self.buttons_info.items():
                self.nukeScript_list.addItem(folder_name)
                
            self.nukeScript_list.itemDoubleClicked.disconnect()
            self.nukeScript_list.itemDoubleClicked.connect(self.open_first_nknc_file)
            
            # Enregistrer les boutons
            self.save_buttons(directory_path, self.buttons_info, self.project_label.text())
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Erreur", str(e))

    def load_templates(self):
        # Chemin du dossier des templates
        templates_path = 'D:\\Templates_Nuke'

        # Réinitialiser les boutons de templates existants
        if hasattr(self, 'templates_layout'):
            for i in reversed(range(self.templates_layout.count())):
                widget = self.templates_layout.itemAt(i).widget()
                if isinstance(widget, QtWidgets.QPushButton):
                    widget.deleteLater()

        # Créer un layout pour les boutons de templates
        self.templates_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.templates_layout)

        # Vérifier si le répertoire existe
        if not os.path.isdir(templates_path):
            QtWidgets.QMessageBox.warning(self, "Erreur", "Le dossier des templates n'existe pas.")
            return

        try:
            templates = [f for f in os.listdir(templates_path) if f.endswith('.nknc')]
            self.templates_info = {template: os.path.join(templates_path, template) for template in templates}

            for template_name, template_path in self.templates_info.items():
                button = QtWidgets.QPushButton(template_name)
                button.clicked.connect(functools.partial(self.import_template, template_path))
                self.templates_layout.addWidget(button)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Erreur", str(e))

    def import_template(self, file_path):
        try:
            if os.path.exists(file_path):
                # importe les templates dans le file_path
                nuke.nodePaste(file_path)
            else:
                QtWidgets.QMessageBox.information(self, "Information", "Le fichier spécifié n'existe pas.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Erreur", str(e))



    def open_first_nknc_file(self, item):
        folder_path = self.buttons_info.get(item.text())
        if folder_path:
            try:
                files = [f for f in os.listdir(folder_path) if f.endswith('.nknc')]
                if files:
                    file_to_open = os.path.join(folder_path, files[0])
                    # Ouvrir le fichier dans Nuke
                    nuke.scriptOpen(file_to_open)
                else:
                    QtWidgets.QMessageBox.information(self, "Information", "Aucun fichier .nknc trouvé dans ce dossier.")
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Erreur", str(e))


    def save_buttons(self, path, buttons_info, project_name):
        data = {}
    
        # Si le fichier existe déjà, charger les données existantes
        if os.path.exists('saved_buttons.json'):
            with open('saved_buttons.json', 'r') as f:
                data = json.load(f)
    
        # Mettre à jour les informations du projet et des boutons
        data['path'] = path
        data['buttons_info'] = buttons_info
        data['project_name'] = project_name
    
        # Sauvegarder les données mises à jour dans le fichier JSON
        with open('saved_buttons.json', 'w') as f:
            json.dump(data, f)


    def load_buttons(self):
        # Charger les boutons à partir d'un fichier JSON
        if os.path.exists('saved_buttons.json'):
            with open('saved_buttons.json', 'r') as f:
                data = json.load(f)
                directory_path = data.get('path', '')
                buttons_info = data.get('buttons_info', {})
                project_name = data.get('project_name', 'Pirates')

                self.text_field.setText(directory_path)
                self.project_label.setText(f"{project_name}")

                self.buttons_info = buttons_info  # Conserver les infos des boutons

            for folder_name, folder_path in buttons_info.items():
                self.nukeScript_list.addItem(folder_name)
                
            self.nukeScript_list.itemDoubleClicked.connect(self.open_first_nknc_file)


    def change_project_name(self):
        # Modifier le texte du label avec le nouveau nom du projet
        new_name = self.new_project_name_field.text()
        if new_name:
            self.project_label.setText(f"{new_name}")
            #Appeler la fonction save_buttons pour sauvegarder le nouveau nom du projet
            self.save_buttons(self.text_field.text(), self.buttons_info, new_name)
        else:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Le nom du projet ne peut pas être vide.")

    def read_project_preset(self):
        # charger les presets a partir du fichier JSON

        try:
            with open('save_preset.json', 'r' ) as f:
                data_preset = json.load(f)

                #Reinitialiser la QComboBox
                self.project_preset.clear()

                #parcourir les presets et les ajouter a la QComboBox
                presets = data_preset.get('presets', {})
                for project_name, directory_path in presets.items():
                    self.project_preset.addItem(project_name, directory_path)

                # Connecter le changement de sélection du preset à la méthode de mise à jour du label
                self.project_preset.currentIndexChanged.connect(self.update_project_label_from_preset)

                #Connecter le changement de selection de preset a une methode
                self.project_preset.currentIndexChanged.connect(self.select_preset)
        except IOError:
            QtWidgets.QMessageBox.warning(self, "Error", "Le fichier des presets n'existe pas")
        except json.JSONDecodeError:
            QtWidgets.QMessageBox.warning(self, "Error", "Erreur de lecture du fichier JSON")

    def select_preset(self):
        #Recuperer le chemin du preset selectionne
        directory_path = self.project_preset.currentData()
        if directory_path:
            self.text_field.setText(directory_path)
            self.load_folders()
            self.update_project_label_from_preset()

    def save_project_preset(self, project_name, path):
        try:
            #Verifier si le fichier JSON existe
            if not os.path.exists('save_preset.json'):
                # Creer le fichier JSON
                with open('save_preset.json', 'w') as f:
                    json.dump({'presets': {}}, f, indent=4)

            # Charger les donnees existantes dans le fichier JSON
            data_preset = {}
            if os.path.exists('save_preset.json'):
                with open('save_preset.json', 'r') as f:
                    data_preset = json.load(f)

            #Ajouter ou mettre a jour le preset
            presets = data_preset.get('presets', {})
            if project_name in presets:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Le projet est deja enregristre dans les presets")
                return

            presets[project_name] = path
            data_preset['presets'] = presets

            #Sauvegarder les donnees mise a jour 
            with open('save_preset.json', 'w') as f:
                json.dump(data_preset, f, indent=4)

        except IOError as e:
            QtWidgets.QMessageBox.warning(self, "Erreur", f"Erreur d'entrée/sortie: {e}")
        except json.JSONDecodeError:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Erreur de lecture du fichier JSON")

        #Mettre a jour la QComboBox
        self.read_project_preset()

    def on_save_preset_clicked(self):
        project_name = self.new_project_name_field.text()
        path = self.text_field.text()

        self.save_project_preset(project_name, path)

    def update_project_label_from_preset(self):
        # Je recup le nom selectionne dans la QComboBox
        project_name = self.project_preset.currentText()
        #Je met a jour le label avec le nom du currentText de ma QComboBox
        self.project_label.setText(f"Nom du projet : {project_name}")






    @classmethod
    def open_window(cls):
        # Vérifier si la fenêtre existe déjà, et la fermer si c'est le cas
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if isinstance(widget, cls):
                widget.close()
                break

        # Créer et afficher une nouvelle fenêtre
        window = cls()
        window.show()

        # Ajouter la fenêtre à Nuke pour qu'elle reste ouverte
        nuke.mainWindow().addDockWidget(QtCore.Qt.BottomDockWidgetArea, window)

# Ouvrir la fenêtre
ElieAssistantWindow.open_window()


