import spotify

config = spotify.Config()
config.user_agent = "My Spotify Client"
config.tracefile = b"/tmp/libspotify-trace.log"
session = spotify.Session(config)