Title: Infraspace PowerPipes Mod
Description: A first mod to Infraspace a factory/automation game by Dionic Software
Date: 2023-09-28 23:00
Tags: modding, games, infraspace


## Introduction

[Dionic software modding guide](https://forum.dionicsoftware.com/t/introduction-to-infraspace-modding/3134)  
[Dionic software ModKit](https://github.com/DionicSoftware/ISModKit/tree/master)  
[] Link to unity version  

### Setting up the workplace environment 

### Patching

added to `resources.json` (may be removed in favor of the existing power resource)
``` json
	"electicity": {
        "name": "electicity", 
        "stackSize": 50,
        "colorHex": "E2E099",
        "carModelName": "Car_A",
        "canBePrioritized": true,
        "canHaveExportRule": false,
        "maxOrderStackSize": 1000
    },
```

added to `roads.json`
``` json
  "pipe_power": {
    "vehicleType": "pipe",
    "type": "pipe",
    "resourceName": "power",
    "floorOffset": -25,
    "costs": [
      {"resourceName": "steel", "amount": 50 },
      {"resourceName": "concrete", "amount": 100},
    ],
    "requiredTech": ["powerPipes"],
  },
```

added to `techs.json`
``` json
	"powerPipes": {
		"cost": 40,
		"predecessors": ["pipes"],
		"locationX": 2,
		"locationY": -1.5,
		"requiredResources": ["sciencePack2"]
	},
```

added powerpipe to pipes menu in  to `constructionCategories.json`
``` json
  { 
    "categoryName": "pipes",
    "buttonsType": "pipes",
    "children": [
      {"itemName": "pipe_oxygen"},
      {"itemName": "pipe_water"},
      {"itemName": "pipe_crudeOil"},
      {"itemName": "pipe_methane"},
      {"itemName": "pipe_power"}, // <- Only line modified
    ]
  },
```
