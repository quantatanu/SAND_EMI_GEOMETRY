#! /bin/bash


# example run:
# ./build_ND.sh opt3RPC -C -O $(date +"%Y%m%d%H%M%S")       # where -C invokes a compilation and whatever comes after -O is added as a tag to the output gdml file name


curdir=$(pwd);
outdir="${curdir}/OUTPUT/GDML/";



main (){

    reset;
    echo "---------------------------------------"
    if [[ "${@}" == *"-O"* ]]
    then
        tags=$(echo "${@}" | awk -F '-O' '{print $2}' | sed 's/\ /_/g');
    else 
        tags="";
    fi

    if [[ "${@}" == *"-C"* ]] || [[ "${@}" == *"-compile"* ]]
    then
        echo "You have chosen to compile, compiling...."
        sudo python3 setup.py develop
        echo ""
        echo ""
    fi





    # SAND OPT 3RPC
    if [[ "${@}" == *"opt3RPC"* ]];
    then
        output="${outdir}/SAND_opt3RPC${tags}.gdml"
        gegede-cli duneggd/Config/WORLDggd.cfg \
                   duneggd/Config/ND_Hall_Air_Volume.cfg \
                   duneggd/Config/ND_Hall_Rock.cfg \
                   duneggd/Config/SAND_MAGNET.cfg \
                   duneggd/Config/SAND_ECAL.cfg \
                   duneggd/Config/SAND_EMI_RPC.cfg \
                   -w World -o $output
                read -r -p "Do you want to display \"$output\"? [y/N] " response
                case "$response" in
                    [yY][eE][sS]|[yY]) 
                        echo "./geodisplay_gdml \"$output\""; 
                        ./geodisplay_gdml "$output"; 
                        ;;
                    *)
                        echo "Exiting...";
                        ;;
                esac
                read -r -p "Do you want to delete the file: \"$output\"? [y/N] " response
                case "$response" in
                    [yY][eE][sS]|[yY]) 
                        echo "deleting \"$output\" ..."; 
                        echo "rm -rf \"$output\""; 
                        rm -rf "$output"; 
                        ;;
                    *)
                        echo "";
                        ;;
                esac

    fi


}


main "$@"
