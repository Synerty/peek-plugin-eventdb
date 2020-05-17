#!/usr/bin/env bash


# remove the git index
[ -f .git/index ] && rm .git/index || true

rm -rf dist *egg-info || true

# Remove compile generated javascript
find ./ -name '__pycache__' -exec rm -rf {} \; || true
find ./ -type f -not -name '.git' -name "*.js" -exec rm {} \; || true
find ./ -type f -not -name '.git' -name "*.js.map" -exec rm {} \; || true


set nounset
set errexit

function replace {
    from=$1
    to=$2

    for d in `find ./ -depth -type d`
    do
        new=`echo $d | sed "s/$from/$to/g"`
        [ "$d" != "$new" ] && mv $d $new
    done

    for f in `find ./ -type f`
    do
        new=`echo $f | sed "s/$from/$to/g"`
        [ "$f" != "$new" ] && mv $f $new
    done

    for f in `find ./ -type f -not -name '.git' -not -name 'rename_plugin.sh'`
    do
        sed -i "s/$from/$to/g" $f
    done

}

# RENAME THE PLUGIN
replace "_livedb"  "_eventdb"
replace "livedb_" "eventdb_"

replace "-livedb"  "-eventdb"
replace "livedb-" "eventdb-"

replace "_LIVEDB" "_EVENTDB"
replace "-LIVEDB" "-EVENTDB"

replace "LiveDB" "EventDB"
replace "LiveDb" "EventDB"
replace "liveDb" "eventdb"
replace "livedb" "eventdb"

## RENAME THE STRING INT OBJECT
#replace "_string_int"  "_thing_one"
#replace "string_int_"  "thing_one_"
#
#replace "-string-int" "-thing-one"
#replace "string-int-" "thing-one-"
#
#replace "STRING_INT" "THING_ONE"
#replace "STRING-INT" "THING-ONE"
#
#replace "StringInt" "ThingOne"
#replace "stringInt" "thingOne"
#
#replace "String Int" "Thing One"
