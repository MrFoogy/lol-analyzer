## Screencast Link:

https://youtu.be/U8s0KsVAYqs

# League of Legends Play Pattern Analyzer
This project is a web application that uses the Riot Games API ([https://developer.riotgames.com/](https://developer.riotgames.com/)) to give an analysis of match data from the game League of Legends. The focus of the application is to give individual players data that summarizes their individual play patterns, in order to highlight areas where they can improve.

## Functionality
The following is the desired functionality of the application. Since many of these use similar API calls, the focus will be on implementing high-quality data visualizations for at least some of them rather than including precisely all items on the list.
* The user types their account name to start using the application
* The user can see a summary of their percentage of matches played per role and the winrate per role
* The user can see their most frequently played champions and winrate per champion
* The user can see their most frequently used items and winrate per item
* The user can see their most frequently used masteries and winrate per mastery
* The user can view a heatmap of the locations where different types of events commonly occur in their matches. These events could include kills, deaths, overall player movements and ward placements. 
* For all of the above, filters can be applied to restrict data to specific champions, game types and date intervals

## Front-end

I will build the front-end using Vue.js. I have limited web development experience and from my research this is one of the easier frameworks to learn. The front-end will perform REST calls to the back-end and visualize the data that it receives. The main focus of my front-end development will be creating intuitive and pretty visualizations for the player data. I will structure the webpage as a single-page application.

## Back-end

The back-end will be a Flask application that is responsible for receiving requests for different player data from the front-end, and then making calls to the Riot Games API to collect that data. Note that in most cases, it won't be enough to make one single call to the Riot API - most of the visualizations will require data from multiple calls, e.g. game events from multiple matches.

---