<!DOCTYPE html>
<HTML>
	<HEAD>
		<meta HTTP-EQUIV="content-type" CONTENT="text/html; charset=UTF-8">
		<title>Annotation View</title>
		<!-----------css------------>
		<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
	</HEAD>
	<BODY style="background-color:#000000;">
	<div style="padding-top:30px;">
		<form role="form" class="form-horizontal" action = "annotation_view1.php" method="post">
			<div class="form-group">
				<label for="xml_content" class="col-sm-2 control-label"><font color="white">Input User Name:</font></label>
				<div class="col-sm-1">
					<textarea  rows="1" class="form-control" id="user_name" name="user_name"><?php if(isset($_POST['user_name'])){echo $_POST['user_name'];} ?></textarea>
				</div>
			</div>
			<div class="form-group">
				<label for="movie1_content" class="col-sm-2 control-label"><font color="white">系統說明</font></label>
				<div class="col-sm-8">
					<textarea rows="3" class="form-control" id="article" name="article" readonly>整體的系統分為兩大部分(一篇文章與對應的五篇故事情節), 標記過程中請考慮當閱讀此文章時會想看的電影, 並考慮故事情節本身描述的關係與情境!</textarea>
				</div>
			</div>
			<div class="form-group">
				<label for="movie1_content" class="col-sm-2 control-label"><font color="white">標記說明</font></label>
				<div class="col-sm-3">
					<textarea rows="1" class="form-control" id="article" name="article" readonly>5分非常適合(完全適切可相呼應)</textarea>
				</div>
			</div>
			<div class="form-group">
				<label for="movie1_content" class="col-sm-2 control-label"><font color="white"></font></label>
				<div class="col-sm-3">
					<textarea rows="1" class="form-control" id="article" name="article" readonly>4分適合(有符合但還可以更好)</textarea>
				</div>
			</div>
			<div class="form-group">
				<label for="movie1_content" class="col-sm-2 control-label"><font color="white"></font></label>
				<div class="col-sm-3">
					<textarea rows="1" class="form-control" id="article" name="article" readonly>3分還可以(關係與情境有部分可以相呼應)</textarea>
				</div>
			</div>
			<div class="form-group">
				<label for="movie1_content" class="col-sm-2 control-label"><font color="white"></font></label>
				<div class="col-sm-3">
					<textarea rows="1" class="form-control" id="article" name="article" readonly>2分不適合(不太貼切)</textarea>
				</div>
			</div>
			<div class="form-group">
				<label for="movie1_content" class="col-sm-2 control-label"><font color="white"></font></label>
				<div class="col-sm-3">
					<textarea rows="1" class="form-control" id="article" name="article" readonly>1分非常不適合(文章與劇情完全不符合)</textarea>
				</div>
			</div>
			<div class="form-group">
				<label for="user_name" class="col-sm-10 control-label"></label>
				<button type="submit" class="btn btn-default" onclick="" style="width:120px;height:40px;border:2px blue none;background-color:white;">Submit</button>
			</div>			
		</form>	
	
	</div>
	</BODY>
</HTML>


