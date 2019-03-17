<!DOCTYPE html>
<?php
 
// Cross-Origin Resource Sharing Header
header('Access-Control-Allow-Origin: http://localhost');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: X-Requested-With, Content-Type, Accept');
 
?>
<HTML>
	<HEAD>
		<meta HTTP-EQUIV="content-type" CONTENT="text/html; charset=UTF-8">
		<title>RSTR</title>
		<!-----------css------------>
		<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
		<link rel="stylesheet" type="text/css" href="css/bootstrap.css" />
		<link rel="stylesheet" type="text/css" href="css/style.css" />
	</HEAD>
	<body style="background-color:#000000;">
	<div class="container-fluid">
		<div class="row">
			<div id="title-blk" class="col-md-12 col-sm-12">
				<p id="title">Relationship-Scenario based Trailer Recommendation</p>
			</div>
			<div id="inputBlock" class="col-md-6 col-sm-12">
				<div id="info-blk" class="col-md-12 col-sm-12">
					<p><b>Testing Input Source :</b> Dcard Mood Article
					<br>Testing Input 1: 節錄自 2016-09-22 "時光時光慢些吧"
					<br>Testing Input 2: 節錄自 2016-11-05 "致 · 單身"
					<br>Testing Input 3: 節錄自 2016-12-08 "有沒有那麼一個人，不敢往前因為害怕失去"</p>
				</div>
				<button id="testinput-1" class="btn btn-default test-btn pull-left">Testing Input 1</button>
				<button id="testinput-2" class="btn btn-default test-btn pull-left">Testing Input 2</button>
				<button id="testinput-3" class="btn btn-default test-btn pull-left">Testing Input 3</button>
				<div id="input-blk">
					<form id="inputData" role="form">
						
						<button type="submit" class="btn btn-primary test-btn pull-right">Recommend Trailer</button>
						<!--inputdata-->
						<div class="form-group">
							<textarea id="article" class="form-control" rows="15" name="article" onkeyup="this.value=this.value.slice(0, 350)"></textarea>
						</div>
					</form>
				</div>
			</div>
			<!-- RESULT FORMAT-->
			<div id="resultBlock" class="col-md-6 col-sm-12">
				<p id="resultblk-title">Recommended Top 3 Trailer List</p>
				<div id="spinner" style="display: none; text-align:center; padding:120px 0;">
					<img src="img/spinner.gif" />
				</div>
				<div id="errormsg" style="display: none; padding:20px">
					<p>Sorry, something wrong happened, please try again later</p>
				</div>
				<div id="cards" style="display: none">
					<div class="col-md-12 col-sm-12 result-blk">
						<div class="result-card">
							<div class="result-rank">1</div>
							<h5 class="result-title"><span id="artist0"></span>&nbsp &nbsp <span id="trailer_name0"></span></h5>
							<iframe id="video0" class="video-display col-md-6 col-sm-12" src="" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
							<p id="storyline0" class="result-lyrics col-md-6 col-sm-12"></p>
						</div>
					</div>
					<div class="col-md-12 col-sm-12 result-blk">
						<div class="result-card">
							<div class="result-rank">2</div>
							<h5 class="result-title"><span id="artist1"></span> &nbsp &nbsp <span id="trailer_name1"></span></h5>
							<iframe id="video1" class="video-display col-md-6 col-sm-12" src="" frameborder="0"></iframe>
							<p id="storyline1" class="result-lyrics col-md-6 col-sm-12"></p>
						</div>
					</div>
					<div class="col-md-12 col-sm-12 result-blk">
						<div class="result-card">
							<div class="result-rank">3</div>
							<h5 class="result-title"><span id="artist2"></span>&nbsp &nbsp <span id="trailer_name2"></span></h5>
							<iframe id="video2" class="video-display col-md-6 col-sm-12" src="" frameborder="0"></iframe>
							<p id="storyline2" class="result-lyrics col-md-6 col-sm-12"></p>
						</div>
					</div>
					<!--<div class="col-md-12 col-sm-12 result-blk">
						<div class="result-card">
							<div class="result-rank">4</div>
							<h5 class="result-title"><span id="artist3"></span>&nbsp &nbsp <span id="trailer_name3"></span></h5>
							<iframe id="video3" class="video-display col-md-6 col-sm-12" src="" frameborder="0"></iframe>
							<p id="storyline3" class="result-lyrics col-md-6 col-sm-12"></p>
						</div>
					</div>
					<div class="col-md-12 col-sm-12 result-blk">
						<div class="result-card">
							<div class="result-rank">5</div>
							<h5 class="result-title"><span id="artist4"></span>&nbsp &nbsp <span id="trailer_name4"></span></h5>
							<iframe id="video4" class="video-display col-md-6 col-sm-12" src="" frameborder="0"></iframe>
							<p id="storyline4" class="result-lyrics col-md-6 col-sm-12"></p>
						</div>
					</div>-->
				</div>
			</div>
		</div>
	</div>
	</body>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js" crossorigin="anonymous" type="text/javascript"></script>
