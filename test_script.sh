DATA_SIZE="100 200 500 1000 2000"
CLUSTER_NUM="4 8"
DNA_LEN="8 32 64"
PROCESS_NUM="1 2 4 6 8 10 12"
ITERATION=300
SERVER_LIST="ghc68.ghc.andrew.cmu.edu,ghc69.ghc.andrew.cmu.edu,ghc70.ghc.andrew.cmu.edu"

echo 'generate data'
for dSize in $DATA_SIZE
   do
   for cSize in $CLUSTER_NUM
      do
      # points data
      python generaterawdata.py -c $cSize -p $dSize -o points-n$dSize-c$cSize.txt
      for dnaLen in $DNA_LEN
      do
         python generaterawdata_dna.py -c $cSize -p $dSize -l $dnaLen -o dnas-n$dSize-c$cSize-l$dnaLen.txt
      done
   done
done

# Do K-mean
echo 'seq run'
for dSize in $DATA_SIZE
   do
   for cSize in $CLUSTER_NUM
      do
      # analysis point data
      echo resultPoints-seq-n$dSize-c$cSize.txt...
      { time python kMeans_seq.py -c $cSize -i points-n$dSize-c$cSize.txt -o resultPoints-seq-n$dSize-c$cSize.txt -r $ITERATION -p;} 2> time-resultPoints-seq-n$dSize-c$cSize.txt 1> inner-resultPoints-seq-n$dSize-c$cSize.txt
      for dnaLen in $DNA_LEN
      do
         echo resultDnas-seq-n$dSize-c$cSize-l$dnaLen.txt...
         { time python kMeans_seq.py -c $cSize -i dnas-n$dSize-c$cSize-l$dnaLen.txt -o resultDnas-seq-n$dSize-c$cSize-l$dnaLen.txt -r $ITERATION -d;} 2> time-resultDnas-seq-n$dSize-c$cSize-l$dnaLen.txt 1> inner-resultDnas-seq-n$dSize-c$cSize-l$dnaLen.txt
      done
   done
done
echo 'mpi run'
for dSize in $DATA_SIZE
   do
   for cSize in $CLUSTER_NUM
      do
      # analysis point data
      for pNum in $PROCESS_NUM
         do
         echo resultPoints-mpi-n$dSize-c$cSize-p$pNum.txt...
         { time mpirun -np $pNum python kMeans_prl.py -c $cSize -i points-n$dSize-c$cSize.txt -o resultPoints-mpi-n$dSize-c$cSize-p$pNum.txt -r $ITERATION -p;} 2> time-resultPoints-mpi-n$dSize-c$cSize-p$pNum.txt 1> inner-resultPoints-mpi-n$dSize-c$cSize-p$pNum.txt
         for dnaLen in $DNA_LEN
         do
            echo resultDnas-mpi-n$dSize-c$cSize-l$dnaLen-p$pNum.txt...
            { time mpirun -np $pNum python kMeans_prl.py -c $cSize -i dnas-n$dSize-c$cSize-l$dnaLen.txt -o resultDnas-mpi-n$dSize-c$cSize-l$dnaLen-p$pNum.txt -r $ITERATION -d;} 2> time-resultDnas-mpi-n$dSize-c$cSize-l$dnaLen-p$pNum.txt 1> inner-resultDnas-mpi-n$dSize-c$cSize-l$dnaLen-p$pNum.txt
         done
      done
   done
done