/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2021 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
extern "C"
{
#include <gst/check/gstcheck.h>
#include <gst/gst.h>
}

#define EOS_TIMEOUT 		-1
#define DEFAULT_TEST_SUITE_TIMEOUT	360
#define VIDEO_STATUS 		"/CheckVideoStatus.sh"
#define PLAYBIN_ELEMENT 	"playbin"
#define WESTEROS_SINK 		"westerossink"
#define BUFFER_SIZE_LONG	1024
#define BUFFER_SIZE_SHORT	264


char tcname[BUFFER_SIZE_SHORT] = {'\0'};
char m_play_url[BUFFER_SIZE_LONG] = {'\0'};
char TDK_PATH[BUFFER_SIZE_SHORT] = {'\0'};
/*
 * Default values for avstatus check flag and play_timeout if not received as input arguments
 */
bool checkAVStatus = false;
int play_timeout = 10; 

/* 
 * Playbin flags 
 */
typedef enum {
  GST_PLAY_FLAG_VIDEO         = (1 << 0), 
  GST_PLAY_FLAG_AUDIO         = (1 << 1), 
  GST_PLAY_FLAG_TEXT          = (1 << 2) 
} GstPlayFlags;

/*
 * Methods
 */

/********************************************************************************************************************
Purpose:               To get the current status of the AV running
Parameters:
scriptname [IN]       - The input scriptname
Return:               - bool SUCCESS/FAILURE
*********************************************************************************************************************/
bool getstreamingstatus(char* script)
{
    char buffer[BUFFER_SIZE_SHORT]={'\0'};
    char result[BUFFER_SIZE_LONG]={'\0'};
    FILE* pipe = popen(script, "r");
    if (!pipe)
    {
            GST_ERROR("Error in opening pipe \n");
            return false;
    }
    while (!feof(pipe)) 
    {
        if (fgets(buffer, BUFFER_SIZE_SHORT, pipe) != NULL)
        {
            strcat(result, buffer);
        }
    }
    pclose(pipe);
    GST_LOG("Script Output: %s %s\n", script, result);
    if (strstr(result, "SUCCESS") != NULL)
    {
    	return true;
    }
    else
    {
        return false;
    }
}


/********************************************************************************************************************
Purpose:               To check the current status of the AV running
Parameters:
scriptname [IN]       - The input scriptname
Return:               - bool SUCCESS/FAILURE
*********************************************************************************************************************/
bool check_for_AV_status()
{
    GST_LOG("\nCheck_for_AV_status\n");
    char video_status[BUFFER_SIZE_SHORT]={'\0'};

    strcat(video_status, TDK_PATH);
    strcat(video_status, VIDEO_STATUS);
  
    /*
     * TODO Similar to VideoStatus Check, AudioStatus Check Needs to be implemented
     */
    return (getstreamingstatus(video_status));
 
}

/********************************************************************************************************************
Purpose:               Callback function to set a variable to true on receiving first frame
*********************************************************************************************************************/
static void firstFrameCallback(GstElement *sink, guint size, void *context, gpointer data)
{
   bool *gotFirstFrameSignal = (bool*)data;

   printf ("Received first frame signal\n");
   /*
    * Set the Value to global variable once the first frame signal is received
    */
   *gotFirstFrameSignal = true;
}

/********************************************************************************************************************
 * Purpose     	: Test to do generic playback using playbin element and westeros-sink
 * Parameters   : Playback url
 ********************************************************************************************************************/
