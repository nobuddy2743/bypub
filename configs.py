import os


class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "5711421545:AAH50_KzU2tt7xVML7oHBb8GofGDxosmG0o")
    API_HASH = os.environ.get("API_HASH", "209169a882ff43c4f1621b7cc97c255b") 
    API_ID = os.environ.get("API_ID", "15050363")
     
    #SESSION_NAME = os.environ.get("SESSION_NAME", "Mdisk-Bot")
    #UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL")
    LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "-1001899279654")
    #DOWN_PATH = os.environ.get("DOWN_PATH", "./downloads")
    #TIME_GAP = int(os.environ.get("TIME_GAP", 5))
    
    MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://bypasskrish:nlcaTBOgnCeRy51h@cluster0.7ncdvjq.mongodb.net/?retryWrites=true&w=majority")
    #BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", False))
    BOT_OWNER = int(os.environ.get("BOT_OWNER", 660755963))
