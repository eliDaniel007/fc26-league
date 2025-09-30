from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random
import math
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_clé_secrète'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fifa25.db'
db = SQLAlchemy(app)

@app.context_processor
def inject_season():
    """Injecte la saison actuelle dans tous les templates"""
    season = Season.query.filter_by(is_active=True).first()
    return dict(current_season=season)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    current_week = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, finished

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    match_number = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    player1_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player1_score = db.Column(db.Integer)
    player2_score = db.Column(db.Integer)
    is_completed = db.Column(db.Boolean, default=False)
    
    season = db.relationship('Season')
    player1 = db.relationship('Player', foreign_keys=[player1_id])
    player2 = db.relationship('Player', foreign_keys=[player2_id])
    
    def get_winner(self):
        if self.player1_score is None or self.player2_score is None:
            return None
        if self.player1_score > self.player2_score:
            return self.player1
        elif self.player2_score > self.player1_score:
            return self.player2
        return None  # Match nul

class WeeklyStandings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    matches_played = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    goals_for = db.Column(db.Integer, default=0)
    goals_against = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
    goal_average = db.Column(db.Float, default=0.0)
    
    season = db.relationship('Season')
    player = db.relationship('Player')
    
    def calculate_stats(self):
        self.goal_average = self.goals_for / self.matches_played if self.matches_played > 0 else 0.0
        self.points = self.wins * 3 + self.draws

@app.route('/')
def home():
    # Récupérer ou créer la saison active
    season = Season.query.filter_by(is_active=True).first()
    if not season:
        season = Season(name=f"Saison FC 26 {datetime.now().year}")
        db.session.add(season)
        db.session.commit()
        
        # Initialiser les 5 joueurs si c'est une nouvelle saison
        initialize_default_players()
    
    # Récupérer tous les joueurs actifs
    players = Player.query.filter_by(is_active=True).all()
    
    # Récupérer les matchs de la semaine actuelle
    current_week_matches = Match.query.filter_by(
        season_id=season.id, 
        week_number=season.current_week
    ).order_by(Match.match_number).all()
    
    # Calculer les statistiques de la semaine actuelle
    weekly_standings = calculate_weekly_standings(season.id, season.current_week)
    
    # Calculer les statistiques cumulées
    cumulative_standings = calculate_cumulative_standings(season.id)
    
    return render_template('home.html', 
                         season=season,
                         players=players, 
                         current_week_matches=current_week_matches,
                         weekly_standings=weekly_standings,
                         cumulative_standings=cumulative_standings)

@app.route('/manage_players', methods=['GET', 'POST'])
def manage_players():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        
        if not player_name:
            flash('Le nom du joueur est requis', 'error')
            return redirect(url_for('manage_players'))
        
        # Vérifier si le joueur existe déjà
        existing_player = Player.query.filter_by(name=player_name).first()
        if existing_player:
            if existing_player.is_active:
                flash('Ce joueur est déjà actif', 'error')
            else:
                existing_player.is_active = True
                db.session.commit()
                flash(f'{player_name} réactivé !', 'success')
        else:
            # Vérifier qu'on n'a pas plus de 5 joueurs actifs
            active_count = Player.query.filter_by(is_active=True).count()
            if active_count >= 5:
                flash('Maximum 5 joueurs actifs autorisés', 'error')
                return redirect(url_for('manage_players'))
            
            # Créer un nouveau joueur
            new_player = Player(name=player_name, is_active=True)
            db.session.add(new_player)
            db.session.commit()
            flash(f'{player_name} ajouté !', 'success')
        
        return redirect(url_for('manage_players'))
    
    # Récupérer tous les joueurs
    active_players = Player.query.filter_by(is_active=True).all()
    inactive_players = Player.query.filter_by(is_active=False).all()
    
    return render_template('manage_players.html', 
                         active_players=active_players,
                         inactive_players=inactive_players)

