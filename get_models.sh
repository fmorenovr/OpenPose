if ! command -v gdown &> /dev/null; then 
	pip install gdown 
fi

gdown --fuzzy https://drive.google.com/file/d/1EZeKTOttVNEW-3ms4_KOIDYYX1Gy2KtA/view?usp=drive_link

unzip models
rm models.zip
