#!/bin/sh
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
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

getUptime()
{
    uptime_str=`uptime | tr -d "," " "`
    uptime_counter=0
    days=""
    hours=""
    minutes=""
    
    days=`echo "$uptime_str" | grep -o '[0-9]* day' | cut -d ' ' -f1`
    hours_string=`echo "$uptime_str" | grep -o '[0-9][0-9]*:[0-9][0-9]* load average' | cut -d ' ' -f1`
    if [ -n "$hours_string" ]
    then
        hours=`echo $hours_string | cut -d':' -f1`
        minutes=`echo $hours_string | cut -d':' -f2`
    else
        minutes=`echo "$uptime_str" | grep -o '[0-9]* min' | cut -d ' ' -f1`
    fi
    
    # Convert uptime to minutes
    if [ -n "$days" ]
    then
        uptime_counter="$(($days * 1440))"
    fi
    
    if [ -n "$hours" ]
    then
        counter="$(($hours * 60))"
        uptime_counter="$(($uptime_counter + $counter))"
    fi
    
    if [ -n "$minutes" ]
    then
        minutes=`echo "$minutes" | sed 's/0*//'`
        if [ -z "$minutes" ]
        then
            minutes=0
        fi
        uptime_counter="$(($uptime_counter + $minutes))"
    fi
    
    echo "$uptime_counter"
}



touch /opt/logs/file_copy_logs.log






timestamp=`date +%Y-%m-%d_%H-%M-%S`
echo "$timestamp: Started execution of tar_logs.sh" > /opt/tar_logs.out
rm -rf /opt/zipfile.txt

LineNumber=44
curent_uptime=$(getUptime)
reboot_flag="True"
if [ -f /opt/logs/.lastuptime.txt ] && [ -n "$curent_uptime" ]
then
    prev_uptime=`cat /opt/logs/.lastuptime.txt`
    if [ -n "$prev_uptime" ]
    then
        echo "previous uptime : $prev_uptime" >> file_copy_logs.log
        if [ "$curent_uptime" -lt "$prev_uptime" ]
        then
            reboot_flag="True"
        else
            reboot_flag="False"
            #time_diff="$(($curent_uptime - $prev_uptime))"
        fi
    else
        reboot_flag="True"
    fi    
else
    reboot_flag="True"
    prev_uptime=0
fi
echo "$curent_uptime" > /opt/logs/.lastuptime.txt

result=`/sbin/ifconfig | grep -c 'wan:1'`
directory=$1
#Change the working directroy to /opt/logs/
cd /opt/logs/
echo "Starting zip operation $(date)" >> file_copy_logs.log
#Remove old folder if any
if [ -d $directory ]
then
    rm -rf $directory
    echo "removing  directory $directory" >> file_copy_logs.log	
fi

#Create a new directory with name as MAC Id
mkdir -p $directory
sleep 1
echo "created directory $directory" >> file_copy_logs.log	

zip_filename="$directory.tgz"
echo "zipfilename $zip_filename"
rm -rf $zip_filename #Delete old zip file

rm -rf /opt/logs/logfile_list

CheckPreviousLogFlag="True"
LineNumber=96

scp_path="/opt/cpetool/Delia_TempDir/"

#if [ -f /version.txt ]
#then
#    xg1_result=`grep -c 'imagename:MX' /version.txt`
#    if [ $xg1_result -eq 1 ]
#    then
#        scp_path="/mnt/Vivid/ScpLogs/"
#    fi
#fi


