from time import time

def build_deck(deckname:str, autoplay:bool =True):
    deckId = int(time()*1000)
    deckConfigId = deckId+1

    # 1. dconf
    dconf = dconf_default["1"]
    dconf['autoplay'] = autoplay
    dconf['id'] = deckConfigId
    dconf['name'] = deckname

    # 2. decks
    decks = decks_default["1"]
    decks['conf'] = deckConfigId
    decks['name'] = deckname
    decks['id'] = deckId

    return {
        'dconf':{str(deckConfigId):dconf},
        'decks':{str(deckId):decks},
        'id': deckId
    }

def build_model(ttstype:str):
    modelId = int(time()*1000)
    model = models_default["1678093076416"]
    model['tmpls'][0]['afmt'] = model['tmpls'][0]['afmt'] % ('<tts style="display: none" service="android" voice="en_US">{{TTSText}}</tts>' if ttstype == 'ankidroid' else '{{tts en_US:TTSText}}',)
    model['id'] = modelId

    return {str(modelId):model}

conf_default = {
    "activeDecks": [
        1
    ],
    "addToCur": True,
    "collapseTime": 1200,
    "creationOffset": -210,
    "curDeck": 1,
    "curModel": 1678131619188,
    "dayLearnFirst": False,
    "dueCounts": True,
    "estTimes": True,
    "newSpread": 0,
    "nextPos": 1,
    "schedVer": 2,
    "sortBackwards": False,
    "sortType": "noteFld",
    "timeLim": 0
}

mid_default = '1678093076416'

