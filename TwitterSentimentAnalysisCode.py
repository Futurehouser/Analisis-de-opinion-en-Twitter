# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 18:19:26 2018

@author: Equipo
"""


import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt

class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):
        # authenticating
        consumerKey = 'Aquí va el consumerKey'
        consumerSecret = 'Aquí va el consumerSecret'
        accessToken = 'Aquí va el accessToken'
        accessTokenSecret = 'Aquí va el accessTokenSecret'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        searchTerm = input("Introduzca la palabra clave a buscar: ")
        NoOfTerms = int(input("Introduzca cuántos tweets analizar: "))
        print()

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polaridad = 0
        positivo = 0
        dpositivo = 0
        fpositivo = 0
        negativo = 0
        dnegativo = 0
        fnegativo = 0
        neutral = 0

        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        
        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            print(analysis.sentiment)  # print tweet's polarity
            print()
            polaridad += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                dpositivo += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positivo += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                fpositivo += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                dnegativo += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negativo += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                fnegativo += 1


        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positivo = self.percentage(positivo, NoOfTerms)
        dpositivo = self.percentage(dpositivo, NoOfTerms)
        fpositivo = self.percentage(fpositivo, NoOfTerms)
        negativo = self.percentage(negativo, NoOfTerms)
        dnegativo = self.percentage(dnegativo, NoOfTerms)
        fnegativo = self.percentage(fnegativo, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polaridad = polaridad / NoOfTerms

        # printing out data
        print("Como reacciona la gente ante la palabra " + searchTerm + " al analizar " + str(NoOfTerms) + " tweets.")
        print()
        print("Informe general: ")

        if (polaridad == 0):
            print("Neutral")
        elif (polaridad > 0 and polaridad <= 0.3):
            print("Débilmente Positivo")
        elif (polaridad > 0.3 and polaridad <= 0.6):
            print("Positivo")
        elif (polaridad > 0.6 and polaridad <= 1):
            print("Fuertemente Positivo")
        elif (polaridad > -0.3 and polaridad <= 0):
            print("Débilmente Negativo")
        elif (polaridad > -0.6 and polaridad <= -0.3):
            print("Negativo")
        elif (polaridad > -1 and polaridad <= -0.6):
            print("Fuertemente Negativo")

        print()
        print("Informe detallado: ")
        print(str(fpositivo) + "% de la gente pensó que era fuertemente positivo")
        print(str(positivo) + "% de la gente pensó que era positivo")
        print(str(dpositivo) + "% de la gente pensó que era débilmente positivo")
        print(str(neutral) + "% de la gente pensó que era neutral")
        print(str(dnegativo) + "% de la gente pensó que era débilmente negativo")
        print(str(negativo) + "% de la gente pensó que era negativo")
        print(str(fnegativo) + "% de la gente pensó que era fuertemente negativo")


        self.plotPieChart(positivo, dpositivo, fpositivo, negativo, dnegativo, fnegativo, neutral, searchTerm, NoOfTerms)


    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positivo, dpositivo, fpositivo, negativo, dnegativo, fnegativo, neutral, searchTerm, noOfSearchTerms):
        labels = ['Fuertemente Positivo [' + str(fpositivo) + '%]', 'Positivo [' + str(positivo) + '%]','Débilmente Positivo [' + str(dpositivo) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Débilmente Negativo [' + str(dnegativo) + '%]', 'Negativo [' + str(negativo) + '%]', 'Fuertemente Negativo [' + str(fnegativo) + '%]']
        sizes = [fpositivo, positivo, dpositivo, neutral, dnegativo, negativo, fnegativo]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('Cómo reacciona la gente ante la palabra ' + searchTerm + ' al analizar ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()



if __name__== "__main__":
    sa = SentimentAnalysis()
sa.DownloadData()