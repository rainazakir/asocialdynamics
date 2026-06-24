//
// Created by Till Konrad Aust on 17.12.21.
//
// in case of simulation set flag
#define SIMULATION
#define MIN_TIME_BETWEEN_MSG 1

#include "kilogrid_stub.h"

/*-----------------------------------------------------------------------------------------------*/
/* Initialization of the Loopfunctions.                                                          */
/*-----------------------------------------------------------------------------------------------*/
CKilogrid::CKilogrid():
CLoopFunctions() {}

CKilogrid::~CKilogrid() {}



/*-----------------------------------------------------------------------------------------------*/
/* Init method runs before every experiment starts.                                              */
/*-----------------------------------------------------------------------------------------------*/
void CKilogrid::Init(TConfigurationNode &t_tree) {
    // random tool for selecting messages and more
    m_pcRNG = CRandom::CreateRNG("argos");

    // get all Kilobots
    get_kilobots_entities();

    // get the debug info structs aka communication with the Kilogrid
    GetDebugInfo();

    // read configuration - map and parameters
    read_configuration(t_tree);
    // run the setup message of the Kilogrid
    for(int x_it = 0; x_it < 10; x_it++){
        for(int y_it = 0; y_it < 20; y_it++){
            setup(x_it, y_it);
        }
    }

    // initialize some helpers to track the kilobots - only needed in sim
    robot_positions.resize(kilobot_entities.size());

    // TODO setup logging
       Reset();
    TConfigurationNode& tExperimentVariablesNode = GetNode(t_tree,"variables");
    
        /* Get the output datafile name and open it */
    GetNodeAttribute(tExperimentVariablesNode, "datafilename", m_strOutputFileName);
    GetNodeAttribute(tExperimentVariablesNode, "datafilename2", m_strOutputFileName2 );
    GetNodeAttribute(tExperimentVariablesNode, "datafilename3", m_strOutputFileName3 );
    GetNodeAttribute(tExperimentVariablesNode, "datafilename4", m_strOutputFileName4 );
    GetNodeAttribute(tExperimentVariablesNode, "datafilename5", m_strOutputFileName5 );


    // Open a log file
    m_cOutput.open(m_strOutputFileName, std::ios_base::trunc | std::ios_base::out);
    m_cOutput2.open(m_strOutputFileName2, std::ios_base::trunc | std::ios_base::out);
    m_cOutput3.open(m_strOutputFileName3, std::ios_base::trunc | std::ios_base::out);
    m_cOutput4.open(m_strOutputFileName4, std::ios_base::trunc | std::ios_base::out);
    m_cOutput5.open(m_strOutputFileName5, std::ios_base::trunc | std::ios_base::out);

    // write the log file header (it is not mendatory)
    m_cOutput << "time;";

}

/*-----------------------------------------------------------------------------------------------*/
/* Gets called when the experiment is resetted.                                                  */
/*-----------------------------------------------------------------------------------------------*/
void CKilogrid::Reset() {
    // TODO implement what should happen when the simulation gets reset
}


/*-----------------------------------------------------------------------------------------------*/
/* Gets called when the experiment ended.                                                        */
/*-----------------------------------------------------------------------------------------------*/
void CKilogrid::Destroy() {
    // TODO implement what should happen if simulation quits

}