GST_START_TEST (test_generic_playback)
{
    bool is_av_playing = false;
    bool firstFrameReceived;
    GstElement *playbin;
    GstElement *westerosSink;
    gint flags;

    /*
     * Create the playbin element
     */
    playbin = gst_element_factory_make(PLAYBIN_ELEMENT, NULL);
    fail_unless (playbin != NULL, "Failed to create 'playbin' element");
    /*
     * Set the url received from argument as the 'uri' for playbin
     */
    fail_unless (m_play_url != NULL, "Playback url should not be NULL"); 
    g_object_set (playbin, "uri", m_play_url, NULL);
    /*
     * Update the current playbin flags to enable Video and Audio Playback
     */
    g_object_get (playbin, "flags", &flags, NULL);
    flags |= GST_PLAY_FLAG_VIDEO | GST_PLAY_FLAG_AUDIO;
    g_object_set (playbin, "flags", flags, NULL);

    /*
     * Set westros-sink
     */
    westerosSink = gst_element_factory_make(WESTEROS_SINK, NULL);
    fail_unless (westerosSink != NULL, "Failed to create 'westerossink' element");

    /*
     * Link the westeros-sink to playbin
     */
    g_object_set (playbin, "video-sink", westerosSink, NULL);

    /*
     * Set the first frame recieved callback
     */
    g_signal_connect( westerosSink, "first-video-frame-callback", G_CALLBACK(firstFrameCallback), &firstFrameReceived);
    /*
     * Set the firstFrameReceived variable as false before starting play
     */
    firstFrameReceived= false;
    
    /*
     * Set playbin to PLAYING
     */
    GST_FIXME( "Setting to Playing State\n");
    fail_unless (gst_element_set_state (playbin, GST_STATE_PLAYING) !=  GST_STATE_CHANGE_FAILURE);
    GST_FIXME( "Set to Playing State\n");
    
    /*
     * Wait for 'play_timeout' seconds(recieved as the input argument) before checking AV status
     */
    sleep (play_timeout);
    /*
     * Check if the first frame received flag is set
     */
    fail_unless (firstFrameReceived == true, "Failed to receive first video frame signal");
    /*
     * Check for AV status if its enabled
     */
    if (true == checkAVStatus)
    {
        is_av_playing = check_for_AV_status();
        fail_unless (is_av_playing == true, "Video is not playing in TV");
    }
    GST_LOG("DETAILS: SUCCESS, Video playing successfully \n");

    if (playbin)
    {
       gst_element_set_state (playbin, GST_STATE_NULL);
    }
    /*
     * Cleanup after use
     */
    gst_object_unref (playbin);
}
GST_END_TEST;

/********************************************************************************************************************
 * Purpose      : Test to change the state of pipeline from play to pause
 * Parameters   : Playback url
 ********************************************************************************************************************/
GST_START_TEST (test_play_pause_pipeline)
{
    bool is_av_playing = false;
    bool firstFrameReceived;
    gint flags;
    GstState cur_state;
    GstElement *playbin;
    GstElement *westerosSink;
    
    /*
     * Create the playbin element
     */
    playbin = gst_element_factory_make(PLAYBIN_ELEMENT, NULL);
    fail_unless (playbin != NULL, "Failed to create 'playbin' element");

    /*
     * Set the url received from argument as the 'uri' for playbin
     */
    fail_unless (m_play_url != NULL, "Playback url should not be NULL");
    g_object_set (playbin, "uri", m_play_url, NULL);

    /*
     * Update the current playbin flags to enable Video and Audio Playback
     */
    g_object_get (playbin, "flags", &flags, NULL);
    flags |= GST_PLAY_FLAG_VIDEO | GST_PLAY_FLAG_AUDIO;
    g_object_set (playbin, "flags", flags, NULL);

    /*
     * Set westros-sink
     */
    westerosSink = gst_element_factory_make(WESTEROS_SINK, NULL);
    fail_unless (westerosSink != NULL, "Failed to create 'westerossink' element");

    /*
     * Link the westeros-sink to playbin
     */
    g_object_set (playbin, "video-sink", westerosSink, NULL);

     /*
     * Set the first frame recieved callback
     */
    g_signal_connect( westerosSink, "first-video-frame-callback", G_CALLBACK(firstFrameCallback), &firstFrameReceived);
    /*
     * Set the firstFrameReceived variable as false before starting play
     */
    firstFrameReceived= false;

    /*
     * Set playbin to PLAYING
     */
    GST_FIXME( "Setting to Playing State\n");
    fail_unless (gst_element_set_state (playbin, GST_STATE_PLAYING) !=  GST_STATE_CHANGE_FAILURE);
    GST_FIXME( "Set to Playing State\n");

    /*
     * Wait for 'play_timeout' seconds(recieved as the input argument) before chaging the pipeline state
     * We are waiting for 5 more seconds before checking pipeline status, so reducing the wait here
     */
    sleep (play_timeout - 5);
    /*
     * Ensure that playback is happening before pausing the pipeline
     */
    /*
     * Check if the first frame received flag is set
     */
    fail_unless (firstFrameReceived == true, "Failed to receive first video frame signal");
    /*
     * Check for AV status if its enabled
     */
    if (true == checkAVStatus)
    {
        is_av_playing = check_for_AV_status();
        fail_unless (is_av_playing == true, "Video is not playing in TV");
    }
    printf ("DETAILS: SUCCESS, Video playing successfully \n");

    /*
     * Set pipeline to PAUSED
     */
    gst_element_set_state (playbin, GST_STATE_PAUSED);
    /*
     * Wait for 5 seconds before checking the pipeline status
     */
    sleep(5);
    fail_unless_equals_int (gst_element_get_state (playbin, &cur_state,
            NULL, 0), GST_STATE_CHANGE_SUCCESS);
    GST_LOG("\n********Current state: %s\n",gst_element_state_get_name(cur_state));

    fail_unless_equals_int (cur_state, GST_STATE_PAUSED);
    printf ("DETAILS: SUCCESS, Current state is: %s \n", gst_element_state_get_name(cur_state));
    if (playbin)
    {
       gst_element_set_state(playbin, GST_STATE_NULL);
    }
    /*
     * Cleanup after use
     */
    gst_object_unref (playbin);
}
GST_END_TEST;

