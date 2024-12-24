# LamoniAI


There is a total of 62,181 pages in the Lamoni Chronicle Achieve. Because you can extract the GETpdf URL from the https://lamoni.advantage-preservation.com website you don’t have to store the pdfs on a drive you can just have the Docling converter pipeline access the GETpdf URL.

GPU
The computer that I’ve been using has an NVIDIA® GeForce RTX™ 3080 GPU in it. 
It has Memory 10GB GDDR6X, 8704 cuda cores. 

Files

UrlSaver.py gets the GETpdf urls and names of each pdf from the Lamoni preservation website. It then saves those pieces of information in GetPDFUrls.csv in two columns. Every GETpdf url takes around 1.23 seconds to save. For the entire Lamoni archive this would take around 21 hours give or take depending on the response time of the Lamoni archive. 

CSVDigitalizer.py extracts the GETpdf and name from each row int he the GetPDFUrls.csv file. Then using the Docling library to digitalizes the newspaper pdf using the GETpdf url. Finally, it names the scan with the corresponding name from GetPDFUrls.csv and saves it to the RawDigitalizedScans directory. Each file takes on average 94 seconds to digitalize on my Mac but thankfully Docling can leverage GPUs to make this digitalization go faster.

DirectWebDegitalizer.py Does what the above two files do but in one python file and without using an intermediate csv file to store the GETpdf urls and names.
      
Bugs
For some reason the UrlSaver.py file will execute for a while and then pause for some reason. The code doesn’t crash or anything which is frustrating. Might have something to do with my laptop that I’m running it on or worst case the actual website itself having a hiccup in its API. 

UrlSaver had an error at url 49544: 

File "/Users/jackflickinger/Desktop/GracelandGPT/UrlSaver.py", line 125, in <module>
    fileName = CreateFileName(url)
               ^^^^^^^^^^^^^^^^^^^
  File "/Users/jackflickinger/Desktop/GracelandGPT/UrlSaver.py", line 45, in CreateFileName
    fileName = raw_iframe.split(start)[1].split(end)[0]
               ~~~~~~~~~~~~~~~~~~~~~~~^^^
IndexError: list index out of range


In the CSVDigitalizer.py and presumably the DirectWebDegitalizer.py the code gets to about 17-18 files digitalized and then throws this error.

