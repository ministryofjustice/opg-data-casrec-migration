mkdir -p data
mkdir -p anon_data

for i in `aws s3 ls {{INSERT S3 ADDRESS HERE}} | awk '{print $2}' | awk -F'/' '{print $1}'`; do aws s3 cp {{INSERT S3 ADDRESS HERE}}/$i/$i.csv ./data ; done

apt-get update
apt-get -y install python3

python3 -m venv ./venv





