#ifndef __STATEMACHINES_H
#define __STATEMACHINES_H

#include "SM.h"

void ExecStatemachines();

// Loading screen animation
void  SetDisplayLoading();
State FrameLoadingHead();
State FrameLoadingBody();

// Number scrolling animation
State FrameStaticHead();
State FrameStaticBody();
State FrameScrollingHead();
State FrameScrollingBody();

#endif