/*-----------------------------------------------------------------------------------------------*/
/* Gets called before every simulation step.                                                     */
/*-----------------------------------------------------------------------------------------------*/
void CKilogrid::PreStep(){
    // collect all the data from the robots - and virtualize them
    if(GetSpace().GetSimulationClock() == 15000){
        for(UInt16 it = 0; it < kilobot_entities.size(); it++) {
            robot_positions[GetKilobotId(*kilobot_entities[it])] = position2cell(GetKilobotPosition(*kilobot_entities[it]));
            //int module_x = GetKilobotPosition(*kilobot_entities[it]).GetX() * 10;
            //int module_y = GetKilobotPosition(*kilobot_entities[it]).GetY() * 10;
            Real module_x = (*kilobot_entities[it]).GetEmbodiedEntity().GetOriginAnchor().Position.GetX();
            Real module_y = (*kilobot_entities[it]).GetEmbodiedEntity().GetOriginAnchor().Position.GetY();
            if (debug_info_kilobots[it]->currentopinion == 99){
                m_cOutput3 << GetSpace().GetSimulationClock() << " " <<debug_info_kilobots[it]->torecord_prev_opinion_before_uncomm <<"  " << GetKilobotId(*kilobot_entities[it]) << "    " << robot_positions[GetKilobotId(*kilobot_entities[it])] << " " << module_x << " " << module_y  <<std::endl;

            }else{
                m_cOutput3 << GetSpace().GetSimulationClock() << " " <<debug_info_kilobots[it]->currentopinion <<"  " << GetKilobotId(*kilobot_entities[it]) << "    " << robot_positions[GetKilobotId(*kilobot_entities[it])] << " " << module_x << " " << module_y  <<std::endl;

            }
            m_cOutput5 << GetSpace().GetSimulationClock() << " " <<debug_info_kilobots[it]->currentopinion <<"  " << GetKilobotId(*kilobot_entities[it]) << "    " << robot_positions[GetKilobotId(*kilobot_entities[it])] << " " << module_x << " " << module_y  <<std::endl;

        }


    }
    virtual_message_reception();

    // simulate IR message reception for each cell
    for(int x_it = 0; x_it < 10; x_it++){
        for(int y_it = 0; y_it < 20; y_it++){
            if(module_memory[x_it][y_it].robot_messages.size() > 0){
                // IMPORTANT: cellid, distance and crc error are not used in simulation: here they are
                // dummy values
                IR_rx(x_it, y_it, module_memory[x_it][y_it].robot_messages[m_pcRNG->Uniform(CRange<UInt32>(0,module_memory[x_it][y_it].robot_messages.size()))], cell_id[0], d, 0);
                module_memory[x_it][y_it].robot_messages.clear();
            }
        }
    }

    // simulate reception of can messages
    for(int x_it = 0; x_it < 10; x_it++){
        for(int y_it = 0; y_it < 20; y_it++){
            // if we have multiple messages at the same time select a random one
            if(module_memory[x_it][y_it].received_cell_messages.size() > 0){
                // shuffle and take first element (this way because we also consider case == 1)
                CAN_rx(x_it, y_it, &module_memory[x_it][y_it].received_cell_messages[m_pcRNG->Uniform(CRange<UInt32>(0,module_memory[x_it][y_it].received_cell_messages.size()))]);
                // clear list afterwards
                module_memory[x_it][y_it].received_cell_messages.clear();
            }
        }
    }

    // run the loop
    for(int x_it = 0; x_it < 10; x_it++){
        for(int y_it = 0; y_it < 20; y_it++){
            loop(x_it, y_it);
        }
    }
}


/*-----------------------------------------------------------------------------------------------*/
/* Gets called after every simulation step.                                                      */
/*-----------------------------------------------------------------------------------------------*/
void CKilogrid::PostStep(){
    // TODO implement what happens after the robots moved
       /* Go through the kilobots */
       int op1 = 0;
       int op2 = 0;
       int unc = 0;
       int dissemA = 0;
       int dissemB = 0;
       int dissemAr = 0;
       int dissemBr = 0;
    
   for (unsigned int i = 0; i < kilobot_entities.size(); i++) {
        //printf( debug_info_kilobots[i]->commitement);
        ///printf("%d\n",debug_info_kilobots[i]->currentopinion);
     //  printf("%d \n",debug_info_kilobots[i]->pool);

       if(debug_info_kilobots[i]->currentopinion == 1){
           op1 +=1;


           }
              
       if(debug_info_kilobots[i]->currentopinion == 2){
           op2 +=1;

       }
                 
       if(debug_info_kilobots[i]->currentopinion == 99){
           unc +=1;
       }
       if(debug_info_kilobots[i]->record_it == 1){
           for (unsigned int r = 0; r < kilobot_entities.size(); r++) {

               if(debug_info_kilobots[r]->currentopinion == 1){
                   if(debug_info_kilobots[r]->c_s == 1) {
                       dissemAr +=1;
                   }

               }


               if(debug_info_kilobots[r]->currentopinion == 2){
                   if(debug_info_kilobots[r]->c_s == 1) {
                       dissemBr +=1;
                   }


               }




           }

           m_cOutput4 << GetSpace().GetSimulationClock() << "    " << debug_info_kilobots[i]->torecord_prev_opinion_before_uncomm << " " << debug_info_kilobots[i]->torecord_new_opinion_after_uncomm << " " << dissemAr <<  " "  << dissemBr  <<std::endl;

       }
       if(debug_info_kilobots[i]->pool == 1){
            for (unsigned int j = 0; j < kilobot_entities.size(); j++) {

                if(debug_info_kilobots[j]->currentopinion == 1){
                    if(debug_info_kilobots[j]->c_s == 1) {
                        dissemA +=1;
                    }

                }


                if(debug_info_kilobots[j]->currentopinion == 2){
                    if(debug_info_kilobots[j]->c_s == 1) {
                        dissemB +=1;
                    }


                }




            }
            m_cOutput2 << GetSpace().GetSimulationClock() << "    " << debug_info_kilobots[i]->op_record << " " << debug_info_kilobots[i]->neighbour_op_rec << " " << dissemA <<  " "  << dissemB  <<std::endl;


        }


       
   }
 
        m_cOutput << GetSpace().GetSimulationClock() << "    " << op1 << " " << op2 <<  " "  << unc <<std::endl;
}


