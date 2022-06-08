#! /bin/bash


# example run:
# ./build_ND.sh opt3RPC -C -O "tags"       # where -C invokes a compilation and whatever comes after -O is added as a tag to the output gdml file name


curdir=$(pwd);
outdir="${curdir}/OUTPUT/GDML/";



main (){

    reset;
    time_stamp=$(date +"%Y-%m-%d_%Z")
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
        output="${outdir}/SAND_opt3RPC_${time_stamp}${tags}.gdml"
        gegede-cli duneggd/Config/WORLDggd.cfg \
                   duneggd/Config/ND_Hall_Air_Volume.cfg \
                   duneggd/Config/ND_Hall_Rock.cfg \
                   duneggd/Config/ND_ElevatorStruct.cfg \
                   duneggd/Config/SAND_MAGNET.cfg \
                   duneggd/Config/SAND_INNERVOLOPT2.cfg \
                   duneggd/Config/SAND_EMI_RPC.cfg \
                   duneggd/Config/SAND_ECAL.cfg \
                   duneggd/Config/SAND_STT.cfg \
                   duneggd/Config/SAND_GRAIN.cfg \
                   duneggd/Config/ND_CraneRailStruct1.cfg \
                   duneggd/Config/ND_CraneRailStruct2.cfg \
                   duneggd/Config/ND_HallwayStruct.cfg \
                   duneggd/Config/ND_CryoStruct.cfg \
                   duneggd/Config/ND-GAr/ND-GAr-SPYv3_noTPC.cfg \
                   duneggd/Config/ND-GAr/ND-GAr-SPYv3.cfg \
                   duneggd/Config/ArgonCube/ArgonCubeCryostat.cfg \
                   duneggd/Config/ArgonCube/ArgonCubeDetector.cfg \
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
                echo -e "\e[31m"
                read -r -p "\e[31m Do you want to delete the file: \"$output\"\e[0m? [y/N] " response
                echo -e "\e[0m"
                case "$response" in
                    [yY][eE][sS]|[yY]) 
                        echo -e "\e[31m"
                        echo "deleting \"$output\" ..."; 
                        echo "rm -rf \"$output\""; 
                        rm -rf "$output"; 
                        echo -e "\e[0m"
                        ;;
                    *)
                        echo "";
                        ;;
                esac

    fi









    # JUST EMI

    if [[ "${@}" == *"justEMI"* ]];
    then
        output="${outdir}/SAND_justEMI_${time_stamp}${tags}.gdml"
        gegede-cli duneggd/Config/JUSTEMI/WORLDggd.cfg \
                   duneggd/Config/JUSTEMI/ND_Hall_Air_Volume.cfg \
                   duneggd/Config/JUSTEMI/ND_Hall_Rock.cfg \
                   duneggd/Config/JUSTEMI/SAND_MAGNET.cfg \
                   duneggd/Config/JUSTEMI/SAND_EMI_RPC.cfg \
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
                echo -e "\e[31m"
                read -r -p "\e[31m Do you want to delete the file: \"$output\"\e[0m? [y/N] " response
                echo -e "\e[0m"
                case "$response" in
                    [yY][eE][sS]|[yY]) 
                        echo -e "\e[31m"
                        echo "deleting \"$output\" ..."; 
                        echo "rm -rf \"$output\""; 
                        rm -rf "$output"; 
                        echo -e "\e[0m"
                        ;;
                    *)
                        echo "";
                        ;;
                esac

    fi




















}


main "$@"
