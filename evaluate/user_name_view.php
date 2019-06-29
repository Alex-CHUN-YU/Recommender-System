	<div style="padding-top:30px;">
		<form role="form" class="form-horizontal">
			<div class="form-group">
				<label for="movie1_content" class="col-sm-2 control-label"><font color="white">User Name:</font></label>
			<div class="col-sm-1">
				<textarea rows="1" class="form-control" id="username" name="username" readonly><?php if(isset($_POST['user_name'])){echo $_POST['user_name'];} ?></textarea>
			</div>
			</div>			
		</form>	
	</div>