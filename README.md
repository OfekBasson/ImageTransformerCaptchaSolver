# Image Transformer Captcha Solver
## Overview
This project presents a code for solving captcha from the Israeli real-estate tax website.
**The project is divided into 3 parts and most of it is presented inside the jupyter notebook attached to this repo (inside "/src" folder):**
1. Fetching 2,500 captchas from the website, crop each captcha to 4 parts (4 digits) and save digit images (10,000 total) inside "/Data" folder.
*This part and the fetched data is not presented in the jupyter notebook*.
![Example of 4 seperated digits](/images/digits.png)
2. Training and evaluating vision transformer (As explained in the article "AN IMAGE IS WORTH 16X16 WORDS").
Final accuracy is 98.7%.
![Training Results (20 epochs)](/images/training_results.png)
3. Online captcha "hacking" demonstration.

## Installation guide
For installation - follow those steps:
1. Run the following commands in your terminal:
```bash
git clone https://github.com/OfekBasson/ImageTransformerCaptchaSolver.git

cd ImageTransformerCaptchaSolver

pip install -r requirements.txt
```
2. Enter /src/captcha_solver.ipynb
3. Run all 




