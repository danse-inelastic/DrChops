<div id="bd">
<div class="yui-g">


<div class="rst-doc">


${ h.form(h.url(action='upload'), multipart=True) }
<h1>Convert LRMECS data file in binary format to ascii format</h1>
<p>
Upload lrmecs data file in binary format: 
${ h.file_field('uploaded_file') } <br />
</p>
<p></p>
<p>
${ h.submit('Submit') }
</p>
${ h.end_form() }


</div> <!--rst-doc-->


</div>
</div>
