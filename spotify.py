__module_name__ = "NowPlayingSpotify"
__module_version__ = "1.0"
__module_description__ = "Spotify Now Playing Plugin"

import dbus
import hexchat

hook_timer_bad = None
last_playing = ""

def get_track_string():
    try:
        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
        spotify_properties = dbus.Interface(spotify_bus, "org.freedesktop.DBus.Properties")
        metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
        title = metadata['xesam:title']
        artist = metadata['xesam:artist'][0]
        album = metadata['xesam:album'] 
        now_playing = "1,0*** (0,3Spotify1,0) " + artist + " - " + title + " (" + album + ") - SpotifyNowPlaying by bad"
        return now_playing
    except:
        return last_playing

    
def send_message_all_channels(msg):
    if (msg != "empty") or (msg != ""):
        for chan in hexchat.get_list('channels'):
            if (chan.type == 2):
                chan.context.command("MSG " + chan.channel + " " + msg)
                
def check_last_playing(attr):
    current_playing = get_track_string()
    global last_playing
    
    if (last_playing != current_playing):
        last_playing = current_playing
        send_message_all_channels(current_playing)
    return True

def start_timer(word, word_eol, userdata):
    hexchat.prnt("*** Now playing activated")
    hexchat.prnt("*** to stop plugin, use: /stop-np")
    hook_timer_bad = hexchat.hook_timer(3000, check_last_playing)
    return True

def stop_timer(word, word_eol, userdata):
    global hook_timer_bad
    if hook_timer_bad is not None:
        hexchat.unhook(hook_timer_bad)
        hook_timer_bad = None
        
        hexchat.prnt("*** Now playing disabled")
        hexchat.prnt("*** to start plugin, use: /start-np")
        return hexchat.EAT_ALL


hexchat.hook_command("start-np", start_timer)
hexchat.hook_command("stop-np", stop_timer)

hexchat.prnt("*** Now playing loaded;")
hexchat.prnt("*** to start plugin, use: /start-np")
hexchat.prnt("*** to stop plugin, use: /stop-np")
