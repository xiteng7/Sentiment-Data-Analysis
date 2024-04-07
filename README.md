# Sentiment-Data-Analysis
A data processing and analysis pipeline created to scratch video, audio, and financial data from public sources. Analyze sentiment information extracted from video and audio files based on an open source model. Run regression analysis of public companies' financial metrics on sentiment data, and calculate alpha returns.

**Process**
1. Download video files using YouTube links and process them into audio files uing 'download script.py'.
2. Generate sentiment results of video and audio files using 'video model.py' and 'audio model with try and except.py' respectively.
3. Download and process financial data using 'get yf data modified.py'.
4. Download relevant fundamental financial data from WRDS API.
5. Compute regressional results using 'alpha_calculation.py'.

**References**:

Video Algo Model: https://github.com/Nirmalvekariya/Video-Sentiment-Analysis

Audio Algo Model: https://github.com/CyberMaryVer/speech-emotion-webapp
