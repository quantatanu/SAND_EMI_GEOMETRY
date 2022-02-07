#! /bin/bash


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
        sleep 1
        echo ""
        echo ""
    fi





    # SAND OPT 3RPC
    if [[ "${@}" == *"opt3RPC"* ]];
    then
    gegede-cli duneggd/Config/WORLDggd.cfg \
               duneggd/Config/ND_Hall_Air_Volume.cfg \
               duneggd/Config/ND_Hall_Rock.cfg \
               duneggd/Config/SAND_MAGNET.cfg \
               duneggd/Config/SAND_ECAL.cfg \
               duneggd/Config/SAND_EMI_RPC.cfg \
               -w World -o ${outdir}/SAND_opt3RPC${tags}.gdml
                read -r -p "Do you want to display \"${outdir}/SAND_opt3RPC${tags}.gdml\"? [y/N] " response
                case "$response" in
                    [yY][eE][sS]|[yY]) 
                        echo "./geodisplay_gdml \"${outdir}/SAND_opt3RPC${tags}.gdml)\""; 
                        ./geodisplay_gdml "${outdir}/SAND_opt3RPC${tags}.gdml"; 
                        ;;
                    *)
                        echo "Exiting...";
                        ;;
                esac
    fi


}


main "$@"
