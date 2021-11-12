//anger inspired by ryoho https://openprocessing.org/sketch/1084140
//sorrow inspired by the coding train pixel manipulation
//joy inspired by artisan's https://openprocessing.org/sketch/696867
//surprise inspired by the coding train painting with pixels https://www.youtube.com/watch?v=NbX3RnlAyGU&t=435s

String URL = "http://raspberrypi10.local:8000/";
int imageCounter = 0;

// FOR TEXT 
String angerList = "We never know when but being cheerful helps:If you don’t like it you may choose to avoid it :What is meant by Judge and regardless of the consequences? : If we are irritated it is not a pleasure: The important questions are answered not by liking only but disliking and accepting equally what one likes and dislikes. Otherwise there is no access to the dark night of the soul: A fire rages: It is not irritating to be where one is, it is only irritating to think one would like to be somewhere else";
String angerArray[] = split (angerList, ':'); 

String joyList = "-When in the state of nothing, one diminished the something in one: Life seems shabby and chaotic, disordered, ugly in contrast:What are the important questions and what is that greater earnestness that is required:Blackbirds rise from a field making a sound delicious beyond compare: Life is one: Each moment is absolute, alive and significant";
String joyArray[] = split(joyList, ':');

String surpriseList ="Let us say in life: no earthquakes are permissible. What happens then?:The idea, consequences, suggests musical term continuity: To accept whatever comes regardless of the consequences:How do you feel about Bach?:Next time he hears the piece, it will be different, perhaps less interesting, perhaps suddenly exciting: Anything may happen and it all does go together ";
String surpriseArray[] = split (surpriseList, ':');

String sorrowList = "There seemed to be no truth, no good, in anything big in society.:At any moment one is free to take on character again, but then it is without fear, full of life and love: We have found that by excluding we grow thin inside:When nothing is securly possessed one is free to accept any of the somethings:After several years of working alone, I began to feel lonely.:Falling down on some of one of the various banana peels is what we have been calling tragedy";
String sorrowArray[] = split (sorrowList, ':');
PFont font;
int textNum;
String displayText;

int textX, textY, textHue;

// FOR IMAGE EFFECTS
PImage img;
JSONObject json;
int joy, anger, surprise, sorrow;

// WHICH EMOTION EFFECT IS BEING DISPLAYED? 
// USED FOR BOTH IMAGE EFFECTS AND TEXT DISPLAY
String emotion = ""; // values can be "joy", "anger", "surprise", or "sorrow"
String[] emotions = {"joy", "anger", "surprise", "sorrow"};

int lastTimeStamp = millis();

void setup() {
  strokeWeight(int(random(2, 20)));
  background(0);
  //fullScreen(SPAN);
  size(800, 600);
  colorMode(HSB);
  //img.resize(width,height);
  
  img = loadImage("data/4.jpg");
  img.resize(width, height);
  
  chooseRandomEmotion();
  chooseDisplayText();
  
  tryLoadNewImage();
}

void draw() {
  image(img, 0, 0);

  quoteText();

  if (millis() - lastTimeStamp > 25000) {
    chooseRandomEmotion();
    tryLoadNewImage();
    chooseDisplayText();
    lastTimeStamp = millis();
  }
}

void chooseRandomEmotion() {
  emotion = emotions[int(random(4))];
}

void tryLoadNewImage() {
  background(0);
  println("Loading " + imageCounter+".jpg");
  
  try {
    imageCounter++;
    
    img = loadImage(URL + imageCounter+".jpg");
    img.resize(width, height);
    image(img,0,0);
    
    json = loadJSONObject(URL + imageCounter+".json");
    
    joy = json.getInt("joy");
    anger = json.getInt("anger");
    surprise = json.getInt("surprise");
    sorrow = json.getInt("sorrow");
    
    clear();
  }
  catch (Exception e) {
    imageCounter--;
    println((imageCounter+1) + ".jpg not found. Reloading current image.");
  }
  finally {

  }
  
  // choose the emotion status depending on emotional likelihoods
  if (surprise >= 3) {
    emotion = "surprise";
  } 
  else if (sorrow >= 3) {
    emotion = "sorrow";
  }
  else if (anger >= 3) {
    emotion = "anger";
  }
  else if (joy >= 3) {
    emotion = "joy"; 
  } else { // if no emotion is detected, pick one at random
    emotion = emotions[int(random(emotions.length))];
  }
}

//TEXT -----------------------------------------------------

void chooseDisplayText() {
  // choose the displayText depending on emotional likelihoods
  if ( emotion.equals("surprise") ) {
    displayText = surpriseArray[int(random(surpriseArray.length)-1)];
  } 
  else if ( emotion.equals("sorrow") ) {
    displayText = sorrowArray[int(random(sorrowArray.length)-1)];
  }
  else if ( emotion.equals("anger") ) {
    displayText = angerArray[int(random(angerArray.length)-1)];
  }
  else if ( emotion.equals("joy" ) ) {
    displayText = joyArray[int(random(joyArray.length)-1)];
  } else {
    displayText = "";
  }
  print("displayText = ", displayText);
  
  textX = width;
  textY = int(random(100, height-100));
  textHue = int(random(255));
}

void quoteText() {
  //textNum = int(random(6));
  font = createFont("Arial", 100, true); 
  textFont(font);
  textSize(150);
  
  //displayText = angerArray[textNum] + joyArray[textNum] + sorrowArray[textNum] + surpriseArray[textNum];

  if (textX < 0) {
    // drawing the text, offset, in dark beforehand gives it a dark "shadow"
    // a cheap n easy way to help readability
    fill(textHue, 100, 80);
    text(displayText, textX + textWidth(displayText) + 50 + 10, textY);
    fill(textHue, 255, 255);
    text(displayText, textX + textWidth(displayText) + 50, textY);
  }

  // if the first copy of the text is completely offscreen, set x to be 
  // at the current location of the second copy
  if (textX <= -textWidth(displayText)) {
    textX = textX + (int)textWidth(displayText) + 50;
  }

  // Draw the text
  // drawing the text, offset, in dark beforehand gives it a dark "shadow"
  // a cheap n easy way to help readability
  fill(textHue, 100, 80);
  text(displayText, textX+5, textY);
  fill(textHue, 255, 255);
  text(displayText, textX, textY);
  // move the position to the left
  textX = textX - 10;
  // textX--;

  // println( completeTest);
}
