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
package com.comcast.rdk;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.net.Inet6Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.util.Enumeration;
import java.util.Properties;
import java.util.regex.Pattern;

import org.codehaus.groovy.grails.validation.routines.InetAddressValidator;
import org.springframework.util.StringUtils;

public class InetUtility {

	private static final Pattern IPV6_STD_PATTERN = Pattern.compile("^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$");
	
	public static String TM_IPV4_ADDRESS = "";
	public static String TM_IPV6_ADDRESS = "";
	/**
	  * Check whether it is IPv6 address or not.
	  * 
	  * @param ipAddress
	  *            Ipv6 address.
	  * @return True if given ip address is Ipv6.
	  */
	 public static boolean isIPv6Address(final String ipAddress) {
	  return IPV6_STD_PATTERN.matcher(ipAddress).matches();
	 }
	 
	public static String getDefaultNetworkInterface(File configFile, String type) {
		try {
			Properties prop = new Properties();
			if (configFile.exists()) {
				InputStream is = new FileInputStream(configFile);
				prop.load(is);
				String value = prop.getProperty(type);
				if (value != null && !value.isEmpty()) {
					return value;
				}
			}else{
				System.out.println("DBG :::: No Config File !!! ");
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;
	}
	
	public static String getIPAddress(File configFile , String ipType){
		String ipAddress = "";

		if (ipType.equals(Constants.IPV4_INTERFACE)) {
			ipAddress = TM_IPV4_ADDRESS;
		} else if (ipType.equals(Constants.IPV6_INTERFACE)) {
			ipAddress = TM_IPV6_ADDRESS;
		}

		if (ipAddress == null || ipAddress.isEmpty()) {
			try {
				String nwInterface = getDefaultNetworkInterface(configFile,
						ipType);
				if (nwInterface != null) {
					NetworkInterface netFace = NetworkInterface
							.getByName(nwInterface);
					if (netFace != null) {
						Enumeration ae = netFace.getInetAddresses();
						while (ae.hasMoreElements()) {
							InetAddress address = (InetAddress) ae
									.nextElement();
							String hostAddr = address.getHostAddress();
							if (ipType.equals(Constants.IPV6_INTERFACE) && hostAddr.contains(Constants.PERCENTAGE)) {
								hostAddr = hostAddr.substring(0,hostAddr.indexOf(Constants.PERCENTAGE));
							}
							if ((ipType.equals(Constants.IPV4_INTERFACE) && InetAddressValidator.getInstance().isValidInet4Address(hostAddr))
									|| (ipType.equals(Constants.IPV6_INTERFACE) && address instanceof Inet6Address && StringUtils.countOccurrencesOf(hostAddr,Constants.COLON) > 4)) {
								if (!address.isLoopbackAddress() && !address.isLinkLocalAddress()) {
									ipAddress = hostAddr;
									if (ipType.equals(Constants.IPV4_INTERFACE)) {
										TM_IPV4_ADDRESS = ipAddress;
									} else if (ipType.equals(Constants.IPV6_INTERFACE)) {
										TM_IPV6_ADDRESS = ipAddress;
									}
									break;
								}
							}
						}
					}
				}
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		return ipAddress;
	}
	 
	 
}
