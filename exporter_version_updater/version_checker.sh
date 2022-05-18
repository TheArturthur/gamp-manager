#!/bin/bash

if [ "$EUID" -ne 0 ]
then
    echo "Please run as root/sudo!"
    exit 1
fi

source ./config.sh

version_regex="v[[:digit:]]+(\.[[:digit:]]+)+"

function get_latest_repository_version {
    curl -s https://github.com/$1/$2/releases/ > $webs_dir/$2_releases.html
    
    # For non latest releasers:
    #if [[ $2 == "oracle_exporter" ]]
    #then
    #    version=$(cat webs/$2_releases.html | grep -A20 -m1 "href=\"/$1/$2/releases/tag/" | sed -E '/releases\/tag\/.*/!d' | sed -E 's/.*href="//g' | sed -E 's/[" |">].*//g' | sed -E 's/.*tag\///g')
    #else

        version_type=$(cat webs/$2_releases.html | grep -A8 -m1 "href=\"/$1/$2/releases/latest\"" | sed '2,8d' | sed -E 's/.*href="//g' | sed -E 's/[" |">].*//g' | awk 'NR < 2')

        if [[ $version_type =~ .*releases/latest ]]
        then
            version=$(cat webs/$2_releases.html | grep -A8 -m1 "href=\"/$1/$2/releases/latest\"" | sed '2,8d' | sed -E 's/.*href="//g' | sed -E 's/[" |">].*//g' | awk 'NR > 1' | sed -E 's/.*tree\///g')
        fi
    #fi
    
    repo_version=$version
}

function get_local_version {
    
    local_version=""
    for exporter_dir in $(ls $common_exporters_dir)
    do
        if [[ $exporter_dir = $1 ]]
        then
            local_version=$($common_exporters_dir/$exporter_dir/bin/$exporter_dir --version 2>&1 > /dev/null | cut -d',' -f 2 | cut -d'(' -f 1 | sed '2,4d' | cut -d'+' -f 1 | sed -E 's/version /v/g' | sed -E 's/ //g')
            break
        fi
    done

    if ! [[ $local_version =~ $version_regex ]]
    then
        local_version="Could not get '$1' local version!"
        echo -e "\e[31mERROR: $local_version \e[0m\n"
    else
        echo -e "\e[32mRepository version is: $repo_version, whereas local version is: $local_version \e[0m\n"
    fi
}

function set_custom_metric {
    if [[ $local_version = $repo_version ]]
    then
        echo -e "cbgi_cm_versioning{exporter=\"$1\",repo_version=\"$repo_version\",local_version=\"$local_version\"} 1" >> $cm_file 
    else
        echo -e "cbgi_cm_versioning{exporter=\"$1\",repo_version=\"$repo_version\",local_version=\"$local_version\"} 0" >> $cm_file
    fi
}

mkdir -p $webs_dir
> $cm_file
while IFS="" read -r exporter || [ -n "$exporter" ]
do
    IFS=" " read -ra exporter_array <<< "$exporter"
    echo "Getting ${exporter_array[0]}/${exporter_array[1]} versions..."
    
    get_latest_repository_version $exporter
    get_local_version ${exporter_array[1]}

    if [[ $local_version =~ $version_regex ]] && [[ $repo_version =~ $version_regex ]]
    then
        set_custom_metric ${exporter_array[1]}
    fi
done < $exporters_file
unset IFS
