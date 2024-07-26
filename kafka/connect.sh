ssh -L 9092:localhost:9092 tunnel@128.2.204.215 -NTf -i '/kafka/id_rsa'
ps -eaf | grep ssh 