<script type="text/javascript" src="js/bootstrap.js"></script>
<script>
	 $(document).ready(function() {
		$('#inputData').submit(function() {
			var input = $('#article').val();
			console.log(input);
			$.ajax({
				data: {'article': input}, // get the form data
				type: "GET", // GET or POST
				url: "http://localhost:9000/getRecommendSystemResult", // the file to call
				//dataType: "text",
				//dataType: "json",
				beforeSend : function(xhr, opts){
					//show loading gif
					$('#cards').hide();
					$('#errormsg').hide();
					$('#spinner').show();
				},
				success: function(response) { // on success..
					console.log("success!");
					console.log(response);
					
					for (order = 0; order <= 2; order++) {
						song = response[order];
						replaceRecommendSong(order, song);
					}
					
					//remove loading gif
					$('#cards').show();
					$('#errormsg').hide();
					$('#spinner').hide();
				},
				error: function(response) {
					console.log("error!");
					console.log(response);
					
					//remove loading gif
					$('#cards').hide();
					$('#errormsg').show();
					$('#spinner').hide();
				},
			});
			return false;
		});
		
		
		$('#testinput-1').bind("click", {tid:1}, alterTestingInput);
		$('#testinput-2').bind("click", {tid:2}, alterTestingInput);
		$('#testinput-3').bind("click", {tid:3}, alterTestingInput);
	});
	
	function replaceRecommendSong(order, song){
		artistBlk = '#artist' + order.toString();
		trailernameBlk = '#trailer_name' + order.toString();
		videoBlk = '#video' + order.toString();
		storylineBlk = '#storyline' + order.toString();
		$(artistBlk).text(song['artist']); 
		$(trailernameBlk).text(song['trailer_name']);
		$(videoBlk).attr("src", song['link']);
		$(storylineBlk).text(song['storyline']);
	}
	
	function alterTestingInput(e){
		var tid = e.data.tid;
		console.log(tid);
		switch(tid){
			case 1:
				var text = "小時候因為被父母誤會，被罵、被打，\n總想著以後一定要考間離他們很遠的學校，\n反正獨立不是件難事，\n至少可以不被管著，自由自在，一定很開心吧！\n\n長大後，終於考上自己要的好遠好遠的學校，\n卻發現在每一個父母送別我們的時刻，\n在每一次的轉身，都能讓你泛紅了眼眶。\n\n嗨，爸爸好久不見，你好像又老了許多。\n嗨，媽媽好久不見，你好像記性又更差了。\n\n在離開了之後，才發現得到了自己想要的。\n卻失去了更多你以為不會改變的，\n我們能陪著的，他們能陪著的時間有多少呢？";
				break;
			case 2:
				var text = "我認為的愛情是兩人一起互相的成長\n即使遇到困難都能一起面對一起解決\n而不是因為寂寞或新鮮感而在一起\n\n現在的我還沒遇到那個能陪我一起成長的人\n但我不覺得孤單\n因為我有多餘的時間可以充實自己\n例如學語言、做志工或自己喜歡做的事\n都是讓自己成為一個更好的人\n當你遇到了對的人\n你才能更有自信與勇氣去面對愛情\n\n也期勉所有失戀的人\n不要因為那個讓你傷心的人就懼怕愛情\n因為你值得用更好的自己去遇到更好的人\n\n單身沒有什麼不好\n當我們都成為最好的人\n就會擁有最好的愛情\n\n以上\n獻給所有單身的你/妳";
				break;
			case 3:
				var text = "互開玩笑，聊過夢想，聊過未來，聊過過去\n聊過許許多多朋友的定義\n就是沒有聊過彼此\n\n可能你陪他走過過去的瘡疤\n可能他拉你走出情感的黑窖\n可能你們只是碰巧興趣相投\n可能你們都很小心翼翼地維持友誼的平衡\n可能你一直害怕面對內心的期待\n可能他有話一直說不出口\n\n你是他的好朋友，他也是你很重要的那一個人\n別人都覺得你們好的不能再好了\n但你深知道，也很害怕\n不敢往前弄明白彼此的關係\n不敢試著去打破那距美好只差一步的距離\n因為一旦友情失衡\n失去的可能比沒有在一起來的更多\n寧願就這樣，隔著一條銀河\n做彼此眼中最溫暖的那顆星。\n\n碰觸不到的距離\n最讓人心痛\n卻是最永恆的存在。";
				break;
		}
		$('#article').val(text);
	}
</script>
</HTML>