/*-----------------------------------------------------------------------------------------------*/
/* This function reads the config file for the kilogrid and saves the content to configuration.  */
/*-----------------------------------------------------------------------------------------------*/
void CKilogrid::read_configuration(TConfigurationNode& t_node){
    // getting config script name from .argos file
    TConfigurationNode& tExperimentVariablesNode = GetNode(t_node,"variables");
    GetNodeAttribute(tExperimentVariablesNode, "config_file", config_file_name);

    // variables used for reading
    int tmp_x_module;
    int tmp_y_module;
    int tmp_value;
    int read_mode = 0; // 1 is address, 2 is data
    std::string tmp_str;

    // reading
    input.open(config_file_name);
    for( std::string line; getline( input, line ); ){
        // for each line
        if(!line.empty() && line[0] != '#'){  // exclude comments and empty lines

            //printf("%s\n",line.c_str()); // <- this way you can pring the line out!
            if (line == "address"){
                read_mode = 1;
            }else if(line == "data"){
                read_mode = 2;
            } else{
                // reading address
                if(read_mode == 1){
                    // isolating numbers
                    tmp_str = line;
                    tmp_str = tmp_str.substr(7);  // remove module
                    std::string::size_type p  = tmp_str.find('-');
                    tmp_y_module = std::stoi(tmp_str.substr(p+1));
                    tmp_x_module = std::stoi(tmp_str);
                }else if(read_mode == 2){ // read data
                    tmp_value = std::stoi(line, 0, 16);
                    //printf("%d\n",tmp_value);
                    configuration[tmp_x_module][tmp_y_module].push_back(tmp_value);
                }
            }
        }
    }
}


void CKilogrid::set_LED_with_brightness(int x, int y, cell_num_t cn, color_t color, brightness_t brightness){
    module_memory[x][y].cell_colour[cn] = color;
    GetSpace().GetFloorEntity().SetChanged();
}


/*-----------------------------------------------------------------------------------------------*/
/* Visualization of the floor color.                                                             */
/*-----------------------------------------------------------------------------------------------*/
CColor CKilogrid::GetFloorColor(const CVector2 &vec_position_on_plane) {
    CColor cColor=CColor::WHITE;
    int id = position2option(vec_position_on_plane);

    // checks if the option is in time
    if(id == 0){
        // this is wall
        cColor = CColor::WHITE;
    }else if(id == 1){
        cColor=CColor::YELLOW;
    }else if(id == 2){

        cColor=CColor::BLUE; //bad approach for testing is to change to blue.
    }else if(id == 3){
        cColor=CColor::GREEN;
    }else if(id == 4){
        cColor=CColor::BROWN;
    }else if(id == 5){
        cColor=CColor::BLACK;
    }
    else if(id == 6){   //for cells near wall that are red- op A
        cColor=CColor::RED;
    }else if(id == 9){ //for cells near wall that are red- op B
        cColor=CColor::BLUE;
    }


    return cColor;
}


