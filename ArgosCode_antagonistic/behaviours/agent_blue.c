/*-----------------------------------------------------------------------------------------------*/
/* This file gives a template of what functions need to be implemented for Kilobot in order to   */
/* work on the Kilogrid.                                                                         */
/*-----------------------------------------------------------------------------------------------*/

// macro if we are in sim or reality -> command out if on real robot
#define SIMULATION


/*-----------------------------------------------------------------------------------------------*/
/* Imports - depending on the platform one has different imports                                 */
/*-----------------------------------------------------------------------------------------------*/

#include "kilolib.h"
#include <kilolib.h>

#ifdef SIMULATION

#include <stdio.h>
#include <float.h>
#include <math.h>
#include "agent.h"
#include <debug.h>


#else

#include "utils.h"  // TODO check if this is needed ?!?
#include "kilob_tracking.h"
#include "kilo_rand_lib.h"
#include "../communication.h"
#include "kilob_messaging.h"
#include <math.h>

#endif


/*-----------------------------------------------------------------------------------------------*/
/* Define section here you can define values, e.g., messages types                               */
/*-----------------------------------------------------------------------------------------------*/
// options
#define UNCOMMITTED 0
// message types
#define FROMBOT 9
#define INIT_MSG 10  // initial message from the kilogrid
#define GRID_MSG 11  // info msg from the kilogrid with option and position
#define VIRTUAL_AGENT_MSG 12  // msg forwarded from the kilogrid
#define TO_KILOGRID_MSG 62




#define SWARMSIZE 50

#define MODEL 0 // 0 --> Voter Model      1 --> CrossInhibition

double noise = 0.9; // SET THIS TO -1 FOR NO NOISE 


//opinion = A -->1   //opinion = B --> 2  //uncommited = C --> 3
int currentopinion = 2; //1

/*-----------------------------------------------------------------------------------------------*/
/* Enum section - here we can define useful enums                                                */
/*-----------------------------------------------------------------------------------------------*/
typedef enum{
    false = 0,
    true = 1,
} bool;

/* Enum for different motion types */
typedef enum {
	STOP = 0,
	FORWARD,
	TURN_LEFT,
	TURN_RIGHT,
} motion_t;

motion_t current_motion_type = STOP;

//bool broadcast_msg = false;
int received_option;
int received_uid;
unsigned int turning_ticks = 0;
const uint8_t max_turning_ticks = 150; //*** constant to set maximum rotation to turn during random walk 
const uint32_t max_straight_ticks = 300; //*** set the time to walk straight beofre randomnly turning
//const uint32_t broadcast_ticks = 32;
uint32_t last_motion_ticks = 0;


/*-----------------------------------------------------------------------------------------------*/
/* Robot state variables.                                                                        */
/*-----------------------------------------------------------------------------------------------*/
uint8_t robot_gps_x;  // current x position
uint8_t robot_gps_y;  // current y position

uint8_t my_commitment = 0;  // This is the initial commitment
float my_commitment_quality = 0.0;

uint8_t communication_range = 0;  // communication range in cells


int last_changed = 0;

message_t message;

// Flag to keep track of new messages.
int new_message = 0;
message_t received;
int distance;
// Flag to keep track of message transmission.
int last_changed;
//bool calibrated = false;

int message_sent = 0;

int neighbourid[SWARMSIZE] = {};//***change the size if running with more than 25 kilobots--> mention no of robots used in size
int neighbouropinion[SWARMSIZE] = {}; //right now voter *** k->5, change to vary according to the majority rule


//sets the qratios, 6/3=2, change values to vary
   //  double q3 = 0.003;//***
    // double q1 = 0.006;//***
double timer; // to hold time to be in each state 
double q3 = 0.003;//***qualities are same for A and B for now
double q1 = 0.003;//***qualities are same for A and B for now
double qnorm = 0.001; //***--> time to be in latent state


//int checknum = 2;
//int checkother = 1;
//int checkloop = 0;

int state = 0; //0--> ND, 1-->D, 2-->Voting // start in exploration state 


/*-----------------------------------------------------------------------------------------------*/
/* Communication variables - used for communication and stuff                                    */
/*-----------------------------------------------------------------------------------------------*/
// how often we try to send the msg - in simulation once is sufficient
#ifdef SIMULATION
#define MSG_SEND_TRIES 1
#else
#define MSG_SEND_TRIES 10
#endif
// Kilobot -> Kilogrid
uint32_t msg_counter_sent = MSG_SEND_TRIES + 1;  // counts the messages sent
uint32_t msg_number_send = 0;  // change if you want to send a msg
uint32_t msg_number_current_send = 0;  // var for checking against the last
// Kilogrid -> Kilobot
bool init_flag = false;
bool received_grid_msg_flag = false;
bool received_virtual_agent_msg_flag = false;
// message content
#ifdef SIMULATION
bool broadcast_msg = false;
uint8_t communication_range_msg = 0;
uint8_t x_pos_msg = 0;
uint8_t y_pos_msg = 0;
uint32_t msg_counter = 0;