Encountered an error during conversion of document cdda6d73de21cedd29c2b8236c39ddc3d3943e97f3458233fad68baac0d0e58c:
Traceback (most recent call last):

  File "/opt/anaconda3/lib/python3.12/site-packages/docling/pipeline/base_pipeline.py", line 149, in _build_document
    for p in pipeline_pages:  # Must exhaust!

  File "/opt/anaconda3/lib/python3.12/site-packages/docling/pipeline/base_pipeline.py", line 116, in _apply_on_pages
    yield from page_batch

  File "/opt/anaconda3/lib/python3.12/site-packages/docling/models/page_assemble_model.py", line 59, in __call__
    for page in page_batch:

  File "/opt/anaconda3/lib/python3.12/site-packages/docling/models/table_structure_model.py", line 93, in __call__
    for page in page_batch:

  File "/opt/anaconda3/lib/python3.12/site-packages/docling/models/layout_model.py", line 281, in __call__
    for page in page_batch:

  File "/opt/anaconda3/lib/python3.12/site-packages/docling/models/easyocr_model.py", line 67, in __call__
    result = self.reader.readtext(im)
             ^^^^^^^^^^^^^^^^^^^^^^^^

  File "/opt/anaconda3/lib/python3.12/site-packages/easyocr/easyocr.py", line 456, in readtext
    horizontal_list, free_list = self.detect(img,
                                ^^^^^^^^^^^^^^^^

  File "/opt/anaconda3/lib/python3.12/site-packages/easyocr/easyocr.py", line 321, in detect
    text_box_list = self.get_textbox(self.detector,
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/opt/anaconda3/lib/python3.12/site-packages/easyocr/detection.py", line 95, in get_textbox
    bboxes_list, polys_list = test_net(canvas_size, mag_ratio, detector,
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/opt/anaconda3/lib/python3.12/site-packages/easyocr/detection.py", line 46, in test_net
    y, feature = net(x)
                 ^^^^^^

  File "/opt/anaconda3/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1736, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/opt/anaconda3/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1747, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/opt/anaconda3/lib/python3.12/site-packages/torch/nn/parallel/data_parallel.py", line 173, in forward
    return self.module(*inputs, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/opt/anaconda3/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1736, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/opt/anaconda3/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1747, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/opt/anaconda3/lib/python3.12/site-packages/easyocr/craft.py", line 75, in forward
    y = torch.cat([y, sources[4]], dim=1)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

RuntimeError: MPS backend out of memory (MPS allocated: 4.20 GB, other allocations: 4.09 GB, max allowed: 9.07 GB). Tried to allocate 810.00 MB on private pool. Use PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 to disable upper limit for memory allocations (may cause system failure).

Traceback (most recent call last):
  File "/Users/jackflickinger/Desktop/GracelandGPT/CSVDigitalizer.py", line 56, in <module>
    result = converter.convert(url)
             ^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/pydantic/validate_call_decorator.py", line 60, in wrapper_function
    return validate_call_wrapper(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/pydantic/_internal/_validate_call.py", line 96, in __call__
    res = self.__pydantic_validator__.validate_python(pydantic_core.ArgsKwargs(args, kwargs))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/document_converter.py", line 170, in convert
    return next(all_res)
           ^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/document_converter.py", line 189, in convert_all
    for conv_res in conv_res_iter:
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/document_converter.py", line 220, in _convert
    for item in map(
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/document_converter.py", line 264, in _process_document
    conv_res = self._execute_pipeline(in_doc, raises_on_error=raises_on_error)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/document_converter.py", line 283, in _execute_pipeline
    conv_res = pipeline.execute(in_doc, raises_on_error=raises_on_error)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/pipeline/base_pipeline.py", line 52, in execute
    raise e
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/pipeline/base_pipeline.py", line 44, in execute
    conv_res = self._build_document(conv_res)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/pipeline/base_pipeline.py", line 162, in _build_document
    raise e
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/pipeline/base_pipeline.py", line 149, in _build_document
    for p in pipeline_pages:  # Must exhaust!
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/pipeline/base_pipeline.py", line 116, in _apply_on_pages
    yield from page_batch
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/models/page_assemble_model.py", line 59, in __call__
    for page in page_batch:
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/models/table_structure_model.py", line 93, in __call__
    for page in page_batch:
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/models/layout_model.py", line 281, in __call__
    for page in page_batch:
  File "/opt/anaconda3/lib/python3.12/site-packages/docling/models/easyocr_model.py", line 67, in __call__
    result = self.reader.readtext(im)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/easyocr/easyocr.py", line 456, in readtext
    horizontal_list, free_list = self.detect(img, 
                                 ^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/easyocr/easyocr.py", line 321, in detect
    text_box_list = self.get_textbox(self.detector, 
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/easyocr/detection.py", line 95, in get_textbox
    bboxes_list, polys_list = test_net(canvas_size, mag_ratio, detector,
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/easyocr/detection.py", line 46, in test_net
    y, feature = net(x)
                 ^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1736, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1747, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/torch/nn/parallel/data_parallel.py", line 173, in forward
    return self.module(*inputs, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1736, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1747, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/anaconda3/lib/python3.12/site-packages/easyocr/craft.py", line 75, in forward
    y = torch.cat([y, sources[4]], dim=1)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: MPS backend out of memory (MPS allocated: 4.20 GB, other allocations: 4.09 GB, max allowed: 9.07 GB). Tried to allocate 810.00 MB on private pool. Use PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 to disable upper limit for memory allocations (may cause system failure).