/*-----------------------------------------------------------------------------------------------*/
/* Returns the Option of the given position.                                                     */
/*-----------------------------------------------------------------------------------------------*/
UInt16 CKilogrid::position2option(CVector2 t_position){
    int module_x = t_position.GetX()*10;
    int module_y = t_position.GetY()*10;

    uint8_t cell = 0;
    int x = t_position.GetX()*20;
    int y = t_position.GetY()*20;

    if (x >= 20) x = 19;
    if (y >= 40) y = 39;
    if (x < 0) x = 0;
    if (y < 0) y = 0;

    // get the cell
    if(x % 2 == 0 && y % 2 == 1){
        cell = 0;
    }else if(x % 2 == 1 && y % 2 == 1){
        cell = 1;
    }else if(x % 2 == 0 && y % 2 == 0){
        cell = 2;
    }else if(x % 2 == 1 && y % 2 == 0){
        cell = 3;
    }

    return module_memory[module_x][module_y].cell_colour[cell];
}


CVector2 CKilogrid::position2cell(CVector2 t_position){
    int x = t_position.GetX()*20;
    int y = t_position.GetY()*20;

    if (x >= 20) x = 19;
    if (y >= 40) y = 39;
    if (x < 0) x = 0;
    if (y < 0) y = 0;

    return CVector2(x,y);
}


CVector2 CKilogrid::position2module(CVector2 t_position) {
    float x = t_position.GetX() * 10;
    float y = t_position.GetY() * 10;

    if (x >= 10) x = 9;
    if (y >= 20) y = 19;
    if (x < 0) x = 0;
    if (y < 0) y = 0;

    return CVector2(int(x),int(y));
}


CVector2 CKilogrid::module2cell(CVector2 module_pos, cell_num_t cn){
    int cur_x = module_pos.GetX() * 2;
    int cur_y = module_pos.GetY() * 2;

    switch(cn){
        case 0:
            cur_y += 1;
            break;
        case 1:
            cur_x += 1;
            cur_y += 1;
            break;
        case 2:
            break;
        case 3:
            cur_x += 1;
    }

    return CVector2(cur_x, cur_y);
}


void CKilogrid::get_kilobots_entities(){
    // Get the map of all kilobots from the space
    CSpace::TMapPerType& mapKilobots=GetSpace().GetEntitiesByType("kilobot");
    // Go through them
    for(CSpace::TMapPerType::iterator it = mapKilobots.begin();it != mapKilobots.end();++it) {
        kilobot_entities.push_back(any_cast<CKilobotEntity*>(it->second));
    }
}


/*-----------------------------------------------------------------------------------------------*/
/* Returns the position of the kilobot.                                                          */
/*-----------------------------------------------------------------------------------------------*/
CVector2 CKilogrid::GetKilobotPosition(CKilobotEntity& c_kilobot_entity){
    CVector2 vecKP(c_kilobot_entity.GetEmbodiedEntity().GetOriginAnchor().Position.GetX(),
                   c_kilobot_entity.GetEmbodiedEntity().GetOriginAnchor().Position.GetY());
    return vecKP;
}


/*-----------------------------------------------------------------------------------------------*/
/* Returns the id of the kilobot.                                                                */
/*-----------------------------------------------------------------------------------------------*/
UInt16 CKilogrid::GetKilobotId(CKilobotEntity& c_kilobot_entity){
    std::string strKilobotID((c_kilobot_entity).GetControllableEntity().GetController().GetId());
    return std::stoul(strKilobotID.substr(2));
}