#else
IR_message_t* message;
#endif


/*-----------------------------------------------------------------------------------------------*/
/* Arena variables                                                                               */
/*-----------------------------------------------------------------------------------------------*/
uint8_t NUMBER_OF_OPTIONS = 0;
uint8_t current_ground = 0;

void set_motion( motion_t new_motion_type ) {
	if( current_motion_type != new_motion_type ){
	
		switch( new_motion_type ) {
		case FORWARD:
			spinup_motors();
			set_motors(kilo_straight_left,kilo_straight_right);
			break;
		case TURN_LEFT:
			spinup_motors();
			set_motors(kilo_turn_left,0);
			break;
		case TURN_RIGHT:
			spinup_motors();
			set_motors(0,kilo_turn_right);
			break;
		case STOP:
            set_motors(0,0);
            break;
		}
		current_motion_type = new_motion_type;
	}
}

void random_walk(){
   switch( current_motion_type ) {
   case TURN_LEFT:
   case TURN_RIGHT:
      if(  kilo_ticks > last_motion_ticks + turning_ticks ) {
         /* start moving forward */
         last_motion_ticks = kilo_ticks;
         set_motion(FORWARD);
      }
      break;
   case FORWARD:
   	   //spinup_motors();
	   //set_motors(20,20);
      if( kilo_ticks > last_motion_ticks + max_straight_ticks ) {
         /* perform a radnom turn */
         last_motion_ticks = kilo_ticks;
         if( rand()%2 ) {
            set_motion(TURN_LEFT);
            current_motion_type = TURN_LEFT;
         }
         else {
            set_motion(TURN_RIGHT);
            current_motion_type = TURN_RIGHT;
         }
         turning_ticks = rand()%max_turning_ticks + 1;
      }
      break;
    case STOP:
         set_motion(STOP);
    default:
        set_motion(FORWARD);
   }
}

/* FUNCTIONS FOR THE EXPERIMENT-----------------------------------------------------------------------------------------------*/
double ran_expo(double lambda){
    double u;
    u = rand() / (RAND_MAX + 0.05);
    return -log(1- u) / lambda;
}

double r2()
{
    return (double)rand() / (double)RAND_MAX ;
}

int countOccurrences(int arr[], int n, int x) 
{ 
    int res = 0; 
    for (int i=0; i<n; i++) 
        if (x == arr[i]) 
          res++; 
    return res; 
} 

int find_index(int a[], int num_elements, int value)
{
   int ii;
   for (ii=0; ii<num_elements; ii++)
   {
	 if (a[ii] == value)
	 {
	    return(value);  /* it was found */
	 }
   }
   return(-1);  /* if it was not found */
}


void gotoexploration(){
    
        random_walk();
        if (currentopinion == 1){
            set_color(RGB(1, 0, 0));

        } else if (currentopinion == 2){
            set_color(RGB(0, 1, 1));

        }else{
            set_color(RGB(1, 1, 0)); //uncomitted

        }


         if ((kilo_ticks - last_changed) < timer) {//check if still in latent mode or not
         } else{
             
            state = 1;//got to Dissemination mode
            if (currentopinion == 1){
                timer =  ran_expo(q3); //time for dissem if opinionA
            }else{
                 timer =  ran_expo(q1);//time for dissem if opinionB
            }
            last_changed = kilo_ticks;
            // last_changed = 0;
            //kilo_ticks = 0;
           set_color(RGB(0, 0, 0));
           // set_color(RGB(0, 0, 0));
    
     } 
    
}


