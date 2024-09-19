if(ARGOS_BUILD_FOR_SIMULATOR)
  include_directories(${CMAKE_SOURCE_DIR}/argos3/plugins/robots/kilobot/control_interface)

add_executable(agent_stubred agent.h agent_red.c)
add_executable(agent_stubblue agent.h agent_blue.c)

#if(UNIX AND NOT APPLE)
  target_link_libraries(agent_stubred  argos3plugin_simulator_kilolib -lrt -lm)
  target_link_libraries(agent_stubblue  argos3plugin_simulator_kilolib -lrt -lm)

#else(UNIX AND NOT APPLE)
#  target_link_libraries(agent_stubred  argos3plugin_simulator_kilolib)
# target_link_libraries(agent_stubblue  argos3plugin_simulator_kilolib)

#endif()

endif(ARGOS_BUILD_FOR_SIMULATOR)
