import os
import shutil
from colorama import Style
from colorama import Fore as Color
from colorama import init as ColoramaInit


def multiEndsWith(text, folder): return any(item.endswith(text) for item in folder)
def doubleEndsWith(lst, folder): return any(multiEndsWith(item, folder) for item in lst)
    

ColoramaInit(autoreset=True)

print(Style.BRIGHT + Color.MAGENTA + "\n█▀█ █ █▀ █▀▀ █▀▀\n█▄█ ▄ ▄█ █▀░ █▄▄\n\n" + Color.RESET + Style.DIM + "by _Joey (imperialwool) | v0.1\ncontacts: linktr.ee/imperialwool\ngithub: https://github.com/toxichead/osu-songs-folder-cleaner\n\n" + Style.NORMAL)
path = str(input("[>] Folder to osu!: ") + "/Songs").replace("\\", "/").replace("//", "/").replace("/Songs/Songs", "/Songs")
try: beatmapsFolder = os.listdir(path)
except: 
    print(Color.RED + "\n[X] Path not exists. Try again.\n\n" + Color.RESET)
    exit()

detectImages = True if input("\n[>] Check for images in folders? (y for yes)\n> ").lower() in ['y', 'yes', 'д', 'да'] else False

text4input = Color.RED + "\nThis script will delete empty, useless and duplicate folders on CODE's opinion. Deletion of files is not reversible!\nIf you are agree to start, enter \"IM AGREE TO GIVE MY SOUL TO BTMC\"\n> " + Color.RESET
if input(text4input) != "IM AGREE TO GIVE MY SOUL TO BTMC":
    print("\n[X] Ok. Exiting...\n\n")
    exit()

print(
    Color.CYAN  + "\n\n█░█░█ █▀█ █▀█ █▄▀ █ █▄░█ █▀▀ ░ ░ ░\n▀▄▀▄▀ █▄█ █▀▄ █░█ █ █░▀█ █▄█ ▄ ▄ ▄"
                + "\n\n[.] Delete empty folders...\n"
                + Color.RESET
)
for beatmap in beatmapsFolder:
    beatmapFiles = os.listdir(path + "/" + beatmap)
    Mp3, Osu, Images = multiEndsWith(".mp3", beatmapFiles), multiEndsWith(".osu", beatmapFiles), doubleEndsWith(['.jpg', '.jpeg', '.png'], beatmapFiles)
    
    if Mp3 and Osu and (not detectImages or Images):
        print(f"[.] {beatmap} is ok.")
    else:
        toPrint = f"[V] {beatmap} is missing: "
        if not Mp3: toPrint += "mp3, "
        if not Osu: toPrint += "osu files, "
        if not Images and detectImages: toPrint += "images, "
        toPrint = toPrint[:-2]
        
        try:
            shutil.rmtree(path + "/" + beatmap)
            print(Color.GREEN + toPrint + '. So, I deleted folder.' + Color.RESET)
        except:
            print(Color.RED + toPrint + '. But I cannot delete folder.' + Color.RESET)
        
print(Color.CYAN + "\n\n[.] Finding duplicates..." + Color.RESET)  
beatmapsFolder = os.listdir(path)
allBeatmaps = [beatmap.partition(" ")[0] for beatmap in beatmapsFolder]
duplicates = list(set([beatmapId for beatmapId in allBeatmaps if allBeatmaps.count(beatmapId) > 1]))

print(Color.CYAN + f"\n\n[.] Found {len(duplicates)} duplicates. Deleting...\n" + Color.RESET if len(duplicates) > 0 else Color.CYAN + f"\n\n[.] Found {len(duplicates)} duplicates.\n" + Color.RESET) 
for beatmap in beatmapsFolder:
    beatmapId = beatmap.partition(" ")[0]
    if beatmapId in duplicates:
        duplicates.remove(beatmapId)
        try:
            shutil.rmtree(path + "/" + beatmap)
            print(Color.GREEN + f'[V] {beatmapId} is duplicate, so folder "{beatmap}" deleted.'          + Color.RESET)
        except:
            print(Color.RED +   f'[X] {beatmapId} is duplicate, but I cannot delete folder "{beatmap}".' + Color.RESET)

