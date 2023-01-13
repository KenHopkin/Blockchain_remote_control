geth --http --http.corsdomain="*" --http.api web3,eth,debug,personal,net,txpool,admin --http.addr=0.0.0.0 --vmdebug --datadir devnode --allow-insecure-unlock --nodiscover > log.txt 2>&1 &