if [ -f ocap_scpindex_tm ]
then
    echo "ocap_scpindex_tm exists" >> file_copy_logs.log	
    cp ocap_scpindex_tm mpeos_ocap_scpindex_tm.txt
    lastlinetext=`head -n 1 ocap_scpindex_tm`
    if [ -n "$lastlinetext" ]
    then
        retval=`awk "/$lastlinetext/" ocapri_log.txt`
        touch /opt/logs/logfile_list
        foundfile="ocapri_log.txt"
            
        if [ -z "$retval" ]
        then
            echo "ocapri_log.txt" >> /opt/logs/logfile_list
            for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
            do
                filename="ocapri_log.txt.$i" 
                if [ -f $filename ]
                then
		      echo "ocapri file : $filename" >> file_copy_logs.log
                    retval=`awk "/$lastlinetext/" $filename`
                    if [ -z "$retval" ]
                    then
                        echo "$filename" >> /opt/logs/logfile_list
                        continue
                    else
                        foundfile="$filename"
                        CheckPreviousLogFlag="False"
                        LineNumber=123
                        break
                    fi            
                else
                    break
                fi        
            done
        else
            CheckPreviousLogFlag="False"
            LineNumber=132
        fi      
        linecount=`cat ocapri_log.txt| wc -l`
        if [ $linecount -lt 100 ]
        then
            linecount=$linecount
        else
            linecount=100
        fi
        ocapindex=`tail -n $linecount ocapri_log.txt | cut -d ' ' -f1 | grep -E '^[0-9]{6}-[0-9]{2}:[0-9]{2}:[0-9]{2}.' | tail -n 1`
        #If ocapindex is Null, cut first field of last line 
        if [ -z "$ocapindex" ]
        then
            ocapindex=`tail -n 1 ocapri_log.txt | cut -d ' ' -f1`
        fi
        if [ "$lastlinetext" != "$ocapindex" ]
        then            
            echo $ocapindex > ocap_scpindex_tm
            linenumber=`awk "/$lastlinetext/ {print NR}" $foundfile | head -n 1`
            tail -n +$linenumber $foundfile > onehour_ocapri_log.txt
            echo "onehour_ocapri_log.txt" >> /opt/logs/logfile_list
        fi
    else
        CheckPreviousLogFlag="False"
        LineNumber=151
        #rm -rf ocap_scpindex_tm
        ls /opt/logs/ocapri_log.txt* | sort -r | grep -v tgz | grep -v 'tar.gz' | grep -v 'mpeos-main' > /opt/logs/logfile_list
        linecount=`cat ocapri_log.txt| wc -l`
        if [ $linecount -lt 100 ]
        then
            linecount=$linecount
        else
            linecount=100
        fi
        ocapindex=`tail -n $linecount ocapri_log.txt | cut -d ' ' -f1 | grep -E '^[0-9]{6}-[0-9]{2}:[0-9]{2}:[0-9]{2}.' | tail -n 1`
        #If ocapindex is Null, cut first field of last line 
        if [ -z "$ocapindex" ]
        then
            ocapindex=`tail -n 1 ocapri_log.txt | cut -d ' ' -f1`
        fi
        echo $ocapindex > ocap_scpindex_tm
    fi    
else
    echo "ocap_scpindex_tm doesnot exist" >> file_copy_logs.log
    CheckPreviousLogFlag="False"
    LineNumber=166
    ret=`grep -s -c -i "Vendor Serial Number" ocapri*.txt ocapri_log.txt.? | awk -F: '{ s+=$2 } END { print s }'`
    if [ "$ret" == "1" ]
    then
        #ls /opt/logs/ocapri_log.txt* | sort -r | grep -v tgz | grep -v 'tar.gz' > /opt/logs/logfile_list
        ls /opt/logs/ocapri_log.txt* | sort -r | grep -v tgz | grep -v 'tar.gz' | grep -v 'mpeos-main' > /opt/logs/logfile_list
    else
        #ls /opt/logs/PreviousLogs_backup/*-ocapri_log*.txt | sort -r > /opt/logs/logfile_list
        #ls /opt/logs/ocapri_log.txt* | sort -r | grep -v tgz >> /opt/logs/logfile_list
        ls /opt/logs/ocapri_log.txt* | sort -r | grep -v tgz | grep -v 'tar.gz' | grep -v 'mpeos-main' > /opt/logs/logfile_list
    fi
    linecount=`cat ocapri_log.txt| wc -l`
    if [ $linecount -lt 100 ]
    then
        linecount=$linecount
    else
        linecount=100
    fi
    ocapindex=`tail -n $linecount ocapri_log.txt | cut -d ' ' -f1 | grep -E '^[0-9]{6}-[0-9]{2}:[0-9]{2}:[0-9]{2}.' | tail -n 1`
    #If ocapindex is Null, cut first field of last line 
    if [ -z "$ocapindex" ]
    then
        ocapindex=`tail -n 1 ocapri_log.txt | cut -d ' ' -f1`
    fi
    echo $ocapindex > ocap_scpindex_tm
fi

timestamp=`date "+%m-%d-%y-%I-%M%p"`
# Tar and upload ocapri_log.txt
for item in `cat /opt/logs/logfile_list`
do
    #copy file to directory
    echo "copying file $item to directory $directory " >> file_copy_logs.log   	
    cp $item $directory/
    item=`basename $item`

    if [ -f "$directory/$item" ]
    then
        mv $directory/$item $directory/${timestamp}_${item}
    fi
done

rm -rf onehour_ocapri_log.txt

