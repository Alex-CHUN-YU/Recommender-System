	<div style="padding-top:30px;">
		<form role="form" class="form-horizontal">
			<div class="form-group">
				<label for="movie1_content" class="col-sm-2 control-label"><font color="white">Movie1:</font></label>
			<div class="col-sm-6">
				<textarea rows="6" class="form-control" id="movie1" name="movie1" readonly><?php if(isset($movie1[0])){echo $movie1[0];} ?></textarea>
				<iframe id="video1" class="video-display col-md-6 col-sm-12" src="<?php if(isset($movie1[1])){echo $movie1[1];} ?>" frameborder="0"></iframe>
			</div>
			</div>			
		</form>	
		<form role="form" class="form-horizontal">
			<div class="form-group">
				<label for="movie2_content" class="col-sm-2 control-label"><font color="white">Movie2</font></label>
			<div class="col-sm-6">
				<textarea rows="6" class="form-control" id="movie2" name="movie2" readonly><?php if(isset($movie2[0])){echo $movie2[0];} ?></textarea>
				<iframe id="video2" class="video-display col-md-6 col-sm-12" src="<?php if(isset($movie2[1])){echo $movie2[1];} ?>" frameborder="0"></iframe>
			</div>
			</div>			
		</form>	
		<form role="form" class="form-horizontal">
			<div class="form-group">
				<label for="movie3_content" class="col-sm-2 control-label"><font color="white">Movie3</font></label>
			<div class="col-sm-6">
				<textarea rows="6" class="form-control" id="movie3" name="movie3" readonly><?php if(isset($movie3[0])){echo $movie3[0];} ?></textarea>
				<iframe id="video3" class="video-display col-md-6 col-sm-12" src="<?php if(isset($movie3[1])){echo $movie3[1];} ?>" frameborder="0"></iframe>			
			</div>
			</div>			
		</form>	
		<form role="form" class="form-horizontal">
			<div class="form-group">
				<label for="movie4_content" class="col-sm-2 control-label"><font color="white">Movie4:</font></label>
			<div class="col-sm-6">
				<textarea rows="6" class="form-control" id="movie4" name="movie4" readonly><?php if(isset($movie4[0])){echo $movie4[0];} ?></textarea>
				<iframe id="video4" class="video-display col-md-6 col-sm-12" src="<?php if(isset($movie4[1])){echo $movie4[1];} ?>" frameborder="0"></iframe>
			</div>
			</div>			
		</form>	
		<form role="form" class="form-horizontal">
			<div class="form-group">
				<label for="movie5_content" class="col-sm-2 control-label"><font color="white">Movie5:</font></label>
			<div class="col-sm-6">
				<textarea rows="6" class="form-control" id="movie5" name="movie5" readonly><?php if(isset($movie5[0])){echo $movie5[0];} ?></textarea>
				<iframe id="video5" class="video-display col-md-6 col-sm-12" src="<?php if(isset($movie5[1])){echo $movie5[1];} ?>" frameborder="0"></iframe>				
			</div>
			</div>			
		</form>	
	</div>
