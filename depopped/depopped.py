
# - - - - - - - - - - - - -  - - - - - - - - -
# Name: Depopped
# Description: A simple API wrapper for Depop.
# Author: github.com/akimbo7
# Current line count: 491
# - - - - - - - - - - - - -  - - - - - - - - -

import os
import uuid
import json
import requests
import random
import string
from colorama import *; init()

class Client:

    def __init__(self, log = False, agent = 'IOS'):

        self.log = log
        self.baseUrl = 'https://api.depop.com'

        if self.log: print(f'{Fore.LIGHTBLUE_EX} * {Fore.RESET} Logging enabled.')

        self.session = requests.Session()
        if self.log: print(f'{Fore.LIGHTMAGENTA_EX} * {Fore.RESET} Session created.')


        if agent.lower() == 'ios':
            agents = open(f'{os.path.join(os.path.dirname(__file__))}/User-Agents/ios.txt').read().splitlines()
            self.userAgent = random.choice(agents)
            self.session.headers.update({'user-agent': self.userAgent})
            if self.log: print(f'{Fore.LIGHTBLUE_EX} * {Fore.RESET} User Agent: "{self.userAgent}"')
            if self.log: print(f'{Fore.LIGHTMAGENTA_EX} * {Fore.RESET} User Agent set.')

        if agent.lower() == 'android':
            agents = open(f'{os.path.join(os.path.dirname(__file__))}/User-Agents/android.txt').read().splitlines()
            self.userAgent = random.choice(agents)
            self.session.headers.update({'user-agent': self.userAgent})
            if self.log: print(f'{Fore.LIGHTBLUE_EX} * {Fore.RESET} User Agent: "{self.userAgent}"')
            if self.log: print(f'{Fore.LIGHTMAGENTA_EX} * {Fore.RESET} User Agent set.')


    def login(self, username, password):

        def standardLogin(username, password):
            payload = {
            'client_id': '7264cc83bea2e101bd11',
            'grant_type': 'password',
            'idfv': str(uuid.uuid1()),
            'password': password,
            'username': username}

            response = self.session.post(f'{self.baseUrl}/oauth2/access_token', json = payload)
            try:
                self.token = response.json()['access_token']
                self.session.headers.update({'authorization': f'Bearer {self.token}'})

                with open(f"{os.path.join(os.path.dirname(__file__))}/Config/Access-Token.json", "r") as jsonFile:
                    data = json.load(jsonFile)

                data["access_token"] = self.token

                with open(f"{os.path.join(os.path.dirname(__file__))}/Config/Access-Token.json", "w") as jsonFile:
                    json.dump(data, jsonFile, indent = 4)

                if self.log: print(f'{Fore.LIGHTGREEN_EX} + {Fore.RESET} Standard login successfull.')
                return response

            except:
                if self.log: print(f'{Fore.LIGHTRED_EX} - {Fore.RESET} Standard login unsuccessfull.')
                return response


        f = open(f'{os.path.join(os.path.dirname(__file__))}/Config/Access-Token.json')
        data = json.load(f)
        access_token = data['access_token']

        response = requests.get(f'https://api.depop.com/api/v1/seller-info', headers = {'authorization': f'Bearer {access_token}'})

        if response.status_code == 200:
            if response.json()['username'] == username:
                self.session.headers.update({'authorization': f'Bearer {access_token}'})
                if self.log: print(f'{Fore.LIGHTGREEN_EX} + {Fore.RESET} Smart login successfull.')
                return response
            else:
                response = standardLogin(username, password)
                return response
        else:
            response = standardLogin(username, password)
            return response


    def getUserInfo(self, id = None):

        if id == None:
            id = 'me'

        response = self.session.get(f'{self.baseUrl}/api/v1/users/{id}/')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def isSuperman(self):

        response = self.session.get(f'{self.baseUrl}/api/v1/users/me/')

        if response.json()['is_superman']:
            if self.log: print(f"WOW, you're {Fore.LIGHTBLUE_EX}Su{Fore.LIGHTRED_EX}p{Fore.LIGHTYELLOW_EX}er{Fore.LIGHTRED_EX}m{Fore.LIGHTBLUE_EX}an{Fore.RESET}! :D")
            return "WOW, you're Superman! :D"
        else:
            if self.log: print(f"{Fore.LIGHTRED_EX}Nope, not Superman :'({Fore.RESET}")
            return "Nope, not Superman :("


    def getUserCounters(self, id = None):

        if id == None:
            id = self.getMyID()

        response = self.session.get(f'{self.baseUrl}/api/v1/users/{id}/counters/')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def getSwitch(self):

        response = self.session.get(f'{self.baseUrl}/api/v1/feature/switch/')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def getExperiments(self):

        response = self.session.get(f'{self.baseUrl}/api/v1/feature/experiment/')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def getExchangeRate(self, currency):
        # E.G.   GBP
        response = self.session.get(f'{self.baseUrl}/api/v1/currency/rates/{currency.upper()}/')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def getShareTemplate(self):

        response = self.session.get(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/share-template/')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def getShippingStats(self, id = None):

        if id == None:
            id = self.getMyID()

        response = self.session.get(f'{self.baseUrl}/api/v1/seller/{id}/shipping-stats/')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def getExplorePage(self):

        response = self.session.get(f'{self.baseUrl}/api/v3/screens/discover/explore/')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def getMyDNA(self):

        response = self.session.get(f'{self.baseUrl}/api/v5/screens/discover/my-dna/')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def usernameChangeability(self):

        response = self.session.get(f'{self.baseUrl}/api/v1/users/me/usernames/changeability/')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def changeEmail(self, newEmail):

        payload = {'email': newEmail}

        response = self.session.patch(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/', json = payload)
        if self.log: print(f'{Fore.LIGHTYELLOW_EX}{response.json()}{Fore.RESET}')
        return response


    def changeUsername(self, newUsername):

        payload = {'username': newUsername}

        response = self.session.patch(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/', json = payload)
        if self.log: print(f'{Fore.LIGHTYELLOW_EX}{response.json()}{Fore.RESET}')
        return response


    def changePassword(self, newPassword):

        payload = {'password': newPassword}

        response = self.session.patch(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/', json = payload)
        if self.log: print(f'{Fore.LIGHTYELLOW_EX}{response.json()}{Fore.RESET}')
        return response


    def changeBio(self, newBio):

        payload = {'bio': newBio}

        response = self.session.patch(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/', json = payload)
        if self.log: print(f'{Fore.LIGHTYELLOW_EX}{response.json()}{Fore.RESET}')
        return response


    def changeWebsite(self, newWebsite):

        payload = {'website': newWebsite}

        response = self.session.patch(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/', json = payload)
        if self.log: print(f'{Fore.LIGHTYELLOW_EX}{response.json()}{Fore.RESET}')
        return response


    def changeFirstName(self, newFirstName):

        payload = {'first_name': newFirstName}

        response = self.session.patch(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/', json = payload)
        if self.log: print(f'{Fore.LIGHTYELLOW_EX}{response.json()}{Fore.RESET}')
        return response


    def changeLastName(self, newLastName):

        payload = {'last_name': newLastName}

        response = self.session.patch(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/', json = payload)
        if self.log: print(f'{Fore.LIGHTYELLOW_EX}{response.json()}{Fore.RESET}')
        return response


    def changeGender(self, gender):

        genderDict = {'male': 'm', 'female': 'f', 'other': 'o', 'remove': None}

        payload = {'gender': genderDict.get(gender)}

        response = self.session.patch(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/', json = payload)
        if self.log: print(f'{Fore.LIGHTYELLOW_EX}{response.json()}{Fore.RESET}')
        return response


    def changeLanguage(self, language):

        payload = {'language': language[0:3]} # Depop only allows up to 3 characters

        response = self.session.patch(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/', json = payload)
        if self.log: print(f'{Fore.LIGHTYELLOW_EX}{response.json()}{Fore.RESET}')
        return response


    def sendReport(self, message, fromUser):

        payload = {
            "user": {
                "email": str(self.getUserInfo().json()['email']),
                "sdk_guid": str(uuid.uuid1())
                }
            }

        response = requests.post(f'https://depophelp.zendesk.com/access/sdk/anonymous', json = payload, headers = {'client-identifier': 'mobile_sdk_client_d13068684130040e1a9d'})
        if self.log: print(f'{Fore.LIGHTBLUE_EX}{response.json()}{Fore.RESET}')
        self.access_tokenV2 = response.json()['authentication']['access_token']

        payload = {
            "request": {
                "comment": {
                    "body": f"{message}\n\n\n==============================\nInformation for Depop Support\n\nSender os version: Depopped\nSender system: Depopped\nSender app version: 1.0.0\nSender device: Depopped",
                    "uploads": []
                },
                "custom_fields": [
                    {
                        "id": int(''.join(random.choice(string.digits) for i in range(8))),
                        "value": "bug_report"
                    }
                ],
                "metadata": {
                    "sdk": {
                        "device_battery": 69,
                        "device_model": "Depopped",
                        "device_os": "12.3.4",
                        "device_storage": 69,
                        "device_total_memory": 6969
                    }
                },
                "subject": f"Something went wrong from user @{fromUser}",
                "tags": [
                    "bug_report"
                ]
            }
        }

        response = requests.post(f'https://depophelp.zendesk.com/api/mobile/requests.json?include=last_comment', json = payload, headers = {'user-agent': 'Zendesk-SDK/5.0.0 iOS/12.5.5 Variant/Support', 'authorization': f'Bearer {self.access_tokenV2}'})
        if self.log: print(f'ff{Fore.LIGHTBLUE_EX}{response.json()}{Fore.RESET}')

        return response


    def createListing(self, pictureID, price = '6969', quantity = 1, description = 'Listed with Depopped.py - https://github.com/akimbo7/depopped', currency = 'GBP'):
        payload = {
            "address": "Albania",
            "age": [],
            "brand_id": None,
            "categories": [
                177
            ],
            "colour": [],
            "condition": None,
            "description": str(description),
            "hand_delivery": False,
            "international_shipping_cost": "0",
            "national_shipping_cost": "0",
            "pictures": [f"/api/v1/pictures/{pictureID}/"],
            "place_data": {
                "address_components": [
                    {
                        "long_name": "Albania",
                        "short_name": "AL",
                        "types": [
                            "country",
                            "political"
                        ]
                    }
                ],
                "formatted_address": "Albania",
                "geometry": {
                    "location": {
                        "lat": 41.3281168,
                        "lng": 19.8162348
                    }
                }
            },
            "price_amount": str(price),
            "price_currency": str(currency),
            "purchase_via_paypal": True,
            "quantity": int(quantity),
            "share_on_tw": False,
            "shippable": True,
            "shipping_methods": None,
            "source": [],
            "style": [],
            "video_ids": None}

        response = self.session.post(f'{self.baseUrl}/api/v1/products/', json = payload)
        if self.log: print(f'{Fore.LIGHTBLUE_EX}{response.json()}{Fore.RESET}')
        return response


    def paypalConnection(self):

        response = self.session.get('https://prod-prod-paypalfees-api.depop.com/v1/users')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def removePaypal(self):

        response = self.session.delete('https://prod-prod-paypalfees-api.depop.com/v1/users')
        if self.log: print(f'{Fore.LIGHTRED_EX}{response.json()}{Fore.RESET}')
        return response


    def getMyID(self):

        response = self.session.get(f'{self.baseUrl}/api/v1/seller-info')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response.json()['id']


    def getBannedWords(self):

        response = self.session.get(f'{self.baseUrl}/api/v1/banned-hashtags/')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response.json()['banned']


    def follow(self, id):

        response = self.session.put(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/following/?user_id={id}')
        if self.log: print(f'{Fore.LIGHTCYAN_EX}{response.json()}{Fore.RESET}')
        return response


    def unfollow(self, id):

        response = self.session.delete(f'{self.baseUrl}/api/v1/users/{getMyID()}/following/{id}/')
        if self.log: print(f'{Fore.LIGHTRED_EX}{response.json()}{Fore.RESET}')
        return response


    def reportListing(self, message, listingID):

        payload = {
            "message": str(message),
            "sender_app_version": "6.96.9",
            "sender_device": "akimbo7",
            "sender_name": "akimbo7",
            "sender_os_version": "6.96.9",
            "sender_system": "akimboOS",
            "sender_username": "akimbo",
            "target_product": int(listingID),
            "user": int(self.getMyID())}

        response = self.session.post(f'{self.baseUrl}/api/v1/reports/product_report/', json = payload)
        if self.log: print(f'{Fore.LIGHTBLUE_EX}{response.json()}{Fore.RESET}')
        return response


    def likeListing(self, listingID):

        response = self.session.put(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/likes/?product_id={listingID}', json = {})
        if self.log: print(f'{Fore.LIGHTCYAN_EX}{response.json()}{Fore.RESET}')
        return response


    def removeLikeListing(self, listingID):

        response = self.session.delete(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/likes/{listingID}/')
        if self.log: print(f'{Fore.LIGHTRED_EX}{response.json()}{Fore.RESET}')
        return response


    def saveListing(self, listingID):

        response = self.session.put(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/saved-products/?product_id={listingID}')
        if self.log: print(f'{Fore.LIGHTCYAN_EX}{response.json()}{Fore.RESET}')
        return response


    def removeSavedListing(self, listingID):

        response = self.session.delete(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/saved-products/{listingID}/')
        if self.log: print(f'{Fore.LIGHTRED_EX}{response.json()}{Fore.RESET}')
        return response


    def commentOnListing(self, listingID, message):

        payload = {"text": message}

        response = self.session.post(f'{self.baseUrl}/api/v1/products/{listingID}/comments/', json = payload)
        if self.log: print(f'{Fore.LIGHTBLUE_EX}{response.json()}{Fore.RESET}')
        return response


    def removeListingComment(self, listingID):
        pass


    def getFeed(self):

        response = self.session.get(f'{self.baseUrl}/api/v1/users/{self.getMyID()}/feed/?limit=200&offset_id=')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def getNotifications(self):

        response = self.session.get(f'{self.baseUrl}/api/v2/notifications/me/?user_id={self.getMyID()}')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def getBrowseScreen(self):

        response = self.session.get(f'{self.baseUrl}/api/v2/screens/browse/')
        if self.log: print(f'{Fore.LIGHTGREEN_EX}{response.json()}{Fore.RESET}')
        return response


    def sendMessage(self, targetID, message):

        # won't be releasing as i'm creating a private mass dm tool which makes my depop sales go through the roof, would be stupid to give away free sauce.
        print(f'{Fore.LIGHTRED_EX} --- {Fore.RESET}sendMessage(){Fore.LIGHTRED_EX} will not be releasing until further notice --- {Fore.RESET}')
