set -o errexit
set -o pipefail
set -o nounset
shopt -s failglob
set -o xtrace

export DEBIAN_FRONTEND=noninteractive

apt-get update

apt-get install -y software-properties-common

add-apt-repository ppa:deadsnakes/ppa

apt-get update

apt-get install -y git python3.5 python3.6 python3.7

curl -O https://bootstrap.pypa.io/get-pip.py
python get-pip.py

pip install tox

# ensure tox is available
tox --version
