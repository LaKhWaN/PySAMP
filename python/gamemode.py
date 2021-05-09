from samp import *
from const import *
import mysql.connector as sql
import time
from cmdparser import *
import hashlib
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ===================== [ DEFINES ] ========================== #

# SQL DEFINES
# SQL_HOST    =   "localhost"
# SQL_USER    =   "root"
# SQL_PASS    =   ""
# SQL_DB      =   "pysamp"

# DIALOG DEFINES
DIALOG_LOGIN = 0
DIALOG_REGISTER = 1

# COLOR DEFINES
COLOR_GROUP  =  0x216B98FF
COLOR_HELPEROOC  =  0xADFF2FFF
COLOR_HELPERCHAT  =  0xf3d7b9FF
COLOR_GARAGE  =  0x0066CCFF
COLOR_GM_REG  =  0xFFFFFFAA
COLOR_GM_UNREG  =  0xFF9999AA
COLOR_GM_ADMIN  =  0xFFCC66AA
COLOR_IRC  =  0x66CCFFAA
COLOR_ADMINCHAT  =  0xFF9933AA
COLOR_SYSTEM_PM  =  0x66CC00AA
COLOR_SYSTEM_GM  =  0xFF9966AA
COLOR_SYSTEM_PW  =  0xFFFF33AA
COLOR_SYSTEM_GW  =  0xCCCCCCAA
COLOR_MONEY_INC  =  0x00CC66AA
COLOR_MONEY_DEC  =  0xFF6600AA
COLOR_CMD  =  0xFFFFFFAA
COLOR_ADMIN_CMD  =  0xCC6666AA
COLOR_ADMIN_PM  =  0x6699CCAA
COLOR_ADMIN_PW  =  0x99CCFFAA
COLOR_ADMIN_GM  =  0xFF6633AA
COLOR_STATS  =  0xCCCCFFAA
COLOR_MESSAGE  =  0xFFCCFFAA
COLOR_RULES  =  0xDC143CAA
COLOR_ADMIN_TOALL  =  0x00FFFFAA
COLOR_GROUPTALK  =  0x87CEEBAA
COLOR_ADMIN_REPORT  =  0xFF69B4AA
COLOR_ADMIN_SPYREPORT  =  0xB0E0E6AA
COLOR_ADMIN  =  0xFF8200FF
COLOR_CARDIVE  =  0xEE82EEAA
COLOR_BLACK_PD  =  0x000000FF
COLOR_WHITE_PD  =  0xFFFFFFFF
COLOR_DISARMING  =  0xEE82EEBB
COLOR_WHITE  =  0xFFFFFF77
COLOR_ORANGE  =  0xFF9900AA
COLOR_PLAYER_ORANGE  =  0xFF9900AA
COLOR_PLAYER_KEMIROV  =  0xb89571FF
COLOR_PLAYER_SAN  =  0xFF0909FF
COLOR_IVORY  =  0xFFFF82FF
COLOR_BLUE  =  0x0000FFFF
COLOR_PURPLE  =  0x800080FF
COLOR_RED  =  0xCC3300FF
COLOR_PIR  =  0x80BFBF
COLOR_RED22  =  0xCC3300FF
COLOR_LIGHTGREEN  =  0x4BB32BFF
COLOR_VIOLET  =  0xEE82EEFF
COLOR_YELLOW  =  0xFFFF00FF
COLOR_SILVER  =  0xC0C0C0FF
COLOR_LIGHTBLUE  =  0x87CEFAFF
COLOR_PINK  =  0xFFB6C1FF
COLOR_INDIGO  =  0x4B00B0FF
COLOR_GOLD  =  0xFFD700FF
COLOR_FIREBRICK  =  0xB22222FF
COLOR_GREEN  =  0x008000FF
COLOR_LIGHTYELLOW  =  0xFAFA02FF
COLOR_GREY  =  0x778899FF
COLOR_LIGHTGREY  =  0xCCCCCCFF
COLOR_LIGHTGREYEX  =  0xA3A0A0FF
COLOR_MAGENTA  =  0xFF00FFFF
COLOR_BRIGHTGREEN  =  0x7CFC00FF
COLOR_DARKBLUE  =  0x000080AFF
COLOR_SYSTEM  =  0xDB7093FF
COLOR_BROWN  =  0x8B4513FF
COLOR_GREENYELLOW  =  0xADFF2FFF
COLOR_THISTLE  =  0xD8BFD8FF
COLOR_TURQUISE  =  0x48D1CCFF
COLOR_MAROON  =  0x800000FF
COLOR_STEELBLUE  =  0xB0C4DEFF
COLOR_GROUP_CHAT  =  0xFFFF80C8
COLOR_ME  =  0xC2A2DAAA
COLOR_ME2  =  0xC3A3DBAA
COLOR_GRAD1  =  0xB4B5B7FF
COLOR_GRAD2  =  0xBFC0C2FF
COLOR_GRAD3  =  0xCBCCCEFF
COLOR_LIME  =  0x81F600AA
COLOR_ERROR  =  0xFFB0B0DD
COLOR_USAGE  =  0xD9D9D9FF
COLOR_INFO  =  0xFFB0B0DD