void CKilogrid::virtual_message_reception(){
    for(UInt16 it = 0; it < kilobot_entities.size(); it++){
        // get position information, later used for sending stuff!!
        robot_positions[GetKilobotId(*kilobot_entities[it])] = position2cell(GetKilobotPosition(*kilobot_entities[it]));
        int module_x = GetKilobotPosition(*kilobot_entities[it]).GetX() * 10;
        int module_y = GetKilobotPosition(*kilobot_entities[it]).GetY() * 10;

        // if robot send message set it here
        if(debug_info_kilobots[GetKilobotId(*kilobot_entities[it])]->broadcast_flag == 1){
            IR_message_t* tmp_msg = new IR_message_t;
            tmp_msg->type = debug_info_kilobots[GetKilobotId(*kilobot_entities[it])]->type;
            tmp_msg->data[0] = debug_info_kilobots[GetKilobotId(*kilobot_entities[it])]->data0;
            tmp_msg->data[1] = debug_info_kilobots[GetKilobotId(*kilobot_entities[it])]->data1;
            tmp_msg->data[2] = debug_info_kilobots[GetKilobotId(*kilobot_entities[it])]->data2;
            tmp_msg->data[3] = debug_info_kilobots[GetKilobotId(*kilobot_entities[it])]->data3;
            tmp_msg->data[4] = debug_info_kilobots[GetKilobotId(*kilobot_entities[it])]->data4;
            tmp_msg->data[5] = debug_info_kilobots[GetKilobotId(*kilobot_entities[it])]->data5;
            tmp_msg->data[6] = debug_info_kilobots[GetKilobotId(*kilobot_entities[it])]->data6;
            tmp_msg->data[7] = debug_info_kilobots[GetKilobotId(*kilobot_entities[it])]->data7;
            //module_memory[module_x][module_y].robot_message = tmp_msg;
            module_memory[module_x][module_y].robot_messages.push_back(tmp_msg);
        }
    }
}


void CKilogrid::set_IR_message(int x, int y, IR_message_t &m, cell_num_t cn) {
    // get correct cell
    CVector2 cell_pos = module2cell(CVector2(x,y), cn);

    // get kilobots on this cell
    kilobot_entities_vector current_robots;

    for(uint8_t it=0;it < kilobot_entities.size();it++){
        if(robot_positions[GetKilobotId(*kilobot_entities[it])].GetX() == cell_pos.GetX()
        and robot_positions[GetKilobotId(*kilobot_entities[it])].GetY() == cell_pos.GetY()){
            current_robots.push_back(kilobot_entities[it]);
        }
    }

    // send to all kilobots on this cell
    for(UInt16 it=0; it < current_robots.size(); it++){
        message_t message_to_send;
        message_to_send.type = m.type;
        message_to_send.data[0] = m.data[0];
        message_to_send.data[1] = m.data[1];
        message_to_send.data[2] = m.data[2];
        message_to_send.data[3] = m.data[3];
        message_to_send.data[4] = m.data[4];
        message_to_send.data[5] = m.data[5];
        message_to_send.data[6] = m.data[6];
        message_to_send.data[7] = m.data[7];
        GetSimulator().GetMedium<CKilobotCommunicationMedium>("kilocomm").SendOHCMessageTo(*current_robots[it], &message_to_send);
    }
}


/*-----------------------------------------------------------------------------------------------*/
/* Set up the getting of debug information from the robot (e.g. the robots state).               */
/*-----------------------------------------------------------------------------------------------*/
void CKilogrid::GetDebugInfo(){
    debug_info_kilobots.clear();
    for(UInt16 it=0;it< kilobot_entities.size();it++){
        // Check if there is a message to send to the kilobot "i" and get the message

        /*
         * When the 'reset' method is called on the kilobot controller, the
         * kilobot state is destroyed and recreated. Thus, we need to
         * recreate the list of controllers and debugging info from scratch
         * as well.
         */
        // Create a pointer to the current kilobot
        CCI_KilobotController* pcKBC = &dynamic_cast<CCI_KilobotController&>(kilobot_entities[it]->GetControllableEntity().GetController());
        // Create debug info for controller
        debug_info_t* ptDebugInfo = pcKBC->DebugInfoCreate<debug_info_t>();
        // Append to list
        debug_info_kilobots.push_back(ptDebugInfo);
    }
}


void CKilogrid::init_CAN_message(CAN_message_t* cell_msg){
    uint8_t d;

    cell_msg->id = 0;
    cell_msg->header.rtr = 0;
    cell_msg->header.length = 8;

    for(d = 0; d < 8; d++) cell_msg->data[d] = 0;
}


