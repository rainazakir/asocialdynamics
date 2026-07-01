if(ARGOS_BUILD_FOR_SIMULATOR)
  include_directories(${CMAKE_SOURCE_DIR}/argos3/plugins/robots/kilobot/control_interface)

add_executable(agent_stub_ant agent.h agent_antagonistic.c)
add_executable(agent_stub_syn agent.h agent_synergistic.c)

if(UNIX AND NOT APPLE)
  target_link_libraries(agent_stub_ant  argos3plugin_simulator_kilolib -lrt -lm)
  target_link_libraries(agent_stub_syn  argos3plugin_simulator_kilolib -lrt -lm)

else(UNIX AND NOT APPLE)
  target_link_libraries(agent_stub_ant  argos3plugin_simulator_kilolib)
 target_link_libraries(agent_stub_syn  argos3plugin_simulator_kilolib)

endif()

endif(ARGOS_BUILD_FOR_SIMULATOR)
