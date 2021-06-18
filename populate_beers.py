from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///beer_catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user

user = User(username="dlaurence269")
session.add(user)
session.commit()

# Items for IPA

category1 = Category(name="IPA")

session.add(category1)
session.commit()

Item1 = Item(user=user, name="Frigid IPA",
                    description="Intense hoppy flavor, only for the cold and bitter at heart or taste. Best served chilled.",
                    picture_path="../static/images/med_ipa.jpg",
                    price="$5.00", ibu="90", abv="7", category=category1)

session.add(Item1)
session.commit()


Item2 = Item(user=user, name="IPA lot when I drink Beer",
                    description="Very hoppy and flavorfull aromatics, with medium hoppy flavor. Mid-range alcohol level, easily approachable IPA.",
                    picture_path="../static/images/ipa.jpg",
                    price="$2.00", ibu="40", abv="5", category=category1)

session.add(Item2)
session.commit()

Item3 = Item(user=user, name="IPA IPA IPA",
                    description="Classic IPA. If you're trying for the first time, this is the most typical IPA around.",
                    picture_path="../static/images/another_ipa.png",
                    price="$3.00", ibu="50", abv="6", category=category1)

session.add(Item3)
session.commit()

Item4 = Item(user=user, name="Yippie Aye Yay IPA!",
                    description="If you want an IPA to get pumped about, this is it. Enjoy The best IPA around!",
                    picture_path="../static/images/light_foam.jpeg",
                    price="$3.00", ibu="60", abv="6", category=category1)

session.add(Item4)
session.commit()

Item5 = Item(user=user, name="Boring IPA, NOT Today",
                    description="This complex mix of smokey, hoppy, curtness will blow you away. No better beer here.",
                    picture_path="../static/images/tall_foam.jpg",
                    price="$2.50", ibu="50", abv="5", category=category1)

session.add(Item5)
session.commit()

# Items for Lager

category2 = Category(name="Lager")

session.add(category2)
session.commit()

Item1 = Item(user=user, name="YingYing Lager",
                    description="America's not oldest brewery makes the yes freshest lager around.",
                    picture_path="../static/images/lager.jpg",
                    price="$1.00", ibu="12", abv="4.4", category=category2)

session.add(Item1)
session.commit()


Item2 = Item(user=user, name="Bragger Lager",
                    description="With a lager this good, you'd be bragging as well.",
                    picture_path="../static/images/md_lager.jpg",
                    price="$1.50", ibu="15", abv="5", category=category2)

session.add(Item2)
session.commit()

Item3 = Item(user=user, name="Logger Lager",
                    description="For those hardworking, woods loving, thirsty folk. There's nothing better.",
                    picture_path="../static/images/tall_wheat.jpeg",
                    price="$1.00", ibu="12", abv="4.5", category=category2)

session.add(Item3)
session.commit()

Item4 = Item(user=user, name="Lady Lager",
                    description="The most elegant lager in town, now at its most affordable.",
                    picture_path="../static/images/med_lager.jpeg",
                    price="$1.00", ibu="10", abv="4", category=category2)

session.add(Item4)
session.commit()

Item5 = Item(user=user, name="Basic Beer Here",
                    description="No suprise Lager. Cheap and easy to drink, like a lager should be.",
                    picture_path="../static/images/classic_lager.jpg",
                    price="$1.00", ibu="11", abv="5", category=category2)

session.add(Item5)
session.commit()

Item6 = Item(user=user, name="Trusty Lager",
                    description="This is an incredibly flavorfull and complex beer for a lager. Impress your friends with the flavor you can rely on.",
                    picture_path="../static/images/another_lager.jpeg",
                    price="$2.50", ibu="15", abv="6", category=category2)

session.add(Item6)
session.commit()

Item7 = Item(user=user, name="Nice Slice Lager",
                    description="Look no further. This lager is enjoyable and well worth the cost.",
                    picture_path="../static/images/dark_lager.jpg",
                    price="$1.50", ibu="10", abv="5", category=category2)

session.add(Item7)
session.commit()

# Items for Pale Ale
category3 = Category(name="Pale Ale")

session.add(category3)
session.commit()

Item1 = Item(user=user, name="STill pale ALE",
                    description="STill pale ALE is STALE but never stale! It is what it is, always was, always will be. Enjoy!",
                    picture_path="../static/images/tall_wheat.jpeg",
                    price="$2.00", ibu="30", abv="6", category=category3)

session.add(Item1)
session.commit()


Item2 = Item(user=user, name="Pale Ginger Root",
                    description="Unique pale ale with a subtle, yet delicious ginger afterbirth.",
                    picture_path="../static/images/light_foam.jpeg",
                    price="$3.00", ibu="30", abv="5", category=category3)

session.add(Item2)
session.commit()

Item3 = Item(user=user, name="Pail of Pale",
                    description="This beer is for those pale ale lovers on a buget.",
                    picture_path="../static/images/wheat.jpeg",
                    price="$1.00", ibu="30", abv="5", category=category3)

