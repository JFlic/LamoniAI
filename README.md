# LamoniAI - RAG Model

There is a total of 62,181 pages in the Lamoni Chronicle Achieve. Because you can extract the GETpdf URL from the https://lamoni.advantage-preservation.com website you don’t have to store the pdfs on a drive you can just have the Docling converter pipeline access the GETpdf URL. I plan on making a RAG model based on this youtube video. https://www.youtube.com/watch?app=desktop&v=qN_2fnOPY-M. 

# GPU
The computer that I’ve been using has an NVIDIA® GeForce RTX™ 3080 GPU in it. 
It has Memory 10GB GDDR6X, 8704 cuda cores. 

# Files
UrlSaver.py gets the GETpdf urls and names of each pdf from the Lamoni preservation website. It then saves those pieces of information in GetPDFUrls.csv in two columns. Every GETpdf url takes around 1.23 seconds to save. For the entire Lamoni archive this would take around 21 hours give or take depending on the response time of the Lamoni archive. 

CSVDigitalizer.py extracts the GETpdf and name from each row int he the GetPDFUrls.csv file. Then using the Docling library to digitalizes the newspaper pdf using the GETpdf url. Finally, it names the scan with the corresponding name from GetPDFUrls.csv and saves it to the RawDigitalizedScans directory. Each file takes on average 94 seconds to digitalize on my Mac but thankfully Docling can leverage GPUs to make this digitalization go faster.

DirectWebDegitalizer.py Does what the above two files do but in one python file and without using an intermediate csv file to store the GETpdf urls and names.

Spellchecker.py uses the spellchecker python library to make spelling and grammer corrects to the files in RawDigitalizedScans folder and then saves the new files to SpellcheckedScans.

GetPDFUrls.csv is where the Get pdf urls are stored (example: https://lamoni.advantage-preservation.com/viewer/GetPdfFile?105873767) and the name the file will eventually be called after it goes through the digitalizer. 

# Folders
The Prototypes folder holds different prototypes that were used to make the current pipeline. I saved them just in case.

RawDigitalizedScans folder holds all the raw mark down files that haven't been spell checked yet.

The SpellcheckedScans folder holds the files that have been spell checked by the Spellchecker.py
      
# Bugs
For some reason the UrlSaver.py file will execute for a while and then pause for some reason. The code doesn’t crash or anything which is frustrating. Might have something to do with my laptop that I’m running it on or worst case the actual website itself having a hiccup when the GETpdf url is being created. 

UrlSaver had an error at url 49544: 

File "/Users/jackflickinger/Desktop/GracelandGPT/UrlSaver.py", line 125, in <module>
    fileName = CreateFileName(url)
               ^^^^^^^^^^^^^^^^^^^
  File "/Users/jackflickinger/Desktop/GracelandGPT/UrlSaver.py", line 45, in CreateFileName
    fileName = raw_iframe.split(start)[1].split(end)[0]
               ~~~~~~~~~~~~~~~~~~~~~~~^^^
IndexError: list index out of range

***************************************************************************************************

In the CSVDigitalizer.py and presumably the DirectWebDegitalizer.py on my Mac the code gets to about 17-18 files digitalized and then throws a memory error. I'll either have to use batches and clear my cache or just use the NVIDIA® GeForce RTX™ 3080 GPU at Graceland for this part unfortunately.

Encountered an error during conversion of document, the error is as follows:

RuntimeError: MPS backend out of memory (MPS allocated: 4.20 GB, other allocations: 4.09 GB, max allowed: 9.07 GB). Tried to allocate 810.00 MB on private pool. Use PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 to disable upper limit for memory allocations (may cause system failure).

***************************************************************************************************