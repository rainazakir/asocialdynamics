/*-----------------------------------------------------------------------------------------------*/
/* This file provides functions need to be implemented for Kilobot in order to
work on the */ /* Kilogrid with self-sourced noise and social interaction*/
/*-----------------------------------------------------------------------------------------------*/

// macro if we are in sim or reality -> comment out if on real robot
//IMPORTANT
// #define SIMULATION


/*-----------------------------------------------------------------------------------------------*/
/* Imports - depending on the platform one has different imports         */
/*-----------------------------------------------------------------------------------------------*/
#include <kilolib.h>
#include <math.h>
#include <time.h>
#include "kilolib.h"
#include <stdlib.h>
#include <string.h>


#ifdef SIMULATION

#include <stdio.h>
#include <float.h>
#include "agent.h"
#include <debug.h>
#include <time.h>

#else

#include "utils.h" // TODO check if this is needed ?!?
#include <util/delay.h>   // delay macros
#include "kilob_tracking.h"
#include "kilo_rand_lib.h"
#include "../communication.h"
#include "kilob_messaging.h"

#endif

int8_t received_x = 0;
uint8_t received_y = 0;
uint8_t received_ground = 0;
uint8_t received_role = 0;
/*-----------------------------------------------------------------------------------------------*/
/* Define section here you can define values, e.g., messages types        */
/*-----------------------------------------------------------------------------------------------*/
// options
#define UNCOMMITTED 99 //opinion for uncommitted
// message types
#define FROMBOT 16 //the message is from robot and not kilogrid
#define INIT_MSG 11 // initial message from the kilogrid
#define GRID_MSG 11 // info msg from the kilogrid with option and position
#define VIRTUAL_AGENT_MSG 12 // msg forwarded from the kilogrid
// #define TO_KILOGRID_MSG 62
#define CALIBRATED true


#define min(a, b) ((a) < (b) ? a : b)
/*-----------------------------------------------------------------------------------------------*/
/* Change these when running experiment                                                          */
/*-----------------------------------------------------------------------------------------------*/
#define MODEL 1 // 0 --> Voter Model  1 --> CrossInhibition
double noise = 0.1; // SET THIS TO -1 FOR NO NOISE
int how_many_op = 2; //set the number of opinion in Kilogrid--> max is 4 for now
int prev_option;
int currentopinion; 
int pool = 0;
int record_it = 0;
int torecord_op_quality_estimation;
float qualityestimate;
double timer; 
double avg_exploration_time = 2800;   // time to be in exploration state--> fixed
double avg_uncommitted_time = 800;     // time to stay in dormant for uncommitted agents
double dissemparam = 1800; // time to stay in dissemination state for agents
double qualityb = 1;   //quality of inferior option(s)
/*-----------------------------------------------------------------------------------------------*/

int foundmodules[18][38] = {0}; //to keep track of tiles visited in one exploration cycle
float qratio; //to store quality based ont the tiles explored
float qratio_scaled; //to store quality based ont the tiles explored


/* Wall Avoidance manouvers */
uint32_t wallAvoidanceCounter=0; // to decide when the robot is stuck...

/*-----------------------------------------------------------------------------------------------*/
/* Enum section - here we can define useful enums            */
/*-----------------------------------------------------------------------------------------------*/
/* Enum for true/false flags */

typedef enum {
       false = 0,
       true = 1,
} bool;

/* Enum for different motion types */
typedef enum {
       STOP_N = 0,
       FORWARD_N,
       TURN_LEFT_N,
       TURN_RIGHT_N,
} motion_t;

/* Enum for different states*/
typedef enum {
       EXPLORATION,
       DISSEMINATION,
       POLL_OR_READ_GROUND,
} state;

/* Enum for different wall function states */
typedef enum {
       TURN_TO_AVOID_WALL,
       STRAIGHT_TO_AVOID_WALL,
       COMPLETE_WALL_AVOIDANCE,
} wall_state;
/*-----------------------------------------------------------------------------------------------*/
state current_state = EXPLORATION; //start robot sin exploration state
int c_s = 0;
int neighbour_op_rec = 0;
wall_state wall_function_state = TURN_TO_AVOID_WALL;
/*-----------------------------------------------------------------------------------------------*/
/* Motion related Variables                                                                      */
/*-----------------------------------------------------------------------------------------------*/
motion_t current_motion_type = STOP_N;
unsigned int turning_ticks = 0;
const uint8_t max_turning_ticks = 100; // constant to set maximum rotation to turn during random walk
const uint32_t max_straight_ticks = 380; // set the time to walk straight before randomly turning
const uint8_t max_wall_avoidance_turning_ticks = 130;
const uint32_t max_wall_avoidance_straight_ticks = 380;
uint32_t last_motion_ticks = 0;
uint32_t last_motion_wall_ticks = 0;

