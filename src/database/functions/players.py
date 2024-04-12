from src.database.tables import Players


def get_player_by_id(player_id: int) -> Players:
    return Players.query.filter_by(player_id=player_id).first()
