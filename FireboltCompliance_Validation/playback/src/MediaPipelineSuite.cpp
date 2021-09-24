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
#include <unistd.h>
#include <iterator>
#include <string>
#include <vector>
#include <cmath>
extern "C"
{
#include <gst/check/gstcheck.h>
#include <gst/gst.h>
}

using namespace std;

#define EOS_TIMEOUT 			-1
#define DEFAULT_TEST_SUITE_TIMEOUT	360
#define VIDEO_STATUS 			"/CheckVideoStatus.sh"
#define AUDIO_STATUS 			"/CheckAudioStatus.sh"
#define PLAYBIN_ELEMENT 		"playbin"
#define WESTEROS_SINK 			"westerossink"
#define BUFFER_SIZE_LONG		1024
#define BUFFER_SIZE_SHORT		264
#define NORMAL_PLAYBACK_RATE		1.0
#define FCS_MICROSECONDS		1000000


char tcname[BUFFER_SIZE_SHORT] = {'\0'};
char m_play_url[BUFFER_SIZE_LONG] = {'\0'};
char TDK_PATH[BUFFER_SIZE_SHORT] = {'\0'};
vector<string> operationsList;
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
 * Trickplay operations
 */
typedef enum {
  REWIND16x_RATE        = -16,
  REWIND4x_RATE         = -4,
  REWIND2x_RATE		= -2,
  FASTFORWARD2x_RATE 	= 2,
  FASTFORWARD4x_RATE    = 4,
  FASTFORWARD16x_RATE  	= 16
} PlaybackRates;


/* 
 * Structure to pass arguments to/from the message handling method
 */