if [ -f /rename_rotated_logs.sh ]
then
    sh /rename_rotated_logs.sh $directory/${timestamp}_ocapri_log.txt
fi
echo "removed logs"

if [ -f /opt/logs/messages.txt ]
then
    messagefile_list=""
    if [ -f messages_scpindex.txt ]
    then
	echo "messages_scpindex.txt exists" >> file_copy_logs.log  	
        message_lastlinetext=`head -n 1 messages_scpindex.txt`
        linenumberoffset=`tail -n 1 messages_scpindex.txt`
        if [ -n "$message_lastlinetext" ]
        then
            retval=`awk "/$message_lastlinetext/" messages.txt`
            message_foundfile="messages.txt"
            if [ -z "$retval" ]
            then
                messagefile_list="messages.txt"
                for i in 0 1 2 3 4 5 6 7 8 9 10
                do
                    filename="messages.txt.$i"
                    if [ -f "$filename" ]
                    then
			echo "messages file : $filename" >> file_copy_logs.log
                        retval=`awk "/$message_lastlinetext/" $filename`
                        if [ -z "$retval" ]
                        then
                            messagefile_list="$messagefile_list $filename"
                            continue
                        else
                            message_foundfile="$filename"
                            break
                        fi
                    else
                        break
                    fi        
                done
            fi
            linenumber=`awk "/$message_lastlinetext/ {print NR}" $message_foundfile | head -n 1`
            if [ -n "$linenumber" ]
            then
                linenumber=$(($linenumber + $linenumberoffset))
            fi
            tail -n +$linenumber $message_foundfile > onehour_messages.txt
            messagefile_list="$messagefile_list onehour_messages.txt"        
        else
            #cp /opt/logs/messages.txt $directory/
            #if [ -f "$directory/messages.txt" ]
            #then
            #    mv $directory/messages.txt $directory/${timestamp}_messages.txt
            #fi
            messagefile_list=`ls messages.txt*`
        fi
    else
        #cp /opt/logs/messages.txt $directory/
        #if [ -f "$directory/messages.txt" ]
        #then
        #    mv $directory/messages.txt $directory/${timestamp}_messages.txt
        #fi
        messagefile_list=`ls messages.txt*`
    fi
    messageindex=`tail -n 50 /opt/logs/messages.txt | cut -d ' ' -f1-4 | grep -E '^[aA-zZ]{3}\s*[0-9]{1,2} [0-9]{2}:[0-9]{2}:[0-9]{2}' | tail -n 1`
    #messageindex=`tail -n 50 messages.txt | cut -d ' ' -f1-3 | grep -E '^[aA-zZ]{3} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}' | tail -n 1`
    echo "$messageindex" > messages_scpindex.txt
    index_count=`grep -c "$messageindex" messages.txt`
    echo "$index_count" >> messages_scpindex.txt    

    #copy message file to the MAC directory    
    for item in $messagefile_list
    do
        cp /opt/logs/$item $directory/
        mv $directory/$item $directory/${timestamp}_${item}
    done
    
    rm -rf onehour_messages.txt
fi


if [ -f /opt/logs/receiver.log ]
then
    echo "receiver.log exists"
    receiverfile_list=""
    if [ -f receiver_scpindex.txt ]
    then
        lastlinetext=`head -n 1 receiver_scpindex.txt`
        echo "lastlinetext : $lastlinetext" >>  file_copy_logs.log
        prev_recv_scpindex=$lastlinetext
        if [ -n "$lastlinetext" ]
        then
            retval=`awk "/$lastlinetext/" receiver.log`
            receiver_foundfile="receiver.log"
            
            if [ -z "$retval" ]
            then
                receiverfile_list="receiver.log"
                for i in 1 2 3 4 5 6 7 8 9 10
                do
                    filename="receiver.log.$i"
                    if [ -f "$filename" ]
                    then
			echo "receiver log : $filename"
                        retval=`awk "/$lastlinetext/" $filename`
                        if [ -z "$retval" ]
                        then
                            receiverfile_list="$receiverfile_list $filename"
                            continue
                        else
                            receiver_foundfile="$filename"
                            break
                        fi
                    else
                        break
                    fi        
                done
            fi
            
            linenumber=`awk "/$lastlinetext/ {print NR}" $receiver_foundfile | head -n 1`
            echo "linenumber : $linenumber"
            if [ -z "$linenumber" ]
            then
                linenumber=1
            fi
            reciverindex=`awk 'NF{s=$0}END{print s}' receiver.log | awk '{print $1" " $2}'`
            if [ "$lastlinetext" != "$reciverindex" ]
            then
                tail -n +$linenumber $receiver_foundfile > onehour_receiver.log
                if [ "$receiver_foundfile" == "receiver.log" ]
                then
                    receiverfile_list=""
                fi
                receiverfile_list="$receiverfile_list onehour_receiver.log" 
            fi
        else
            #rm -rf receiver_scpindex.txt
            #cp /opt/logs/receiver.log $directory/
            #if [ -f "$directory/receiver.log" ]
            #then
            #    mv $directory/receiver.log $directory/${timestamp}_receiver.log
            #fi    
            receiverfile_list=`ls receiver.log*`
            echo "receiverfile_list : $receiverfile_list"
            reboot_flag="False"
        fi    
    else
        #cp /opt/logs/receiver.log $directory/
        #if [ -f "$directory/receiver.log" ]
        #then
        #    mv $directory/receiver.log $directory/${timestamp}_receiver.log
        #fi
        receiverfile_list=`ls receiver.log*`
    fi
    #tail -n 1 receiver.log | cut -d ' ' -f1-2 > receiver_scpindex.txt
    #Get last non blank line
    awk 'NF{s=$0}END{print s}' receiver.log | cut -d ' ' -f1-2 > receiver_scpindex.txt
    
    #copy receiver file to the MAC directory    
    for item in $receiverfile_list
    do
        cp /opt/logs/$item $directory/
        mv $directory/$item $directory/${timestamp}_${item}
    done
    
    rm -rf onehour_receiver.log
