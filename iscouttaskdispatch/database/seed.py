from .db import Status, Task, Team, db


def seed_database():
    Status.create_new(1, "Created")
    Status.create_new(2, "Work in Progress")
    Status.create_new(3, "Done")
    Status.create_new(4, "Failed")


def seed_demo_data():
    team1 = Team.create_new("Team 1")
    team2 = Team.create_new("Team 2")

    """
    Tasks are took from the 2024 iScout edition. [https://files.iscoutgame.com/game-2024/site/tasks-en.pdf]
    """
    Task.create_new(id=1, name="Team photo",
                    description="Your very first task. Take a group photo of your team. As many of your team members as possible should be visible in the photo. Your team flag must also be clearly visible.",
                    format="Hand in a photo.").assign_to_team(team1)
    Task.create_new(id=2, name="Stuffed",
                    description="You are at the supermarket, have paid for everything, and... forgotten your bag. But as a true scout you of course have pants with those pockets on the side. And a sweater with pouch and hood. And a jacket with pockets. You know where this is going: put a full shopping basket of snacks in/on/between your clothes. As much as you can until it no longer fits. You don't really have to go to the supermarket, but you can.",
                    format="Hand in a photo.").assign_to_team(team1)
    Task.create_new(id=3, name="Sit down please",
                    description="Have a seat. But do it like this: https://www.instagram.com/reel/CzL9DGVrG_b.",
                    format="Hand in a short video.",
                    link="https://www.instagram.com/reel/CzL9DGVrG_b")
    Task.create_new(id=4, name="Best Friends Forever",
                    description="At scouting, you make friends for life. This must of course be documented appropriately. Take a friend photo like this: https://www.instagram.com/reel/C1kHMBmt_7B. We want to see the heads of at least 12 people in the photo (less if fine if your team is small).",
                    format="Hand in a photo.",
                    link="https://www.instagram.com/reel/C1kHMBmt_7B")
    Task.create_new(id=5, name="Toilet paper challenge",
                    description="Catch toilet paper! Drop the toilet roll behind your head and catch it again from between your legs. And make a video of this. See this example: https://www.instagram.com/reel/C2xMPUgPbBI",
                    format="Hand in a short video.",
                    link="https://www.instagram.com/reel/C2xMPUgPbBI")
    Task.create_new(id=6, name="Bring the story to life",
                    description="Find a piece of existing literature (i.e. a novel, chick lit, children's book, etc. But not a newspaper or magazine or fan fiction) in which the character does/says/experiences something related to a place. Go to that place and read the passage out loud. The place should be quite specific, for example the Church street, but not the city of Berlin. Submit a video of the reading and a photo of the text from the (paper or digital) book.",
                    format="Hand in a short video.")
    Task.create_new(id=7, name="Silly Sandwich",
                    description="Prepare a sandwich with 5 ingredients that start with the same letter. The toppings must be realistic sandwich toppings, so for example no candy. You can choose the language yourself, but be consistent. To make it easy for us you have to make a list of all the ingredients and put it next to the sandwich.",
                    format="Hand in a photo.")
    Task.create_new(id=8, name="Blowing bubbles",
                    description="Find a fan and make a bubble machine like this: https://www.instagram.com/tv/CYKVw79r1OD. In your video we see the machine working and the bubbles floating in the air.",
                    format="Hand in a short video.",
                    link="https://www.instagram.com/tv/CYKVw79r1OD")
    Task.create_new(id=9, name="Furniture Tetris",
                    description="Start by collecting everything you can find in an average living room: dining table, 4 chairs, sofa, coffee table, floor lamp, TV with cabinet, hocker and the cat scratching post. Then you start tetrising with that. In other words, stack everything against the wall as efficiently as possible. For inspiration: https://s3-newsifier.ams3.digitaloceanspaces.com/vkmag.newsifier.com/images/2024-02/pix-dump1877-010-65dd063a94ed5.jpeg",
                    format="Hand in a photo.",
                    link="https://s3-newsifier.ams3.digitaloceanspaces.com/vkmag.newsifier.com/images/2024-02/pix-dump1877-010-65dd063a94ed5.jpeg")
    Task.create_new(id=10, name="I am a scout",
                    description="We are scouts, and that of course comes with a number of customs, habits and skills. We are curious about what really makes you typical scouts. Make a video of about 30 seconds like this example: https://www.instagram.com/reel/C2feEyVt15Z. We're looking for at least five examples of what makes your typical scouts, and of course we also want to see them depicted.",
                    format="Hand in a short video.",
                    link="https://www.instagram.com/reel/C2feEyVt15Z")
    Task.create_new(id=11, name="Pass it on",
                    description="Find three people, give them all a party blowout, and let them stand or sit in a row. The first person picks up something long and skinny with the blowout (pencil, pen, breadstick, etc) and passes it to the second person. The second person passes it to the third.",
                    format="Hand in a short video.")
    Task.create_new(id=12, name="Stack the cups",
                    description="Supplies: 4 people, 4 pieces of paper, 4 strings and 5 cups. The task is then to do this: https://www.instagram.com/reel/CxGcLOZJHEF. From experience we know that this goes wrong the first twenty times. We like to see a video that includes footage from where it goes right (and possibly the subsequent cheering).",
                    format="Hand in a short video.",
                    link="https://www.instagram.com/reel/CxGcLOZJHEF")
    Task.create_new(id=13, name="Bus stop",
                    description="This is the 15th edition of iScout and we are going to celebrate in a bus shelter! Decorate the bus shelter for a good party. Think balloons (at least one with '15' on it), garlands, snacks, and (if possible) your old iScout team flags on the wall.",
                    format="Hand in a photo.")
    Task.create_new(id=14, name="Surfing",
                    description="You know those beautiful pictures of a surfer surfing through a breaking wave, as if it were a tunnel of water. You are going to recreate those, but on dry land. Take a blue (or other color) tarp, a skateboard and get to work: https://www.instagram.com/p/C25Cq_1xCEs/.",
                    format="Hand in a photo collage.",
                    link="https://www.instagram.com/p/C25Cq_1xCEs/")
    Task.create_new(id=15, name="Floating",
                    description="Bla bla, negative charge, bla bla, physics, bla bla, static electricity, bla bla. But in the end, a plastic ring floats above a balloon. And that's what we want to see. Fortunately, Science Bob can explain it a lot better: https://www.instagram.com/p/CKsEIfOApxo/.",
                    format="Hand in a photo collage.",
                    link="https://www.instagram.com/p/CKsEIfOApxo/")
    Task.create_new(id=16, name="Crossword",
                    description="Complete 'The Mini Crossword' puzzle from today's New York Times or the Guardian, and submit a photo of the completed version. We want to see the real newspaper! Not the online version.",
                    format="Hand in a photo.")
    Task.create_new(id=17, name="Sawing contest",
                    description="You are going to have a sawing contest. Take two tree trunks (or beams from the hardware store, or discarded pioneer poles, remnants of a pallet or whatever) a little over 2 meters. Put two tables about 2 meters apart and run the beams from one table to the other. A scout sits on each beam, holding a saw. The referee counts down, and then it is up to the scouts to saw through the beam the other is sitting on as quickly as possible. Whoever saws through the other person's beam first wins.",
                    format="Hand in a short video.")
    Task.create_new(id=18, name="Aluminium",
                    description="What do you need to get a piece of aluminum foil in half? Indeed, some 9-volt batteries and a pencil led (filling of a mechanical pencil).",
                    format="Hand in a photo collage.")
    Task.create_new(id=19, name="Mirror run challenge",
                    description="The mirror run challenge, we all have seen it on insta-snap-tik-x-tok: https://www.youtube.com/watch?v=8FlhOQJ6Yas. You are going to make your version, but of course in scouting theme. We will see you run past the mirror at least 10 times, one of which with a team flag.",
                    format="Hand in a short video.",
                    link="https://www.youtube.com/watch?v=8FlhOQJ6Yas")
    Task.create_new(id=20, name="Snow",
                    description="Place at least 6 separate screens (TVs or monitors) together. Stack these and place them against each other. Make sure they fit properly. Show noise/snow on all screens. You can now use tape and paper to cover parts of the screen, until you only see ISCOUT in noise over the screens.",
                    format="Hand in a photo.")
    Task.create_new(id=21, name="Light reading",
                    description="You can create beautiful things with a long exposure photos. Take a look: https://www.thephoblographer.com/2016/06/29/2wenty-shares-words-insight-via-long-exposure-photography/",
                    format="Hand in a photo.",
                    link="https://www.thephoblographer.com/2016/06/29/2wenty-shares-words-insight-via-long-exposure-photography/")
    Task.create_new(id=22, name="Pneumatic tube",
                    description="Some bank offices and hospitals use a pneumatic tube system. With this system air pressure is used to transport objects from A to B. Very convenient! In this assignment you are going to make such a system yourself with a drainpipe and some vacuum cleaners.",
                    format="Hand in a short video.")
    Task.create_new(id=23, name="A brand new floor",
                    description="Every now and then it's time for some house renovations. For example, by laying a new floor! How about a retro black and white checkered? Cover the floor of a room entirely with chess and/or checkers boards.",
                    format="Hand in a photo.")
    Task.create_new(id=24, name="Mooncrasher",
                    description="The Japanese space agency has created a lunar lander that landed very precisely. Super impressive! Unfortunately it fell over at the last minute and a photo was taken of it. We also want to see something like that from you. So a homemade space vehicle that has clearly crashed, on a lunar landscape and with the Earth in the background.",
                    format="Hand in a photo.")
    Task.create_new(id=25, name="Greetings from the hot air balloon",
                    description="This year's iScout logo is a hot air balloon, because you can travel around the world with it! We want to see your (self-made) hot air balloon. So a basket, (the bottom part of) a large balloon above the basket, and at least 3 people in the basket looking at the view.",
                    format="Hand in a photo.")
    Task.create_new(id=26, name="Reverse basketball",
                    description="You are going to play reverse basketball. In this, the ball is fixed on the post, and you throw the basketball ring (with or without a board) over the ball. See this video: https://www.instagram.com/reel/CxwTYErvMQZ.",
                    format="Hand in a short video.",
                    link="https://www.instagram.com/reel/CxwTYErvMQZ")
    Task.create_new(id=27, name="Real or cake?",
                    description="iScout celebrates its 15th anniversary, so time for cake! Professionals can make edible cakes that look exactly like everyday objects. It's a hefty task, but we'd like to see you try!",
                    format="Hand in a photo collage.")
    Task.create_new(id=28, name="Mini hot air balloon (out of the window)",
                    description="Make a mini hot air balloon. There are numerous tutorials on the Internet, for example this: https://www.wikihow.com/Make-a-Mini-Flyable-Hot-Air-Balloon-with-Candles.",
                    format="Hand in a short video.",
                    link="https://www.wikihow.com/Make-a-Mini-Flyable-Hot-Air-Balloon-with-Candles")
    Task.create_new(id=29, name="Campfire",
                    description="In more and more places in the Netherlands it is (temporarily) prohibited to light a campfire. Very unfortunate for the real scouts. That's why we have to look for an alternative. Make a fake campfire from wood and paper and place a fan underneath so that the fire flutters.",
                    format="Hand in a photo collage.")
    Task.create_new(id=30, name="Singing backwards",
                    description="If you sing a song, you can play it backwards and you won't really recognize the song. You can also do that the other way around. So singing the song backwards, and then play it backwards to have it sound as normal again.",
                    format="Hand in a short video.")
