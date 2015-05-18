## Lamp Management Documentation

### Intro

There are two Lamp modes:

* Automatic
* Manual

#### Manual mode
It's a diagnostic mode only. It allows to set the driver to any value.

#### Automatic mode
Lamp Brightness Regulation - 
	
	y = f (j,k)
	j - wanted lighting level
	k - external ligthning level

### Data Structure


##### Building
	identifier
	label

##### Hardware:
	identifier
	protocol
	building
	is_sensor (True or False)
	type ( Lamp, Lightning Sensor, Movement Sensor itp )
	computer_ip
	address (csv)

##### Lamp:
	# static
	identifier
	mode
	virtual_sensor (virtual)
	group (multi field)
	geo position
	hardware
	# semi static
	working lightning (wanted level) setting
	special ligthing (wanted level) setting
	presence lighting (wanted level) setting 
	# dynamic
	(actual lighning level)
	wanted lightning level
	actual driver value
	flag - presence
	flag - special
	flag - working 

	change required
	
	
	Flag priorities:
		Working
		Presence
		Special setting

##### Area

    identifier 
    label
    mpoly
    level

##### LGroup
	identifier
	madli (opt)

### Engine Workers

#### Triggers:
Triggers are external events.

	Changes flags
	changes boolean "change required"	
	changes wanted lighting level

#### Executers:
Polling database for lamps that needs change and executing hardware commands.
	
#### Sensor Worms
Polling sensors for changes and updating databases