typedef struct CustomData {
    GstElement *playbin;  		/* Playbin element handle */
    GstState cur_state;         	/* Variable to store the current state of pipeline */
    gint64 seekPosition;		/* Variable to store the position to be seeked */
    gint64 currentPosition; 		/* Variable to store the current position of pipeline */
    gboolean terminate;    		/* Variable to indicate whether execution should be terminated in case of an error */
    gboolean seeked;    		/* Variable to indicate if seek to requested position is completed */
    gboolean eosDetected;		/* Variable to indicate if EOS is detected */
    gboolean stateChanged;              /* Variable to indicate if stateChange is occured */
} MessageHandlerData;


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
bool check_for_AV_status ()
{
    GST_LOG ("\nCheck_for_AV_status\n");
    char video_status[BUFFER_SIZE_SHORT] = {'\0'};
    char audio_status[BUFFER_SIZE_SHORT] = {'\0'};

    strcat (video_status, TDK_PATH);
    strcat (video_status, VIDEO_STATUS);
    strcat (audio_status, TDK_PATH);
    strcat (audio_status, AUDIO_STATUS);
  
    /*
     * VideoStatus Check, AudioStatus Check script execution
     */
    return (getstreamingstatus (video_status) && getstreamingstatus (audio_status));
 
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
Purpose:               Method to handle the different messages from gstreamer bus
Parameters:
message [IN]          - GstMessage* handle to the message recieved from bus
data [OUT]	      - MessageHandlerData* handle to the custom structure to pass arguments between calling function
Return:               - None
*********************************************************************************************************************/
static void handleMessage (MessageHandlerData *data, GstMessage *message) 
{
    GError *err;
    gchar *debug_info;

    switch (GST_MESSAGE_TYPE (message)) 
    {
        case GST_MESSAGE_ERROR:
            gst_message_parse_error (message, &err, &debug_info);
            printf ("Error received from element %s: %s\n", GST_OBJECT_NAME (message->src), err->message);
            printf ("Debugging information: %s\n", debug_info ? debug_info : "none");
            g_clear_error (&err);
            g_free (debug_info);
            data->terminate = TRUE;
            break;
        case GST_MESSAGE_EOS:
            printf ("End-Of-Stream reached.\n");
            data->eosDetected = TRUE;
            data->terminate = TRUE;
            break;
            /*
            * In case of seek event, state change of various gst elements occur asynchronously
            * We can check if the seek event happened in between by querying the current position while ASYNC_DONE message is retrieved
            * If the current position is not updated, we will wait until bus is clear or error/eos occurs
            */
        case GST_MESSAGE_STATE_CHANGED:
            data->stateChanged = TRUE;
        case GST_MESSAGE_ASYNC_DONE:
            fail_unless (gst_element_query_position (data->playbin, GST_FORMAT_TIME, &(data->currentPosition)), 
                                                     "Failed to querry the current playback position");

            //Added GST_SECOND buffer time between currentPosition and seekPosition
            if (abs( data->currentPosition - data->seekPosition) <= (GST_SECOND))
            {
               data->seeked = TRUE;
            }
            break;
        default:
            printf ("Unexpected message received.\n");
            data->terminate = TRUE;
            break;
    }
    gst_message_unref (message);
}


/********************************************************************************************************************
Purpose:               To set the playback rate for pipeline
Parameters:
playbin [IN]          - GstElement* 'playbin' for which the playback rate should be set 
rate [IN]             - gdouble value for the playback rate to be set 
Return:               - None
*********************************************************************************************************************/
static void setRate (GstElement* playbin, gdouble rate)
{
    gint64 currentPosition = GST_CLOCK_TIME_NONE;
    /*
     * Get the current playback position
     */
    fail_unless (gst_element_query_position (playbin, GST_FORMAT_TIME, &currentPosition), "Failed to query the current playback position");

    GST_LOG ("Setting the playback rate to %f\n", rate);
    /*
     * Playback rates can be positive or negative depending on whether we are fast forwarding or rewinding
     * Below are the Playback rates used in our test scenarios
     * Fastforward Rates:
     * 	1) 2.0
     * 	2) 4.0
     * 	3) 16.0
     * Rewind Rates:
     * 	1) -2.0
     * 	2) -4.0
     * 	3) -16.0
     */
    /*
     * Rewind the pipeline if rate is a negative number
     */
    if (rate < 0)
    {
    	fail_unless (gst_element_seek (playbin, rate, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH,
    		     GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE, GST_SEEK_TYPE_SET, currentPosition), "Failed to set playback rate");
    }
    /*
     * Fast forward the pipeline if rate is a positive number
     */
    else
    {
    	fail_unless (gst_element_seek (playbin, rate, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, currentPosition,
    			GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE), "Failed to set playback rate");
    }
}


/********************************************************************************************************************
Purpose:               To get the current playback rate of pipeline
Parameters:
playbin [IN]          - GstElement* 'playbin' whose playback rate should be queried
Return:               - gdouble value for the current playback rate
*********************************************************************************************************************/
static gdouble getRate (GstElement* playbin)
{
    GstQuery *query;
    gdouble currentRate = 0.0;
    /*
     * Retrieve the current playback speed of the pipeline using gst_element_query()
     */
    /*
     * Create a GstQuery to retrieve the segment
     */
    query = gst_query_new_segment (GST_FORMAT_DEFAULT);
    /*
     * Query the playbin element
     */
    fail_unless (gst_element_query (playbin, query), "Failed to query the current playback rate");
    /*
     * Parse the GstQuery structure to get the current playback rate
     */
    gst_query_parse_segment (query, &currentRate, NULL, NULL, NULL);

    /*
     * Unreference the query structure
     */
    gst_query_unref (query);

    /*
     * The returned playback rate should be validated 
     */
    return currentRate;
}

/********************************************************************************************************************
Purpose:               To seek to a particular position in pipeline
Parameters:
playbin [IN]          - GstElement* 'playbin' for which the seek should be done
seekSeconds [IN]      - double value for the position to seek to
Return:               - None
*********************************************************************************************************************/
static void seek (GstElement* playbin, double seekSeconds)
{
    gint64 seekPosition = GST_SECOND * seekSeconds;
    gint64 currentPosition = GST_CLOCK_TIME_NONE;
    GstMessage *message;
    GstBus *bus;
    MessageHandlerData data;
    /*
     * Set the playback position to the seekSeconds position
     */
    fail_unless (gst_element_seek (playbin, NORMAL_PLAYBACK_RATE, GST_FORMAT_TIME, 
                                   GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seekPosition, 
                                   GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE), "Failed to seek");

    /*
     * During seek, the state of various gstreamer elements changes,
     * so we are polling the bus to wait till the bus is clear of state change events 
     * before verifying the success of seek operation. We are exiting the loop if the position change happens in between
     * or if an error/eos is recieved
     */
    bus = gst_element_get_bus (playbin);
    /*
     * Set all the required variables before polling for the message
     */
    data.terminate = FALSE;
    data.seeked = FALSE;
    data.playbin = playbin;
    data.seekPosition = seekPosition;
    data.currentPosition = GST_CLOCK_TIME_NONE;
    data.stateChanged = FALSE;

    do 
    {
        message = gst_bus_timed_pop_filtered (bus, 2 * GST_SECOND,
                                             (GstMessageType) ((GstMessageType) GST_MESSAGE_STATE_CHANGED | 
                                             (GstMessageType) GST_MESSAGE_ERROR | (GstMessageType) GST_MESSAGE_EOS |
                                             (GstMessageType) GST_MESSAGE_ASYNC_DONE ));
        /* 
         * Parse message 
         */
        if (NULL != message) 
        {
            handleMessage (&data, message);
        } 
        else 
        {
            printf ("All messages are clear. No more message after seek\n");
            break;
        }
    } while (!data.terminate && !data.seeked);
    
    /*
     * Verify that ERROR/EOS messages are not recieved
     */
    fail_unless (FALSE == data.terminate, "Unexpected error or End of Stream recieved\n");

    /*
     * Verify that SEEK message is received
     */
    fail_unless (TRUE == data.seeked, "Seek Unsuccessfull\n");

    /*
     * Verify that stateChanged message is received
     */
    fail_unless (TRUE == data.stateChanged, "State change message was not received\n");

    //Convert time to seconds
    data.currentPosition /= GST_SECOND;
    data.seekPosition /= GST_SECOND;

    printf("SEEK SUCCESSFULL :  CurrentPosition %lld seconds, SeekPosition %lld seconds\n", data.currentPosition, data.seekPosition);
    GST_LOG ("SEEK SUCCESSFULL :  CurrentPosition %lld seconds, SeekPosition %lld seconds\n", data.currentPosition, data.seekPosition);

    gst_object_unref (bus);
}

/********************************************************************************************************************
Purpose:               To change the plyabin state to play/pause
Parameters:
playbin [IN]          - GstElement* 'playbin' for which the play/pause state change should be done
pause [IN]            - bool value based on which playbin state is changed to Pause (if pause = true) or Play (if pause = false)
Return:               - None
*********************************************************************************************************************/
static void playPause (GstElement* playbin, bool pause)
{
    GstState cur_state;
    GstStateChangeReturn state_change;
    /*
     * If pause is true, set the state to GST_STATE_PAUSED otherwise set the state to GST_STATE_PLAYING
     */
    GstState state = pause?GST_STATE_PAUSED:GST_STATE_PLAYING;

    /*
     * Set the playbin state
     */
    fail_unless (gst_element_set_state (playbin, state) !=  GST_STATE_CHANGE_FAILURE, "Failed to change playbin state");
    /*
     * Ensure that pipeline state is changed correctly by retreiving the current
     * playbin state and checking if its same as the state we tried to set
     */
    do 
    {
        /* 
         * Polling for the state change to reflect with 10 ms timeout 
         */
	state_change = gst_element_get_state (playbin, &cur_state, NULL, 10000000);
    } while (state_change == GST_STATE_CHANGE_ASYNC);

    fail_unless (state_change != GST_STATE_CHANGE_FAILURE, "Failed to get current playbin state");

    fail_unless_equals_int (cur_state, state);

    printf ("Playbin state changed successfully.\nCurrent state is: %s\n", gst_element_state_get_name(cur_state));
    GST_LOG("Playbin state changed successfully.\nCurrent state: %s\n",gst_element_state_get_name(cur_state));
}


/********************************************************************************************************************
Purpose:               To perform fastforward/rewind operation on playbin
Parameters:
playbin [IN]          - GstElement* 'playbin' for which the fastforward/rewind operation should be done
rate [IN]             - gdouble value for the playback rate to be set 
timeout [IN]          - double time in seconds for which the fastforward/rewind operation should be performed
Return:               - None
*********************************************************************************************************************/
static void trickplayOperation (GstElement* playbin, gdouble rate, double timeout)
{
    gdouble currentRate = 0.0;
    bool is_av_playing = false;
    gint64 currentPosition = GST_CLOCK_TIME_NONE;

    /*
     * Playback rates can be positive or negative depending on whether we are fast forwarding or rewinding
     * Below are the Playback rates used in our test scenarios
     * Fastforward Rates:
     * 	1) 2.0
     * 	2) 4.0
     * 	3) 16.0
     * Rewind Rates:
     * 	1) -2.0
     * 	2) -4.0
     * 	3) -16.0
     */
    /*
     * For rewind operations were playback rate is negative, ensure that there is enough duration 
     * to rewind the pipeline correctly by querying the current position and checking if 
     * current position >= required duration (abs (rate) * timeout)
     */
    if (rate < 0)
    {
        /*
         * Get the current playback position
         */
        fail_unless (gst_element_query_position (playbin, GST_FORMAT_TIME, &currentPosition), 
            	     "Failed to querry the current playback position");
        /*
         * If the current position is greater than required duration
         */
        if (currentPosition < ((int)abs (rate) * timeout * GST_SECOND))
        { 
            /*
             * Seek to the required position
             */
            printf ("There is not enough duration for rewinding the pipeline, so seeking to %f before rewind\n", 
            	    ((int)abs (rate) * timeout));
            seek (playbin, ((int)abs (rate) * timeout));
        }
    }
    /*
     * Set the playbin playback rate
     */
    setRate (playbin, rate);
    /*
     * Sleep for the requested time
     */
    usleep (timeout * FCS_MICROSECONDS);
    /*
     * Retrieve the current playback rate of pipeline and verify that its same as rate
     */
    currentRate = getRate (playbin);
    fail_unless (rate == currentRate, "Failed to do set rate to %f correctly\nCurrent playback rate is: %f\n", rate, currentRate);

    /*
     * Ensure that playback is happening correctly
     */
    /*
     * Check for AV status if its enabled
     */
    if (true == checkAVStatus)
    {
        is_av_playing = check_for_AV_status();
        fail_unless (is_av_playing == true, "Video is not playing in TV");
        printf ("DETAILS: SUCCESS, Video playing successfully \n");
    }

    printf ("Successfully executed %s %dx speed for %f seconds\n", (rate > 0)?"fastforward":"rewind", (int)abs (rate), timeout); 

}

/********************************************************************************************************************
 * Purpose     	: Test to do basic initialisation and shutdown of gst pipeline with playbin element and westeros-sink
 * Parameters   : Playback url
 ********************************************************************************************************************/
GST_START_TEST (test_init_shutdown)
{
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

/********************************************************************************************************************
 * Purpose      : Test to do trickplay in the pipeline
 * Parameters   : Playback url
 ********************************************************************************************************************/
GST_START_TEST (test_trickplay)
{
    bool is_av_playing = false;
    bool firstFrameReceived = false;
    bool pause = false;
    vector<string>::iterator operationItr;
    char* operationBuffer = NULL;
    string operation;
    double operationTimeout = 10.0;
    int seekSeconds = 0;
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
     * Set playbin to PLAYING by setting boolean pasue to false
     */
    GST_FIXME( "Setting to Playing State\n");
    fail_unless (gst_element_set_state (playbin, GST_STATE_PLAYING) !=  GST_STATE_CHANGE_FAILURE);
    GST_FIXME( "Set to Playing State\n");

    /*
     * Wait for 5 seconds before verifying the playback status
     */
    sleep(5);
    /*
     * Ensure that playback is happening before starting trickplay
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
    /*
     * Iterate through the list of operations recieved as input arguments and execute each of them for the requesed operation and timeperiod
     */
    for (operationItr = operationsList.begin(); operationItr != operationsList.end(); ++operationItr) 
    {
	/*
	 * Operating string will be in operation:operationTimeout format,
	 * so split the string to retrieve operation string and timeout values
	 */   
        operationBuffer = strdup ((*operationItr).c_str());
        operation = strtok (operationBuffer, ":");
	operationTimeout = atof (strtok (NULL, ":"));

	if (!operation.empty())
	{
	        /*
	         * If the operation is to fast forward at rate 2x, set the playback rate for playbin to 2
	         */
	        if ("fastforward2x" == operation)
		{  
	            /*
		     * Fastforward the pipeline to 2
		     */
		    trickplayOperation (playbin, FASTFORWARD2x_RATE, operationTimeout);
		}
	        /*
	         * If the operation is to fast forward at rate 4x, set the Rate for playbin to 4
	         */
	        else if ("fastforward4x" == operation)
                {
	            /*
		     * Fastforward the pipeline to 4
		     */
		    trickplayOperation (playbin, FASTFORWARD4x_RATE, operationTimeout);
		}
	        /*
	         * If the operation is to fast forward at rate 16x, set the Rate for playbin to 16
	         */
	        else if ("fastforward16x" == operation)
                {
	            /*
		     * Fastforward the pipeline to 16
		     */
		    trickplayOperation (playbin, FASTFORWARD16x_RATE, operationTimeout);
		}
	        /*
	         * If the operation is to rewind at rate 2x, set the Rate for playbin to -2
	         */
	        else if ("rewind2x" == operation)
                {
	            /*
		     * Rewind the pipeline to -2
		     */
		    trickplayOperation (playbin, REWIND2x_RATE, operationTimeout);
		}
	        /*
	         * If the operation is to rewind at rate 4x, set the Rate for playbin to -4
	         */
	        else if ("rewind4x" == operation)
                { 
	            /*
		     * Rewind the pipeline to -4
		     */
		    trickplayOperation (playbin, REWIND4x_RATE, operationTimeout);
		}
	        /*
	         * If the operation is to rewind at rate 16x, set the Rate for playbin to -16
	         */
	        else if ("rewind16x" == operation)
                {
	            /*
		     * Rewind the pipeline to -16
		     */
		    trickplayOperation (playbin, REWIND16x_RATE, operationTimeout);
		}
	        /*
	         * If the operation is to do playback 
	         */
	        else if ("play" == operation)
                {
		    /*
		     * If pipeline is already in playing state with normal playback rate (1.0),
		     * just wait for operationTimeout seconds, instaed os setting the pipeline to playing state again
		     */	
		    fail_unless_equals_int (gst_element_get_state (playbin, &cur_state,
                                                                   NULL, 0), GST_STATE_CHANGE_SUCCESS);
		    if ((cur_state != GST_STATE_PLAYING) || (cur_state == GST_STATE_PLAYING && NORMAL_PLAYBACK_RATE != getRate (playbin)))
		    {
			/*
			 * Set the playbin playback rate to 1 incase trickplay modes were being executed 
			 */
			setRate (playbin, 1);
			/*
                     	 * Set the playbin state to GST_STATE_PLAYING
                         */
   		        pause = false;
	    		playPause (playbin, pause);
	    		/*
	    		 * Sleep for the requested time
	    		 */
	    		usleep (operationTimeout * FCS_MICROSECONDS);
		    }
		    /*
		     * If playback is already happening wait for the requested time
		     */
		    else
	 	    {
                        printf ("Playbin is already playing, so waiting for %f seconds\n", operationTimeout);
			usleep (operationTimeout * FCS_MICROSECONDS);
		    }
		    /*
                     * Ensure that playback is happening properly
                     */
                    /*
                     * Check for AV status if its enabled
                     */
                    if (true == checkAVStatus)
                    {
                        is_av_playing = check_for_AV_status();
                        fail_unless (is_av_playing == true, "Video is not playing in TV");
                        printf ("DETAILS: SUCCESS, Video playing successfully \n");
                    }
		}
	        /*
	         * If the operation is to pause the pipeline 
	         */
	        else if ("pause" == operation)
                {
		    /*
		     * Set the playbin state to GST_STATE_PAUSED
		     */	
		    pause = true;
	    	    playPause (playbin, pause);
	    	    /*
	    	     * Sleep for the requested time
	    	     */
	    	    usleep (operationTimeout * FCS_MICROSECONDS);
		}
	        /*
                 * If the operation is to do seek in the pipeline
                 */
                else if ("seek" == operation)
                { 
	            /*
		     * For seek operation get the third input argument which is the stream position 
		     * in seconds to which the seeking should be done
		     */
		    seekSeconds = atoi(strtok(NULL, ":"));
		    /*
		     * Seek to the requested position
		     */
	    	    seek (playbin, seekSeconds);		    
                    /*
                     * Sleep for the requested time seconds
                     */
                    usleep (operationTimeout * FCS_MICROSECONDS);
		    /*
                     * Ensure that playback is happening properly
                     */
                    /*
                     * Check for AV status if its enabled
                     */
                    if (true == checkAVStatus)
                    {
                        is_av_playing = check_for_AV_status();
                        fail_unless (is_av_playing == true, "Video is not playing in TV");
                        printf ("DETAILS: SUCCESS, Video playing successfully \n");
                    }
                    
		}
	        else
		{
		    GST_ERROR ("Invalid operation\n");
		}
	}
    }
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

    GST_INFO ("Test Case name is %s\n", tcname);
    printf ("Test Case name is %s\n", tcname);
    
    if (strcmp ("test_generic_playback", tcname) == 0)
    {
       tcase_add_test (tc_chain, test_generic_playback);
       GST_INFO ("tc %s run successfull\n", tcname);
       GST_INFO ("SUCCESS\n");
    }
    else if (strcmp ("test_play_pause_pipeline", tcname) == 0)
    {
       tcase_add_test (tc_chain, test_play_pause_pipeline);
       GST_INFO ("tc %s run successfull\n", tcname);
       GST_INFO ("SUCCESS\n");
    }
    else if (strcmp ("test_EOS", tcname) == 0)
    {
       tcase_add_test (tc_chain, test_EOS);
       GST_INFO ("tc %s run successfull\n", tcname);
       GST_INFO ("SUCCESS\n");
    }
    else if (strcmp ("test_trickplay", tcname) == 0)
    {
       tcase_add_test (tc_chain, test_trickplay);
       GST_INFO ("tc %s run successfull\n", tcname);
       GST_INFO ("SUCCESS\n");
    }
    else if (strcmp ("test_init_shutdown", tcname) == 0)
    {
       tcase_add_test (tc_chain, test_init_shutdown);
       GST_INFO ("tc %s run successfull\n", tcname);
       GST_INFO ("SUCCESS\n");
    }

    return gstPluginsSuite;
}



int main (int argc, char **argv)
{
    Suite *testSuite;
    int returnValue = 0;
    int arg = 0;
    char *operationString = NULL;
    char* operation = NULL;
    /*
     * Get TDK path
     */
    if (getenv ("TDK_PATH") != NULL)
    {
    	strcpy (TDK_PATH, getenv ("TDK_PATH"));
    }
    else
    {
    	GST_ERROR ("Environment variable TDK_PATH should be set!!!!");
    	printf ("Environment variable TDK_PATH should be set!!!!");
	returnValue = 0;
	goto exit;
    }
    if (argc == 2)
    {
    	strcpy (tcname, argv[1]);

    	GST_INFO ("\nArg 2: TestCase Name: %s \n", tcname);
    	printf ("\nArg 2: TestCase Name: %s \n", tcname);
    }
    else if (argc >= 3)
    {
        strcpy (tcname, argv[1]);
	if ((strcmp ("test_init_shutdown", tcname) == 0) || 
	    (strcmp ("test_play_pause_pipeline", tcname) == 0) || 
            (strcmp ("test_generic_playback", tcname) == 0) ||
            (strcmp ("test_EOS", tcname) == 0) ||
            (strcmp("test_trickplay", tcname) == 0))
	{
            strcpy(m_play_url,argv[2]);
            for (arg = 3; arg < argc; arg++)
            {
                if (strcmp ("checkavstatus=yes", argv[arg]) == 0)
                {
                    checkAVStatus = true;
                }
                if (strstr (argv[arg], "timeout=") != NULL)
                {
                    strtok (argv[arg], "=");
      		    play_timeout = atoi (strtok (NULL, "="));
                }
                if (strstr (argv[arg], "operations=") != NULL)
		{
		   /*
		    * The trickplay operations can be given in
		    * operations="" argument as coma separated string
		    * eg: operations=play:play_timeout,fastforward2x:timeout,seek:timeout:seekvalue
		    */
                   strtok (argv[arg], "=");
		   operationString = strtok(NULL, "=");
		   operation = strtok (operationString, ",");
                   while (operation != NULL)
		   {
		       operationsList.push_back(operation);
   		       operation = strtok (NULL, ",");
		   }
                }
            }
	}


        printf ("\nArg : TestCase Name: %s \n", tcname);
        printf ("\nArg : Playback url: %s \n", m_play_url);
    }
    else
    {
        printf ("FALIURE : Insufficient arguments\n");
        returnValue = 0;
	goto exit;
    }
    gst_check_init (&argc, &argv);
    testSuite = media_pipeline_suite ();
    returnValue =  gst_check_run_suite (testSuite, "playbin_plugin_test", __FILE__);
exit:
    return returnValue;
}