uint8_t kilogrid_commitment = 0; // This is the initial commitment attained from kilogrid
int last_changed = 0;
bool wall_avoidance_turning = false;
bool wall_avoidance_straight = false;
int op_record;


/*-----------------------------------------------------------------------------------------------*/
/* Communication variables - used for communication and stuff                                    */
/*-----------------------------------------------------------------------------------------------*/
bool broadcast_msg = false;
//message_t message;
// how often we try to send the msg - in simulation once is sufficient
#ifdef SIMULATION
#define MSG_SEND_TRIES 1
#else
#define MSG_SEND_TRIES 10
#endif
// Kilobot -> Kilogrid
uint32_t msg_counter_sent = MSG_SEND_TRIES + 1; // counts the messages sent
uint32_t msg_number_send = 0; // change if you want to send a msg
uint32_t msg_number_current_send = 0; // var for checking against the last
// Kilogrid -> Kilobot
bool init_flag = false;
bool received_grid_msg_flag = false;
bool received_virtual_agent_msg_flag = false;

// message content
#ifdef SIMULATION

message_t message;

#else
IR_message_t message;
#endif

// Flag to keep track of new messages.
int new_message = 0;
int buffer_msg = 0;
int buffer_full = 0;

int last_changed;
// Flag to keep track of message transmission.
int message_sent = 0;

int received_option; //to save an opinion received from another bot
int buffer_op; //to save an opinion received from another bot
int buffer_uid; //to save an opinion received from another bot

int received_option_kilogrid; // to save option received from kilogrid
int received_uid; //previously used to save neighbours kilouid temporarily
int wall_flag; //to check if wall signal or not
/*-----------------------------------------------------------------------------------------------*/
/* Arena variables                                                                               */
/*-----------------------------------------------------------------------------------------------*/

bool hit_wall = false;
// set to true if wall detected
bool wall_avoidance_state = false;
//to keep track of tiles and quality
int total_tiles_found;
int tiles_of_my_option;
int option_received_from_neighbour;
tracking_user_data_t tracking_data;


/*-----------------------------------------------------------------------------------------------*/
/* Generate a random float number in specific range                            */
/*-----------------------------------------------------------------------------------------------*/
float RandomFloat(float min, float max) {
       return (max - min) * ((((float) rand()) / (float) RAND_MAX)) + min;
}

/*-----------------------------------------------------------------------------------------------*/
/* Retruns a random number in range_rnd.                             */
/*-----------------------------------------------------------------------------------------------*/
unsigned int GetRandomNumber(unsigned int range_rnd){
      int randomInt = RAND_MAX;
      while (randomInt > 30000){
            randomInt = rand();
          }
      unsigned int random = randomInt % range_rnd + 1;
      return random;
}


/*-----------------------------------------------------------------------------------------------*/
/* Setting the Motion of the Bot                 */
/*-----------------------------------------------------------------------------------------------*/
void set_motion(motion_t new_motion_type) {
       if (current_motion_type != new_motion_type) {

              spinup_motors();
              switch (new_motion_type) {
                     case FORWARD_N:
                           // spinup_motors();
                            if (CALIBRATED) set_motors(kilo_straight_left, kilo_straight_right);
                            break;
                           case TURN_LEFT_N:
                            if (CALIBRATED){

            uint8_t leftStrenght = kilo_turn_left + wallAvoidanceCounter;

                          set_motors(leftStrenght, 0);
                        } else{
                         set_motors(60, 0);

                        }
                            break;
                           case TURN_RIGHT_N:
                            if (CALIBRATED) {

            uint8_t rightStrenght = kilo_turn_right+ wallAvoidanceCounter;

                          set_motors(0, rightStrenght);
                        } else{
                         set_motors(0, 60);

                        }
                            break;
                           case STOP_N:
                            set_motors(0, 0);
                            break;
                         
                    }
              current_motion_type = new_motion_type;
            
          }
}

