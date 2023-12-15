# Image Transformer Captcha Solver
## Overview
This project presents a code for solving captcha from the Israeli real-estate tax website.
**The project is divided into 3 parts and most of it is presented inside the jupyter notebook attached to this repo (inside "/src" folder):**
1. Fetching 2,500 captchas from the website, crop each captcha to 4 parts (4 digits) and save digit images (10,000 total) inside "/Data" folder.
*This part and the fetched data is not presented in the jupyter notebook*.
<img src="/images/digits.png" alt="Example of 4 separated digits" width="400"/>
2. Training and evaluating vision transformer (As explained in the article "AN IMAGE IS WORTH 16X16 WORDS").
Final accuracy is 98.7%.
<img src="/images/training_results.png" alt="Example of 4 separated digits" width="400"/>
3. Online captcha "hacking" demonstration.

## Demonstration GIF:
![](/images/demonstration_gif.gif)
