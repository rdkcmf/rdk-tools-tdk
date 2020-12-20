#!/bin/sh
# ============================================================================
# RDK MANAGEMENT, LLC CONFIDENTIAL AND PROPRIETARY
# ============================================================================
# This file (and its contents) are the intellectual property of RDK Management, LLC.
# It may not be used, copied, distributed or otherwise  disclosed in whole or in
# part without the express written permission of RDK Management, LLC.
# ============================================================================
# Copyright (c) 2020 RDK Management, LLC. All rights reserved.
# ============================================================================
#------------------------------------------------------------------------------------------------------
# update_parser_result_string
# syntax       : update_parser_result_string "key" "val"
# description  : Method to update or append parser result string with the provided key-val pair
# parameters   : key - tag name
#              : val - parsed result
# return value : nil
#------------------------------------------------------------------------------------------------------
update_parser_result_string()
{
    [[ ! -z $PARSER_RES_STRING ]] && PARSER_RES_STRING+=","
    PARSER_RES_STRING+="\"$1\":\"$2\""
}
#------------------------------------------------------------------------------------------------------
# generate_parser_result_log
# syntax       : generate_parser_result_log "utility_name" "parser_result_string"
# description  : Method to create log file with parser result in json format
# parameters   : utility_name           - name of the test
#              : parser_result_string   - result string in key-val pair
# return value : nil
#------------------------------------------------------------------------------------------------------
generate_parser_result_log()
{
    parser_result_json="{\"utility\": \"$1\",\"values\":{$2}}"
    echo -e "$parser_result_json" > $PARSER_RES_FILE
    echo -e "Generated Json string : $parser_result_json " >> $PARSER_LOG_FILE
}
#------------------------------------------------------------------------------------------------------
# Checking Command Line Arguments
#------------------------------------------------------------------------------------------------------
# TDK log location
TDK_LOC=$TDK_PATH
TDK_LOG="$TDK_LOC/logs"
PARSER_RES_STRING=""
PARSER_LOG_FILE="$TDK_LOG/logparser-details.log"
PARSER_RES_FILE="$TDK_LOG/logparser-results.txt"
PARSER_CONFIG_XML="$TDK_LOC/HWPerf_metric_details.xml"
if [[ -f $PARSER_CONFIG_XML ]]; then
    echo -e "[INFO]: Parser configuration XML : $PARSER_CONFIG_XML\n" > $PARSER_LOG_FILE
else
    echo -e "[INFO]: Parser configuration XML : $PARSER_CONFIG_XML : not found\n" > $PARSER_LOG_FILE
    exit 0
fi
[[ -f $PARSER_RES_FILE ]] && rm -rf $PARSER_RES_FILE
UTILITY_NAME=""
UTILITY_CONF=0
argument_count=$#
if [[ $argument_count == 1 ]]; then
    UTILITY_NAME=$1
else
    echo -e "[INFO]: $0 takes exactly one argument [ test utility name ]\n" >> $PARSER_LOG_FILE
    echo "Usage : parser_script \"test_utility_name\"" >> $PARSER_LOG_FILE
    echo "Eg    : $0 \"tdk-benchmark-test\""      >> $PARSER_LOG_FILE
    exit 0
fi
#------------------------------------------------------------------------------------------------------
# Getting List of tdk Test Utilities
#------------------------------------------------------------------------------------------------------
index=0
declare -a tdk_test_utilities
tdk_utility_list=$(echo `xmllint --xpath "//parserConfig/tdkTestUtility/@name" $PARSER_CONFIG_XML 2>/dev/null` | sed 's/^ //' | sed 's/name=//' | sed 's/name=/,/g' | sed 's/\"//g' | tr "," "\n")
echo -e "[INFO]: List of Utilities configured in parser xml:" >> $PARSER_LOG_FILE
while read -r utility; do
    tdk_test_utilities[$index]=$utility
    s_no=`expr $index + 1`
    echo "$s_no. ${tdk_test_utilities[$index]}" >> $PARSER_LOG_FILE
    index=`expr $index + 1`
done <<< "$tdk_utility_list"
#------------------------------------------------------------------------------------------------------
# Checking whether parser config for provided test utility is available
#------------------------------------------------------------------------------------------------------
for ((index=0; index<${#tdk_test_utilities[@]}; index++)); do
    if [[ $UTILITY_NAME == ${tdk_test_utilities[$index]} ]]; then
        UTILITY_CONF=1
        echo -e "\n[INFO]: Selected Test Utility : $UTILITY_NAME\n" >> $PARSER_LOG_FILE
        break
    fi
done
#------------------------------------------------------------------------------------------------------
# Parsing the tdk Test Utility custom log
#------------------------------------------------------------------------------------------------------
if [[ $UTILITY_CONF -eq 1 ]]; then
    parser_index=1
    parser_sec_count=`xmllint --xpath 'count(//parserConfig/tdkTestUtility[@name='"\"$UTILITY_NAME\""']/parser_section)' $PARSER_CONFIG_XML`
    while [[ $parser_index -le $parser_sec_count ]]; do
        log_file_path=`xmllint --xpath 'string(//parserConfig/tdkTestUtility[@name='"\"$UTILITY_NAME\""']/parser_section['"$parser_index"']/log_file_path)'  $PARSER_CONFIG_XML`
        parser_info_count=`xmllint --xpath 'count(//parserConfig/tdkTestUtility[@name='"\"$UTILITY_NAME\""']/parser_section['"$parser_index"']/parser_info)' $PARSER_CONFIG_XML`
        echo -e "[INFO]: Parser Section  : $parser_index" >> $PARSER_LOG_FILE
        echo -e "----------------------------"            >> $PARSER_LOG_FILE
        echo -e "Custom Log File Name : $log_file_path\n" >> $PARSER_LOG_FILE
        value_index=1
        while [[ $value_index -le $parser_info_count ]]; do
            key=`xmllint --xpath 'string(//parserConfig/tdkTestUtility[@name='"\"$UTILITY_NAME\""']/parser_section['"$parser_index"']/parser_info['"$value_index"']/tag)' $PARSER_CONFIG_XML`
            cmd=`xmllint --xpath 'string(//parserConfig/tdkTestUtility[@name='"\"$UTILITY_NAME\""']/parser_section['"$parser_index"']/parser_info['"$value_index"']/cmd)' $PARSER_CONFIG_XML`
            val=`eval "$cmd" 2>/dev/null`
            value_index=`expr $value_index + 1`
            echo -e "Tag Name   : $key "   >> $PARSER_LOG_FILE
            echo -e "Parser Cmd : $cmd "   >> $PARSER_LOG_FILE
            echo -e "Parsed Val : $val \n" >> $PARSER_LOG_FILE
            update_parser_result_string "$key" "$val"
        done
        parser_index=`expr $parser_index + 1`
    done
    generate_parser_result_log "$UTILITY_NAME" "$PARSER_RES_STRING"
    echo "SUCCESS" > $TDK_LOC/logs/postreq_details.log
else
    echo -e "\n[INFO]: Selected Test Utility : $UTILITY_NAME : config not found" >> $PARSER_LOG_FILE
    echo "FAILURE" > $TDK_LOC/logs/postreq_details.log
fi

