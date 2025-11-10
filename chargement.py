import json
from room import Room

class Chargement:
    """
    Cette classe utilitaire gère le chargement des données du jeu
    (salles, sorties, etc.) à partir d'un fichier JSON.
    """

    @classmethod
    def charger_depuis_json(cls, fichier_json: str):
        """
        Charge la configuration du jeu depuis un fichier JSON.
        
        Ce méthode lit le fichier, crée toutes les instances de Room,
        lie leurs sorties, et retourne la liste des salles et
        la salle de départ.
        """
        try:
            with open(fichier_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"ERREUR: Le fichier de configuration '{fichier_json}' est introuvable.")
            return [], None
        except json.JSONDecodeError:
            print(f"ERREUR: Le fichier '{fichier_json}' contient un JSON invalide.")
            return [], None

        salles_creees = {}

        if 'rooms' not in data:
            print("ERREUR: Le JSON doit contenir une clé 'rooms'.")
            return [], None

        for room_id, room_data in data['rooms'].items():
            try:
                new_room = Room(room_data['name'], room_data['description'])
                salles_creees[room_id] = new_room
            except KeyError:
                print(f"ERREUR: Données manquantes (name/description) pour la salle ID '{room_id}'.")

        for room_id, room_data in data['rooms'].items():
            if room_id not in salles_creees:
                continue
                
            current_room_obj = salles_creees[room_id]
            
            if 'exits' in room_data:
                for direction, destination_id in room_data['exits'].items():
                    if destination_id is None:
                        current_room_obj.exits[direction] = None
                    elif destination_id in salles_creees:
                        current_room_obj.exits[direction] = salles_creees[destination_id]
                    else:
                        print(f"AVERTISSEMENT: La sortie '{direction}' de '{room_id}' mène à un ID inconnu: '{destination_id}'.")

        start_room_id = data.get('start_room')
        start_room_obj = None
        
        if not start_room_id:
            print("ERREUR: 'start_room' n'est pas défini dans le JSON.")
        else:
            start_room_obj = salles_creees.get(start_room_id)
            if not start_room_obj:
                print(f"ERREUR: La salle de départ ID '{start_room_id}' n'a pas été trouvée.")

        return list(salles_creees.values()), start_room_obj