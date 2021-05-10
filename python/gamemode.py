from samp import *
from const import *
import time
from cmdparser import *
import hashlib
from defines import *
from connection import * 

# ================= [ PlayerData Class ] =================== #
class PlayerData():
    def __init__(self):
        self.admin_level = session.query(Player.admin_level).filter(Player.name == GetPlayerName(self,MAX_PLAYER_NAME.get())).one_or_none()[0]
        self.name = GetPlayerName(self,MAX_PLAYER_NAME.get())

def OnGameModeInit():
    time.sleep(2)
    print(" ========================= [ Loaded SAMP PY GAMEMODE ] =========================")
    print(" =============================== [ BY LAKHWAN ] ================================")
    print(" ===============================================================================") 
    
    
    return True
    
def OnGameModeExit():
    session.commit()
    session.close()
    return True

def OnPyUnload():
    OnGameModeExit()
    return True

def OnPyReload():
    OnGameModeInit()
    return True

def OnPlayerConnect(playerid):
    SendClientMessage(playerid,0xFFFFFF,f"Welcome to the Server {GetPlayerName(playerid,MAX_PLAYER_NAME.get())}")
    SendClientMessage(playerid,-1,"[SERVER] Please wait while we make connection to our database...")
    if(IsPlayerRegistered(playerid)):
        ShowPlayerDialog(playerid,DIALOG_LOGIN,DIALOG_STYLE_PASSWORD.get(),"Login","Please enter your password to Login.","Login","Exit")
    else:
        ShowPlayerDialog(playerid,DIALOG_REGISTER,DIALOG_STYLE_PASSWORD.get(),"Register","Please enter your password to register below.","Register","Exit")
    return True
    
def OnPlayerDisconnect(playerid, reason):
    return True
    
def OnPlayerSpawn(playerid):
    SetPlayerPos(playerid,1643.2782,-2286.4919,-1.1964)
    SetPlayerFacingAngle(playerid,269.6626)
    return True
    
def OnPlayerDeath(playerid, killerid, reason):
    return True
    
def OnVehicleSpawn(vehicleid):
    return True
    
def OnVehicleDeath(vehicleid, killerid):
    return False
    
def OnPlayerText(playerid, text):
    text = decode(text)
    return False
    
def OnPlayerCommandText(playerid, cmdtext):
    cmdtext = decode(cmdtext)
    return handle_command(playerid, cmdtext)
    
def OnPlayerRequestClass(playerid, classid):
    return True
    
def OnPlayerEnterVehicle(playerid, vehicleid, ispassenger):
    return False
    
def OnPlayerExitVehicle(playerid, vehicleid):
    return False
    
def OnPlayerStateChange(playerid, newstate, oldstate):
    return False
    
def OnPlayerEnterCheckpoint(playerid):
    return False
    
def OnPlayerLeaveCheckpoint(playerid):
    return False
    
def OnPlayerEnterRaceCheckpoint(playerid):
    return False
    
def OnPlayerLeaveRaceCheckpoint(playerid):
    return False
    
def OnRconCommand(cmd):
    cmd = decode(cmd)
    return False
    
def OnPlayerRequestSpawn(playerid):
    return True
    
def OnObjectMoved(objectid):
    return False
    
def OnPlayerObjectMoved(playerid, objectid):
    return False
    
def OnPlayerPickUpPickup(playerid, pickupid):
    return False
    
def OnVehicleMod(playerid, vehicleid, componentid):
    return True
    
def OnEnterExitModShop(playerid, enterexit, interiorid):
    return False
    
def OnVehiclePaintjob(playerid, vehicleid, paintjobid):
    return True
    
def OnVehicleRespray(playerid, vehicleid, color1, color2):
    return True
    
def OnVehicleDamageStatusUpdate(vehicleid, playerid):
    return False
    
def OnUnoccupiedVehicleUpdate(vehicleid, playerid, passenger_seat, new_x, new_y, new_z, vel_x, vel_y, vel_z):
    return True
    
def OnPlayerSelectedMenuRow(playerid, row):
    return False
    
def OnPlayerExitedMenu(playerid):
    return False
    
def OnPlayerInteriorChange(playerid, newinteriorid, oldinteriorid):
    return False
    
def OnPlayerKeyStateChange(playerid, newkeys, oldkeys):
    return False
    
def OnRconLoginAttempt(ip, password, success):
    password = decode(password)
    return False
    
def OnPlayerUpdate(playerid):
    return True
    
def OnPlayerStreamIn(playerid, forplayerid):
    return False
    
def OnPlayerStreamOut(playerid, forplayerid):
    return False
    
def OnVehicleStreamIn(vehicleid, forplayerid):
    return False
        
def OnVehicleStreamOut(vehicleid, forplayerid):
    return False
    
def OnActorStreamIn(actorid, forplayerid):
    return False
    
def OnActorStreamOut(actorid, forplayerid):
    return False
    
