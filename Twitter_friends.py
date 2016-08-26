import time
import tweepy
import random


class getDirectConnection:
    def __init__(self, user, authkeylist):
        self.username = user
        self.authlist = authkeylist
        self.NodeList = []
        self.LinkList = []
        self.i = 0
        self.Key = None
        self.api = None
        self.user = None

    def setup_api(self, first=False, rest_interval=10):
        """
        finds an available set of OAUTH keys from authlist.json. authlist passed to
        getdDirectConnection class must be JSON form.
        :param first: is it the initial api setup
        :param rest_interval: how long to wait to try a new key (15 min if only one key).
        :return: None
        """
        if first:
            for _ in self.authlist:
                self.authlist[_] = {'keys': self.authlist[_], 'timeIn': 0}
        else:
            # when current api runs out of requests reset its availability tracked time
            self.authlist[self.Key]['timeIn'] = time.time()

        # do while:
        # find all keys that have been sitting for longer than 15 minutes
        available = [key for key in self.authlist if (self.authlist[key]['timeIn'] + 960) - time.time() <= 0]
        print 'looking for available api key auth code'
        while not available:
            time.sleep(rest_interval)
            available = [key for key in self.authlist if (self.authlist[key]['timeIn'] + 960) - time.time() <= 0]

        print 'found api key auth'
        self.Key = random.choice(available)
        oauth_key = self.authlist[self.Key]['keys']

        auth = tweepy.OAuthHandler(oauth_key['consumerKey'], oauth_key['consumerSecret'])
        auth.set_access_token(oauth_key['accessToken'], oauth_key['accessSecret'])
        self.api = tweepy.API(auth)

    def get_friends(self, username, first=False):
        """
        gets the friends of a user and adds their info to storage.
        :param username: individuals name
        :param first: is this the initial friend group request
        :return: if a successful query
        """
        time.sleep(0.5)

        # get friends of user
        try:
            friends = self.api.friends_ids(username)
        except tweepy.RateLimitError:
            self.setup_api()
            return False
        except tweepy.TweepError as e:
            print e
            return True

        count = 0
        # add users and links
        for screenName in friends:
            if first:
                if screenName not in [node['id'] for node in self.NodeList]:
                    self.NodeList.append({'id': screenName, 'group': 1, 'Size': 5})
                if (username,screenName) not in [(pair['source'], pair['target']) for pair in self.LinkList]:
                    self.LinkList.append({"source":username, "target": screenName, "value": 5, "co": 'DarkCyan'})
            else:
                if screenName in [node['id'] for node in self.NodeList]:
                    self.LinkList.append({"source": username, "target": screenName, "value": 5, "co": 'DarkCyan'})
            count += 1
            if count == 175: #dont take any more than a page of data
                break
        return True


    def makeNetwork(self):
        """
        class execution function. sets up initial api, and user 1st level network.
        gets all friends and friends of friends that are in 1st level network.
        :return: tuple object with nodes and links
        """
        self.setup_api(first=True)
        self.user = self.api.get_user(self.username).id
        self.NodeList.append({'id': self.user, 'group': 1, 'Size': 10})
        self.get_friends(self.user, first=True)
        for Name in [node['id'] for node in self.NodeList]:
            while 1:
                if self.get_friends(Name):
                    break
            self.i += 1

        data = {'nodes': self.NodeList, 'links': self.LinkList}

        # find the number of links that are targeted to user and scale node size by this value
        for obj in [n['id'] for n in data['nodes']]:
            count = [x['target'] for x in data['links']].count(obj)
            for node in data['nodes']:
                if node['id'] == obj:
                    node['Size'] += (count / 2)

        # find whether a link is reciprocal
        for link in data['links']:
            source = link['source']
            target = link['target']
            if (source, target) in [(l['target'], l['source']) for l in data['links']]:
                link['co'] = 'LightCoral'

        return data['nodes'], data['links']
