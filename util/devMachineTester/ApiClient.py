import requests
import json

class ApiClient():
  baseURL = None
  def __init__(self, baseURL):
    self.baseURL = baseURL

  def getStatsA(self, postBody, tenant, name):
    url = self.baseURL + "/api/public/main/statsA/" + tenant + "/" + name
    headers={}
    headers["content-type"] = "application/json"
    response = requests.post(url, data=json.dumps(postBody), headers=headers)
    if response.status_code != 200:
      print("FAILED call to " + url + " - bad response ", response.status_code, response.text)
      return None

    response = json.loads(response.text)
    if "daily" not in response:
      print(response)
      raise Exception("Unrecogniesd response")
    return response