uint8_t CKilogrid::CAN_message_tx(CAN_message_t *m, kilogrid_address_t add) {
    // this is a hack because we can only virtually set msgs
    // TODO is this message coppied or just the pointer
    // module_memory[add.x][add.y].received_cell_message = m;
    //printf("goes here");
    module_memory[add.x][add.y].received_cell_messages.push_back(*m);

    return 1;
}




/*-----------------------------------------------------------------------------------------------*/
/* The following methods need to be implemented by the user - they aim to be such as the         */
/* methods used on the real Kilogrid.                                                            */
/*-----------------------------------------------------------------------------------------------*/
void CKilogrid::setup(int x, int y){
    // the real line is
    // cell_x[0] = (configuration[0] * 2);
    module_memory[x][y].cell_x[0] = (configuration[x][y][0] * 2);
    module_memory[x][y].cell_x[1] = (configuration[x][y][0] * 2 + 1);
    module_memory[x][y].cell_x[2] = (configuration[x][y][0] * 2);
    module_memory[x][y].cell_x[3] = (configuration[x][y][0] * 2 + 1);

    module_memory[x][y].cell_y[0] = (configuration[x][y][1] * 2 + 1);
    module_memory[x][y].cell_y[1] = (configuration[x][y][1] * 2 + 1);
    module_memory[x][y].cell_y[2] = (configuration[x][y][1] * 2);
    module_memory[x][y].cell_y[3] = (configuration[x][y][1] * 2);

    module_memory[x][y].cell_role[0] = (configuration[x][y][2]);
    module_memory[x][y].cell_role[1] = (configuration[x][y][2]);
    module_memory[x][y].cell_role[2] = (configuration[x][y][2]);
    module_memory[x][y].cell_role[3] = (configuration[x][y][2]);
    
    //last 4 hex in file of each data represent colour

    module_memory[x][y].cell_colour[0] = color_t (configuration[x][y][3]);
    module_memory[x][y].cell_colour[1] = color_t (configuration[x][y][4]);
    module_memory[x][y].cell_colour[2] = color_t (configuration[x][y][5]);
    module_memory[x][y].cell_colour[3] = color_t (configuration[x][y][6]);
    module_memory[x][y].test_counter = 0;

    for(int i = 0; i < 4; i++){
        set_LED_with_brightness(x, y, cell_id[i], module_memory[x][y].cell_colour[i], HIGH);
    }
}


void CKilogrid::loop(int x, int y){
    // the real line is
    // test_counter += 1;
    module_memory[x][y].test_counter += 1;

    // send initial message
    if(!module_memory[x][y].init_flag){
        module_memory[x][y].init_flag = true;
        for (int f = 0; f < 4; f++){
            module_memory[x][y].ir_message_tx->type = 10;  // TODO check if free
            module_memory[x][y].ir_message_tx->crc = 0;
            module_memory[x][y].ir_message_tx->data[0] = module_memory[x][y].cell_x[f];
            module_memory[x][y].ir_message_tx->data[1] = module_memory[x][y].cell_y[f];
            module_memory[x][y].ir_message_tx->data[2] = module_memory[x][y].cell_role[f];
            set_IR_message(x, y, *module_memory[x][y].ir_message_tx, cell_id[f]);
        }
    }    


    if(module_memory[x][y].test_counter > 20){
        module_memory[x][y].test_counter = 0;
        for (int c = 0; c < 4; c++){
            
                    //printf("goes here");

                    module_memory[x][y].ir_message_tx->type = 11;//GRID_MSG
                    module_memory[x][y].ir_message_tx->crc = 0;
                    module_memory[x][y].ir_message_tx->data[0] = module_memory[x][y].cell_x[c];
                    module_memory[x][y].ir_message_tx->data[1] = module_memory[x][y].cell_y[c];
                    module_memory[x][y].ir_message_tx->data[2] = module_memory[x][y].cell_colour[c];
                    module_memory[x][y].ir_message_tx->data[3] = module_memory[x][y].cell_role[c];
                    set_IR_message(x, y, *module_memory[x][y].ir_message_tx, cell_id[c]);
            
            // HOW TO CHANGE COLOR OF ONE CELL
            // int tmp_int = (module_memory[x][y].cell_colour[c]+1)%4;
            // set_LED_with_brightness(x, y, cell_id[c], (color_t)(tmp_int), HIGH);

            // HOW TO SET MESSAGES
            // set_IR_message(x_it, y_it, *module_memory[x_it][y_it].ir_message_tx, cell_id[c]);

            // HOW TO SEND CAN MESSAGES
//             init_CAN_message(&module_memory[x][y].cell_message);
//             module_memory[x][y].cell_address.type = ADDR_INDIVIDUAL;
//             module_memory[x][y].cell_address.x = x_of_module_to_send_to;
//             module_memory[x][y].cell_address.y = y_of_module_to_send_to;
//             CAN_message_tx(&module_memory[x][y].cell_message, module_memory[x][y].cell_address);

            // some example useage of sending messages between modules
            
            /*
            if ((module_memory[x][y].cell_x[c] == 10 && module_memory[x][y].cell_y[c] == 10) || (module_memory[x][y].cell_x[c] == 14 && module_memory[x][y].cell_y[c] == 14)){
                                printf("goes hedere");
                init_CAN_message(&module_memory[x][y].cell_message);
                module_memory[x][y].cell_address.type = ADDR_INDIVIDUAL;
                module_memory[x][y].cell_address.x = 2;
                module_memory[x][y].cell_address.y = 2;
                // some payload
                module_memory[x][y].cell_message.id = 55;
                module_memory[x][y].cell_message.data[0] = 55;
                module_memory[x][y].cell_message.data[1] = 1;
                module_memory[x][y].cell_message.data[2] = 1;
                module_memory[x][y].cell_message.data[3] = 1;
                module_memory[x][y].cell_message.data[4] = 1;
                    printf("goes here1");
                CAN_message_tx(&module_memory[x][y].cell_message, module_memory[x][y].cell_address);
            }
            
            */
        }
    }
}