def OnDialogResponse(playerid, dialogid, response, listitem, inputtext):
    if(dialogid == DIALOG_REGISTER): # {hashlib.sha256(inputtext).hexdigest()}
        player = Players(name=GetPlayerName(playerid,MAX_PLAYER_NAME.get()),password=ReturnHashed(inputtext))
        session.add(player)
        session.commit()
        # SendClientMessage(playerid,COLOR_WHITE,"You have been registered sucessfully. Please login again to continue.")
        ShowPlayerDialog(playerid,DIALOG_LOGIN,DIALOG_STYLE_PASSWORD.get(),"Login","Please enter your password to Login.","Login","Exit")
        return True        

    elif(dialogid == DIALOG_LOGIN):
        sql_password = session.query(Player.password).filter(Player.name == GetPlayerName(playerid,MAX_PLAYER_NAME.get())).one_or_none()[0]
        if(ReturnHashed(inputtext) == sql_password):
            SendClientMessage(playerid,COLOR_WHITE,"You have logged in sucessfully.!") 
            LoadPlayer(playerid)
            return True
        
        else:
            SendClientMessage(playerid,COLOR_WHITE,"Incorrect Password Please try again.!")
            ShowPlayerDialog(playerid,DIALOG_LOGIN,DIALOG_STYLE_PASSWORD.get(),"Login","Please enter your password to Login.","Login","Exit")
            return True

    return False
    
def OnPlayerTakeDamage(playerid, issuerid, amount, weaponid, bodypart):
    return False
    
def OnPlayerGiveDamage(playerid, damagedid, amount, weaponid, bodypart):
    return False
    
def OnPlayerGiveDamageActor(playerid, damaged_actorid, amount, weaponid, bodypart):
    return False
    
def OnPlayerClickMap(playerid, fX, fY, fZ):
    return False
    
def OnPlayerClickTextDraw(playerid, clickedid):
    return False
    
def OnPlayerClickPlayerTextDraw(playerid, playertextid):
    return False
    
def OnIncomingConnection(playerid, ip_address, port):
    ip_address = decode(ip_address)
    return False
    
def OnTrailerUpdate(playerid, vehicleid):
    return True
    
def OnVehicleSirenStateChange(playerid, vehicleid, newstate):
    return False
    
def OnPlayerClickPlayer(playerid, clickedplayerid, source):
    return False
    
def OnPlayerEditObject(playerid, playerobject, objectid, response, fX, fY, fZ, fRotX, fRotY, fRotZ):
    return False
    
def OnPlayerEditAttachedObject(playerid, response, index, modelid, boneid, fOffsetX, fOffsetY, fOffsetZ, fRotX, fRotY, fRotZ, fScaleX, fScaleY, fScaleZ):
    return False
    
def OnPlayerSelectObject(playerid, type, objectid, modelid, fX, fY, fZ):
    return False
    
def OnPlayerWeaponShot(playerid, weaponid, hittype, hitid, fX, fY, fZ):
    return True

def OnProcessTick():
    return None


def OnThreadingInit():
    return None

def OnThreadingStopSignal():
    return None


# ======================== [ FUNCTIONS ] =========================== #




def IsPlayerRegistered(playerid):
    if session.query(Player.name).filter(Player.name == GetPlayerName(playerid,MAX_PLAYER_NAME.get())).count():
        return True
    else:
        return False

def LoadPlayer(playerid):
    SendClientMessage(playerid,COLOR_PLAYER_DARKGREEN,"Welcome to our server, please enjoy your stay. <3")
    playerid = PlayerData()
    return True

def ReturnHashed(password):
    return hashlib.sha256(password).hexdigest()

def GetPlayerAdminLevel(playerid):
    return playerid.admin_level


# ======================= [ COMMANDS ] ============================== #

# === [ ADMIN COMMANDS] === #

@cmd
def makeadmin(playerid,targetid,level):
    if(GetPlayerAdminLevel(playerid) > 5):
        if not IsPlayerConnected(targetid):
            SendClientMessage(playerid,COLOR_ERROR,"[ADMIN] That player is not connected.")
            return True
        else:
            playerid.admin_level = level
            SendClientMessage(playerid,COLOR_RED,f"[ADMIN] You have made {GetPlayerName(targetid,MAX_PLAYER_NAME.get())} admin of level: {level}")
            return True
    else:
        SendClientMessage(playerid,COLOR_ERROR,"[SERVER] You are not allowed to use this command.")
        return True
@cmd
def setgm(playerid,arg1):
    if(GetPlayerAdminLevel(playerid) > 3):
        SetGameModeText(arg1)
        SendClientMessage(playerid,COLOR_RED,"Game Mode text setted to: LaKhWaN OP")
        return True
    else:
        SendClientMessage(playerid,COLOR_ERROR,"[SERCER] You are not allowed to use this command")
        return True
@cmd
def setgm1(playerid,arg1):
    if(GetPlayerAdminLevel(playerid) > 3):
        SetGameModeText(arg1.decode())
        SendClientMessage(playerid,COLOR_RED,"Game Mode text setted to: LaKhWaN OP")
        return True
    else:
        SendClientMessage(playerid,COLOR_ERROR,"[SERVER] You are not allowed to use this command")
        return True


@cmd
def lakhwanop(playerid):
    OnPyReload()
    return True