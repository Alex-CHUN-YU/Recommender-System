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
					<br>Testing Input 1: 節錄自 2019-07-08 "「我去天堂了要怎麼找你呀」"
					<br>Testing Input 2: 節錄自 2019-03-12 "原來曾經的你很愛我，但我卻忘了珍惜"
					<br>Testing Input 3: 節錄自 2018-12-08 "有沒有那麼一個人，不敢往前因為害怕失去"</p>
				</div>
				<button id="testinput-1" class="btn btn-default test-btn pull-left">Testing Input 1</button>
				<button id="testinput-2" class="btn btn-default test-btn pull-left">Testing Input 2</button>
				<button id="testinput-3" class="btn btn-default test-btn pull-left">Testing Input 3</button>
				<div id="input-blk">
					<form id="inputData" role="form">
						
						<button type="submit" class="btn btn-primary test-btn pull-right">Recommend Trailer</button>
						<!--inputdata-->
						<div class="form-group">
							<textarea id="article" class="form-control" rows="20" name="article" onkeyup="this.value=this.value.slice(0, 400)"></textarea>
						</div>
					</form>
					<!--visualization 12/7-->
					<div id="graph-area" class="col-md-12 area">
						<p class="semi-title"><font color="white" size="6"><b>事件鏈 Event Chain</b></font></p>
						<div id="show-graph" class="show-area"></div>
					</div>
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
							<h5 class="result-title"><span id="artist1"></span>&nbsp &nbsp <span id="trailer_name1"></span></h5>
							<iframe id="video1" class="video-display col-md-6 col-sm-12" src="" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
							<p id="storyline1" class="result-lyrics col-md-6 col-sm-12"></p>
						</div>
					</div>
					<div class="col-md-12 col-sm-12 result-blk">
						<div class="result-card">
							<div class="result-rank">2</div>
							<h5 class="result-title"><span id="artist2"></span> &nbsp &nbsp <span id="trailer_name2"></span></h5>
							<iframe id="video2" class="video-display col-md-6 col-sm-12" src="" frameborder="0"></iframe>
							<p id="storyline2" class="result-lyrics col-md-6 col-sm-12"></p>
						</div>
					</div>
					<div class="col-md-12 col-sm-12 result-blk">
						<div class="result-card">
							<div class="result-rank">3</div>
							<h5 class="result-title"><span id="artist3"></span>&nbsp &nbsp <span id="trailer_name3"></span></h5>
							<iframe id="video3" class="video-display col-md-6 col-sm-12" src="" frameborder="0"></iframe>
							<p id="storyline3" class="result-lyrics col-md-6 col-sm-12"></p>
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
<script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
<script type="text/javascript" src="./graph.js"></script>
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
				url: "http://localhost:8309/getRecommendSystemResult", // the file to call
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
					for (order = 1; order <= 3; order++) {
						trailer = response[order];
						replaceRecommendTrailer(order, trailer);
					}
					// event chain
					trailer = response[4]
					arr = trailer['character'].split(" ")
					character = []
					for(var i = 0; i < arr.length; i++){ 
						if (arr[i] !== "") {
							character.push(arr[i]); 
						}
					}
					arr = trailer['emotion'].split(" ")
					emotion = []
					for(var i = 0; i < arr.length; i++){ 
						if (arr[i] !== "") {
							emotion.push(arr[i]); 
						}
					}
					arr = trailer['event'].split(" ")
					event = []
					for(var i = 0; i < arr.length; i++){ 
						if (arr[i] !== "") {
							event.push(arr[i]); 
						}
					}
					arr = trailer['location'].split(" ")
					locaion_test = []
					for(var i = 0; i < arr.length; i++){ 
						if (arr[i] !== "") {
							locaion_test.push(arr[i]); 
						}
					}
					arr = trailer['time'].split(" ")
					time = []
					for(var i = 0; i < arr.length; i++){ 
						if (arr[i] !== "") {
							time.push(arr[i]); 
						}
					}
					console.log(character);
					console.log(emotion);
					console.log(event);
					// console.log(location);
					console.log(time);
					var title = trailer['title'];
					var clist = character;
					var emlist = emotion;
					var evlist = event;	
					var llist = locaion_test;				
					var tlist = time;
					showGraph(title, clist, emlist, evlist, llist, tlist);
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
	
	function replaceRecommendTrailer(order, trailer){
		console.log(trailer.hasOwnProperty('artist'));
		console.log(trailer.hasOwnProperty('trailer_name'));
		console.log(trailer.hasOwnProperty('link'));
		console.log(trailer.hasOwnProperty('storyline'));
		artistBlk = '#artist' + order.toString();
		trailernameBlk = '#trailer_name' + order.toString();
		videoBlk = '#video' + order.toString();
		storylineBlk = '#storyline' + order.toString();
		$(artistBlk).text(trailer['artist']);		
		$(trailernameBlk).text(trailer['trailer_name']);
		$(videoBlk).attr("src", trailer['link']);
		$(storylineBlk).text(trailer['storyline']);
	}

		function removeSpace(arr) {
		artistBlk = '#artist' + order.toString();
		trailernameBlk = '#trailer_name' + order.toString();
		videoBlk = '#video' + order.toString();
		storylineBlk = '#storyline' + order.toString();
		$(artistBlk).text(trailer['artist']);		
		$(trailernameBlk).text(trailer['trailer_name']);
		$(videoBlk).attr("src", trailer['link']);
		$(storylineBlk).text(trailer['storyline']);
	}
	
	function alterTestingInput(e){
		var tid = e.data.tid;
		console.log(tid);
		switch(tid){
			case 1:
				var text = "下午去吃東西，坐在一家店裡，\n旁邊坐著一個媽媽帶著小弟弟，\n那個媽媽好像跟弟弟的爸爸已經離婚了，\n媽媽一直很擔心的問弟弟跟著爸爸過得好不好，\n問繼母對弟弟好不好，繼母的小孩有沒有欺負弟弟，\n弟弟的回話都很乖很成熟，很天真的孩子。\n那個媽媽好像是生了什麼很嚴重的病，\n然後媽媽跟弟弟說：\n「媽媽跟你說，如果有一天媽媽死掉了，\n舅舅會照顧你的。媽媽已經跟舅舅講好了」\n弟弟：「那是什麼時候呀？」\n媽媽：「媽媽也不知道呀，\n但是媽媽好希望可以陪著你們長大。」\n弟弟：「我只希望你不要死掉，\n我只希望你跟我一起死掉。」\n媽媽：「不行！(哽咽)你們要好好長大！」\n弟弟：「所以你會去天堂嗎，那你還會回來嗎？」\n媽媽：「不會了…」\n弟弟：「那我去天堂的時候就會見到你嗎？」\n媽媽：「對呀，所以你一定要做一個堅強的人唷。」\n弟弟：「可是我去天堂了我不知道你住在哪裡呀，那我要怎麼找你呀？」\n";
				break;
			case 2:
				var text = "經歷了一年多的遠距離\n曾經你包容我的壞脾氣\n曾經你一放假就錯台北到台南找我\n曾經你一有空就安排出遊\n曾經你懂我的壓力，當我的依靠\n曾經你再累都會陪我聊天\n曾經你有空就會陪我視訊聊天\n\n曾經你每天愛我想我總放在嘴邊\n\n現在你不在包容我的脾氣\n現在你放假留在台北\n現在你休假打電動看影片陪朋友\n現在你不在陪我聊天，分享生活\n\n談了分手，說了我們在努力\n但這一週我懂了比失戀更像失戀的心情\n我想分享你說你聽不懂\n我想你，你說我要忙所以不來了\n你上班很辛苦很累，我不敢要求什麼\n\n曾經我努力了解朋友說你對我的好\n但是我好像來不及珍惜\n好像要準備失去你了";
				break;
			case 3:
				var text = "互開玩笑，聊過夢想，聊過未來，聊過過去\n聊過許許多多朋友的定義\n就是沒有聊過彼此\n\n可能你陪他走過過去的瘡疤\n可能他拉你走出情感的黑窖\n可能你們只是碰巧興趣相投\n可能你們都很小心翼翼地維持友誼的平衡\n可能你一直害怕面對內心的期待\n可能他有話一直說不出口\n\n你是他的好朋友，他也是你很重要的那一個人\n別人都覺得你們好的不能再好了\n但你深知道，也很害怕\n不敢往前弄明白彼此的關係\n不敢試著去打破那距美好只差一步的距離\n因為一旦友情失衡\n失去的可能比沒有在一起來的更多\n寧願就這樣，隔著一條銀河\n做彼此眼中最溫暖的那顆星。\n\n碰觸不到的距離\n最讓人心痛\n卻是最永恆的存在。";
				break;
		}
		$('#article').val(text);
	}
</script>
</HTML>