void CKilogrid::IR_rx(int x, int y, IR_message_t *m, cell_num_t c, distance_measurement_t *d, uint8_t CRC_error) {
    // used for debug tracking on the real kilogrid ...
//    if(!CRC_error && m->type == TRACKING) {
//        CAN_message_t *msg = next_CAN_message();
//        if (msg != NULL) { // if the buffer is not full
//            serialize_tracking_message(msg, c, m->data);
//        }
//    }else if(!CRC_error && m->type == VIRTUAL_ROBOT_MSG){
    // check if msg is zero ... return no msg to send
//    if (m == nullptr){
//        return;
//    }
    if (!CRC_error && m->type == MSG_T_VIRTUAL_ROBOT_MSG) {
          // some example usage
//        module_memory[x][y].received_option = m->data[0];
//        module_memory[x][y].received_com_range = m->data[1];
//        module_memory[x][y].received_x = m->data[2];
//        module_memory[x][y].received_y = m->data[3];
        module_memory[x][y].msg_number_current = m->data[4];
        if (module_memory[x][y].msg_number_current != module_memory[x][y].msg_number) {
            // case new message
            module_memory[x][y].msg_number = module_memory[x][y].msg_number_current;
            // TODO implement logic ...
        } else {
            // message already seen -> discard
            return;
        }
    }
}

void CKilogrid::CAN_rx(int x, int y, CAN_message_t *m){
    // example usage of this method
    if (m->data[0] == 55){  // set msg
        module_memory[x][y].cell_received_op[0] = m->data[1];
        module_memory[x][y].cell_received_op[1] = m->data[2];
        module_memory[x][y].cell_received_op[2] = m->data[3];
        module_memory[x][y].cell_received_op[3] = m->data[4];
        // receive_timer = m->data[5];
        for(uint8_t cell_it_cb = 0; cell_it_cb < 4; cell_it_cb++){
            if(module_memory[x][y].cell_received_op[cell_it_cb] != 0){
                module_memory[x][y].reset_timer[cell_it_cb] = 0;
            }
        }
    }else {
        module_memory[x][y].cell_received_op[0] = 3;
        module_memory[x][y].cell_received_op[1] = 3;
        module_memory[x][y].cell_received_op[2] = 3;
        module_memory[x][y].cell_received_op[3] = 3;
    }
}


REGISTER_LOOP_FUNCTIONS(CKilogrid, "kilogrid_loop_functions")
