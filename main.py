import pygame
import sys
from src.models.Match import Match # Importe la classe Match qui contient toute la logique du jeu

# --- Initialisation de Pygame ---
pygame.init() # Initialise tous les modules nécessaires de Pygame

# --- Paramètres de l'écran ---
WIDTH, HEIGHT = 800, 800 # Dimensions de la fenêtre de jeu (largeur, hauteur)
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Crée la fenêtre de jeu
pygame.display.set_caption("Checkers") # Définit le titre de la fenêtre

# --- Définition des Couleurs (RGB) ---
WHITE = (255, 255, 255) # Couleur blanche
BLACK = (0, 0, 0)     # Couleur noire
LIGHT_BROWN = (205, 133, 63) # Couleur marron clair pour les cases claires du plateau
DARK_BROWN = (139, 69, 19)   # Couleur marron foncé pour les cases sombres du plateau
WHITE_PIECE_COLOR = (255, 255, 255) # Couleur des pièces blanches (blanc pur)
BLACK_PIECE_COLOR = (0, 0, 0)   # Couleur des pièces noires (noir pur)

# --- Propriétés du Plateau ---
ROWS, COLS = 8, 8 # Le plateau de dames est une grille 8x8
SQUARE_SIZE = WIDTH // COLS # Calcule la taille d'une case (800 / 8 = 100 pixels par case)

# --- Propriétés des Pièces ---
PIECE_RADIUS = SQUARE_SIZE // 3 # Rayon des cercles représentant les pièces

# --- Police de Caractères ---
FONT = pygame.font.SysFont("Arial", 30) # Définit la police et la taille pour le texte (ex: 'K' pour les rois)

# --- Fonctions de Dessin ---

def draw_board(win):
    """
    Dessine le plateau de dames sur la fenêtre Pygame.
    Les cases alternent entre marron clair et marron foncé.
    Args:
        win (pygame.Surface): L'objet surface sur lequel dessiner (la fenêtre de jeu).
    """
    for row in range(ROWS):
        for col in range(COLS):
            # Détermine la couleur de la case en fonction de sa position (alternance)
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            # Dessine un rectangle pour chaque case
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(win, match):
    """
    Dessine toutes les pièces sur le plateau en fonction de l'état actuel du jeu.
    Args:
        win (pygame.Surface): L'objet surface sur lequel dessiner.
        match (Match): L'instance de la partie de dames pour obtenir l'état du plateau.
    """
    for row in range(ROWS):
        for col in range(COLS):
            piece = match.board.get_piece(row, col) # Récupère la pièce à la position (row, col)
            if piece: # Si une pièce existe à cette position
                # Calcule les coordonnées centrales de la case pour y dessiner la pièce
                center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                
                # Détermine la couleur du cercle de la pièce
                color = WHITE_PIECE_COLOR if piece.color == "white" else BLACK_PIECE_COLOR
                
                # Dessine le cercle représentant la pièce
                pygame.draw.circle(win, color, (center_x, center_y), PIECE_RADIUS)
                
                if piece.is_king: # Si la pièce est un roi
                    # Rend le texte 'K' (pour King) et le centre sur la pièce
                    text_surface = FONT.render("K", True, BLACK if piece.color == "white" else WHITE)
                    text_rect = text_surface.get_rect(center=(center_x, center_y))
                    win.blit(text_surface, text_rect) # Affiche le texte sur la pièce

def get_row_col_from_mouse(pos):
    """
    Convertit les coordonnées de la souris en coordonnées de ligne/colonne du plateau.
    Args:
        pos (tuple): Un tuple (x, y) représentant les coordonnées du clic de souris.
    Returns:
        tuple: Un tuple (row, col) correspondant à la case cliquée.
    """
    x, y = pos
    row = y // SQUARE_SIZE # Division entière pour obtenir la ligne
    col = x // SQUARE_SIZE # Division entière pour obtenir la colonne
    return row, col

def display_message(win, message):
    """
    Affiche un message centré sur l'écran.
    Args:
        win (pygame.Surface): La surface sur laquelle dessiner.
        message (str): Le message à afficher.
    """
    font = pygame.font.SysFont("Arial", 70, bold=True) # Police plus grande pour le message de fin
    text_surface = font.render(message, True, WHITE) # Rendre le texte en blanc
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2)) # Centrer le texte
    win.blit(text_surface, text_rect) # Afficher le texte
    pygame.display.flip() # Mettre à jour l'affichage pour montrer le message
    pygame.time.wait(3000) # Attendre 3 secondes avant de quitter

