import json

import pandas as pd
import requests


class ApiParis:
    def __init__(self):
        self.token = 'YOUR_TOKEN'
        self.headers = {'Accept': '*/*', 'Content-Type': 'application/json'}

    def get_categories(self):
        url = 'https://api.paris.fr/api/data/2.1/QueFaire/get_categories/?token=' + self.token
        response = requests.get(url=url)
        return pd.DataFrame(data=json.loads(response.text)['data'])

    def get_tags(self):
        url = 'https://api.paris.fr/api/data/2.1/QueFaire/get_tags/?token=' + self.token
        response = requests.get(url=url)
        return pd.DataFrame(data=json.loads(response.text)['data'])

    def get_activities(self):
        url = 'https://api.paris.fr/api/data/2.1/QueFaire/get_activities/?token=' + self.token + \
              '&disciplines=0&offset=&limit='
        response = requests.get(url=url)

        selected_fields = ['zipCode', 'priceType', 'accessType', 'title', 'name']
        result = list()

        activities = json.loads(response.text)['data']

        for activity in activities:
            activity.update(activity['place'])
            del activity['place']

            activity.update(activity['modality'])
            del activity['modality']

            specific_activity = {your_key: activity[your_key] for your_key in selected_fields}
            result.append(specific_activity)

        res_df = pd.DataFrame(result)
        res_df['interest'] = 1

        return res_df


if __name__ == '__main__':
    api_paris = ApiParis()
    # categories_df = api_paris.get_categories()
    # tags_df = api_paris.get_tags()
    activities_df = api_paris.get_activities()