fi

#get top output
top -b -n 1 > $directory/${timestamp}_toplog.txt

# Copy ocap_scpindex_tm value
if [ -f ocap_scpindex_tm ]
then
	echo "ocap_scpindex_tm 2 exists"
    index=`cat ocap_scpindex_tm`
    echo "$index" >> $directory/${timestamp}_toplog.txt    
    echo "CheckPreviousLogFlag = $CheckPreviousLogFlag" >> $directory/${timestamp}_toplog.txt
    echo "reboot_flag = $reboot_flag" >> $directory/${timestamp}_toplog.txt
else
    echo "ocap_scpindex_tm not found" >> $directory/${timestamp}_toplog.txt
    echo "CheckPreviousLogFlag = $CheckPreviousLogFlag" >> $directory/${timestamp}_toplog.txt
    echo "reboot_flag = $reboot_flag" >> $directory/${timestamp}_toplog.txt
fi

#get dmesg output
dmesg  > $directory/${timestamp}_dmesg.txt

if [ -f /version.txt ]
then
    cp /version.txt $directory/
    if [ -f "$directory/version.txt" ]
    then
        mv $directory/version.txt $directory/${timestamp}_version.txt
    fi    
fi

uptime=`uptime | tr -d "," " "`
echo "uptime = $uptime" > $directory/${timestamp}_misc.txt
echo "added uptime"

# if [ $result -eq 0 ]
# then
    # estbip_address=`/sbin/ifconfig wan | nice awk '/inet addr:/' | tr -s ' ' | cut -d ' ' -f3 | sed -e 's/addr://g'`
    # if [ -z "$estbip_address" ]
    # then
        # estbip_address=`/sbin/ifconfig bcm0 | nice awk '/inet addr:/' | tr -s ' ' | cut -d ' ' -f3 | sed -e 's/addr://g'`
    # fi
    # if [ -z "$estbip_address" ]
    # then
        # estbip_address=`/sbin/ifconfig pci0 | nice awk '/inet addr:/' | tr -s ' ' | cut -d ' ' -f3 | sed -e 's/addr://g'`
    # fi
# else
    # estbip_address=`/sbin/ifconfig wan:1 | nice awk '/inet/' | tr -s ' ' | cut -d ' ' -f3 | sed -e 's/addr://g'`
# fi    
estbip_address=`/sbin/ifconfig wan:1 | nice awk '/inet/' | tr -s ' ' | cut -d ' ' -f3 | sed -e 's/addr://g'`
echo "estbip = $estbip_address" >> $directory/${timestamp}_misc.txt

if [ -f /version.txt ]
then
    echo "version.txt exists"  	
    imgname=`cat /version.txt | grep -i 'imagename'`
    imgname=`echo $imgname | sed 's/=/:/g'`
else
    imgname="UNKNOWN"
fi

if [ -n "$imgname" ] && [ "$imgname" != "UNKNOWN" ]
then
    firmware=`echo $imgname | cut -d ':' -f2`
