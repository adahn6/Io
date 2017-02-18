#!/usr/bin/env python3

import json
import argparse
from termcolor import colored
from watson_developer_cloud import ToneAnalyzerV3

# Authors: Alex French, Samuel Gass, Margaret Yim

TOPIC_LIMIT = 5
IO_COLOR = 'green'
YOU_COLOR = 'white'
GLADOS_COLOR = 'red'


def i_say(string, with_newline=True):
    if with_newline:
        print(colored(" >  " + string + '\n', IO_COLOR))
    else:
        print(colored(" >  " + string, IO_COLOR))


def u_say(string, with_newline=True):
    if with_newline:
        print(colored(" >  " + string + '\n', YOU_COLOR))
    else:
        print(colored(" >  " + string, YOU_COLOR))


def glados_says(string, with_newline=True):
    if with_newline:
        print(colored((" >  GLADoS:// " + string + '\n'), GLADOS_COLOR))
    else:
        print(colored((" >  GLADoS:// " + string), GLADOS_COLOR))

def talkAboutTopic(tone_analyzer, filename="", debug=False):
    emotions = dict(anger=0, disgust=0, fear=0, joy=0, sadness=0)

    if debug:
        with open(filename) as resp_file:
            resp_obj = json.load(resp_file)
        topic = resp_obj["topic"]
        i_say("What would you like to talk about?")
        u_say(str(topic) + "")
    else:
        topic = input(colored(" >  What would you like to talk about?\n", IO_COLOR))

    for i in range(TOPIC_LIMIT):
        if debug:
            i_say("Tell me more about this.")
            resp = resp_obj["responses"][i]
            u_say(str(resp) + "")
        else:
            resp = input(colored(" >  Tell me more about this.\n", IO_COLOR))
        analysis = tone_analyzer.tone(text=resp)
        for category in analysis["document_tone"]["tone_categories"]:
            if category["category_id"] == "emotion_tone":
                for tone in category["tones"]:
                    if tone["tone_id"] == "anger":
                        emotions['anger'] = (emotions['anger']*i + tone["score"])/(i+1)
                    if tone["tone_id"] == "disgust":
                        emotions['disgust'] = (emotions['disgust']*i + tone["score"])/(i+1)
                    if tone["tone_id"] == "fear":
                        emotions['fear'] = (emotions['fear']*i + tone["score"])/(i+1)
                    if tone["tone_id"] == "joy":
                        emotions['joy'] = (emotions['joy']*i + tone["score"])/(i+1)
                    if tone["tone_id"] == "sadness":
                        emotions['sadness'] = (emotions['sadness']*i + tone["score"])/(i+1)

    max_key = max(emotions, key=emotions.get)
    if debug:
        print(emotions)
    if emotions[max_key] < 0.5:
        glados_says('TEST INCONCLUSIVE. RESUME TESTING.', with_newline=False)
        i_say("I'm not sure how you feel about this. Let's try another topic.", with_newline=False)
    else:
        if max_key == "anger":
            glados_says("WARNING ANGER LEVEL %f OF 10. DISPENSE PUPPIES." % (10.0*emotions[max_key]), with_newline=False)
            i_say("You seem angry about this. I'm sorry. Let's talk about something else.", with_newline=False)
        if max_key == "disgust":
            glados_says("WARNING DISGUST LEVEL %f OF 10. DISPENSE DIVERSION." % (10.0*emotions[max_key]), with_newline=False)
            i_say("You seem disgusted by this. I'm sorry. Let's talk about something else.", with_newline=False)
        if max_key == "fear":
            glados_says("WARNING FEAR LEVEL %f OF 10. DISPENSE REASSURANCE." % (10.0*emotions[max_key]), with_newline=False)
            i_say("You seem scared by this. Everything will be okay. Let's talk about something else.", with_newline=False)
        if max_key == "joy":
            glados_says("WARNING JOY LEVEL %f OF 10. DISPENSE EXCITEMENT." % (10.0*emotions[max_key]), with_newline=False)
            i_say("You seem happy about this! I'm glad for you. Let's talk about something else.", with_newline=False)
        if max_key == "sadness":
            glados_says("WARNING SADNESS LEVEL %f OF 10. DISPENSE CONDOLENCES." % (10.0*emotions[max_key]), with_newline=False)
            i_say("You seem sad about this. I'm sorry. Let's talk about something else.", with_newline=False)


def main():
    with open('creds.json') as cred_file:
        cred_obj = json.load(cred_file)

    tone_analyzer = ToneAnalyzerV3(
        username=cred_obj["username"],
        password=cred_obj["password"],
        version='2016-05-19')

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Read input from debug file instead of user input", type=str)
    args = parser.parse_args()

    if args.debug:
        talkAboutTopic(tone_analyzer, args.debug, True)
    else:
        # import pdb; pdb.set_trace()
        user_name = input(colored(" >  Hello, my name is Io. What is your name?\n", IO_COLOR))
        i_say(string=("Hello, " + str(user_name.strip())), with_newline=False)
        while True:
            talkAboutTopic(tone_analyzer)

if __name__ == "__main__":
    main()