models_default = {
    "1678093076416": {
        "css": ".card {\n    font-family: arial;\n    font-size: 20px;\n    text-align: left;\n    color: black;\n    background-color: white;\n}\n\n.ldoceEntry .Entry\n{\n    font-size : 12pt;\n    text-align : justify;\n    display : block;\n    margin-top : 8px;\n}\n\n.ldoceEntry .Thesref {\n    color : #364395;\n}\n\n\n.ldoceEntry .ABBR\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .ACTIV\n{\n    display : none;\n}\n\n.ldoceEntry .AMEQUIV\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .BOX\n{\n    display : none;\n}\n\n.ldoceEntry .BREQUIV\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .COLLO\n{\n    font-weight : bold;\n    margin-left : 20px;\n}\n\n.ldoceEntry .ColloExa\n{\n    display : block;\n}\n\n.ldoceEntry .COLLOINEXA\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .COMMENT\n{\n    display : none;\n}\n\n.ldoceEntry .COMP\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .Crossrefto\n{\n    font-weight : bold;\n    font-size : 120%;\n}\n\n.ldoceEntry .DERIV\n{\n    font-weight : bold;\n    font-size : 120%;\n}\n\n.ldoceEntry .Entry\n{\n    font-size : 11pt;\n    text-align : justify;\n}\n\n.ldoceEntry .ErrorBox\n{\n    display : block;\n}\n\n.ldoceEntry .EXAMPLE\n{\n    display : block;\n    margin-left : 20px;\n    color : gray;\n}\n\n\n.ldoceEntry .FIELD\n{\n    display : none;\n}\n\n.ldoceEntry .AC,\n.ldoceEntry .synopp {\n    color : #fff;\n    border-color: #f1d600;\n    background-color:#f1d600;\n}\n\n.ldoceEntry .FREQ\n{\n    color : red;\n    border-color : red;\n}\n\n.ldoceEntry .LEVEL\n{\n    color : red;\n    font-size : 120%;\n}\n\n.ldoceEntry .FULLFORM\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .GEO,\n.ldoceEntry .geo\n{\n    font-weight : normal;\n    color : #364395;\n}\n\n.ldoceEntry .GLOSS\n{\n    color : #364395;\n    font-weight : normal;\n    font-style : normal;\n}\n\n.ldoceEntry .GRAM,\n.bussdictEntry .GRAM\n{\n    color : green;\n    font-weight:bold;\n    margin:0 5px 10px 3px\n}\n\n.ldoceEntry .GramExa\n{\n    display : block;\n}\n\n.ldoceEntry .HINTBOLD\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .HINTITALIC\n{\n    font-style : italic;\n}\n\n.ldoceEntry .HINTTITLE\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .frequent .HOMNUM {\n    vertical-align : super;\n    font-size : 12pt;\n    color : red;\n    font-weight : bold;\n}\n\n.ldoceEntry .frequent .HYPHENATION {\n    color : red;\n    font-size : 160%;\n}\n.ldoceEntry .HOMNUM\n{\n    vertical-align : super;\n    font-size : 12pt;\n    color : red;\n    font-weight : bold;\n}\n\n.ldoceEntry .HWD\n{\n    display : none;\n}\n\n.ldoceEntry .HYPHENATION,\n.ldoceEntry .PHRVBHWD\n{\n    font-weight : bold;\n    font-size : 160%;\n    color : red;\n}\n\n.ldoceEntry .LEXUNIT,\n.ldoceEntry .LEXVAR\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .LINKWORD\n{\n    color : #364395;\n}\n\n.ldoceEntry .NOTE,\n.ldoceEntry .Noteprompt\n{\n    display : none;\n}\n\n.ldoceEntry .OBJECT\n{\n    font-weight : normal;\n}\n\n.ldoceEntry .OPP,\n.ldoceEntry .ORTHVAR,\n.ldoceEntry .PASTPART,\n.ldoceEntry .PASTTENSE\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .PhrVbEntry\n{\n    display : block;\n}\n\n.ldoceEntry .PIC,\n.ldoceEntry .PICCAL\n{\n    display : none;\n}\n\n.ldoceEntry .PLURALFORM\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .POS,\n.bussdictEntry .POS\n{\n    color : green;\n    font-weight:bold;\n    margin:0 0 0 10px\n}\n\n.ldoceEntry .PRESPART,\n.ldoceEntry .PRESPARTX\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .PROPFORM\n{\n    font-weight : bold;\n    margin-left : 20px;\n}\n\n.ldoceEntry .PROPFORMPREP\n{\n    font-weight : bold;\n    margin-left : 20px;\n}\n\n.ldoceEntry .PTandPP,\n.ldoceEntry .PTandPPX\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .REFHOMNUM\n{\n    vertical-align : super;\n    font-size : 60%;\n}\n\n.ldoceEntry .REFHWD\n{\n    font-weight : bold;\n    font-style : normal;\n}\n\n.ldoceEntry .REFLEX\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .REGISTERLAB\n{\n    color : purple;\n    font-style : italic;\n}\n\n.ldoceEntry .RELATEDWD\n{\n    font-weight : bold;\n    color:blue;\n}\n\n.ldoceEntry .RunOn\n{\n    display : block;\n    margin-bottom : 10px;\n}\n\n.ldoceEntry .Sense {\n    display : block;\n    margin-left : 20px;\n    margin-bottom : 15px;\n}\n\n.ldoceEntry .SIGNPOST\n{\n    background-color: #f18500;\n    color: white;\n    font-weight: bold;\n    font-size: 79%;\n    text-transform: uppercase;\n    border-radius: 5px;\n    -moz-border-radius: 5px;\n    -webkit-border-radius: 5px;\n    /* padding-left: 3px; */\n    /* padding-right: 3px; */\n    padding: 0px 5px;\n    letter-spacing: 1px;\n}\n\n.ldoceEntry .STRONG\n{\n    font-style : italic;\n}\n\n.ldoceEntry .Subsense\n{\n    display : block;\n    margin-left : 10px;\n}\n\n.ldoceEntry .SUPERL,\n.ldoceEntry .SYN,\n.ldoceEntry .T3PERSSING,\n.ldoceEntry .T3PERSSINGX\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .UNCLASSIFIED\n{\n    font-weight : bold;\n}\n\n.ldoceEntry .USAGE\n{\n    display : none;\n}\n\n.ldoceEntry .GramBox .CROSS .neutral {\n    color: red;\n    margin-right: 10px;\n}\n\n.ldoceEntry .neutral\n{\n    color : black;\n    font-style : normal;\n    font-weight : normal;\n    font-variant : normal;\n}\n\n .ldoceEntry .EXPL .cross,\n .ldoceEntry .GramBox .EXPL .dont_say,\n .ldoceEntry .BADEXA\n{\n    color : red;\n}\n\n.ldoceEntry .italic\n{\n    font-style : italic;\n    font-weight : normal;\n}\n\n.ldoceEntry .infllab\n{\n    font-style : italic;\n    font-weight : normal;\n}\n\n.ldoceEntry .warning\n{\n    font-style : normal;\n    font-weight : bold;\n    color : red;\n}\n\n.ldoceEntry .sensenum\n{\n    font-style : normal;\n    font-weight : bold;\n    color : black;\n}\n\n.ldoceEntry .synopp,\n.ldoceEntry .FREQ,\n.ldoceEntry .AC\n{\n    display : inline-block;\n    font-style : normal;\n    font-weight : bold;\n    text-transform : uppercase;\n    border-radius : 5px;\n    -moz-border-radius : 5px;\n    -webkit-border-radius : 5px;\n    border : solid 1px;\n    padding-left : 4px;\n    padding-right : 4px;\n}\n\n.bussdictEntry .Box,\n.ldoceEntry .ColloBox,\n.ldoceEntry .ThesBox,\n.ldoceEntry .F2NBox,\n.ldoceEntry .GramBox {\n    display : block;\n    border-radius : 5px;\n    -moz-border-radius : 5px;\n    -webkit-border-radius : 5px;\n    border : solid #364395 1px;\n    padding : 15px;\n    margin : 8px 0;\n}\n\n.GramBox{\n    background-color:#fff;\n    color:#000\n}\n\n.GramBox .boxheader {\n    line-height:2em\n}\n\n.ColloBox .heading {\n    line-height:2em;\n    margin:0 10px 0  0\n}\n\n.ThesBox .heading{\n    line-height:2em\n}\n\n.ldoceEntry .HEADING,\n.ldoceEntry .heading {\n    font-weight : bold;\n    font-size : 120%;\n    color : #364395;\n}\n\n.ldoceEntry .HEADING.newline {\n    display : block;\n}\n\n.ldoceEntry .SECHEADING,\n.ldoceEntry .subheading {\n    display : table;\n    border-radius : 5px;\n    -moz-border-radius : 5px;\n    -webkit-border-radius : 5px;\n    border : solid #6f469d 2px;\n    padding-left : 4px;\n    padding-right : 20px;\n    margin:25px 0 10px 0;\n    font-weight : bold;\n    color : white;\n    text-transform : uppercase;\n    background-color : #6f469d;\n}\n\n.ldoceEntry .Collocate,\n.ldoceEntry .Exponent {\n    display : block;\n    margin:15px 0 0 6px;\n}\n\n.ldoceEntry .EXPL {\n    display : block;\n}\n\n.ldoceEntry .COLLOC,\n.ldoceEntry .EXP,\n.ldoceEntry .EXPR {\n    font-weight : bold;\n}\n\n.ldoceEntry .keycollo {\n    font-weight : bold;\n    color : #364395;\n}\n\n.ldoceEntry .THESPROPFORM {\n    font-weight : bold;\n}\n\n.ldoceEntry .COLLEXA,\n.ldoceEntry .THESEXA {\n    color : gray;\n    display : block;\n}\n\n\n.ldoceEntry .LearnerItem {\n    display : block;\n}\n\n.ldoceEntry .GOODCOLLO {\n    font-style : italic;\n}\n\n.ldoceEntry .BADCOLLO {\n    text-decoration : line-through;\n}\n\n.ldoceEntry .DEFBOLD {\n    font-weight : bold;\n}\n\n.ldoceEntry .exafile {\n    color : gray;\n    font-style : normal;\n    font-size : 120%;\n    padding: 5px;\n}\n\n.ldoceEntry .amefile {\n    color : #4693db;\n    font-size : 130%;\n    padding-left: 5px;\n}\n\n.ldoceEntry .brefile {\n    color : #fa6360;\n    font-size : 130%;\n    padding-left: 5px;\n}\n",
        "did": None,
        "flds": [
            {
                "collapsed": False,
                "description": "",
                "font": "Arial",
                "name": "Headword",
                "ord": 0,
                "plainText": True,
                "rtl": False,
                "size": 20,
                "sticky": False
            },
            {
                "collapsed": False,
                "description": "",
                "font": "Arial",
                "name": "Front",
                "ord": 1,
                "plainText": False,
                "rtl": False,
                "size": 20,
                "sticky": False
            },
            {
                "collapsed": False,
                "description": "",
                "font": "Arial",
                "name": "Back",
                "ord": 2,
                "plainText": False,
                "rtl": False,
                "size": 20,
                "sticky": False
            },
            {
                "collapsed": False,
                "description": "",
                "font": "Arial",
                "name": "TTSText",
                "ord": 3,
                "plainText": True,
                "rtl": False,
                "size": 20,
                "sticky": False
            }
        ],
        "id": 1678093076416,
        "latexPost": "\\end{document}",
        "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
        "latexsvg": False,
        "mod": 1678123210,
        "name": "LDOCE",
        "req": [
            [
                0,
                "any",
                [
                    1
                ]
            ]
        ],
        "sortf": 1,
        "tmpls": [
            {
                "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}\n%s\n<br><a href=\"https://www.wordhippo.com/what-is/sentences-with-the-word/{{text:Headword}}.html\">More examples</a>",
                "bafmt": "",
                "bfont": "",
                "bqfmt": "",
                "bsize": 0,
                "did": None,
                "name": "Card 1",
                "ord": 0,
                "qfmt": "meaning of <b>{{Headword}}</b>:<br>{{Front}}"
            }
        ],
        "type": 0,
        "usn": -1
    }
}