void donoisyswitch(){
            printf("opts for noisy switch noise fro kilgorid");

         if (MODEL == 1){ //if cross inhibition and noise switching
            
              int checkforAorBswitch = rand() % 2; // if 0 -->  switch to A ,  if 1 --> switch to B

              if(checkforAorBswitch == 0){ //A

                currentopinion = 1;

                set_color(RGB(1, 0, 0));

              }
              if(checkforAorBswitch == 1){ //B

                currentopinion = 2;
                set_color(RGB(0, 0, 1));

              }

            
        }
        
        
        if (MODEL == 0){ //if voter model and noise switching
        
           if(init_flag){  // initalization happend

                // run logic
                // process received msgs
                if (received_grid_msg_flag) {
                            //random_walk();
                    //update_grid_msg();
                    printf("changes commitment through noise fro kilgorid");
                    if(my_commitment == 1){
                        
                        currentopinion = my_commitment;
                        
                    } else if(my_commitment == 3){
                        
                        currentopinion = 2;
                        
                    }
                    if (currentopinion == 1){
                        set_color(RGB(1, 0, 0));

                    } else if (currentopinion == 2){
                        set_color(RGB(0, 1, 1));

                    }
                    received_grid_msg_flag = false;
   
                }

                if (received_virtual_agent_msg_flag) {
                   // update_virtual_agent_msg();
                    received_virtual_agent_msg_flag = false;
                }

                // TODO add logic here ...
                // example robot sends empty message to the kilogrid
            //    msg_counter += 1;
           //     if(msg_counter > 30){
           //         msg_counter = 0;
            //        set_message();
              //  }

                // for sending messages
               // message_tx();
            }

        }
    message.data[1] = currentopinion;
    message.data[2] = kilo_uid;
    message.crc = message_crc(&message);
        
           
    
    
}


void gotodissemination(){

       random_walk();

       if ((kilo_ticks - last_changed) < timer) { //if within dessimnation time
           if(currentopinion != 3){
       		broadcast_msg = true;
               
           }else{
               
                   set_color(RGB(2, 2, 0));

           }

        }else{
           last_changed = kilo_ticks;
           state = 2;//got to voting state
       }
              random_walk();
    
    
    
}

/*-----------------------------------------------------------------------------------------------*/
/*-----------------------------------------------------------------------------------------------*/
/* Function to process the data received from the kilogrid regarding the environment             */
/*-----------------------------------------------------------------------------------------------*/
void update_grid_msg() {
    // TODO add logic here
   // set_color(RGB(2, 2, 0));
    delay(2000);
    set_color(RGB(0, 0, 0));

    return;
}


void vote(){
     int x = 0;
        
     //collect opinions from neighbours and their ids to ensure they vote once
     for(int i=0; i<450;i++){//*** increase i loop if more time in voting is required
         delay(5);
         if(x<=20){
          if (new_message == 1){
           new_message = 0;
           int index = find_index(neighbourid, SWARMSIZE, received_uid);//*** change according to array size
//           printf("index is %d",index);
           if (index == -1){//if neighbour has not already voted
            if (distance <= 200){//*** if distance less tahn 200
               neighbourid[x] = received_uid;//put id in array
                neighbouropinion[x] = received_option;//consider the opinion of neighbour and put in array
                x = x+1;
                delay(50);
	//            printf("%d",kilo_uid);
            }
           }
         }
        }
     }

 //neighbouropinion[8] = 2;
  //neighbouropinion[x] = currentopinion;//add own opinion to list of opinion
   //x = x+1;
   
       if(x>=1){ // if an opinion from a neighbouring robot was attained
           
        int check_for_no_val = 0;  

        for (int v = 0; v < SWARMSIZE; ++v){
            if(neighbouropinion[v] != 0) {
                check_for_no_val = check_for_no_val + 1;  //increment when an opinion is found
            }
        }
        
        //randonmly pick an opinion   
        int val_choose = (rand() % ((check_for_no_val-1) + 1 - 0)) + 0;
           
           
        if (MODEL == 1){ //if cross inhibition
           
                if(currentopinion != 3){ //if not uncommited

                      if (neighbouropinion[val_choose] != currentopinion){ //check if your opinion is not equal 
                           //go uncommited
                            currentopinion = 3;    
                            set_color(RGB(1, 1, 0));


                      }else{

                          currentopinion = neighbouropinion[val_choose];

                      }

                }else{

                  currentopinion = neighbouropinion[val_choose];



                }

            
        }
        if (MODEL == 0){ //switch randomly to an opinion
            
          currentopinion = neighbouropinion[val_choose];

        }
        
        message.data[1] = currentopinion;
        message.data[2] = kilo_uid;
        message.crc = message_crc(&message); 
     
           
           //if no neighbour found, stay with current opinion
       }else{
          //currentopinion = current_opinion;
          message.data[1] = currentopinion;
          message.data[2] = kilo_uid;
          message.crc = message_crc(&message);
           
           
       }

           //int occur = countOccurrences(neighbouropinion, 5, checknum);//*** change according to array size
           // int occur2 = countOccurrences(neighbouropinion, 5, checkother);

                
     //clear the neighbour arrays
     for (int n = 0; n < SWARMSIZE; ++n){
        neighbourid[n] = 0;        
     }
     for (int m = 0; m < SWARMSIZE; ++m){
        neighbouropinion[m] = 0;        
     }
            //go to exploration state
            state = 0;
            timer =  ran_expo(qnorm);
            last_changed = kilo_ticks;
            //kilo_ticks = 0;
            set_color(RGB(0, 0, 0));    
    
    
    
    
}