/*-----------------------------------------------------------------------------------------------*/
/* Random Walk                     */
/*-----------------------------------------------------------------------------------------------*/
void random_walk() {
       switch (current_motion_type) {
              case TURN_LEFT_N:
                  case TURN_RIGHT_N:
                     if (kilo_ticks > last_motion_ticks + turning_ticks) {
                /* start moving forward */
                last_motion_ticks = kilo_ticks;
                set_motion(FORWARD_N);
              
          }
                     break;
                    case FORWARD_N:
                     if (kilo_ticks > last_motion_ticks + max_straight_ticks + GetRandomNumber(50)) {
                /* perform a random turn */
                last_motion_ticks = kilo_ticks;
                if (rand() % 2) {
                       set_motion(TURN_LEFT_N);
                       current_motion_type = TURN_LEFT_N;

                     
                } else {
                       set_motion(TURN_RIGHT_N);
                       current_motion_type = TURN_RIGHT_N;

                     
                }
                turning_ticks = rand()%max_turning_ticks + 1;
              
          }
                     break;
                    case STOP_N:
                     set_motion(STOP_N);
                    default:
                     set_motion(FORWARD_N);
                  
              }
}
/*-----------------------------------------------------------------------------------------------*/
/* Function to check if the robot is against the wall            */
/*-----------------------------------------------------------------------------------------------*/
void wall_avoidance_function() {
      // set_color(RGB(3, 0, 3));

       wall_avoidance_state = true;
       hit_wall = false;

       if (wall_function_state == TURN_TO_AVOID_WALL) {
              if (rand() % 2) {
                     /* perform a random turn */
                     set_motion(TURN_LEFT_N);
                     current_motion_type = TURN_LEFT_N;
                     // }
                   
                  } else {
                     /* perform a random turn */
                     set_motion(TURN_RIGHT_N);
                     current_motion_type = TURN_RIGHT_N;
                   
                  }
              last_motion_wall_ticks = kilo_ticks;
              wall_function_state = STRAIGHT_TO_AVOID_WALL;
            
          }
       if (wall_function_state == STRAIGHT_TO_AVOID_WALL) {

              if ((kilo_ticks - last_motion_wall_ticks) > max_wall_avoidance_turning_ticks) {
                     /* start moving forward */
                     last_motion_wall_ticks = kilo_ticks;
                     set_motion(FORWARD_N);
                     wall_function_state = COMPLETE_WALL_AVOIDANCE;

                   
                }
            
          }
       if (wall_function_state == COMPLETE_WALL_AVOIDANCE) {
              if ((kilo_ticks - last_motion_wall_ticks) > max_wall_avoidance_straight_ticks) {
                     last_motion_wall_ticks = kilo_ticks;
                     wall_function_state = TURN_TO_AVOID_WALL;
                     wall_avoidance_state = false;
                   
                }
            
          }

}


/*-----------------------------------------------------------------------------------------------*/
/* Function to get Exponential Distribution for timing to stay is Dissem state                   */
/*-----------------------------------------------------------------------------------------------*/
double ran_expo(double lambda) {
       double u;
       u = rand() / (RAND_MAX + 1.0);
       return -log(1 - u) / lambda;
}

/*-----------------------------------------------------------------------------------------------*/
/* Function to get a random 1 or 0 to check for self-sourced noise or social interaction         */
/*-----------------------------------------------------------------------------------------------*/
double r2() {
       return (double) rand() / (double) RAND_MAX;
}

/*-----------------------------------------------------------------------------------------------*/
/* DEPRECATED, not used: This function is used to count the number of occurrences for   */
/*    each opinion if majority model is used           */
/*-----------------------------------------------------------------------------------------------*/
/*
int countOccurrences(int arr[], int n, int x)
{
 int res = 0;
 for (int i=0; i<n; i++)
  if (x == arr[i])
  res++;
 return res;
}
*/


/*-----------------------------------------------------------------------------------------------*/
/* DEPRECATED, not used: This function is used to check if a received uid from kilobot is  */
/* already present in the neighbour array. If present that means the kilobot has already voted */
/*-----------------------------------------------------------------------------------------------*/

/*
int find_index(int a[], int num_elements, int value)
{
int ii;
for (ii=0; ii<num_elements; ii++)
{
 if (a[ii] == value)
 {
  return(value); // it was found
 }
}
return(-1); //if it was not found
}
*/