session.add(Item3)
session.commit()

Item4 = Item(user=user, name="Can I get a Pale Yeah!",
                    description="For the easily excitable. If you're not excited maybe you should try this pale ale anyway, see how you feel.",
                    picture_path="../static/images/light_lagers.jpeg",
                    price="$1.50", ibu="40", abv="6.5", category=category3)

session.add(Item4)
session.commit()

# Items for Porter
category4 = Category(name="Porter")

session.add(category4)
session.commit()

Item1 = Item(user=user, name="Train Porter",
                    description="A good porter to start with for those who haven't dicovered their love of them yet.",
                    picture_path="../static/images/porter2.jpg",
                    price="$2.00", ibu="20", abv="6", category=category4)

session.add(Item1)
session.commit()


Item2 = Item(user=user, name="Harry Porter",
                    description="Harry Porter is the most famous and magical malty yet hoppy beer you'll ever try!",
                    picture_path="../static/images/porter.jpg",
                    price="$3.00", ibu="45", abv="5", category=category4)

session.add(Item2)
session.commit()

Item3 = Item(user=user, name="Malt Mania",
                    description="Low in hops, high in malts, delicious all around.",
                    picture_path="../static/images/stout.jpg",
                    price="$2.50", ibu="30", abv="6", category=category4)

session.add(Item3)
session.commit()

# Items for Stout
category5 = Category(name="Stout")

session.add(category5)
session.commit()

Item1 = Item(user=user, name="Shout Stout",
                    description="Once you try this beer, you'll shout it out to the world!",
                    picture_path="../static/images/stoutly.jpg",
                    price="$2.00", ibu="40", abv="5", category=category5)

session.add(Item1)
session.commit()


Item2 = Item(user=user, name="Short and Stout",
                    description="Very alcoholoic and flavorful. Serve in small amounts, and enjoy the incredible craftsmanship.",
                    picture_path="../static/images/stout.jpg",
                    price="$3.00", ibu="50", abv="7.5", category=category5)

session.add(Item2)
session.commit()

Item3 = Item(user=user, name="Dark N' Toasty",
                    description="This stout has a unique balance on malts and a hoppy aroma to please with every sip.",
                    picture_path="../static/images/porter.jpg",
                    price="$2.50", ibu="45", abv="5", category=category5)

session.add(Item3)
session.commit()

# Items for Triple
category6 = Category(name="Triple")

session.add(category6)
session.commit()

Item1 = Item(user=user, name="Three Times a Charm",
                    description="A robust triple with that will knock your socks off before or by beer 3, guaranteed.",
                    picture_path="../static/images/md_lager.jpg",
                    price="$5.00", ibu="30", abv="9", category=category6)

session.add(Item1)
session.commit()


Item2 = Item(user=user, name="Tripple and Fall",
                    description="Delicious triple that you will simply fall for from sip 1!",
                    picture_path="../static/images/med_lager.jpeg",
                    price="$4.00", ibu="40", abv="8", category=category6)

session.add(Item2)
session.commit()

Item3 = Item(user=user, name="Next Level Triple",
                    description="The most famous triple in town. Get it while it lasts.",
                    picture_path="../static/images/med_ipa.jpg",
                    price="$4.50", ibu="20", abv="8", category=category6)

session.add(Item3)
session.commit()


# Items for Wheat
category7 = Category(name="Wheat")

session.add(category7)
session.commit()

Item1 = Item(user=user, name="Wheat Femmes",
                    description="Chilling, just like the famous French movie '8 femmes'.",
                    picture_path="../static/images/another_lager.jpeg",
                    price="$3.00", ibu="30", abv="5", category=category7)

session.add(Item1)
session.commit()


Item2 = Item(user=user, name="Classical Wheat",
                    description="Full of flavor, with a sweet banana after taste that can't be beat.",
                    picture_path="../static/images/tall_wheat.jpeg",
                    price="$2.00", ibu="20", abv="5", category=category7)

session.add(Item2)
session.commit()

Item3 = Item(user=user, name="Twick or Twheat!",
                    description="This stunning wheat will put you in a mischievous mood.",
                    picture_path="../static/images/twisted_wheat.jpeg",
                    price="$4.00", ibu="25", abv="6", category=category7)

session.add(Item3)
session.commit()

Item4 = Item(user=user, name="Swheat Ride",
                    description="Light in color, thick in quality, take this beer beer for a joy-drink!",
                    picture_path="../static/images/light_wheat.jpg",
                    price="$2.00", ibu="22", abv="5", category=category7)

session.add(Item4)
session.commit()

Item5 = Item(user=user, name="Last Wheat Standing",
                    description="A beer that can't be beat, so don't try. Just buy, drink, and enjoy.",
                    picture_path="../static/images/medium_lager.jpeg",
                    price="$2.50", ibu="30", abv="6", category=category7)

session.add(Item5)
session.commit()


print ("added menu items!")
