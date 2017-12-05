argc=$#
if [ $argc -ne 2 ]; then
    echo "not param for tar_name worker"
    exit 1
fi
echo "begin >>> >>> >>>"
cd /data/zcash
rm -rf ./$1.tar.gz
wget http://www.315che.com/data/zcash/$1.tar.gz
rm -rf ./$1
tar -xzvf ./$1.tar.gz
rm -rf ./miner
ln -s /data/zcash/$1/miner /data/zcash/miner
echo "cd /data/zcash" > /data/zec.sh
echo "nohup ./miner --server cn1-zcash.flypool.org --user t1g2h1XPT4t8ag5S89FvpDHUqHLkNWJdX7b.$2 --pass x --port 3333 --cuda_devices 0 1 2 3 4 5 &" >> /data/zec.sh
chmod +x /data/zec.sh
echo ">>> >>> >>> done!"


### excute
#wget http://www.315che.com/data/zcash/upzec.sh
#cd /data/zcash
#./upzec.sh 0.3.4b s01e05_cw_gtx1070plus*5