print(
    Color.CYAN  + "\n\n█▀▄ █▀█ █▄░█ █▀▀\n█▄▀ █▄█ █░▀█ ██▄" + Color.RESET
                + "\n\nHave a great day and good luck with clicking circles!\n\n"
                + "⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⡠⢴⣴⣾⣿⡿⠓⡠⠀⠀⠀⠀⠠⢄⠁⢀⠀⠀\n"
                + "⠀⠀⠀⠀⠀⠳⣽⡽⠀⠀⡠⢊⣴⣿⣿⣿⣡⠖⠁⣀⡤⢖⠟⠁⡠⠀⡙⢿⣷⣄\n"
                + "⠀⠀⠐⡀⠀⠀⠀⠀⢠⣾⣿⣿⢽⣿⣿⣿⣥⠖⣻⣯⡾⠃⠀⡔⡀⠀⣷⢸⢿⣿\n"
                + "⠀⠀⠀⢰⠀⠀⠀⢠⢟⣿⠃⢀⣾⣿⠟⠋⢀⡾⢋⣾⠃⣠⡾⢰⡇⡇⣿⣿⡞⣿\n"
                + "⠀⠀⡤⣈⡀⠀⢀⠏⣼⣧⡴⣼⠟⠁⠀⠀⡾⠁⣾⡇⣰⢿⠃⢾⣿⣷⣿⣿⣇⢿\n"
                + "⠀⠀⠱⠼⠊⠀⠄⡜⣿⣿⡿⠃⠈⠁⠀⢸⠁⢠⡿⣰⢯⠃⠀⠘⣿⣿⣿⣿⣿⠸\n"
                + "⠀⠀⠀⠀⠀⠀⡘⡀⣸⣿⣱⡤⢴⣄⠀⠈⠀⠘⣷⠏⠌⠢⡀⠀⢿⣿⣿⣿⡟⡄\n"
                + "⠀⠀⠀⠀⢀⣌⠌⣴⣿⣿⠃⣴⣿⣟⡇⠀⠀⠀⠟⠀⠀⠀⠈⠢⢈⣿⡟⣿⡗⡇\n"
                + "⠀⠀⢀⡴⡻⣡⣾⠟⢹⡇⠀⡇⢄⢿⠇⠀⠀⠀⠀⠀⠀⣽⣶⣄⡀⠘⢷⡹⣿⣿\n"
                + "⠀⠀⣧⣾⡿⠋⠁⢀⡜⠙⡄⠓⠐⠁⠀⠀⠀⠀⠀⠀⡼⠛⠻⣟⠛⣆⠈⢷⣿⣿\n"
                + "⣴⣾⣟⣵⣿⣿⣿⣁⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡧⠠⠔⡹⠀⢸⠀⣼⣿⣿\n"
                + "⠿⡽⢫⡉⠀⣠⠔⠁⡀⠕⠠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠖⠊⠀⠀⢊⣾⢿⡿⠉\n"
                + "⠀⠁⠀⡹⢨⠁⠐⠈⢀⡠⠐⠁⠄⠡⡀⡀⠀⠀⠀⠀⠀⠀⠀⠠⠶⢛⡨⠊⠀⠀\n"
                + "⠀⠀⡜⠀⠈⣂⠀⠀⠀⠀⡠⠐⠉⡆⠀⣀⢀⣀⣀⣀⡀⠀⠀⣀⠴⣁⡀⠤⠀⠀\n"
                + "⠀⠈⠀⠀⠀⡇⠑⢄⠀⠀⠀⠀⣲⢥⡎⠀⢰⠀⢸⠀⢀⠉⠙⣿⣧⣀⣀⣂⣤⣼\n"
                + "⠀⠀⠀⠆⠁⠃⠀⠀⠈⠒⠒⠊⣸⠚⠁⠀⠀⠀⠀⠀⠀⠀⡜⠁⠀⠀⠀⠀⠈⠚\n"
                + "⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⢀⠋⢆⠀⠀⠀⠀⠀⠀⠀⡘⠀⠀⠀⠀⠀⠀⠀⠀\n"
                + "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠒⠂⠀⠀⠐⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
                + "\n"
    )