/*-----------------------------------------------------------------------------------------------*/
/* This function is used to convert the tiles perceived in an expl-dissem cycle to quality  */
/* of its opinion. If q>=0.5, all qr is taken as 1. The function is inverse lambda expon.  */
/*-----------------------------------------------------------------------------------------------*/
/*
void findqualityratio(){

 qratio = ((float)tiles_of_my_option/total_tiles_found); //find % of tiles of opinion bot supports

 if(qratio >= 0.5){ //if % more than or equal to 0.5
  qratio = 1/(dissemparam); //like valentini model inverse lambda, 1300 instead of 1000 to increase dissem time

 }else{ //otherwise calculate dissem time based on % found 0-0.4999
  qratio = 1/(((float)tiles_of_my_option/total_tiles_found)*dissemparam); //like valentini model inverse lambda, 1300 instead of 1000 to increase dissem time

 }

 // qratio = 1/(((float)tiles_of_my_option/total_tiles_found)*1000); //like valentini model inverse lambda

 printf("%d tile my op %d total tiles and qr %f \n", tiles_of_my_option,total_tiles_found, qratio);

}
*/
/*-----------------------------------------------------------------------------------------------*/
/* This function is used to find the time to disseminate based on the output of qr from   */
/*      findqualityratio() function.           */
/*-----------------------------------------------------------------------------------------------*/
/*
void calculatedissemtime(){

 if (isnan(qratio) || isinf(qratio)){ //if quality was found to be 0
  if(MODEL == 1 && currentopinion == UNCOMMITTED){ //if cross-inhibition and if bot is uncommitted

    printf("comes to time of uncommitted agent in noisy switch \n");
    timer = ran_expo(quncommitted); //set time to be in dissem state but will not talk

  }else{ //if not uncommitted and tiles own opinion found to be = 0
   printf("% f goes directly to voting \n", qratio);
   timer = 0; //no time as will go directly to poll/noisy switch state
   //timer = ran_expo(0.003);
  }


 }else{ //if quality was not 0

  //printf("% f goes to random \n", qratio);
  timer = ran_expo(qratio); //get the time to disseminate based on quality
  //}
 }
}
*/


/*-----------------------------------------------------------------------------------------------*/
/* Compute quality op option from Kilogrid tiles incurred                                        */
/*-----------------------------------------------------------------------------------------------*/
void findqualityratio() {
       if (tiles_of_my_option > 0) {
              qratio = ((float) tiles_of_my_option / total_tiles_found);
            
          } else {
              qratio = 0;
            
          }
        qratio_scaled = qratio *100;


       torecord_op_quality_estimation = currentopinion;
       qualityestimate = qratio_scaled;
       record_it = 1;
       ////// printf("%d tile my op %d total tiles and qr %f \n", tiles_of_my_option,total_tiles_found, qratio);
}


/*-----------------------------------------------------------------------------------------------*/
/* This function is used to find the time to disseminate based on  output of quality estimate    */
/*      from findqualityratio() function.           */
/*-----------------------------------------------------------------------------------------------*/
void calculatedissemtime() {

       double lambda = 1.0;

       if (MODEL == 1 && currentopinion == UNCOMMITTED){ // if MODEL is cross-inhibition and bot is uncommitted

              lambda = 1.0 / (0.50 * avg_uncommitted_time); //set time to be in dissem state but will not talk
            
          } else {
              lambda = 1.0 / (qratio * dissemparam);
            
          }

       timer = ran_expo(lambda);

       // printf("cop is %d timer is %f and lambda is %f \n", currentopinion, timer, lambda);


}
/*-----------------------------------------------------------------------------------------------*/
/*        The Exploration function           */
/*                        */
/*-----------------------------------------------------------------------------------------------*/
void gotoexploration() {
       //set led colours
       if (currentopinion == 1) {
              set_color(RGB(1, 0, 0));//RED

            
          } else if (currentopinion == 2) {
              set_color(RGB(0, 0, 1)); //Cyan

            
          } else if (currentopinion == UNCOMMITTED) {
              set_color(RGB(0,1, 0)); //GREEN

            
          }else {
              set_color(RGB(1, 1, 0)); //YELLOW

            
          }

       //if time for exploration not over yet, do nothing else move on to dissemination state
       if ((kilo_ticks - last_changed) < timer) {//check if still within time for exploration state or not

              if (currentopinion == UNCOMMITTED) {
                          set_color(RGB(0, 3, 0 ));   
                }
            
          } else { //if not in exploration state

             // findqualityratio(); //find quality of own opinion based on tiles incurred in the exploration cycle (if no bias)

              calculatedissemtime(); //calculate the time that the bot should be disseminating based on quality found

              last_changed = kilo_ticks;
              current_state = DISSEMINATION;//go to Dissemination mode

              //reset the variable that are used to find the qr for next exploration-dissem cycle
           memset(foundmodules, 0, sizeof(foundmodules[0][0]) * 18 * 38);

            
          }

}

