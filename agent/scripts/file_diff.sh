#!/bin/sh
file_compdir=/opt/TDK/file_comparision
orginalpack_dir=$file_compdir/orginalpack
tdkv_dir=/media/apps/tdk-v
rdm_download_dir=/media/apps/rdm/downloads/tdk-v/

if [ -d "$orginalpack_dir" ]; then rm -Rf $orginalpack_dir; fi
mkdir -p $orginalpack_dir
mkdir -p $file_compdir/log_files
cd $rdm_download_dir
tar -xf tdk-v-pkg.tar -C $orginalpack_dir
cd $orginalpack_dir
mkdir tdkgen
mkdir tdkadv
mkdir tdksm
mkdir combined
mv ./tdk_1.99-r0_mips32el.ipk tdkgen
mv ./tdkadvanced_1.99-r0_mips32el.ipk tdkadv
mv ./tdksm_1.99-r0_mips32el.ipk tdksm
cd tdkgen; ar -x tdk_1.99-r0_mips32el.ipk; mkdir tdkgen_extracted; tar -xf data.tar.gz -C tdkgen_extracted; cd tdkgen_extracted
cp -p usr/ ../../combined -r
cp -p var/ ../../combined -r
cp -p lib/ ../../combined -r
cd ../../tdkadv; ar -x tdkadvanced_1.99-r0_mips32el.ipk; mkdir tdkadv_extracted; tar -xf data.tar.gz -C tdkadv_extracted; cd tdkadv_extracted
cp -p usr/ ../../combined -r
cp -p var/ ../../combined -r
cd ../../tdksm; ar -x tdksm_1.99-r0_mips32el.ipk; mkdir tdksm_extracted; tar -xf data.tar.gz -C tdksm_extracted; cd tdksm_extracted
cp -p usr/ ../../combined -r
cp -p var/ ../../combined -r
cd $orginalpack_dir/combined
find . -type f | grep -vE "httpcode|tdk-v_cpemanifest|file_lists" | xargs md5sum  > ../unsorted_file_lists.txt
cd $orginalpack_dir
sort unsorted_file_lists.txt >  sorted_org_file_lists.txt
cd $tdkv_dir
find . -type f | grep -vE "httpcode|tdk-v_cpemanifest|file_lists" | xargs md5sum > $orginalpack_dir/unsorted_rdm_file_lists.txt
cd $orginalpack_dir
sort unsorted_rdm_file_lists.txt >  sortd_rdm_file_lists.txt
noof_orgfile=`cat sorted_org_file_lists.txt | wc -l`
echo "No.of TDK files in $rdm_download_dir folder: $noof_orgfile"
noof_rdmfiles=`cat sortd_rdm_file_lists.txt | wc -l`
echo "No.of TDK files in $tdkv_dir folder: $noof_rdmfiles"
newfiles_added=`diff -Naur sorted_org_file_lists.txt sortd_rdm_file_lists.txt | grep  "^\+" | grep -v '+++' | cut -d "+" -f2`
echo $newfiles_added
cd $file_compdir/log_files
cur_time=$(date "+%H%M%d%h%y")
touch result_$cur_time
if [ -z "$newfiles_added" ]
then
      echo "\$newfiles_added is NULL" >> result_$cur_time
          echo "No new file got created or affected "  >> result_$cur_time
else
      echo "New files created (or) affected  are: " >> result_$cur_time
          echo "$newfiles_added" >> result_$cur_time
fi
cp $orginalpack_dir/sorted_org_file_lists.txt rdm_download_files_$cur_time.txt
cp $orginalpack_dir/sortd_rdm_file_lists.txt  media_apps_tdkv_files_$cur_time.txt
rm -rf $orginalpack_dir
