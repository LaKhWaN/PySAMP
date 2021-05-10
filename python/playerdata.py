class PlayerData():
    def __init__(self):
        self.admin_level = session.query(Player.admin_level).filter(Player.name == GetPlayerName(pid,MAX_PLAYER_NAME.get()))