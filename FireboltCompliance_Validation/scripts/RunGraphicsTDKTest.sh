##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

TEST=$1
TIMEOUT=$2
DISPLAY=$3
TEST_OPTION=$4

if [ "$1" == "--help" ];then
   printf '#%.0s' {1..100}
   printf "\nThis Test Script executes Essos_TDKTestApp and Westeros_TDKTestApp along with all the pre-requisites\n"
   printf "\nBelow options available for testing\n* Run Essos as Direct EGL application\n* Run Essos as Wayland Client application\n* Run Westeros Test\n* Run Essos Manual validation\n"
   printf "\n* Test script receives 4 command line arguments namely \n   TEST(Test to be executed) \n   TIMEOUT(timeout for the application to be executed) \
   \n   DISPLAY(display name to start westeros renderer)\n   TEST_OPTION(Additional options for TEST application)\n"
   printf "\n* Example Test Scenarios validated using test script"
   printf "\n   sh RunGraphicsTDKTest.sh Essos 30                       //Essos using Direct EGL application, runs for 10 seconds"
   printf "\n   sh RunGraphicsTDKTest.sh Essos 30 wayland-0 USE_WAYLAND //Essos test app runs as wayland client"
   printf "\n   sh RunGraphicsTDKTest.sh Westeros 30 wayland-0          //executes Westeros Test for 30 seconds"
   printf "\n   sh RunGraphicsTDKTest.sh Essos MANUAL                   //MANUAL Essos test application execution\n"
   printf '#%.0s' {1..100}
   printf "\n"
fi

if [ "$2" == "MANUAL" ];then
   TEST_OPTION="MANUAL"
fi

#Export westeros library
export XDG_RUNTIME_DIR=/tmp

start_westeros_renderer(){
  export LD_PRELOAD=libwesteros_gl.so.0.0.0
  timeout 30 westeros --renderer libwesteros_render_embedded.so.0.0.0 --display $DISPLAY --embedded --noFBO &
}

log(){
    if [ $1 == "yes" ];
    then
        resultVar+=("PASSED")
    elif [ $1 ==   "no" ];
    then
        resultVar+=("FAILED")
    else
        printf 'Please respond with yes/no :'
        read input
        log $input
    fi
}

executeTestCase(){
    printf "\n$1\nWaiting 2 seconds for user to initiate the test"
    testcase=$(( testcase  + 1 ));
    sleep 2
    printf "\n$2\nActual Result(yes/no):"
    read input
    log $input
}

if [ "$TEST" == "Essos" ] && [ "$TEST_OPTION" == "MANUAL" ];
then
    printf "Starting Essos_TDKTestApp\n"
    ./Essos_TDKTestApp -d &
    sleep 3
    PROCESS="`pidof Essos_TDKTestApp`"
    if [ -z "$PROCESS" ];
    then
        printf '\n'
        printf '#%.0s' {1..40}
        printf "\nEssos_TDKTestApp didnot run properly\nExiting from Test\n"
        printf '#%.0s' {1..40}
        printf '\n'
        exit
    fi
    resultvar=()
    testcase=0
    printf '\n'
    printf '#%.0s' {1..30}
    printf '\nMANUAL Test Option Initiated'
    printf '\nConfigured keyboard with DUT (yes/no):'
    read input
    log $input
    if [ "$input" == "yes" ];
    then
        printf 'Configured keyboard\n'
        printf "\n\nStarting Test Scenarios\n\n"
        executeTestCase "Scenario 1: Press Up Arrow key from keyboard configured with DUT" "Expected Result : Triangle must move up the axis in the display"
        executeTestCase "Scenario 2: Press Down Arrow key from keyboard configured with DUT" "Expected Result : Triangle must move down the axis in the display"
        executeTestCase "Scenario 3: Press Left Arrow key from keyboard configured with DUT" "Expected Result : Triangle must move left of the axis in the display"
        executeTestCase "Scenario 4: Press Right Arrow key from keyboard configured with DUT" "Expected Result : Triangle must move right of the axis in the display"
    elif [ "$input" == "no" ];
    then
        printf "Keyboard not configured with the DUT. Please configure to proceed"
    else
        printf "Enter yes/no"
    fi
    printf '\n\n'
    printf '#%.0s' {1..100}
    printf '\n'
    printf '\nSUMMARY OF TEST RESULTS\n'
    printf '#%.0s' {1..100}
    printf '\n'
    for test in $(seq 1 $testcase);
    do
        printf "\nScenario $test : ${resultVar[$test -1]}"
    done
    printf '\n'
    printf '#%.0s' {1..100}
    printf '\n'
    pkill -f  Essos_TDKTestApp
    exit
fi

if [ "$TEST_OPTION" == "USE_WAYLAND" ];
then
    start_westeros_renderer
    sleep 3
    export LD_PRELOAD=libwayland-egl.so.0.0.0
    export WAYLAND_DISPLAY=$DISPLAY
fi

if [ "$TEST" == "Essos" ];
then
    Essos_TDKTestApp -d -t=$TIMEOUT
elif [ "$TEST" == "Westeros" ];
then
    start_westeros_renderer
    sleep 3
    Westeros_TDKTestApp --display $DISPLAY -t=$TIMEOUT
fi
