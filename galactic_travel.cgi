#!/usr/bin/python

# Written by Steven Penava

# Establishing HTML type
print "Content-type: text/html\n\n"

# Styling and opening body
print '''
<head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet" href="myStyles.css">
    <title>Conversion Results</title>
</head>
<body>
'''

# Imports
import cgi
import math

# Form data
form = cgi.FieldStorage()

try:
    distX = form["distx"].value
    unitX = form["unitx"].value         # DO WE HAVE TO VALIDATE NUBMER ENTRY, LIKE 76 RAD NOT VALID? 0 < n < 180 ???

    distY = form["disty"].value
    unitY = form["unity"].value

    angleA = form["anglea"].value
    unitA  = form["unita"].value

    unitAnswer = form["unitanswer"].value
except KeyError:
    # Catching empty field value(s)
    print '''
    <div class="galactic-form-container">
        <div class="galactic-titles galactic-results one">
            <h1 class="galactic-h1">Error!</h1>
            <h3 class="text-muted galactic-muted">Looks like you left one or more fields empty or left out a required parameter with the request.</h3>
            <br><br>
            <input type="button" class="btn btn-primary" value="Click here to go back" onclick="history.back(-1)" />
        </div>
    </div>
    '''

# Conversion dictionary information (stores every necessary multiplier)
conversions = {
    "parsec": {
        "parsec": 1,
        "kilometer": 3.086 * math.pow(10, 13),
        "xlarn": 0.1568332236,
        "lightyear": 3.26
    },
    "lightyear": {
        "lightyear": 1,
        "parsec": 0.3067484663,
        "kilometer": 9.461 * math.pow(10, 12),
        "xlarn": 0.04810835079
    },
    "xlarn": {
        "xlarn": 1,
        "parsec": 6.3762,
        "lightyear": 20.786412,
        "kilometer": 1.9676953 * math.pow(10, 14) 
    },
    "kilometer": {
        "kilometer": 1,
        "parsec": 3.2404407 * math.pow(10, -14),
        "lightyear": 1.056970722 * math.pow(10, -13),
        "xlarn": 5.082087659 * math.pow(10, -15) 
    }
    ,
    "degree": {
        "degree": 1,
        "radian": 0.0174533,
        "xarnian": 1.7453286279
    },
    "radian": {
        "radian": 1,
        "degree": 57.2957549575,
        "xarnian": 100
    },
    "xarnian": {
        "xarnian": 1,
        "degree": 0.572958,
        "radian": 0.01
    }
}

# Convert function
def convert(quantity, sourceUnit, destinationUnit):
    return quantity * conversions[sourceUnit][destinationUnit]

# Compute function
def compute(dist1, dist2, angle):
    return math.sqrt(dist1**2 + dist2**2 - (2 * dist1 * dist2 * math.cos(math.radians(angle))))

try:

    answerInput1 = convert(float(distX), unitX, unitAnswer)
    answerInput2 = convert(float(distY), unitY, unitAnswer)
    angleDegrees = convert(float(angleA), unitA, "degree")

    finalAnswer = compute(answerInput1, answerInput2, angleDegrees)
except KeyError:
    # Catching erroneous field value(s)
    print '''
    <div class="galactic-form-container">
        <div class="galactic-titles galactic-results one">
            <h1 class="galactic-h1">Error!</h1>
            <h3 class="text-muted galactic-muted">Looks like you tried to use a unit that doesn't exist, a number for a unit, or some other incorrect input.</h3>
            <br>
            <h1>Possible distance units:</h3>
            <h3 class="text-muted galactic-muted">xlarn</h3>
            <h3 class="text-muted galactic-muted">kilometer</h3>
            <h3 class="text-muted galactic-muted">parsec</h3>
            <h3 class="text-muted galactic-muted">lightyear</h3>
            <br><br>
            <input type="button" class="btn btn-primary" value="Click here to go back" onclick="history.back(-1)" />
        </div>
    </div>
    '''

# Outputting as HTML & importing Bootstrap so the output is pretty :)
print '''
<div class="galactic-form-container">
    <div class="galactic-titles galactic-results one">
        <h1 class="galactic-h1">Computation Results</h1>
        <h3 class="text-muted galactic-muted">by Steven Penava</h2>
    </div>
    <h3 class="galactic-results one">Origin (Distance from Earth): {0} {1}</h3>
    <h3 class="galactic-results two">Destination (Distance from Earth): {2} {3}</h3>
    <h3 class="galactic-results three">Angle (between above vectors): {4} {5}</h3>
    <h3 class="galactic-results four">Answer: {6} {7}</h3>
    <br><br>
    <input type="button" class="btn btn-primary galactic-results four" value="Click here to go back" onclick="history.back(-1)" />
</div>
'''.format(distX, unitX,  distY, unitY, angleA, unitA, finalAnswer, unitAnswer)

# Closing body
print '''
</body>
'''