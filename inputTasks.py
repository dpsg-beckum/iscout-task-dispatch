tasks = [{'id': 1, 'name': 'Group photo', 'desc': 'The very first Task. Take a group picture of your team. In the picture has to be as many team members as possible.\nBesides that, you have to show your group flag.\nYou have to hand in a photo.'}, {'id': 2, 'name': 'The Umbrella Trick', 'desc': "This is how to impress when it rains:\nhttps://weather.com/news/trending/video/coolest-umbrella-trick-how-does-he-do-it\nRain or no rain, impress the Travel Agents with this trick. The technique is not simple, so start with learning from\nothers. For example, watch Youtuber Mike Boyd learning the Umbrella Trick.\nWe want to see you walking naturally, throw up the umbrella and catch it again with the same hand. So don't catch it\nwith both hands and don't run.\nYou have to hand in a short video."}, {'id': 3, 'name': 'Four legs', 'desc': "Humans are one of the few mammals that walk on two legs. That can't be good. So you are going to walk on four\nlegs. Like this: https://www.instagram.com/reel/CjVaZ8uD0vH/?igshid=YmMyMTA2M2Y\nWe would like to see a video of max 15 seconds in which you take at least six steps in this manner.\nYou have to hand in a short video."}, {'id': 4, 'name': 'Balloon Dance', 'desc': "You'll need: 1 balloon, 2 persons, and in the background an Adele song. \nReplicate this balloon dance: https://www.instagram.com/reel/CjihjB9Ju5Y You might need to practice first.\nYou have to hand in a short video."}, {'id': 5, 'name': 'Musical entrance', 'desc': 'Some live music, everytime you walk in. That what you want!\nFor example like this in a music store: https://www.instagram.com/reel/CgLdjE9IleH\nPlace your instrument on a wall or ceiling and make sure it can be played with a door. In your clip, we see two\npeople entering separatly and hear the instrument four times. You may use instruments with strings, keys or wind\ninstruments\nYou have to hand in a short video.'},
         {'id': 6, 'name': 'Under water', 'desc': "During iScout you'll travel around the world. From the highest mountains to the deepest oceans. Take a picture of\nsomeone in scouting uniform stading on the bottom of the pool. This person is fully under water and salutes. The\npicture was taken straight from the front. So the photographer should be in the pool as well.\nYou have to hand in a photo."}, {'id': 7, 'name': 'Statues coming to life', 'desc': "Statues tell stories from the past. Find a statue and become part of a story with it. See for inspiration: \nhttps://www.instagram.com/p/ClgiZTXoEv2/\nHand in a picture in which 2 persons are part of a story with the statue. Make sure the picture clearly tells this story,\njust standing next to it won't be enough.\nYou have to hand in a photo."}, {'id': 8, 'name': 'Modern Art', 'desc': "Look for a painting with an old fashioned idyllic painting (in a thrift store, at your grandma's place or online). Add your\nown modern twist to this painting. Do this by adding modern elements that fit into the landscape. You can add for\nexample a modern verhicles, a restaurant, traffic lights etc. For inspiration: https://www.wesleyaltena.com/paintings/\nHand in a picture of your result.\nYou have to hand in a photo."}, {'id': 9, 'name': 'Vacuum', 'desc': "Redesign your (robot) vacuum cleaner to look like a pirate ship, or a space ship, or a super speedy race car. Don't\nplace a cat on it, but a soft toy / stuffed animal instead. Be creative and hand in a foto of your results.\nYou have to hand in ."}]


while True:
    try:
        id = int(input("ID: "))
        name = input("Name: ")
        print("Desc STRG-D: ")
        desc = ""
        while True:
            try:
                line = input()
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            desc += line + "\n"
        tasks.append({"id": id,
                      "name": name.strip(),
                      "desc": desc.strip()})
        print()
    except Exception:
        print(tasks)
        break
    except KeyboardInterrupt:
        print(tasks)
        break

print(tasks)