decks_default = {
    "1": {
        "browserCollapsed": True,
        "collapsed": True,
        "conf": 1,
        "desc": "",
        "dyn": 0,
        "extendNew": 0,
        "extendRev": 0,
        "id": 1,
        "lrnToday": [
            0,
            0
        ],
        "mod": 0,
        "name": "Default",
        "newLimit": None,
        "newLimitToday": None,
        "newToday": [
            0,
            0
        ],
        "revToday": [
            0,
            0
        ],
        "reviewLimit": None,
        "reviewLimitToday": None,
        "timeToday": [
            0,
            0
        ],
        "usn": 0
    }
}

dconf_default = {
    "1": {
        "autoplay": True,
        "buryInterdayLearning": False,
        "dyn": False,
        "id": 1,
        "interdayLearningMix": 0,
        "lapse": {
            "delays": [
                10.0
            ],
            "leechAction": 1,
            "leechFails": 8,
            "minInt": 1,
            "mult": 0.0
        },
        "maxTaken": 60,
        "mod": 0,
        "name": "Default",
        "new": {
            "bury": False,
            "delays": [
                1.0,
                10.0
            ],
            "initialFactor": 2500,
            "ints": [
                1,
                4,
                0
            ],
            "order": 1,
            "perDay": 20
        },
        "newGatherPriority": 0,
        "newMix": 0,
        "newPerDayMinimum": 0,
        "newSortOrder": 0,
        "replayq": True,
        "rev": {
            "bury": False,
            "ease4": 1.3,
            "hardFactor": 1.2,
            "ivlFct": 1.0,
            "maxIvl": 36500,
            "perDay": 200
        },
        "reviewOrder": 0,
        "timer": 0,
        "usn": 0
    }
}