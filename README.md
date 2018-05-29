# Purpose
* While this project is "Full Stack" in of itself, it is the final project for the "Backend" section of the Udacity Full Stack Web Developer Nanodegree.
* This project is an "Item Catalog" website (beer theme) that provides a list of items (beers) within a variety of catgories (beer styles), where all data is persisted in PostgreSQL.
* It also has a user registration and authentication system (third-party OAuth authentication) using the Github API.
* Utilizes CRUD operations: Everyone can Read, anyone logged in can Create a new item, owners of an item can Edit (Update) or Delete it.

# Update
* After submission this project was updated to also part of the Linux Server Project, Udacity's final. The goal being to configure and secure a server, and then host an old (this) project on it.

# Running the Code
* Visit http://beers.daniellaurence.com/
* OR
* Clone or Fork this repository.
* In your teminal window / command line type "python main.py"
* Open your web browser to http://lvh.me:8000/ and begin navigating the pages.
* You will need to have python 3, and the sqlalchemy and flask libraries installed to run this code.
* You will need to have a Github account, either prior to signing in, or create one through the sign-in process.

# Test Website Functionality
* Scroll down the page looking at the contents. You should be able to click on 3 things.
    1. The "Login" button, which will take you through the Login flow (Github is the third party OAuth provider).
    2. The "Beer Categories". By selecting a beer category you can narrow the list of results to the specific beer category chosen.
    3. The "Click for Details" button will take you to a specific page about that item with more details on it, like price.
* Once you've logged in you will be able to see 1 of 2 scenarios.
    1. In the first scenario you don't "own" any of the items, as in you have not created them, so the only difference you will see from before you logged in is that the "Login" button has been replaced by a "Logout username" where "username" is your Github username. Additionally beneath the Beer Categories, but above the results, you will see an "Add a Beer +" button where you can create your own beer. Once you create a new beer the second scenario will be visible to you.
    2. In the second scenario, you will see everything from the first, but in addtion each beer that you "own", as in you created, will be marked with a "Your Beer" text, so you can recognize which beers are yours. Additionally when you view the details for that specific item "Edit" and "Delete" buttons and functionality are now available.
* Finally click on "Logout username" to go back to seeing the original website with the options you started with.
* Please note that you can Login from any page, as well as "Back to All Beers" which not only take you to the landing page, but refreshes the list of beers to be all beers. Don't forget you can use the browser's native "back" and "forward" buttons to navigate between pages you've already been to.

# Troubleshhoting
* Make sure that you either have pyton 3, or you can run a virtual environment for it, or you convert the code to python 2.
* Everyone can Read, Make sure you signed in in order to Create.
* Confirm that you are the owner of an item if you are trying to Edit (Update) or Delete it.
* I already populated the database with some basic entries. If for some reason you need to wipe your local version of the database you can either pull it down from Github again, or you can run the "populate_beers.py" file I included.

# External Sources
* Other than using Duck Duck Go and Google to facilitate finding the pages, the actual websites I got help from were:
1. Stack Overflow - mostly for error messages
2. Digital Ocean - mostly for setup guides
3. AWS helper pages - for creating a new ubuntu user