else
    if [ -f /version.txt ]
    then
        firmware=`cat /version.txt | egrep '(PARKER_SI)|(PARKER_X1)|(PAC_XRE)' | head -n 1`
    else
        firmware='UNKNOWN'
    fi
fi
echo "version = $firmware" >> $directory/${timestamp}_misc.txt

if [ -f /version.txt ]
then
    generation_date=`cat /version.txt | nice awk '/Generated on/' | head -n 1`
else
    generation_date='UNKNOWN'
fi
echo "GenerationDate = $generation_date" >> $directory/${timestamp}_misc.txt

if [ -f /version.txt ]
then
    comment=`cat /version.txt | nice awk '/Comment/'`
else
    comment=""
fi
echo "Comment = $comment" >> $directory/${timestamp}_misc.txt


rm -rf mpeos_ocap_scpindex_tm.txt

if [ $result -eq 0 ]
then
    folder=`ps -ef | grep mpeos-main | grep -v grep | head -n 1 | awk '{print $2}'`
else
    folder=`ps | grep mpeos-main | grep -v grep | head -n 1 | awk '{print $1}'`
fi
if [ -d "/proc/$folder/task/" ]
then
    thread_count=`ls -l /proc/$folder/task/ | wc -l`
else
    thread_count="REPORT_ERROR"
fi
echo "ThreadCount = $thread_count" >> $directory/${timestamp}_misc.txt


reboot_count=`find /opt/logs  -type d -mtime -2 |grep [0-9]|wc -l`
echo "RebootCount = $reboot_count" >> $directory/${timestamp}_misc.txt

DVR_Space_Usage=`du -h /opt/data/OCAP_MSV/0/0/DEFAULT_RECORDING_VOLUME/dvr/chunks/ | awk '{print $1}'`
echo "DVR_Space_Usage = $DVR_Space_Usage" >> $directory/${timestamp}_misc.txt

#NumberOfRecordings=`grep "Number of recordings found" /opt/logs/ocapri_log.txt* | tail -n 1`
#echo "NumberOfRecordings = $NumberOfRecordings" >> $directory/${timestamp}_misc.txt

RMF_STREAMER_MEM_USAGE=`top -n 1 | awk '/rmfStreamer/' | awk '{print $6}'`
RMF_STREAMER_CPU_USAGE=`top -n 1 | awk '/rmfStreamer/' | awk '{print $7}'`
RECEIVER_MEM_USAGE=`top -n 1 | awk '/Receiver/' | awk '{print $6}'`
RECEIVER_CPU_USAGE=`top -n 1 | awk '/Receiver/' | awk '{print $7}'`

echo "RMF_STREAMER_MEM_USAGE = $RMF_STREAMER_MEM_USAGE" >> $directory/${timestamp}_misc.txt
echo "RMF_STREAMER_CPU_USAGE = $RMF_STREAMER_CPU_USAGE" >> $directory/${timestamp}_misc.txt
echo "RECEIVER_MEM_USAGE = $RECEIVER_MEM_USAGE" >> $directory/${timestamp}_misc.txt
echo "RECEIVER_CPU_USAGE = $RECEIVER_CPU_USAGE" >> $directory/${timestamp}_misc.txt


#writing files in directory to file_copy_logs.log
ls -lh $directory >> file_copy_logs.log

#If directory is not empty
if [ "$(ls -A $directory)" != "" ]
then
    #Compress the file
    echo "compressing directory" >>  file_copy_logs.log	
    tar -czf $zip_filename $directory
    
    sleep 30

    echo "directory zipping complete"	
    timestamp=`date +%Y-%m-%d_%H-%M-%S`
    echo "$timestamp: Compressed log files to $zip_filename" >> /opt/tar_logs.out 

    #Delete the directory
    rm -rf $directory
    echo "removed directory $directory" >>  file_copy_logs.log
    rm -rf /opt/zipfile.txt    
    echo "$zip_filename" > /opt/zipfile.txt
else
    timestamp=`date +%Y-%m-%d_%H-%M-%S`
    echo "$timestamp: Directory $directory is empty" >> /opt/tar_logs.out
fi
#retries=3
if [ -f "$zip_filename" ]
then
    chmod 777 $zip_filename
    echo "File created $zip_filename" >> /opt/tar_logs.out 2>&1

else
    timestamp=`date +%Y-%m-%d_%H-%M-%S`
    echo "$timestamp: No $zip_filename file" >> /opt/tar_logs.out 2>&1   
fi

#rm -rf /opt/zipfile.txt
sleep 2
echo "$zip_filename" > /opt/zipfile.txt
echo "Operation completed $(date)" >> file_copy_logs.log