/********************************************************************************************************************
 * Purpose      : Test to check that EOS message is recieved
 * Parameters   : Playback url
 ********************************************************************************************************************/
GST_START_TEST (test_EOS)
{
    bool is_av_playing = false;
    bool firstFrameReceived;
    GstMessage *message;
    GstBus *bus;
    gint flags;
    GstElement *playbin;
    GstElement *westerosSink;

    /*
     * Create the playbin element
     */
    playbin = gst_element_factory_make(PLAYBIN_ELEMENT, NULL);
    fail_unless (playbin != NULL, "Failed to create 'playbin' element");

    /*
     * Set the url received from argument as the 'uri' for playbin
     */
    fail_unless (m_play_url != NULL, "Playback url should not be NULL");
    g_object_set (playbin, "uri", m_play_url, NULL);

    /*
     * Update the current playbin flags to enable Video and Audio Playback
     */
    g_object_get (playbin, "flags", &flags, NULL);
    flags |= GST_PLAY_FLAG_VIDEO | GST_PLAY_FLAG_AUDIO;
    g_object_set (playbin, "flags", flags, NULL);

    /*
     * Set westros-sink
     */
    westerosSink = gst_element_factory_make(WESTEROS_SINK, NULL);
    fail_unless (westerosSink != NULL, "Failed to create 'westerossink' element");

    /*
     * Link the westeros-sink to playbin
     */
    g_object_set (playbin, "video-sink", westerosSink, NULL);

    /*
     * Set the first frame recieved callback
     */
    g_signal_connect( westerosSink, "first-video-frame-callback", G_CALLBACK(firstFrameCallback), &firstFrameReceived);
    /*
     * Set the firstFrameReceived variable as false before starting play
     */
    firstFrameReceived= false;

    /*
     * Set playbin to PLAYING
     */
    GST_FIXME( "Setting to Playing State\n");
    fail_unless (gst_element_set_state (playbin, GST_STATE_PLAYING) !=  GST_STATE_CHANGE_FAILURE);
    GST_FIXME( "Set to Playing State\n");

    /*
     * Wait for 5 seconds before checking AV status
     */
    sleep (5);
    /*
     * Check if the first frame received flag is set
     */
    fail_unless (firstFrameReceived == true, "Failed to receive first video frame signal");
    /*
     * Check for AV status if its enabled
     */
    if (true == checkAVStatus)
    {
        is_av_playing = check_for_AV_status();
        fail_unless (is_av_playing == true, "Video is not playing in TV");
    }
    printf ("DETAILS: SUCCESS, Video playing successfully \n");

    /*
     * Polling the bus for messages
     */
    bus = gst_element_get_bus (playbin);
    fail_if (bus == NULL);
    /* 
     * Wait for receiving EOS event
     */
    message = gst_bus_poll (bus, (GstMessageType)GST_MESSAGE_EOS, EOS_TIMEOUT);
    fail_unless (GST_MESSAGE_EOS == GST_MESSAGE_TYPE(message), "Failed to recieve EOS message");
    printf ("EOS Recieved\n");
    gst_message_unref (message);

    if (playbin)
    {
       gst_element_set_state(playbin, GST_STATE_NULL);
    }
    /*
     * Cleanup after use
     */
    gst_object_unref (playbin);
    gst_object_unref (bus);
}
GST_END_TEST;