COLOR_PLAYER_LIGHTBLUE  =  0x9292FFDD
COLOR_PLAYER_VLIGHTBLUE  =  0x66FFFFFF
COLOR_PLAYER_BLUE  =  0xA098F0AA
COLOR_PLAYER_NOOSE  =  0xFFFFFF77
COLOR_PLAYER_NOOSEHIGH  =  0xFFFFFF77
COLOR_PLAYER_DARKBLUE  =  0x000096FF
COLOR_PLAYER_SPECIALBLUE  =  0x4169FFFF
COLOR_PLAYER_LIGHTRED  =  0xFFB0B0DD
COLOR_PLAYER_RED  =  0xFF0000DD
COLOR_PLAYER_DARKRED  =  0xA10000FF
COLOR_PLAYER_SPECIALRED  =  0xB22222DD
COLOR_PLAYER_LIGHTGREEN  =  0x92FF92DD
COLOR_PLAYER_GREEN  =  0x00FF00DD
COLOR_PLAYER_DARKGREEN  =  0x009600DD
COLOR_PLAYER_SPECIALGREEN  =  0x00FF00FF
COLOR_PLAYER_LIGHTYELLOW  =  0xFFFF5EDD
COLOR_PLAYER_YELLOW  =  0xFFFF00DD
COLOR_PLAYER_DARKYELLOW  =  0xD3D300FF
COLOR_PLAYER_SPECIALYELLOW  =  0xCFAE00DD
COLOR_PLAYER_LIGHTPURPLE  =  0xFF92FFDD
COLOR_PLAYER_PURPLE  =  0xFF00FFDD
COLOR_PLAYER_DARKPURPLE  =  0x800080FF
COLOR_PLAYER_SPECIALPURPLE  =  0xDA70D6DD
COLOR_PLAYER_LIGHTBROWN  =  0xBA9072DD
COLOR_PLAYER_BROWN  =  0x663300FF
COLOR_PLAYER_DARKBROWN  =  0x6D360EDD
COLOR_PLAYER_LIGHTGREY  =  0xC7C7C7DD
COLOR_PLAYER_GREY  =  0x8B8B8BDD
COLOR_PLAYER_DARKGREY  =  0x656565FF
COLOR_PLAYER_WHITE  =  0xFFFFFF77
COLOR_PLAYER_WHITE_INV  =  0xFFFFFFFF
COLOR_PLAYER_BLACK  =  0x212121FF
COLOR_PLAYER_AQUAMARINE  =  0x7FFFD4DD
COLOR_PLAYER_CYAN  =  0x00FFFFDD
COLOR_PLAYER_VIOLET  =  0xCC0066AA
COLOR_PLAYER_SASF  =  0x556B2FFF
COLOR_PLAYER_POLITIC  =  0xCC9999FF
COLOR_PLAYER_MEXICAN1  =  0xFFFF8099
COLOR_PLAYER_BLACK1  =  0x741827FF

# ==================== [ TABLE CREATION AND OTHER THINGS ] ================== #

Base = declarative_base()

class Players(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    password = Column(String(64), nullable=False)

engine = create_engine("sqlite:///roleplay.db",echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(engine)
session  = Session()

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
        SendClientMessage(playerid,COLOR_WHITE,"You have been registered sucessfully. Please login again to continue.")
        ShowPlayerDialog(playerid,DIALOG_LOGIN,DIALOG_STYLE_PASSWORD.get(),"Login","Please enter your password to Login.","Login","Exit")
        return True        

    elif(dialogid == DIALOG_LOGIN):
        sql_password = session.query(Players.password).filter(Players.name == GetPlayerName(playerid,MAX_PLAYER_NAME.get())).one_or_none()[0]
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

# =================== [ OBJECT ORIANTED APPROACH ] ================= #



# ======================== [ FUNCTIONS ] =========================== #

def IsPlayerRegistered(playerid):
    if session.query(Players.name).filter(Players.name == GetPlayerName(playerid,MAX_PLAYER_NAME.get())).count():
        return True
    else:
        return False

def LoadPlayer(playerid):
    # SpawnPlayer(playerid)
    SendClientMessage(playerid,COLOR_PLAYER_DARKGREEN,"Welcome to our server, please enjoy your stay. <3")
    return True

def ReturnHashed(password):
    return hashlib.sha256(password).hexdigest()
# ======================= [ COMMANDS ] ============================== #
@cmd
def setgm(playerid):
    SetGameModeText("LaKhWaN OP")
    SendClientMessage(playerid,COLOR_RED,"Game Mode text setted to: LaKhWaN OP")
    return True