/*ME 439.01 Group 3
Austin King, John Lepard, Derek Noreen, Daniel Paredes
Cal Poly Pomona*/
int sensor=0;//analog data from Hall sensor
boolean plusTurn=false;//Status of most recent check
long lastTime;//Time of most recent positive check
long curTime;
int counter=0;//#of checks since last poll
double deltat=0;//sum of all periods since last speed calculation
int dimmerPin=9;
int ledPin=7;
double power = 255;//current light power level (0-255)
double curSpeed=0;
double targetSpeed=0;
double kp=.3;
double ki=.0185;
double errNew=0;
double errOld=0;
double errSum=0;

void setup() {
  pinMode(dimmerPin,OUTPUT); 
  pinMode(ledPin,OUTPUT);
  Serial.begin(9600);// connect to the serial port
  Serial.print(0);//allow Python script to run
}
void loop () {
  if (Serial.available()){
    targetSpeed = Serial.read()*100;// read the next byte from the serial port
    //if (Serial.read() == 's'){ 
    //  targetSpeed = Serial.parseInt();// read the next integer from the serial port
      //Serial.flush();
    //}  
  }
  if (analogRead(A0)>20){//check if magnet present
    plusTurn=true;
    digitalWrite(ledPin,HIGH);
  }
  else if (plusTurn){//magnet not currently present but was in last check
    plusTurn=false;
    counter++;
    curTime=micros();//# of microseconds since program start
    deltat=(curTime-lastTime)*.000001;//convert from microseconds to seconds
    lastTime=curTime;
    curSpeed=60.0/deltat;//convert period to RPM
    errNew=targetSpeed-curSpeed;
    errSum=errSum+(errOld+errNew)*deltat*.5;//Integral of error*dt by trapezoidal Riemann sum
    power=kp*errNew+ki*errSum;
    errOld=errNew;
    if (power>255){power=255;}//Fitting power level into allowable range
    else if (power<0){power=0;}
    analogWrite(dimmerPin,int(power));
    digitalWrite(ledPin,LOW);
    counter=0;
    Serial.println(int(curSpeed));//send latest speed to serial port 
    Serial.flush();
  }
}
