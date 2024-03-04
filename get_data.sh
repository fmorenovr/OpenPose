rm -rf inputs
mkdir -p inputs

if ! command -v gdown &> /dev/null; then 
	pip install gdown 
fi

cd inputs

gdown https://drive.google.com/drive/folders/1up_ROJCHqVfndcG1to2uT6NKEJSuydTk -O ./videos --folder
gdown --fuzzy https://drive.google.com/file/d/1kD7vu_qtwUtXfzW-cembNyt4JWqQ4UWm/view?usp=sharing

cd videos

directory=$(pwd)

for file in "$directory"/*; do
    if [ -f "$file" ]; then
        echo "Processing file: $file"
        unzip $file
    fi
done
