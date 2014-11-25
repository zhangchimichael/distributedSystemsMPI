python generaterawdata.py -c 5 -p 300 -o points.txt
python kMeans_seq.py -c 5 -i points.txt -o resultPoints.txt -r 100 -p
mpirun -np 4 python kMeans_prl.py -c 5 -i points.txt -o resultPoints.txt -r 100 -p
python plotClusteredPoints.py -i resultPoints.txt

python generaterawdata_dna.py -c 5 -p 300 -l 10 -o strands.txt
python kMeans_seq.py -c 5 -i strands.txt -o resultStrands.txt -r 100 -d 
mpirun -np 4 python kMeans_prl.py -c 5 -i strands.txt -o resultStrands.txt -r 100 -d 



cat resultPoints.txt | awk -F '\t' '{cnt[$2]+=1;} END {for (i in cnt) {print i,cnt[i]}}'
cat resultStrands.txt | awk -F '\t' '{cnt[$2]+=1;} END {for (i in cnt) {print i,cnt[i]}}'
