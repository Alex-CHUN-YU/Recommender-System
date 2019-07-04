<!DOCTYPE html>
<?php
	session_start();
	$root_path = "./";
	include($root_path . 'config.php');
?>
<?php
	$root_path = "./";
	include('search.php');
	// if(isset($_POST['id']) and !empty($_POST['id'])) {
	// 	echo "<script> alert('ID Exist!'); </script>";
	// }else{
	// 	echo "<script> alert('NO ID!'); </script>";
	// }
	if(isset($_POST['user_name']) and !empty($_POST['user_name'])){
		for ($id = 1; $id <= 60; $id++) {
			$DisList = query_id($id);
			if (query_user_score($_POST['user_name'], $DisList[0], $DisList[1])) {
				if($id == 60) {?>
					<script>url="annotation_view1.php";window.location.href="annotation_view2.php";</script>
				<?php
				}
				continue;
			}
			if (isset($_POST['score1']) and !empty($_POST['score1']) and isset($_POST['score2']) and !empty($_POST['score2']) and isset($_POST['score3']) and !empty($_POST['score3']) and isset($_POST['score4']) and !empty($_POST['score4']) and isset($_POST['score5']) and !empty($_POST['score5'])) {
				insert_score($_POST['user_name'], $DisList[0], $DisList[1], $_POST['score1'], $_POST['score2'], $_POST['score3'], $_POST['score4'], $_POST['score5']);
				$_POST['score1'] = "";
				$_POST['score2'] = "";
				$_POST['score3'] = "";
				$_POST['score4'] = "";
				$_POST['score5'] = "";
				if($id == 60) {?>
					<script>url="annotation_view1.php";window.location.href="annotation_view2.php";</script>
				<?php
				}
				continue;
			} else {
				echo "<script> alert('請評分喔!'); </script>";
			}
			echo $id;
			// include_once($root_path . 'user_name_view.php'); // the user data form
			$article = query_article($DisList[1]);
			if(isset($article[0]) and !empty($article[0])) {
				include_once($root_path . 'article_view.php'); // the user data form
				$movie1 = query_movie($DisList[2]);
				$movie2 = query_movie($DisList[3]);
				$movie3 = query_movie($DisList[4]);
				$movie4 = query_movie($DisList[5]);
				$movie5 = query_movie($DisList[6]);
				if(isset($movie1[0]) and !empty($movie1[0])) {
					include_once($root_path . 'movie_view.php'); // the user data form
					break;
				} else {
					echo "<script> alert('未有 movie1 !'); </script>";
				}
			} else {
				echo "<script> alert('未有 article ! 或 已存在'); </script>";
			}			
		}
		// }
	}else{
		echo "<script> alert('請填 user name !'); </script>";
		?><script>url="annotation_view1.php";window.location.href="annotation_view.php";</script>
	<?php
	}
?>
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
				<label for="xml_content" class="col-sm-2 control-label"><font color="white">User Name:</font></label>
				<div class="col-sm-1">
					<textarea  rows="1" class="form-control" id="user_name" name="user_name" readonly><?php if(isset($_POST['user_name'])){echo $_POST['user_name'];} ?></textarea>
				</div>
			</div>
			<div class="form-group">
				<label for="xml_content" class="col-sm-2 control-label"><font color="white">Movie1 Score:</font></label><br>
				<div class="col-sm-6">
				<input type="radio" name="score1"  value="1"><font color="white">非常不適合&nbsp;&nbsp;</font>      
				<input type="radio" name="score1"  value="2"><font color="white">不太適合&nbsp;&nbsp;</font> 
				<input type="radio" name="score1"  value="3"><font color="white">還可以&nbsp;&nbsp;</font>   
				<input type="radio" name="score1"  value="4"><font color="white">適合&nbsp;&nbsp;</font> 
				<input type="radio" name="score1"  value="5"><font color="white">非常適合&nbsp;&nbsp;</font> 
				</div>
			</div>
			<div class="form-group">
				<label for="xml_content" class="col-sm-2 control-label"><font color="white">Movie2 Score:</font></label><br>
				<div class="col-sm-6">
				<input type="radio" name="score2"  value="1"><font color="white">非常不適合&nbsp;&nbsp;</font>      
				<input type="radio" name="score2"  value="2"><font color="white">不太適合&nbsp;&nbsp;</font> 
				<input type="radio" name="score2"  value="3"><font color="white">還可以&nbsp;&nbsp;</font>   
				<input type="radio" name="score2"  value="4"><font color="white">適合&nbsp;&nbsp;</font> 
				<input type="radio" name="score2"  value="5"><font color="white">非常適合&nbsp;&nbsp;</font>
				</div>
			</div>
			<div class="form-group">
				<label for="xml_content" class="col-sm-2 control-label"><font color="white">Movie3 Score:</font></label><br>
				<div class="col-sm-6">
				<input type="radio" name="score3"  value="1"><font color="white">非常不適合&nbsp;&nbsp;</font>      
				<input type="radio" name="score3"  value="2"><font color="white">不太適合&nbsp;&nbsp;</font> 
				<input type="radio" name="score3"  value="3"><font color="white">還可以&nbsp;&nbsp;</font>   
				<input type="radio" name="score3"  value="4"><font color="white">適合&nbsp;&nbsp;</font> 
				<input type="radio" name="score3"  value="5"><font color="white">非常適合&nbsp;&nbsp;</font>
				</div>
			</div>
			<div class="form-group">
				<label for="xml_content" class="col-sm-2 control-label"><font color="white">Movie4 Score:</font></label><br>
				<div class="col-sm-6">
				<input type="radio" name="score4"  value="1"><font color="white">非常不適合&nbsp;&nbsp;</font>      
				<input type="radio" name="score4"  value="2"><font color="white">不太適合&nbsp;&nbsp;</font> 
				<input type="radio" name="score4"  value="3"><font color="white">還可以&nbsp;&nbsp;</font>   
				<input type="radio" name="score4"  value="4"><font color="white">適合&nbsp;&nbsp;</font> 
				<input type="radio" name="score4"  value="5"><font color="white">非常適合&nbsp;&nbsp;</font>
				</div>
			</div>
			<div class="form-group">
				<label for="xml_content" class="col-sm-2 control-label"><font color="white">Movie5 Score:</font></label><br>
				<div class="col-sm-6">
				<input type="radio" name="score5"  value="1"><font color="white">非常不適合&nbsp;&nbsp;</font>      
				<input type="radio" name="score5"  value="2"><font color="white">不太適合&nbsp;&nbsp;</font> 
				<input type="radio" name="score5"  value="3"><font color="white">還可以&nbsp;&nbsp;</font>   
				<input type="radio" name="score5"  value="4"><font color="white">適合&nbsp;&nbsp;</font> 
				<input type="radio" name="score5"  value="5"><font color="white">非常適合&nbsp;&nbsp;</font>
				</div>
			</div>
			<div class="form-group">
				<label for="XMLContent" class="col-sm-10 control-label"></label>
				<button type="submit" class="btn btn-default" onclick="" style="width:120px;height:40px;border:2px blue none;background-color:pink;">Submit</button>
			</div>			
		</form>	
	</div>

	<script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script><!--put jQuery before bootstrap-->

	</BODY>
</HTML>