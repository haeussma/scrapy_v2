from enum import Enum

class Attribute(Enum):
    TRACK = "track"
    ARTIST = "artist"
    ALBUM = "album"
    PLAYS = "plays"
    LIKES = "likes"
    SHARES = "shares"
    COMMENTS = "comments"

class Type(Enum):
    TRACK = 'track'
    PODCAST = 'podcast'
    CLIP = 'clip'

class Platform(Enum):
    SPOTIFY = 'spotify'
    SOUNDCLOUD = 'soundcloud'
    YOUTUBE = 'youtube'