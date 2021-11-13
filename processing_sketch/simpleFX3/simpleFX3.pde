//anger inspired by ryoho https://openprocessing.org/sketch/1084140
//sorrow inspired by the coding train pixel manipulation
//joy inspired by artisan's https://openprocessing.org/sketch/696867
//surprise inspired by the coding train painting with pixels https://www.youtube.com/watch?v=NbX3RnlAyGU&t=435s

//String URL = "../../test_images/";
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
PImage img, new_img;
JSONObject json;
int joy, anger, surprise, sorrow;

// WHICH EMOTION EFFECT IS BEING DISPLAYED? 
// USED FOR BOTH IMAGE EFFECTS AND TEXT DISPLAY
char emotion = 'J'; // 'J' for joy, 'A' for anger, 'S' for surprise, 'T' for sorrow tears
char[] emotions = {'J', 'A', 'S', 'T'};

int lastTimeStamp = millis();

void setup() {
  background(0);
  //fullScreen(SPAN);
  size(800, 600);
  colorMode(HSB);
  
  chooseRandomEmotion();
  chooseDisplayText();
  
  tryLoadNewImage();
}

void draw() {

  switch(emotion) {
    case 'S': 
      surprise();
      break;
    case 'T': 
      sorrow();
      break;
    case 'A': 
      anger();
      break;
    case 'J': 
      joy();
      break;
    default:              // Default executes if the case names
      image(img, 0, 0);   // don't match the switch parameter
      break;
  }

  quoteText();

  if (millis() - lastTimeStamp > 45000) {
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
  imageCounter++;
  
  background(0);
  println("\n try Loading " + imageCounter+ ".jpg");
  
  try {
    new_img = loadImage(URL + imageCounter+".jpg");
    new_img.resize(width, height);
    
    json = loadJSONObject(URL + imageCounter+".json");
    
    joy = json.getInt("joy");
    anger = json.getInt("anger");
    surprise = json.getInt("surprise");
    sorrow = json.getInt("sorrow");
    
    img = new_img;
    image(img,0,0);
  }
  catch (Exception e) {
    println("\n", imageCounter + ".jpg not found. Reusing current image.");
    imageCounter--;
  }
  finally {

  }
  
  // choose the emotion status depending on emotional likelihoods
  if (surprise >= 3) {
    emotion = 'S';
  } 
  else if (sorrow >= 3) {
    emotion = 'T';
  }
  else if (anger >= 3) {
    emotion = 'A';
  }
  else if (joy >= 3) {
    emotion = 'J'; 
  } else { // if no emotion is detected, pick one at random
    emotion = emotions[int(random(emotions.length))];
  }
  
  println("emotion: ", emotion);
  
  // reset the animations as needed depending on the emotion
  switch(emotion) {
    case 'S': 
      reset_surprise();
      break;
    case 'T': 
      // sorrow has no reset function needed
      break;
    case 'A': 
      reset_anger();
      break;
    case 'J': 
      reset_joy();
      break;
    default:
      println("\n No emotion selected... weird...");
      break;
  }
}

//TEXT -----------------------------------------------------

void chooseDisplayText() {
  switch(emotion) {
    case 'S': 
      displayText = surpriseArray[int(random(surpriseArray.length)-1)];
      break;
    case 'T': 
      displayText = sorrowArray[int(random(sorrowArray.length)-1)];
      break;
    case 'A': 
      displayText = angerArray[int(random(angerArray.length)-1)];
      break;
    case 'J': 
      displayText = joyArray[int(random(joyArray.length)-1)];
      break;
    default:
      displayText = "";
      break;
  }

  println("displayText = ", displayText);
  
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


// ANGER __________________________________________________

//array list and variables for anger particle system
ArrayList<Particle> particles;
float attforce = 0.2;
float repforce = 2;
int numParticle = 500;

void reset_anger() {
  strokeWeight(int(random(10, 60)));
  particles = new ArrayList<Particle>();
  for (int i= 0; i< numParticle; i++) {
    particles.add(new Particle(random(width), random(height), int(random(width)), int(random(height))));
  }
}

void anger() {
  for (int i = 0; i < particles.size(); i++) {
    Particle p = particles.get(i);
    p.move();
    p.display();
  }
}

//particle class for anger function
class Particle {
  PVector position, target, velocity, acceleration;
  color color_anger;
  int x_move;
  int y_move;

  Particle(float x, float y, int x_m, int y_m) {
    x_move = x_m;
    y_move = y_m;

    position = new PVector(x, y);
    target = position.copy();
    velocity = new PVector(0, 0);
    acceleration = new PVector(0, 0);
    color_anger =img.get(int(x), int(y));
  }

  void move() {
    PVector attraction = target.sub(position);
    attraction.mult(attforce);
    PVector mouse_pos = new PVector(x_move, y_move);
    PVector tmpForce =  mouse_pos.sub(position);
    tmpForce.limit(20);
    PVector repulsion = tmpForce.copy().normalize().mult(-30).sub(tmpForce);
    repulsion.mult(repforce);

    acceleration = attraction.add(repulsion);
    velocity.mult(10);
    velocity.add(acceleration);
    velocity.limit(3);
    position.add(velocity);
  }
  void display() {
    stroke(color_anger, 90);
    point(position.x, position.y);
  }

  void reset() {
    position.x = random(width);
    position.y = random(height);
    x_move = int(random(width));
    y_move = int(random(height));
    color_anger = img.get(int(position.x), int(position.y));
  }
}

//JOY -----------------------------------------------

//array list and variables for the joy particle system
ArrayList<Particle_2> particles_2;
float xoff, yoff, zoff, inc, col;
int spread, cols, rows, num;
PVector[] vectors;

//function to initiate joy in setup
void reset_joy() {
  spread = 50;
  inc = random(0.1, 0.8);
  num = 500;
  col = random(255);
  cols = floor(width/spread)+1;
  rows = floor(height/spread) +1;
  vectors = new PVector[cols*rows];
  particles_2 = new ArrayList<Particle_2>();

  for (int j = 0; j < num; j++) {
    particles_2.add(new Particle_2());
  }
}

//function to call joy in draw
void joy() {

  fill(255, 1);  
  rect(0, 0, width, height);
  filter(DILATE);

  xoff = 0;
  for (int y = 0; y < rows; y++) {
    xoff = 0;
    for (int x= 0; x< cols; x++) {
      float angle = noise(xoff, yoff, zoff) * PI *(joy/2)+1;
      PVector v = PVector.fromAngle(angle);
      v.setMag(1);
      vectors[x + y * cols] = v;
      xoff += inc;
    }
    yoff += inc;
  }
  zoff += 0.0005;
  if (col <255)col += 0.5;
  else col= 0 ;
  for (Particle_2 p2 : particles_2)p2.run();
}


//particle class for joy
class Particle_2 {
  PVector pos, vel, acc, prev;
  float max = random(2, 8);

  Particle_2() {
    pos = new PVector(width/3, height/2);
    prev = new PVector(pos.x, pos.y);
    vel = new PVector(0, 0);
    acc = new PVector(0, 0);
  }

  void copy() {
    prev.x = pos.x;
    prev.y = pos.y;
  }

  void run() {
    follow();
    update();
    show();
  }

  void update() {
    pos.add(vel);
    vel.limit(max);
    vel.add(acc);
    acc.mult(0);
    if (pos.x > width) {
      pos.x = 0;
      copy();
    }
    if (pos.x < 0) {
      pos.x = width;
      copy();
    }
    if (pos.y > height) {
      pos.y = 0;
      copy();
    }
    if (pos.y < 0) {
      pos.y = height;
      copy();
    }
  }
  void follow() {
    int x = floor(pos.x / spread);
    int y = floor(pos.y / spread);
    PVector force = vectors[x+y*cols];
    acc.add(force);
  }
  void show() {
    color c = img.get(int(pos.x), int(pos.y));
    stroke(c);
    line(pos.x, pos.y, prev.x, prev.y);
    copy();
  }
}

// SURPRISE  -------------------------------------

//array list and variables for the surprise particle system
Particle_3[] particles_3;
float b, c, vx, vy;

void reset_surprise() {
  stroke(0,0);
  //particles_3 = newArrayList<Particle_3>();
  particles_3 = new Particle_3[200];
  for (int i = 0; i < particles_3.length; i++) {
    particles_3[i] = new Particle_3();
  }
}

void surprise() {
  for (int i = 0; i < particles_3.length; i++) {
    particles_3[i].display_s();
    particles_3[i].move_s();
  }
}


// particle class for surprise
class Particle_3 {
  float x_s;
  float y_s;

  float vx;
  float vy;

  Particle_3() {
    x_s = width/2;
    y_s =(height/2)+100;
    float a = random(TAU);
    float speed_s = random(3);
    vx = cos(a)*speed_s;
    vy = sin(a)*speed_s;
  }

  void display_s() {
    //noStroke();
    color c_s = img.get(int(x_s), int(y_s));
    fill(c_s);
    //ellipse(x,y,30,30);
    rect(x_s, y_s, 30, 30);
  }

  void move_s() {
    x_s = x_s + vx; // random(-5,5);
    y_s = y_s + vy;
    if (y_s < 0) {
      y_s = height;
    }

    if (y_s > height) {
      y_s = 0;
    }

    if (x_s < 0) {
      x_s = width;
    }

    if (x_s > width) {
      x_s = 0;
    }
  }
}

// SORROW  ----------------------------------------------------------

//sorrow function just picks colors and draws ellipses randomly 
void sorrow() {
  for (int i = 0; i<500; i++) {
    float x = random(width);
    float y = random(height);
    color c = img.get(int(x), int(y));
    noStroke();
    float value = int(random(100));
    fill(c, value);
    ellipse(x, y, int(random(5, 30)), int(random(5, 30)));
  }
}