static Suite *
media_pipeline_suite (void)
{
    Suite *gstPluginsSuite = suite_create ("playbin_plugin_test");
    TCase *tc_chain = tcase_create ("general");
    /*
     * Set timeout to play_timeout if play_timeout > DEFAULT_TEST_SUITE_TIMEOUT(360) seconds
     */
    guint timeout = DEFAULT_TEST_SUITE_TIMEOUT;
    if (play_timeout > DEFAULT_TEST_SUITE_TIMEOUT)
    {
        timeout = play_timeout;
    }
    tcase_set_timeout (tc_chain, timeout);
    suite_add_tcase (gstPluginsSuite, tc_chain);

    GST_INFO("Test Case name is %s\n", tcname);
    
    if(strcmp("test_generic_playback", tcname) == 0)
    {
       tcase_add_test (tc_chain, test_generic_playback);
       GST_INFO("tc %s run successfull\n",tcname);
       GST_INFO("SUCCESS\n");
    }
    else if(strcmp("test_play_pause_pipeline",tcname) == 0)
    {
       tcase_add_test (tc_chain, test_play_pause_pipeline);
       GST_INFO("tc %s run successfull\n",tcname);
       GST_INFO("SUCCESS\n");
    }
    else if(strcmp("test_EOS",tcname) == 0)
    {
       tcase_add_test (tc_chain, test_EOS);
       GST_INFO("tc %s run successfull\n",tcname);
       GST_INFO("SUCCESS\n");
    }

    return gstPluginsSuite;
}



int main(int argc, char **argv)
{
    Suite *testSuite;
    int returnValue = 0;
    int arg = 0;
    /*
     * Get TDK path
     */
    if(getenv("TDK_PATH")!=NULL)
    {
    	strcpy(TDK_PATH,getenv("TDK_PATH"));
    }
    else
    {
    	GST_ERROR ("Environment variable TDK_PATH should be set!!!!");
	returnValue = 0;
	goto exit;
    }
    if(argc == 2)
    {
    	strcpy(tcname,argv[1]);
    	GST_INFO("\nArg 2: TestCase Name: %s \n",tcname);
    }
    else if(argc >= 3)
    {
        strcpy(tcname,argv[1]);
	if ((strcmp("test_play_pause_pipeline",tcname) == 0) || 
            (strcmp("test_generic_playback",tcname) == 0) ||
            (strcmp("test_EOS",tcname) == 0))
	{
            strcpy(m_play_url,argv[2]);
            for (arg = 3; arg < argc; arg++)
            {
                if (strcmp ("checkavstatus=yes", argv[arg]) == 0)
                {
                    checkAVStatus = true;
                }
                if (strstr(argv[arg], "timeout=") != NULL)
                {
                    strtok(argv[arg], "=");
      		    play_timeout = atoi(strtok(NULL, "="));
                }
            }
	}


        GST_INFO("\nArg : TestCase Name: %s \n", tcname);
        GST_INFO("\nArg : Playback url: %s \n", m_play_url);
    }
    else
    {
        GST_ERROR ("FALIURE : Insufficient arguments\n");
        returnValue = 0;
	goto exit;
    }
    gst_check_init(&argc,&argv);
    testSuite = media_pipeline_suite();

    returnValue =  gst_check_run_suite (testSuite,"playbin_plugin_test", __FILE__);

exit:
    return returnValue;
}    