@app.route('/generate_week')
def generate_week():
    season = Season.query.filter_by(is_active=True).first()
    if not season:
        flash('Aucune saison active', 'error')
        return redirect(url_for('home'))
    
    # Vérifier qu'il y a exactement 5 joueurs actifs
    active_players = Player.query.filter_by(is_active=True).count()
    if active_players != 5:
        flash('Il faut exactement 5 joueurs actifs', 'error')
        return redirect(url_for('manage_players'))
    
    # Vérifier si la semaine actuelle a déjà des matchs
    existing_matches = Match.query.filter_by(
        season_id=season.id, 
        week_number=season.current_week
    ).first()
    
    if existing_matches:
        flash('Les matchs de cette semaine existent déjà', 'error')
        return redirect(url_for('home'))
    
    # Générer les matchs de la semaine (4 matchs par joueur)
    generate_weekly_matches(season.id, season.current_week)
    
    flash(f'Semaine {season.current_week} générée ! Chaque joueur a 4 matchs.', 'success')
    return redirect(url_for('home'))

@app.route('/week/<int:week_number>')
def view_week(week_number):
    season = Season.query.filter_by(is_active=True).first()
    if not season:
        flash('Aucune saison active', 'error')
        return redirect(url_for('home'))
    
    # Récupérer les matchs de la semaine
    matches = Match.query.filter_by(
        season_id=season.id,
        week_number=week_number
    ).order_by(Match.match_number).all()
    
    # Calculer les statistiques de la semaine
    weekly_standings = calculate_weekly_standings(season.id, week_number)
    
    return render_template('week_view.html', 
                         season=season,
                         matches=matches,
                         week_number=week_number,
                         weekly_standings=weekly_standings)

@app.route('/standings')
def standings():
    season = Season.query.filter_by(is_active=True).first()
    if not season:
        flash('Aucune saison active', 'error')
        return redirect(url_for('home'))
    
    # Calculer les classements
    weekly_standings = calculate_weekly_standings(season.id, season.current_week)
    cumulative_standings = calculate_cumulative_standings(season.id)
    
    return render_template('standings.html',
                         season=season,
                         weekly_standings=weekly_standings,
                         cumulative_standings=cumulative_standings)

@app.route('/update_match/<int:match_id>', methods=['POST'])
def update_match(match_id):
    match = Match.query.get_or_404(match_id)
    
    score1 = int(request.form.get('score1'))
    score2 = int(request.form.get('score2'))
    
    match.player1_score = score1
    match.player2_score = score2
    
    # Déterminer le gagnant
    if score1 > score2:
        match.winner_id = match.player1_id
    elif score2 > score1:
        match.winner_id = match.player2_id
    # Pas de winner_id si égalité (match nul)
    
    db.session.commit()
    
    # Vérifier si tous les matchs de la journée sont terminés
    tournament = match.tournament
    round_matches = Match.query.filter_by(
        tournament_id=tournament.id,
        round_number=match.round_number
    ).all()
    
    all_finished = all(m.player1_score is not None and m.player2_score is not None for m in round_matches)
    
    if all_finished:
        # Vérifier combien de joueurs étaient en lice avant cette journée
        players_before = TournamentPlayer.query.filter_by(
            tournament_id=tournament.id,
            is_eliminated=False
        ).count()
        
        # Si c'était la finale (2 joueurs), le tournoi est terminé
        if players_before == 2:
            tournament.status = 'finished'
            db.session.commit()
            flash('🏆 Tournoi terminé ! Nous avons un champion !', 'success')
        else:
            # Éliminer les joueurs avec le moins de victoires
            eliminate_players(tournament.id, match.round_number)
            
            # Vérifier combien de joueurs restent après élimination
            remaining_players = TournamentPlayer.query.filter_by(
                tournament_id=tournament.id,
                is_eliminated=False
            ).count()
            
            if remaining_players == 2:
                # Générer le match de finale
                tournament.current_round += 1
                db.session.commit()
                generate_final_match(tournament.id, tournament.current_round)
                flash('🔥 Finale générée ! Le match décisif !', 'success')
            elif remaining_players > 2:
                # Générer la prochaine journée
                tournament.current_round += 1
                db.session.commit()
                generate_round_matches(tournament.id, tournament.current_round)
                flash(f'✅ Journée {tournament.current_round} générée ! {remaining_players} joueurs restants.', 'success')
            else:
                # Erreur - ne devrait pas arriver
                tournament.status = 'finished'
                db.session.commit()
                flash('Tournoi terminé de façon inattendue !', 'error')
    
    return redirect(url_for('tournament_round', round_number=match.round_number))

