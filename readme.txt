This is my implementation of raytomely's engine. You can find his original work here:
https://raytomely.itch.io/raycasting-floorcasting

The bulk of credit goes to him. He, in turn, cites the following tutorial, which is amazing:
https://permadi.com/1996/05/ray-casting-tutorial-table-of-contents/

Here are the changes that I made:
1) I added the ability to have different "wall" types
2) I added a ceiling
3) I allowed for the floor and ceiling to have a different tile than the walls
4) I checked for collision with the wall before allowing you to move (kinda important!)
5) I added a soundtrack. The one I am using is Stones, from Ultima IX

There is still something buggy about the rendering of floors and ceilings, and occasionally I get an odd line in one of the walls

There are two versions, the free moving FPS, and grid moving Crawler

Any comments are welcome, I can be reached at https://www.reddit.com/user/TIDMADT