# Automated-Hip-Morphology-Measurements
Automatically calculate the acetabular depth-width ratio, the acetabular index, the alpha angle, the center edge angle, the extrusion index, the neck-shaft angle and the triangular index on anterior-posterior hip DXA scans.


This information is to guide the use of the attached scripts.
A description and validation of the scripts within 13 year olds is provided in the article:
"Automated Radiographic Hip Morphology Measurements: An Open-Access Method" by F. Boel et al.
Please credit this paper when using (any of) these scripts within research.

*This program is free software: Copyright 2023 Fleur Boel

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


1) Landmark points on the femur and acetabulum are needed to run these scripts. The points can be 
generated using the BoneFinder® software (www.bone-finder.com; The University of Manchester, UK). An 
automatic search model for automated landmark point placement for 13 year olds is availble from the BoneFinder
website. A description of the landmark point placement can be found in the description paper mentioned 
above.

2) The point and image files used should be stored in their own folders. The landmark point files should
be in the same format as the example_pointfile.txt. Additionally, the imagelist should be in the same 
format as the example_imglist.txt.

3) For the image file, the assumtion is made that the origin is at the top left corner of the image.

3) All scripts where written using Python 3 and are best opened using a Python editor like Spyder.

4) Please note that specific landmark points are used in all scripts.


If you need any further help or advice, or if you want to collabirate, please email f.boel@erasmusmc.nl