@app.route('/toggle_player/<int:player_id>')
def toggle_player(player_id):
    player = Player.query.get_or_404(player_id)
    
    if player.is_active:
        # Désactiver le joueur
        player.is_active = False
        flash(f'{player.name} désactivé', 'success')
    else:
        # Vérifier qu'on n'a pas déjà 5 joueurs actifs
        active_count = Player.query.filter_by(is_active=True).count()
        if active_count >= 5:
            flash('Maximum 5 joueurs actifs autorisés', 'error')
        else:
            player.is_active = True
            flash(f'{player.name} activé', 'success')
    
    db.session.commit()
    return redirect(url_for('manage_players'))

@app.route('/next_week')
def next_week():
    season = Season.query.filter_by(is_active=True).first()
    if not season:
        flash('Aucune saison active', 'error')
        return redirect(url_for('home'))
    
    # Vérifier que tous les matchs de la semaine actuelle sont terminés
    current_week_matches = Match.query.filter_by(
        season_id=season.id,
        week_number=season.current_week
    ).all()
    
    if not all(m.is_completed for m in current_week_matches):
        flash('Terminez tous les matchs de la semaine avant de passer à la suivante', 'error')
        return redirect(url_for('home'))
    
    # Passer à la semaine suivante
    season.current_week += 1
    db.session.commit()
    
    flash(f'🚀 Passage à la semaine {season.current_week}', 'success')
    return redirect(url_for('home'))

@app.route('/new_season')
def new_season():
    # Terminer la saison actuelle
    current_season = Season.query.filter_by(is_active=True).first()
    if current_season:
        current_season.is_active = False
        current_season.status = 'finished'
    
    # Créer une nouvelle saison
    new_season = Season(
        name=f"Saison FC 26 {datetime.now().year}-{datetime.now().month:02d}",
        start_date=datetime.utcnow(),
        current_week=1,
        is_active=True,
        status='in_progress'
    )
    db.session.add(new_season)
    db.session.commit()
    
    flash(f'🎉 Nouvelle saison créée : {new_season.name}', 'success')
    return redirect(url_for('home'))

@app.route('/season_history')
def season_history():
    # Récupérer toutes les saisons (active et archivées)
    all_seasons = Season.query.order_by(Season.start_date.desc()).all()
    active_season = Season.query.filter_by(is_active=True).first()
    
    return render_template('season_history.html', 
                         seasons=all_seasons,
                         active_season=active_season)

