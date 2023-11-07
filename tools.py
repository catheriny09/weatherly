import json

def fetchKeys():
    """ Retrieves api tokens from a config file
    
    Returns: 
        string: Slack api token
        string: openai api token
    """
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        openai_key=config["openai_api_key"]
        weather_key=config["weather_api"]
        
    return openai_key, weather_key