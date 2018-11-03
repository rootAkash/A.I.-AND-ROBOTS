import numpy as np
import random
import time
import math
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
import serial
from collections import deque

######################################################################

ser = serial.Serial('COM3',115200,timeout=None)
ser2 = serial.Serial('COM8',115200,timeout=None)
time.sleep(.1)
#ser.reset_input_buffer()
#ser2.reset_output_buffer()
#while 1:
 #try:
  #print ser.readline()
  #time.sleep(1)
 #except ser.SerialTimeoutException:
  #print('Data could not be read')
  #time.sleep(1)

#########        angle measurement     #################################
########################################################################
def abs(a):
    if(a[0][0]>0):
        return a
    else:
        b=-a[0][0]
        b=[[b]]  
        return b
class DQN:
    def __init__(self):
        
        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = .125

        self.model        = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        model   = Sequential()
        state_shape  = 1
        model.add(Dense(4, input_dim=state_shape, activation="relu"))
        model.add(Dense(4, activation="relu"))
        model.add(Dense(4))
        model.compile(loss="mean_squared_error",
            optimizer=Adam(lr=0.001))
        return model

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            print('random')
            return random.randint(0,3)
        return np.argmax(self.model.predict(state)[0])
    
    def compute_done(self,angle):
        if (abs(angle)>[[40.0]]):
            return True
                        
    def replay(self,state, action, new_state, done):

        
            target = self.target_model.predict(state)
            #print(target)
            if (done):
                target[0][action] = -5   
            elif(abs(state)<[[2.0]]): 
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = 15 + Q_future * self.gamma
            else: 
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = -1 + Q_future * self.gamma
            
            self.model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

def main():
    gamma   = 0.9
    epsilon = .95

    trials  = 1000000
    trial_len = 50000

    # updateTargetNetwork = 1000
    dqn_agent = DQN()
    for trial in range(trials):
        #ser.reset_input_buffer()
        #ser2.reset_output_buffer()
        if(ser.inWaiting()>0):
            ser.reset_input_buffer()
            ser_bytes = ser.readline()
            print('in')
        else:
            ser.reset_input_buffer()
            ser_bytes = ser.readline()  
        try:
            cur_state = float(ser_bytes[0:len(ser_bytes)-1].decode("utf-8","replace"))#angle as list
        except:
            cur_state=10;
        print("cur state"+str(cur_state))
        cur_state=[[cur_state]]        
        # list in a list
        done=False
        for _ in range(trial_len):
            done=False
            action = dqn_agent.act(cur_state)
            ser.reset_input_buffer()
            ser_bytes = ser.readline()
            try:
                new_state = float(ser_bytes[0:len(ser_bytes)-1].decode("utf-8","replace"))
            except:
                new_state=10
            new_state=[[new_state]]
            print("action :- "+str(action)+"  new state :- "+str(new_state))# angle as list 
            done= dqn_agent.compute_done(new_state)           
            if(int(action)==1):
                ser2.reset_output_buffer()
                ser2.write(b'2')
            elif(int(action)==2):
                ser2.reset_output_buffer()
                ser2.write(b'1')
            elif(int(action)==3):
                ser2.reset_output_buffer()
                ser2.write(b'3')
            else:
                ser2.reset_output_buffer()
                ser2.write(b'4')
                  
            #dqn_agent.remember(cur_state, action, new_state, done)
                   # internally iterates default (prediction) model
             # iterates target model
            dqn_agent.replay(cur_state, action, new_state, done)
            dqn_agent.target_train()
            cur_state = new_state
            #time.sleep(.1)
            if done:    
              #  dqn_agent.random_action(action)
                ser2.reset_output_buffer()
                ser2.write(b'0')
                time.sleep(2)
                print("action above 20")
                break
        print("episode no  :- "+ str(trial)) 
    
    
 
if __name__ == '__main__':
    main()
