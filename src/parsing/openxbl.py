import requests

import config as config
from src.model import achivment
from src.model.achivment import Achievement
import src.model.games as dbGame

BASE_URL = 'https://xbl.io/'
ACCOUNT = BASE_URL + '/api/v2/account'
ACHIEVMENTS = BASE_URL + '/api/v2/achievements'
ACHIEVMENTS_TITLE = BASE_URL + '/api/v2/achievements/title/'
SCREENSHOT = BASE_URL + '/api/v2/activity/history'
PLAYED_MINUTES = BASE_URL + '/api/v2/achievements/stats/'

headers = {
  'accept': '*/*',
  'dnt': '1',
  'referer': 'https://xbl.io/console',
  'sec-ch-ua-platform': "Windows",
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
  'x-authorization': 'f9f594cf-d146-4192-a4f7-37dd083dbc6f'
}

class Account:
  def __init__(self, GamerTag, GamerScore, GemrIconUrl):
    self.GamerTag = GamerTag
    self.GamerScore = GamerScore
    self.GemrIconUrl = GemrIconUrl

class Achievements:
  def __init__(self, game_name, displayImage, currentAchievements,
                currentGamerscore, totalGamerscore, lastTimePlayed):
    self.game_name = game_name
    self.displayImage = displayImage
    self.currentAchievements = currentAchievements
    self.currentGamerscore = currentGamerscore
    self.totalGamerscore = totalGamerscore
    self.lastTimePlayed = lastTimePlayed

class Media:
  def __init__(self, type, screen_url, video_url):
    self.type = type
    self.screen_url = screen_url
    self.video_url = video_url

def get_acc():
    response = requests.get(ACCOUNT, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Parse the JSON data and create Account objects
        for user in data['profileUsers']:
            settings = user['settings']
            gamer_tag = next((setting['value'] for setting in settings if setting['id'] == 'Gamertag'), None)
            gamer_score = next((setting['value'] for setting in settings if setting['id'] == 'Gamerscore'), None)
            game_display_pic_raw = next((setting['value'] for setting in settings if setting['id'] == 'GameDisplayPicRaw'), None)
            account = Account(gamer_tag, gamer_score, game_display_pic_raw)
        return account
    else:
        print(f"Request failed with status code {response.status_code}")
        return None


def update_games(user_id, xapi):

  headers = {
  'accept': '*/*',
  'dnt': '1',
  'referer': 'https://xbl.io/console',
  'sec-ch-ua-platform': "Windows",
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
  'x-authorization': f'{xapi}'
}

  response = requests.get(ACHIEVMENTS, headers=headers)
  if response.status_code == 200:
    data = response.json()

    for game in data['titles']:

      game = dbGame.Game(user_id[0], game['name'], game['titleId'])
      game.add()

def get_achivments(game_id, xapi) -> list[Achievement]:
  headers = {
  'accept': '*/*',
  'x-authorization': f'{xapi}'
}

  response = requests.get(ACHIEVMENTS_TITLE + game_id, headers=headers)
  if response.status_code == 200:
    data = response.json()
    achivments = []
    for a in data['achievements']:

      achivment = Achievement(a["name"], a["progressState"], a["isSecret"], a["description"], a["lockedDescription"], a['rewards'][0]["value"], a['mediaAssets'][0]['url'])

      achivments.append(achivment)

    return achivments


def get_sceenshots(xapi) -> list[Media]:
  headers = {
  'accept': '*/*',
  'x-authorization': f'{xapi}'
}

  response = requests.get(SCREENSHOT, headers=headers)
  if response.status_code == 200:
    data = response.json()
    medias = []
    i=0
    for activity_item in data['activityItems']:
      if i > 5:
        break
      else:
        i+=1
        if 'clipId' in activity_item:
            media = Media('video', activity_item["clipThumbnail"], activity_item["downloadUri"])
            medias.append(media)
        elif 'screenshotId' in activity_item:
            media = Media('photo', activity_item["screenshotUri"], "")
            medias.append(media)
        else:
          continue

    return medias


def get_minuted_playes(xapi, game_id) -> list[Media]:
  headers = {
  'accept': '*/*',
  'x-authorization': f'{xapi}'
}

  response = requests.get(PLAYED_MINUTES+game_id, headers=headers)
  if response.status_code == 200:
    data = response.json()
    minutes = int(data['statlistscollection'][0]['stats'][0]['value'])

    if minutes < 60:
        print(f"{minutes} minutes")
    elif minutes < 24 * 60:
        hours = minutes // 60
        minutes %= 60
        return f"{hours} hours {minutes} minutes"
    else:
        days = minutes // (24 * 60)
        hours = (minutes % (24 * 60)) // 60
        minutes %= 60
        return f"{days} days {hours} hours {minutes} minutes"
