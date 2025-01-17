# Space Invaders Clone
This project has been initiated to get practice in python programming by implementing the famous Arcade game "Space Invaders".
<p align=center>
    <img title="Space Invaders" alt="The famous game Space Invaders" src="resources/SpaceInvaders-Gameplay.gif">
</P>

## Game Control
| Key | Action |
|-----|-----|
| Arrow Left | Move ship left |
| Arrow Right | Move ship right |
| Space | Fire |

## Implementation
The project started with the **Turtle graphics** implementation as this is an easy way to get started with a graphical user-interface (GUI) in python.
It took some days to get the implementation playable - so that it makes fun.
Then the question arose if it wouldn't be easier to use another graphics bundle for a python game.
**pygame** was self-evident for this trial.
Of course it took some time to dive into pygame to get the first game running. But it was worth the effort. - There will be further games with pygame...

The folder structure was chosen to hold the code for **Turtle graphics** and **pygame** in parallel - allowing easy comparison of the two implementations.
The graphics elements used are located in the common folder *resources*.

### Techniques
- When a shot hits an alien, the alien becomes invisible. The dectection of a collision is only done with visible objects.
Shots run through invisible objects.
- There is no infinite number of available shots. Shot objects are kept inside shot buffers.
And it is avoided to destroy a shot object and generate a new one afterwards. Shot objects are reused after they hit some other object or disappear from screen.

## Differences in the Graphics Bundles

| Turtle graphics | pygame |
|-----|-----|
| only works with graphics in gif-format | supports various formats |
| attribute for visibility is intrinsic using a turtle object (see isvisible(), hideturtle()) | Visibility attribute needs to be implemented manually if needed. |
| To measure the distance between two turtle objects the built-in method distance() can be used.| A rectangle object needs to be created for a graphics element in order to move an object. Measurement of distance has to be implemented manually.|
| Distance is always measured from the center of an object. | Every edge or corner of the rectangle can be referenced for measurement - and the center! |
| Screen object has to be passed to other modules for width/height awareness. | User modules can access screen properties. |
| event handler outside of game-loop | event handler inside game-loop |
|||

## TODOs
- [ ] Speed Control Fine-Tuning
- [ ] Add 4 protective barriers where the ship can hide!
- [x] Harmonize key to trigger shot: The pygame implementation currently doesn't react upon space key properly!
- [x] Fix to get shots from aliens while mystery is visible (Same timer was used for aliens and mystery.)

## Sources
- The gif-files have been taken from [Wikipedia](https://en.wikipedia.org/wiki/Space_Invaders)
