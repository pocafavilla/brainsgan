# brainsgan
Trying to use GANs to increase the resolution of MRI scans for my internship at Juelich research center

This is an experiment that I started mostly out of curiosity and because I thought the application was much needed. 
(Apart from MRIs it can probably be used as well to reduce dangerous Xray radiation & speed up the measuring process)
SRGANs have been applied to normal images and vastly outperformed conventional upscaling methods so I thought I'd give it a shot.

I do not want to obfuscate the fact that I am relying to a large extend on other people's code and especially research papers. 
The first results look promising (see res.png)

For this project I modified https://github.com/brade31919/SRGAN-tensorflow slightly to get 2x upsampling because the MRI-scans are too small for 4x upsampling (which was used in the original project.
