import json
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator
from watson_developer_cloud import PersonalityInsightsV3 as PersonalityInsights
import pandas as pd
import numpy as np
import os
import requests


language_translator = LanguageTranslator(username='53d06608-1e59-4fd3-b7a6-06272abf99a9', password='HnXHP3R8pgDj')
personality_insights = PersonalityInsights(username='df9417a6-0efd-4232-9f1c-3b8b265c3830', password='ZFkRifBZ0SBj')


class FindMatch:

    def __init__(self, data):

        self.characteristics = ['user_type']
        self.activities = ['museum', 'park', 'cafe', 'historic', 'unique']

        # create database if none is present
        if not os.path.isfile('database.csv'):
            with open('test.txt') as test:
                test_profile = personality_insights.profile(test.read())
                self.create_database(test_profile)

        self.database = pd.read_csv('database.csv')
        self.index_number = len(self.database)

        # get this from server/facebook
        data = json.loads(data)
        token = data['token']
        r = requests.get("https://graph.facebook.com/v2.11/me/posts?access_token=" + token)
        fb_data = json.loads(r.content)
        self.text = ''
        for i in range(len(fb_data['data'])):
            self.text += fb_data['data'][i]['story']

        self.user_characteristics = [data['usertype']]
        self.date = data['date']
        self.preferences = list(data['likes'])

        # parameters to be tuned
        self.gender_correction = 0.8
        self.age_correction = 1.01

        # provide user with sliders if word count is below 600
        # if len(self.text.split()) < 600:
        #     client.send().....
        #     print 'ERROR: word count too low'

        # read what weight vector is currently being used
        self.weight_vector_id = 0
        self.weight_vector = np.load('weight_vectors.npy')[self.weight_vector_id]


    def create_database(self, generic_profile):

        profile = generic_profile
        database = pd.DataFrame([])
        categories = ['needs', 'personality', 'values']

        for category in categories:
            for i in range(len(profile[category])):
                column_name = profile[category][i]['trait_id']
                database[column_name] = pd.Series([])

        # user characteristics
        for characteristic in self.characteristics:
            database[characteristic] = pd.Series([])

        # availability
        database['date'] = pd.Series([])

        # activities
        for activity in self.activities:
            database[activity] = pd.Series([])

        database.to_csv('database.csv', index=False)

        return


    def get_language(self):
        language = language_translator.identify(self.text)
        return language['languages'][0]['language']


    def translate_text(self):

        language = self.get_language()
        translation = self.text

        if not language == 'en':
            translation = language_translator.translate(text=self.text, source=str(language), target='en')

        return translation


    def analyze_personality(self):
        profile = personality_insights.profile(self.text)
        return profile


    def fill_database(self, profile):

        categories = ['needs', 'personality', 'values']

        for category in categories:
            for i in range(len(profile[category])):
                column_name = profile[category][i]['trait_id']
                self.database.set_value(self.index_number, column_name, profile[category][i]['percentile'])

        for characteristic, user_characteristic in zip(self.characteristics, self.user_characteristics):
            self.database.set_value(self.index_number, characteristic, user_characteristic)

        self.database.set_value(self.index_number, 'date', self.date)

        for activity, preference in zip(self.activities, self.preferences):
            self.database.set_value(self.index_number, activity, preference)

        self.database.to_csv('database.csv', index=False)

        return


    def find_match(self):

        match_id = 0

        for i in range(self.index_number):

            # Now it only checks if user_type is not the same. Must also check if dates are the same:
            # if self.database['date'].loc[self.index_number] == self.database['date'].loc[i]:

            if self.database['user_type'].loc[self.index_number] != self.database['user_type'].loc[i]:
                # calculate error
                error = self.database.loc[i][:22] - self.database.loc[self.index_number][:22]
                weighted_error = np.array(error) * self.weight_vector
                error = np.sum(np.absolute(weighted_error))

                # change error depending on gender and age
                if self.database['gender'].loc[i] == self.database['gender'].loc[self.index_number]:
                    error *= self.gender_correction
                if self.database['age'].loc[i] != self.database['age'].loc[self.index_number]:
                    error *= self.age_correction * (self.database['gender'].loc[i] - self.database['gender'].loc[self.index_number])

                if i == 0:
                    current_best = error
                    match_id = i

                if error < current_best:
                    current_best = error
                    match_id = i

        return match_id


    def main(self):

        self.text = self.translate_text()
        profile = self.analyze_personality()
        self.fill_database(profile)
        match_id = self.find_match()

        return match_id

