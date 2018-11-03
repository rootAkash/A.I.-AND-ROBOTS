int data;

void setup() { 
  Serial.begin(115200); //initialize serial COM at 9600 baudrate
  pinMode(10, OUTPUT);
//make the LED pin (13) as output
  
  
  Serial.println("Hi!, I am Arduino");
}
 
void loop() {
while (Serial.available()){
  data = Serial.read();
}

if (data == '1')
{
  analogWrite(11,255);
digitalWrite (10,HIGH);
}
else if (data == '2')
{
analogWrite(11,255);
digitalWrite (10,LOW);
}
else if (data == '0')
{
  analogWrite(11,0);
}
else if (data == '3')
{
analogWrite(11,120);
digitalWrite (10,LOW);
}
else if (data == '4')
{
analogWrite(11,120);
digitalWrite (10,HIGH);
}

}