/*-----------------------------------------------------------------------------------------------*/
/*   The Noisy switch function- self sourcing noise from Kilogrid      */
/*-----------------------------------------------------------------------------------------------*/

void donoisyswitch() {


   if (init_flag) {
    // initalization happened from Kilogrid
      // run logic
      // process received msgs
      if (received_grid_msg_flag) { //if received message from kilogrid


         if (kilogrid_commitment == 1) {
          //if it option A- red recived from Kilogrid (1 for a normal red tile and 6 for border red tile)

            currentopinion = 1; //change opinion to A- Red - 1
            qratio = 1;
            set_color(RGB(3, 0, 0));


          
      } else if (kilogrid_commitment == 2) {
        //if its option b- Blue received from Kilogrid (3 for a normal blue tile and 9 for border blue tile)

            currentopinion = 2; //change option to B- Blue - 2
            qratio = qualityb;
            set_color(RGB(0, 0, 3));


          
      } else if (kilogrid_commitment == 3) {
        //if its option b- Blue received from Kilogrid (3 for a normal blue tile and 9 for border blue tile)

            currentopinion = 3; //change option to G- Green - 3
             qratio = qualityb;
             set_color(RGB(0, 0, 1));


          
      } else if (kilogrid_commitment == 4) {
        //if its option b- Blue received from Kilogrid (3 for a normal blue tile and 9 for border blue tile)

            currentopinion = 4; //change option to B- Brown - 4
             qratio = qualityb;

             set_color(RGB(0, 1, 0));

          
      }


         received_grid_msg_flag = false; //set Kilogrid messaged received to False to get next

       
    }

      if (received_virtual_agent_msg_flag) { //this we are not using its when Kilobot does communciation
         // update_virtual_agent_msg();
         received_virtual_agent_msg_flag = false;
       
    }

    
  }





   //set parameters for sending message to other bots

    tracking_data.byte[1] = currentopinion;

   //computing exploration time
   if (currentopinion == UNCOMMITTED) {
      timer = ran_expo(1.0 / (0.5 * avg_uncommitted_time)); //get time for exploration
    
  }else {
      timer = ran_expo(1.0 / avg_exploration_time); //get time for exploration

    
  }
   current_state = EXPLORATION; //go to exploration state

   last_changed = kilo_ticks;


}