@app.route('/update_player_names')
def update_player_names():
    """Met à jour les noms des joueurs avec les vrais noms"""
    try:
        # Mapping des anciens noms vers les nouveaux
        name_mapping = {
            'Joueur 1': 'ABOUBACAR',
            'Joueur 2': 'DIOGO', 
            'Joueur 3': 'LIONEL',
            'Joueur 4': 'CHERIF',
            'Joueur 5': 'ELI'
        }
        
        updated_count = 0
        
        # Mettre à jour les noms existants
        for old_name, new_name in name_mapping.items():
            player = Player.query.filter_by(name=old_name).first()
            if player:
                # Vérifier qu'un joueur avec le nouveau nom n'existe pas déjà
                existing_new_player = Player.query.filter_by(name=new_name).first()
                if not existing_new_player:
                    player.name = new_name
                    updated_count += 1
                else:
                    # Si le nouveau nom existe déjà, supprimer l'ancien
                    db.session.delete(player)
        
        # Ajouter les joueurs manquants
        real_names = ['ABOUBACAR', 'DIOGO', 'LIONEL', 'CHERIF', 'ELI']
        for name in real_names:
            existing_player = Player.query.filter_by(name=name).first()
            if not existing_player:
                new_player = Player(name=name, is_active=True)
                db.session.add(new_player)
                updated_count += 1
        
        db.session.commit()
        
        flash(f'✅ {updated_count} joueurs mis à jour avec les vrais noms !', 'success')
        return redirect(url_for('manage_players'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Erreur lors de la mise à jour : {str(e)}', 'error')
        return redirect(url_for('manage_players'))

def initialize_default_players():
    """Initialise les 5 joueurs de la ligue FC 26"""
    default_players = ['ABOUBACAR', 'DIOGO', 'LIONEL', 'CHERIF', 'ELI']
    
    # Remplacer les anciens noms génériques par les vrais noms
    old_names = ['Joueur 1', 'Joueur 2', 'Joueur 3', 'Joueur 4', 'Joueur 5']
    
    # Supprimer les anciens joueurs génériques
    for old_name in old_names:
        old_player = Player.query.filter_by(name=old_name).first()
        if old_player:
            db.session.delete(old_player)
    
    # Ajouter les vrais joueurs
    for player_name in default_players:
        existing_player = Player.query.filter_by(name=player_name).first()
        if not existing_player:
            player = Player(name=player_name, is_active=True)
            db.session.add(player)
    
    db.session.commit()

def generate_weekly_matches(season_id, week_number):
    """Génère les matchs d'une semaine - chaque joueur joue 4 matchs"""
    players = Player.query.filter_by(is_active=True).all()
    
    if len(players) != 5:
        return False
    
    # Créer toutes les combinaisons possibles (10 matchs au total)
    all_matches = []
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            all_matches.append((players[i], players[j]))
    
    # Mélanger et sélectionner 10 matchs pour que chaque joueur joue 4 fois
    random.shuffle(all_matches)
    
    # Compter les matchs par joueur
    player_count = {player.id: 0 for player in players}
    selected_matches = []
    
    # Sélectionner les matchs pour que chaque joueur ait exactement 4 matchs
    for player1, player2 in all_matches:
        if player_count[player1.id] < 4 and player_count[player2.id] < 4:
            selected_matches.append((player1, player2))
            player_count[player1.id] += 1
            player_count[player2.id] += 1
            
            # Si on a 10 matchs (5 joueurs * 4 matchs / 2), on s'arrête
            if len(selected_matches) == 10:
                break
    
    # Créer les matchs en base
    for i, (player1, player2) in enumerate(selected_matches, 1):
        match = Match(
            season_id=season_id,
            week_number=week_number,
            match_number=i,
            player1_id=player1.id,
            player2_id=player2.id
        )
        db.session.add(match)
    
    db.session.commit()
    return True

def calculate_weekly_standings(season_id, week_number):
    """Calcule les statistiques d'une semaine spécifique"""
    players = Player.query.filter_by(is_active=True).all()
    standings = []
    
    for player in players:
        # Récupérer les matchs de cette semaine
        matches_p1 = Match.query.filter_by(
            season_id=season_id,
            week_number=week_number,
            player1_id=player.id,
            is_completed=True
        ).all()
        
        matches_p2 = Match.query.filter_by(
            season_id=season_id,
            week_number=week_number,
            player2_id=player.id,
            is_completed=True
        ).all()
        
        wins = draws = losses = goals_for = goals_against = 0
        
        for match in matches_p1:
                goals_for += match.player1_score
                goals_against += match.player2_score
                if match.player1_score > match.player2_score:
                    wins += 1
                elif match.player1_score == match.player2_score:
                    draws += 1
                else:
                    losses += 1
                    
        for match in matches_p2:
                goals_for += match.player2_score
                goals_against += match.player1_score
                if match.player2_score > match.player1_score:
                    wins += 1
                elif match.player2_score == match.player1_score:
                    draws += 1
                else:
                    losses += 1
        
        matches_played = len(matches_p1) + len(matches_p2)
        points = wins * 3 + draws
        goal_average = goals_for / matches_played if matches_played > 0 else 0
        
        standings.append({
            'player': player,
            'matches_played': matches_played,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'goal_difference': goals_for - goals_against,
            'points': points,
            'goal_average': round(goal_average, 2)
        })
    
    # Trier par points, puis par moyenne de buts, puis par différence de buts
    standings.sort(key=lambda x: (x['points'], x['goal_average'], x['goal_difference']), reverse=True)
    return standings

def calculate_cumulative_standings(season_id):
    """Calcule les statistiques cumulées depuis le début de la saison"""
    players = Player.query.filter_by(is_active=True).all()
    standings = []
    
    for player in players:
        # Récupérer tous les matchs de la saison
        matches_p1 = Match.query.filter_by(
            season_id=season_id,
            player1_id=player.id,
            is_completed=True
        ).all()
        
        matches_p2 = Match.query.filter_by(
            season_id=season_id,
            player2_id=player.id,
            is_completed=True
        ).all()
        
        wins = draws = losses = goals_for = goals_against = 0
        
        for match in matches_p1:
            goals_for += match.player1_score
            goals_against += match.player2_score
            if match.player1_score > match.player2_score:
                wins += 1
            elif match.player1_score == match.player2_score:
                draws += 1
            else:
                losses += 1
        
        for match in matches_p2:
            goals_for += match.player2_score
            goals_against += match.player1_score
            if match.player2_score > match.player1_score:
                wins += 1
            elif match.player2_score == match.player1_score:
                draws += 1
            else:
                losses += 1
        
        matches_played = len(matches_p1) + len(matches_p2)
        points = wins * 3 + draws
        goal_average = goals_for / matches_played if matches_played > 0 else 0
        
        standings.append({
            'player': player,
            'matches_played': matches_played,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'goal_difference': goals_for - goals_against,
            'points': points,
            'goal_average': round(goal_average, 2)
        })
    
    # Trier par points, puis par moyenne de buts, puis par différence de buts
    standings.sort(key=lambda x: (x['points'], x['goal_average'], x['goal_difference']), reverse=True)
    return standings

def update_weekly_standings(season_id, week_number):
    """Met à jour les statistiques hebdomadaires en base"""
    weekly_stats = calculate_weekly_standings(season_id, week_number)
    
    for stats in weekly_stats:
        # Chercher ou créer l'entrée de classement hebdomadaire
        standing = WeeklyStandings.query.filter_by(
            season_id=season_id,
            player_id=stats['player'].id,
            week_number=week_number
        ).first()
        
        if not standing:
            standing = WeeklyStandings(
                season_id=season_id,
                player_id=stats['player'].id,
                week_number=week_number
            )
            db.session.add(standing)
        
        # Mettre à jour les statistiques
        standing.matches_played = stats['matches_played']
        standing.wins = stats['wins']
        standing.draws = stats['draws']
        standing.losses = stats['losses']
        standing.goals_for = stats['goals_for']
        standing.goals_against = stats['goals_against']
        standing.points = stats['points']
        standing.goal_average = stats['goal_average']
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # Crée la base de données seulement si elle n'existe pas
        db.create_all()
        print("⚽ FC 26 League démarrée !")
        print("📊 Base de données prête - vos données sont persistantes !")
        print("🌐 Accédez à: http://localhost:8000")
    app.run(debug=True, host='0.0.0.0', port=8000)
