##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
#########################################################################
#!/usr/bin/perl -w

use strict;
use warnings;
use CGI;
use diagnostics;
use CGI qw(:standard);

use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;

#The size of the file must be within this value.
$CGI::POST_MAX = 1024 * 5000;

#By default the image will get uploaded as TDKScreenShot.png. If you want to upload with your own name,
#provide the name at the end of URL like "?filename=Test.png"
my @values = split(/&/,$ENV{QUERY_STRING});
my($fieldname, $data);
$data = "TDKScreenShot.png";
foreach my $i (@values) {
    ($fieldname, $data) = split(/=/, $i);
}

########USER SHOULD CONFIGURE THIS##########
#Give the path where the file should get uploaded
my $path_to_upload = "";

my $query = new CGI;
my $file_to_upload = $query->param("image");

$file_to_upload = $data;
my $file = $query->param('POSTDATA');
open ( FILEUPLOAD, ">$path_to_upload/$file_to_upload" ) or die "$!";
binmode FILEUPLOAD;
print FILEUPLOAD $file;
close FILEUPLOAD;
print $query->header ( );
print <<END_HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Thanks!</title>
<style type="text/css"> img {border: none;} </style>
</head>
<body>
<p>Image you uploaded:</p>
<p><img src="/upload/$file_to_upload" alt="Photo" /></p>
</body>
</html>
END_HTML