/*-----------------------------------------------------------------------------------------------*/
/* Function to process the data received from the kilogrid regarding other robots                */
/*-----------------------------------------------------------------------------------------------*/
void update_virtual_agent_msg() {
    // TODO add logic here
    return;
}


/*-----------------------------------------------------------------------------------------------*/
/* This function implements the callback, for when the robot receives an infrared message (here  */
/* only from the kilogrid)                                                                       */
/*-----------------------------------------------------------------------------------------------*/
// because there has been an "updated" version of the kilo_lib we have a slightly different
// implementation
#ifdef SIMULATION
void message_rx( message_t *msg, distance_measurement_t *d ) {
#else
void message_rx( IR_message_t *msg, distance_measurement_t *d ) {
#endif
    // check the messages
    // all data should be stored in temporary variables and then be written in the loop
    // in order to dont fuck up your calculations, because this function works like an interrupt!!
    if(msg->type == FROMBOT){
      
       // printf("hey i am a bot");
            // Set the flag on message reception.
        new_message = 1;
        distance = estimate_distance(d);
        received = *msg;
        received_option = msg->data[1];
        received_uid = msg->data[2];
    }
    if(msg->type == GRID_MSG){
      // printf("message received by bots\n");
       // printf("%hhu\n", msg->data[0]);
       // printf("%hhu\n",msg->data[1]);
       // printf("%hhu\n",msg->data[2]);
       // printf("%hhu\n",msg->data[3]);
        my_commitment = msg->data[2];
        received_grid_msg_flag = true;
    }
    if(msg->type == INIT_MSG && !init_flag){
        // TODO add logic ...
        // example usage
//        my_commitment = msg->data[0];
//        my_commitment_quality = msg->data[1];
//        NUMBER_OF_OPTIONS = msg->data[2];
//        option_to_sample = rand() % NUMBER_OF_OPTIONS;
//        current_ground = msg->data[3];
//        communication_range = msg->data[4];

        init_flag = true;
    }else if(msg->type == GRID_MSG && init_flag){
    // TODO add logic ...
        //received_grid_msg_flag = true;
    }else if(msg->type == VIRTUAL_AGENT_MSG  && init_flag){
    // TODO add logic ...
        //received_virtual_agent_msg_flag = true;
    }
    return;
}


/*-----------------------------------------------------------------------------------------------*/
/* This function implements the sending to the kilogrid. you should call this function every     */
/* loop cycle because in reality you dont have a indicator if the message was received so we     */
/* have to send it multiple times. The when and how often to send a message should be            */
/* implemented here!                                                                             */
/*-----------------------------------------------------------------------------------------------
void message_tx(){
    // implementation differs because in simulation we use the debugstruct - faster and easier to
    // understand
    // in reality we send infrared msg - we send more than one to make sure that the messages arrive!
    if (msg_number_current_send != msg_number_send){
        msg_number_current_send = msg_number_send;
        msg_counter_sent = 0;
    }
#ifdef SIMULATION
    // reset broadcast flag - needed in simulation to stop sending messages
    if(msg_counter_sent == MSG_SEND_TRIES){
        debug_info_set(broadcast_flag, 0);
        msg_counter_sent += 1;
    }
#endif
    // send msg if not sent enough yet
    if (msg_counter_sent < MSG_SEND_TRIES){
#ifdef SIMULATION
        // count messages
        msg_counter_sent += 1;
#else
        if((message = kilob_message_send()) != NULL) {
            msg_counter_sent += 1;

        }
#endif
    }
}
*/
void message_tx_success()
{
 broadcast_msg = false;
    if (currentopinion == 1){
            set_color(RGB(2, 0, 0));
            delay(10);
            set_color(RGB(0, 0, 0));
        } else if (currentopinion == 2){
            set_color(RGB(0, 2, 2));
            delay(10);
            set_color(RGB(0, 0, 0));
        }
    
}
message_t *message_tx()
{
    	if( broadcast_msg ) {
		return &message;
	}
	return 0;
}

/*-----------------------------------------------------------------------------------------------*/
/* Setting values of the message                                                                 */
/*-----------------------------------------------------------------------------------------------*/
void set_message(){
    // TODO this needs to be adjusted on what kind of messages you want to send: fill in data !
#ifdef SIMULATION
    msg_number_send += 1;
    debug_info_set(broadcast_flag, 1);
    debug_info_set(type, MSG_T_VIRTUAL_ROBOT_MSG);
    debug_info_set(data0, 1);
    debug_info_set(data1, 2);
    debug_info_set(data2, 3);
    debug_info_set(data3, 4);
    debug_info_set(data4, msg_number_send);
    debug_info_set(data5, 6);
    debug_info_set(data6, 7);
    debug_info_set(data7, 8);
#else
    // sample usage
    /*
    message->type = TO_KILOGRID_MSG;
    message->data[0] = my_commitment;
    message->data[1] = communication_range;
    message->data[2] = robot_gps_x;
    message->data[3] = robot_gps_y;
    message->data[4] = msg_number_current_send;
    */
#endif
}


/*-----------------------------------------------------------------------------------------------*/
/* Init function                                                                                 */
/*-----------------------------------------------------------------------------------------------*/
void setup(){
    
    
    srand(rand_hard());
    
    random_walk();

    //random timing for motion 
	last_motion_ticks = rand() % max_straight_ticks + 1;

    //save the current ticks for comparison later on
    last_changed = kilo_ticks;
    message.type = FROMBOT;
    // Quality A=1, B=2
    message.data[0] = currentopinion;
    //Opinion A=1 , B=2, U =3
    //red
    message.data[1] = currentopinion;
    message.data[2] = kilo_uid;
    message.crc = message_crc(&message);
    timer =  ran_expo(qnorm);
    
    
    
    //kilogrid variables
#ifndef SIMULATION
    // for tracking the robot in real life
    kilob_tracking_init();
    kilob_messaging_init();
    tracking_data.byte[0] = kilo_uid;
    tracking_data.byte[5] = 0;
#endif
    // Initialise motors
    //set_motors(0,0);

    // TODO add logic here ...

    // Intialize time to 0
    //kilo_ticks = 0;
}


/*-----------------------------------------------------------------------------------------------*/
/* Main loop                                                                                     */
/*-----------------------------------------------------------------------------------------------*/
void loop() {
    
         //////////STATE 0-Latent: Exploration//////////////////////
        if(init_flag){  // initalization happend
  //  printf("comes to init");

        // run logic
        // process received msgs
        if (received_grid_msg_flag) {
                    //random_walk();
            //update_grid_msg();
            received_grid_msg_flag = false;
        }

        if (received_virtual_agent_msg_flag) {
            update_virtual_agent_msg();
            received_virtual_agent_msg_flag = false;
        }

        // TODO add logic here ...
        // example robot sends empty message to the kilogrid
    //    msg_counter += 1;
   //     if(msg_counter > 30){
   //         msg_counter = 0;
    //        set_message();
      //  }

        // for sending messages
       // message_tx();
    }else{
        // not initialized yet ... can be omitted just for better understanding
        // also you can do some debugging here
    }

    if (state == 0){
        
        gotoexploration();
        
    }
    
    
         //////////STATE 2-Voting//////////////////////

    if (state == 2){ 
        
        //get the random number 0-1
        double u = r2();
    
        
        if (u <= noise){ //switch to noise check
            set_color(RGB(0, 2, 0));
            delay(1000);
            
            //do switching
        
            donoisyswitch();

    } else{ //Go to Voting
            
        vote();
        
   
    }
    
    }
     //////////STATE 1-Dissemination//////////////////////
   if(state ==1 ){
       
       gotodissemination();

       
       
   }
    


    #ifdef SIMULATION
        // debug info - is now also important for the inter-robot communication, so do not delete
        debug_info_set(currentopinion, currentopinion);
    #else
        tracking_data.byte[1] = received_x;
        tracking_data.byte[2] = received_y;
        tracking_data.byte[3] = com_range;
        tracking_data.byte[4] = msg_number_current;
        kilob_tracking(&tracking_data);
    #endif
  }


/*-----------------------------------------------------------------------------------------------*/
/* Main function - obviously needs to be implemented by both platforms.                          */
/*-----------------------------------------------------------------------------------------------*/
int main(){
    // initialize the hardware of the robot
    kilo_init();
    // now initialize specific things only needed for one platform
#ifdef SIMULATION
    // create debug struct - mimics the communication with the kilogrid
    debug_info_create();
#else
    utils_init();
#endif
    // callback for received messages
    kilo_message_rx = message_rx;
    // start control loop
    
            // Register the message_tx callback function.
    kilo_message_tx = message_tx;
    // Register the message_tx_success callback function.
    kilo_message_tx_success = message_tx_success;
    kilo_start(setup, loop);
    return 0;
}