# --- Fonction Principale du Jeu Pygame ---
def main():
    """
    Fonction principale qui gère la boucle de jeu Pygame.
    Elle initialise la partie, gère les événements utilisateur (clics de souris),
    met à jour l'état du jeu et redessine l'écran.
    """
    match = Match() # Crée une nouvelle instance de la partie de dames
    match.start_game() # Initialise le plateau et les pièces pour la partie
    
    selected_piece = None # Stocke la position de la pièce actuellement sélectionnée par le joueur
    possible_moves = []   # Stocke les mouvements possibles pour la pièce sélectionnée

    running = True # Variable de contrôle de la boucle de jeu
    while running:
        # --- Gestion des Événements Pygame ---
        for event in pygame.event.get(): # Parcourt tous les événements en attente
            if event.type == pygame.QUIT: # Si l'utilisateur clique sur le bouton de fermeture de la fenêtre
                running = False # Arrête la boucle de jeu

            if event.type == pygame.MOUSEBUTTONDOWN: # Si un clic de souris est détecté
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos()) # Obtient la case cliquée
                piece = match.board.get_piece(row, col) # Récupère la pièce (s'il y en a une) sur la case cliquée

                if selected_piece: # Si une pièce était déjà sélectionnée
                    from_row, from_col = selected_piece
                    # Tente de déplacer la pièce sélectionnée vers la nouvelle case cliquée
                    if match.make_move(from_row, from_col, row, col):
                        selected_piece = None # Réinitialise la sélection après un mouvement réussi
                        possible_moves = []   # Efface les mouvements possibles affichés
                    else:
                        # Si le mouvement est invalide, désélectionne la pièce actuelle
                        # et tente de sélectionner une nouvelle pièce à la place
                        selected_piece = None
                        possible_moves = []
                        if piece and piece.color == match.current_player.color: # Si la nouvelle case contient une pièce du joueur actuel
                            selected_piece = (row, col) # Sélectionne cette nouvelle pièce
                            possible_moves = match.get_possible_moves_for_piece(row, col) # Calcule ses mouvements possibles
                elif piece and piece.color == match.current_player.color: # Si aucune pièce n'était sélectionnée et que la case cliquée contient une pièce du joueur actuel
                    selected_piece = (row, col) # Sélectionne cette pièce
                    possible_moves = match.get_possible_moves_for_piece(row, col) # Calcule ses mouvements possibles

        # --- Dessin de l'Écran ---
        WIN.fill(BLACK) # Remplit l'écran en noir (efface le contenu précédent)
        draw_board(WIN) # Dessine le plateau
        draw_pieces(WIN, match) # Dessine les pièces

        # --- Surlignage de la Pièce Sélectionnée et des Mouvements Possibles ---
        if selected_piece:
            s_row, s_col = selected_piece
            # Dessine un rectangle vert autour de la pièce sélectionnée
            pygame.draw.rect(WIN, (0, 255, 0), (s_col * SQUARE_SIZE, s_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
            for move in possible_moves:     
                _, (t_row, t_col) = move
                # Dessine un rectangle jaune autour des cases de destination possibles
                pygame.draw.rect(WIN, (255, 255, 0), (t_col * SQUARE_SIZE, t_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

        pygame.display.flip() # Met à jour l'affichage de la fenêtre (rend visible tout ce qui a été dessiné)

        # --- Vérification de la Fin de Partie ---
        if match.is_game_over():
            winner_color = match.get_winner()
            if winner_color:
                message = f"Winner: {winner_color.upper()}!"
            else:
                message = "Draw!"
            display_message(WIN, message)
            running = False # Arrête la boucle de jeu

    # --- Nettoyage de Pygame ---
    pygame.quit() # Désinitialise Pygame
    sys.exit()    # Quitte le programme

# --- Point d'Entrée du Script ---
if __name__ == "__main__":
    main() # Appelle la fonction principale lorsque le script est exécuté directement


