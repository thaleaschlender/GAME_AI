# GAME_AI - Group 15

## Usage
To launch the game simply run the main.py file.

```bash
# (Optional) From this directory
$ python3 main.py
```

It is important to check that the required packages are installed.

The default agent is a human agent, you can control this agent with the left and right arrows. To load in another agent you need to comment out 

```python
P1 = Player(DISPLAYSURF)  # defines the player object
```

And uncomment the desired agent in `main.py`

## Install packages
```bash
$ python -m pip install -r requirements.txt
```

## Training an EA agent
You can train an EA agent by simply running

```bash
$ python3 EATrainer.py
```

This will start the training process and in the end save your agent in `./models/hidden12/` as the current size of the hidden layer is 12. The name of the file is automatically generated and depends on the fitness of the best performing agent after the last generation and the adjustable parameters. 
Mutation parameters, number of training generations and population size can be easily changed at the bottom of the `EATrainer.py` file. Changing the hidden layer size had to be done in `EAPLayer.py`

## Loading an EA agent
By default the game loads in a human player agent, but an example of how to load an EA agent is present in the comments

```python
P1 = EAPlayer(DISPLAYSURF) # EA player
P1.load_brain('./models/hidden12/best_fit34_pop250_gens15_mrc0.5_mrw0.3_ms0.7')
```

Simply change the argument of `load_brain` to the name of your own agent to load your own EA agent.