/*-----------------------------------------------------------------------------------------------*/
/*   The Dissemination Function               */
/*-----------------------------------------------------------------------------------------------*/
void gotodissemination() {

    
       if ((kilo_ticks - last_changed) < timer) { //if within dissemination time
               tracking_data.byte[0] = 9;

              if (currentopinion == UNCOMMITTED) {
                        set_color(RGB(0, 3, 0));//cyan

                   
                  } else if (currentopinion == 1) {
                  set_color(RGB(3, 0, 0));//Red
                  tracking_data.byte[1] = currentopinion;
                  kilob_tracking(&tracking_data);
                
                  } else if (currentopinion == 2) {
                  set_color(RGB(0, 0, 3)); //Blue
                  tracking_data.byte[1] = currentopinion;
                  kilob_tracking(&tracking_data);
                
                  }else{
                  set_color(RGB(3, 3,0)); //Yellow

                  }


            
          } else { //if time for dissem is over
              tracking_data.byte[0] = 0;

              last_changed = kilo_ticks;
              current_state = POLL_OR_READ_GROUND;//go to polling or noisy switch state
              //reset the variable that are used to find the qr for next exploration-dissem cycle
              tiles_of_my_option = 0;
              total_tiles_found = 0;

              set_color(RGB(0, 0, 0));//off color

}

/*-----------------------------------------------------------------------------------------------*/
/*-----------------------------------------------------------------------------------------------*/
/* NOT USED:Function to process the data received from the kilogrid regarding the environment */
/*-----------------------------------------------------------------------------------------------*/
/*
void update_grid_msg() {
 // TODO add logic here
// set_color(RGB(2, 2, 0));
// delay(2000);
 set_color(RGB(0, 0, 0));

 return;
}


*/

void statechange() {
      delay(500);

       if (MODEL == 1) { //if cross inhibition

              if (currentopinion != UNCOMMITTED) { //if I am not uncommited

                     if (option_received_from_neighbour != currentopinion) { //check if my opinion is not equal
                            //go uncommited

                            currentopinion = UNCOMMITTED;
                            set_color(RGB(0, 3, 0));

                          
                      } else {//same opinion received from neighbour, stay with my own opinion

                            currentopinion = option_received_from_neighbour;
                          
                      }

                   
                } else { //if I am uncommitted then get the opinion attained from neighbour

                     currentopinion = option_received_from_neighbour;


                   
                }



          }

    if (MODEL == 0){ //if voter model
        currentopinion = option_received_from_neighbour;// just switch the option to opinion received from neighbour

    }
      tracking_data.byte[1] = currentopinion;


}
/*-----------------------------------------------------------------------------------------------*/
/*       The Polling Function- Social interaction        */
/*-----------------------------------------------------------------------------------------------*/
void poll() {

        if (new_message == 1 && (received_option == 1 || received_option == 2)) { //if bot seems to be getting a message from neighbour

              op_record = currentopinion;
              neighbour_op_rec = received_option;
              pool = 1;
              new_message = 0; //set message received flag to 0-not received

               option_received_from_neighbour = received_option; //consider the opinion of a message received from neighbour and save it
              statechange();

            
            } else if (buffer_msg == 1 && (buffer_op == 1 || buffer_op == 2)) {

              op_record = currentopinion;
              neighbour_op_rec = buffer_op;

              option_received_from_neighbour = buffer_op; //consider the opinion of a message received from neighbour and save it
              buffer_msg = 0;

              statechange();

            
          } else {

             tracking_data.byte[1] = currentopinion;

            
          }


       //go to exploration state
       if (currentopinion == 1) {
              set_color(RGB(1, 0, 0));//red
              // qratio = 0.5;
               qratio = 1;

            
          } else if (currentopinion == 2) {
              set_color(RGB(0, 0, 1));//blue
              // qratio = 1;
           qratio = qualityb;

            
          } else if (currentopinion == UNCOMMITTED) {
                  set_color(RGB(0, 3, 0));//green

                     
              } else{

                set_color(RGB(3, 3, 0)); //Yellow
           qratio = qualityb;

              }


       current_state = EXPLORATION;

       if (currentopinion == UNCOMMITTED) {
n
              timer = ran_expo(1.0 / (0.5 * avg_uncommitted_time)); //get time for exploration

            
          } else {
              option_received_from_neighbour = 0;

              timer = ran_expo(1.0 / avg_exploration_time); //get time for exploration

            
          }
       last_changed = kilo_ticks;


}




/*-----------------------------------------------------------------------------------------------*/
/* This function implements the callback, for when the robot receives an infrared message (here */
/* also from the kilogrid and from other robots)             */
/*-----------------------------------------------------------------------------------------------*/
// because there has been an "updated" version of the kilo_lib we have a slightly different
// implementation
#ifdef SIMULATION

void message_rx(message_t *msg, distance_measurement_t *d) {
#else


void message_rx(IR_message_t *msg, distance_measurement_t *d) {
#endif
       // check the messages

       if (msg->type == FROMBOT && msg->data[0] == 9) { //if message from another bot




                  set_color(RGB(3, 0, 3));//magenta
                  delay(10);
                  set_color(RGB(0, 0, 0));

              if(msg->data[1] == 1 || msg->data[1] == 2){
                    new_message = 1;  // Set the flag on message reception.

                    if (buffer_full == 0) {
                         received_option = msg->data[1]; //get its option
                         received_uid = msg->data[2]; //get its uid
                         buffer_full = 1;
                       
                        } else {

                         if (msg->data[2] != received_uid) {

                                buffer_msg = 1;

                                buffer_op = received_option; //get its option
                                buffer_uid = received_uid; //get its option

                                received_option = msg->data[1]; //get its option
                                received_uid = msg->data[2]; //get its uid
                                buffer_full = 0;
                              
                            }

                       
                      }
                }

            
          }
       if (msg->type == GRID_MSG) { //if message from Kiogrid
              //printf("message from grid\n");
              //printf("%hhu\n", msg->data[0]);
              //printf("%hhu\n",msg->data[1]);
              //printf("%hhu\n",msg->data[2]);
              //printf("%hhu cell role\n",msg->data[3]);

              received_option_kilogrid = msg->data[2];// get the opinion of the tile
              wall_flag = msg->data[3];// if wall then 42, if near wall 62 else 0

              received_grid_msg_flag = true; //set the flag that message received from Kilogrid to true


              if (current_state == EXPLORATION) { //if the bot is in exploration state
                     if (received_option_kilogrid != 0) { //if the the bot is not on the wall-white border
                            if (foundmodules[msg->data[0]][msg->data[1]] == 0) { //if tile not counted previously

                                   foundmodules[msg->data[0]][msg->data[1]] = 1; //set the flag that tile has been counted now
                                   total_tiles_found += 1;
                                   if ((received_option_kilogrid == 1) &&
                                    currentopinion == 1) { //if I am Red and I receive red from kilogrid
                                          tiles_of_my_option += 1;

                                        
                                  } else if ((received_option_kilogrid == 2) &&
                                     currentopinion ==
                                             2) { //if I am blue and I receive blue from Kilogrid
                                          tiles_of_my_option += 1;

                                        
                                  } else if ((received_option_kilogrid == 3) &&
                                     currentopinion ==
                                             3) { //if I am blue and I receive blue from Kilogrid
                                          tiles_of_my_option += 1;

                                        
                                  } else if ((received_option_kilogrid == 4) &&
                                     currentopinion ==
                                             4) { //if I am blue and I receive blue from Kilogrid
                                          tiles_of_my_option += 1;

                                        
                                  }
                                 
                              
                          }
                       
                    }

                  if (wall_flag == 62 || wall_flag == 42) {
                      // robot sensed wall or near wall
                         // printf("received hitwall option");
                         hit_wall = true; //-> set hit wall flag to true
                         /* Wall Avoidance manouvers */
                         if (wall_flag == 62) { //if near the border of wall and not on white wall

                                kilogrid_commitment = msg->data[2]; //still get the opinion from grid
                                //printf("gets commitments\n");

                              
                          }
                       
                    } else {
                         hit_wall = false; //not hitting the wall
                         //leftStrenght = kilo_turn_left;
                        // rightStrenght = kilo_turn_right;
                         kilogrid_commitment = msg->data[2]; //get the opinion from kilogrid
                       
                    }

                
              }
           if (msg->type == INIT_MSG && !init_flag) {


                  init_flag = true;
                
              } else if (msg->type == GRID_MSG && init_flag) {
                  // TODO add logic ...
                  //received_grid_msg_flag = true;
                
              } else if (msg->type == VIRTUAL_AGENT_MSG && init_flag) {
                  // TODO add logic ...
                  //received_virtual_agent_msg_flag = true;
                
              }
           return;
    }
}


/*-----------------------------------------------------------------------------------------------*/
/* NOT USED: This function implements the sending to the kilogrid. you should call this function */
/* everyloop cycle because in reality you dont have a indicator if the message was received so we*/
/* have to send it multiple times. The when and how often to send a message should be   */
/* implemented here!                    */
/*-----------------------------------------------------------------------------------------------
*/

void message_tx(){
      // implementation differs because in simulation we use the debugstruct - faster and easier to
      // understand
      // in reality we send infrared msg - we send more than one to make sure that the messages arrive!
     
}


void message_tx_success() { //if transmitted
    // / set_color(RGB(3, 0, 0));
     // delay(10);
     // set_color(RGB(0, 0, 0));
     // broadcast_msg = false; //set transmitted flag to false
      //set the colour
}
/*-----------------------------------------------------------------------------------------------*/
/* etting values of the message                 */
/*-----------------------------------------------------------------------------------------------*/
void set_message() {
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
 message->data[0] = kilogrid_commitment;
 message->data[1] = communication_range;
 message->data[2] = robot_gps_x;
 message->data[3] = robot_gps_y;
 message->data[4] = msg_number_current_send;
*/
#endif
}


/*-----------------------------------------------------------------------------------------------*/
/* Init function                     */
/*-----------------------------------------------------------------------------------------------*/
void setup() {

      // Initialise random seed
      uint8_t seed = rand_hard();
      rand_seed(seed);
      seed = rand_hard();
      srand(seed);

       // Initialise motors
       set_motors(0, 0);
      

       //random timing for motion
       last_motion_ticks = rand() % max_straight_ticks + 1;

       //save the current ticks for comparison later on
       last_changed = kilo_ticks;



        
       if (how_many_op == 2) {
              if (kilo_uid % 2 == 0) { //choose my opinion based on odd or even kilouid
                     currentopinion = 1;
                     set_color(RGB(1,0,0));//MAGENTA
                     //qratio = 1;
                   
                } else {
                     currentopinion = 2;
                     set_color(RGB(0,0,1));//CYAN
                     // qratio = 1;
                   
                }

            
          }

       tracking_data.byte[0] = 0;
       tracking_data.byte[1] = currentopinion;

       timer = ran_expo(1.0 / avg_exploration_time); //get time to be in exploration state



       //kilogrid variables
#ifndef SIMULATION
       // for tracking the robot in real life
       kilob_tracking_init();
       kilob_messaging_init();
      // tracking_data.byte[0] = kilo_uid;
       //tracking_data.byte[5] = 0;
#endif

}


/*-----------------------------------------------------------------------------------------------*/
/* Main loop                      */
/*-----------------------------------------------------------------------------------------------*/
void loop() {

       if (init_flag) {
            // initialization happened and messaged received from Kilogrid


              if (received_virtual_agent_msg_flag) {
                     // update_virtual_agent_msg();
                     received_virtual_agent_msg_flag = false;
                   
                }

            

             if (wall_avoidance_state || hit_wall) {

                    wallAvoidanceCounter=+2; // to decide when the robot is stuck...
            
                    wall_avoidance_function();
                  
                } else {
                  wallAvoidanceCounter=0;

                    random_walk();
                  
                }

             if (current_state == EXPLORATION) { // if state is set to 0


                    gotoexploration(); //go to exploration

                  
                }


             if (current_state == POLL_OR_READ_GROUND) {
                  // state is set to choose between Vote or Noise

                    //get the random number 0-1 to flip between self-sourced or social
                 double u = r2();

                 if (u <= noise){ //switch to noise check
                     set_color(RGB(2, 2, 0));

                     donoisyswitch(); //do noisy switch

                 } else{ //Go to Voting

                     poll();

                 }

                  
                }


             if (current_state == DISSEMINATION) { // state is set to 1- Dissem

                    gotodissemination(); //go to dissemination function



                  
                }

           
          } else {
              // set initia; opinion
              if (kilo_uid % 2 == 0) { //choose muy opinion based on odd or even kilouid
                     currentopinion = 1;
                     set_color(RGB(1,0,0));//MAGENTA
                     //qratio = 1;
                   
                } else {
                     currentopinion = 2;
                     set_color(RGB(0,0,1));//CYAN
                     // qratio = 1;
                   
                }
           
          }
#ifdef SIMULATION
// debug info - is now also important for the inter-robot communication, so do not delete
 debug_info_set(currentopinion, currentopinion);
 debug_info_set(qualityestimate, qualityestimate);
 debug_info_set(record_it, record_it);
 debug_info_set(torecord_op_quality_estimation, torecord_op_quality_estimation);



#else
       // tracking_data.byte[1] = currentopinion;
        tracking_data.byte[2] = kilo_uid;
        tracking_data.byte[3] = qualityestimate;
        tracking_data.byte[4] = received_option;
        tracking_data.byte[5] = received_uid;

        kilob_tracking(&tracking_data);

#endif
}


/*-----------------------------------------------------------------------------------------------*/
/* Main function - obviously needs to be implemented by both platforms.       */
/*-----------------------------------------------------------------------------------------------*/
int main() {
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
       //kilo_message_tx_success = message_tx_success;
       // Register the message_tx callback function.
      // kilo_message_tx = message_tx;
       // Register the message_tx_success callback function.
       kilo_message_tx_success = message_tx_success;
       kilo_start(setup, loop);
       return 0;
}
