# Chat Intents manual

`Chat Intents` are a JSON file thats contains a intent's tag, training sentence and bot respose to those training sentence in a list of JSON objects.

Each language's chat intents data are separated into it's own file inside **[data folder](../data)**. For example, English chat intents data are stored in file named `intents_en.json`. And for Thai, the data is stored in file named `intents_th.json`.

## Intents object

```json
"intents_en": [
    {
      "tag": "goodnight_en",
      "patterns": [
        "goodnight",
        "g9",
        "guess I'll sleep now",
        "have a good night",
        "Have a good dream",
        "GN"
      ],

      "responses": [
        "Have a good night sir!",
        "Good night!"
      ]
    },
]
```

* **tag**: is a name of the intent(**Note**: the tag of each intents must be unique or it will get overwrited when training).
* **patterns**: is a list of training sentence/word.
* **responses**: is a list of bot response(the response will be selected randomly from this list when the intent is detected).

## Time-based intents

`Time-based intents` are intents that has two sets of response: `fes` and `nonfes`.

* **fes**: This list of response will be selected as bot response if the date is the same or in the range that defined in the intent.
* **nonfes**: This list of resonse will be selected as bot response if the date is not the same or not in range that defined in the intent.

### Time-based intents(one-day)

```json
"intents_en": [
    {
        "tag": "halloween_en",
        "date": 31,
        "month": 10,
        "patterns": [
            "halloween",
            "happy halloween"
        ],
        "responses": {
            "fes": [
                "Trick or Treat! If you don't want to get trick, you have to give me candies!",
                "Booh! It's Halloween!"
            ],
            "nonfes": [
                "Wrong date for pulling out costume, but you can still give me candies."
            ]
        }
    },
]
```

* **tag**: is a name of the intent(**Note**: the tag of each intents must be unique or it will get overwrited when training).
* **date**: is a date of an event.
* **month** is a month of an event.
* **patterns**: is a list of training sentence/word.
* **responses**: is an JSON object that contains list of `fes` and `nonfes` response.

### Time-based intents(variable-length)

```json
"intents_en": [
    {
        "tag": "songkran_en",
        "date": [13, 15],
        "month": 4,
        "patterns": [
          "songkran"
        ],
        "responses": {
            "fes": [
                "Songkran is here! Pls don't splash water on me.",
                "Happy Songkran day!"
            ],
            "nonfes": [
                "You want to splash some water? I think its not the time for that."
            ]
        }
    },
]
```

* **tag**: is a name of the intent(**Note**: the tag of each intents must be unique or it will get overwrited when training).
* **date**: is a date range of an event(First element is the starting date and second element is the ending date).
* **month** is a month of an event.
* **patterns**: is a list of training sentence/word.
* **responses**: is an JSON object that contains list of `fes` and `nonfes` response.

**Note**: the date range cannot exceed the date of the month. If your festival is in between two month, you can separate the intents to define your event date range.

```json
"intents_en": [

    {
        "tag": "new_year_pre_en",
        "date": 31,
        "month": 12,
        "patterns": [
            "Happy new year"
        ],
        "responses": {
            "fes": [
                "Happy new year! I hope next year would be a great year!"
            ],
            "nonfes": [
                "It's not new year yet.",
                "I think it's not new year right now"
            ]
        }
    },
    
    {
        "tag": "new_year_post_en",
        "date": [1, 2],
        "month": 1,
        "patterns": [
            "Happy new year"
        ],
        "responses": {
            "fes": [
                "Happy new year! I hope this year would be a great year!"
            ],
            "nonfes": [
                "It's not new year yet.",
                "I think it's not new year right now"
            ]
        }
    },

]
```

## Special variable integration

You can integrate a built-in variable of the bot into the bot's response by using `$variable_name`.

### Example

```json
"intents_en": [
    {
        "tag": "age_en",
        "patterns": [
            "how old are you?",
            "how old you are?",
            "whats your age?",
            "what your age?",
            "your age?",
            "age"
        ],
        "responses": [
            "I'm $age year old now!",
            "I think I'm $age now."
        ]
    },
]
```

### Available special variable list

* **$age**: age of the bot(counted since the init commit of the project)

There will be more special variable soon.
