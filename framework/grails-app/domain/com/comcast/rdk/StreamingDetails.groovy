/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
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
package com.comcast.rdk

/**
 * Domain class which holds the streaming details
 * @author sreejasuma
 *
 */

class StreamingDetails {

    /**
     * Stream Id
     */
    String streamId
	
    /**
     * Channel Type : The channel is either HD or SD
     */
    ChannelType channelType

    /**
     * Audio Format : Either ac3/mp3/wav/aac
     */
    AudioFormat audioFormat

    /**
     * Video Format : Either mpeg2/mpeg4/h.264
     */
    VideoFormat videoFormat

	/**
	 * Indicates the group name which the device belongs
	 */
	Groups groups
	
    static constraints = {
        streamId(nullable:false, blank:false, maxSize:64, unique:true)   
        channelType(nullable:false, blank:false)
        audioFormat(nullable:false, blank:false)
        videoFormat(nullable:false, blank:false)
		groups(nullable:true, blank:true)
    }
    
    
    @Override
    String toString() {
        return streamId ?: 'NULL'
    }

	static mapping = {
		datasource 'ALL'
	}
}
