<?php
    include("mysql_connect.inc.php");   
    function query_id($id){
        $con = connect();
        $DisList = array();
        $SQL_Command = sprintf("SELECT system_type, article_id, movie_id1, movie_id2, movie_id3, movie_id4, movie_id5 FROM experiment_system WHERE id >= %s", $id);
        $result = mysqli_query($con, $SQL_Command);
         while($row = mysqli_fetch_array($result))
            {
                array_push($DisList, $row["system_type"]);
                array_push($DisList, $row["article_id"]);
                array_push($DisList, $row["movie_id1"]);
                array_push($DisList, $row["movie_id2"]);
                array_push($DisList, $row["movie_id3"]);
                array_push($DisList, $row["movie_id4"]);
                array_push($DisList, $row["movie_id5"]);
            }
        mysqli_close($con);
        return $DisList;
    }
    function query_user_score($user_name, $system_type, $article_id){
        $con = connect();
        $DisList = array();
        $SQL_Command = sprintf("SELECT * FROM experiment_system_user WHERE user_name = '%s' and system_type = %s and article_id = %s", $user_name, $system_type, $article_id);
        // echo $SQL_Command;
        $result = mysqli_query($con, $SQL_Command);
        $rowcount=mysqli_num_rows($result);
        mysqli_close($con);
        if ($rowcount > 0){
            return True;
        } else {
          return False;
        }
    }
    function insert_score($user_name, $system_type, $article_id, $score1, $score2, $score3, $score4, $score5){
        $con = connect();
        $DisList = array();
        $SQL_Command = sprintf("INSERT INTO experiment_system_user (user_name, system_type, article_id, score1, score2, score3, score4, score5) VALUES ('".$user_name."', ".$system_type.", ".$article_id.", ".$score1.", ".$score2.", ".$score3.", ".$score4.", ".$score5.")");
        $result = mysqli_query($con, $SQL_Command);
        mysqli_close($con);
        return $DisList;
    }
    function query_article($article_id){
        $con = connect();
        $DisList = array();
        $SQL_Command = sprintf("SELECT content FROM articles WHERE id = %s", $article_id);
        $result = mysqli_query($con, $SQL_Command);
        #echo $SQL_Command;
         while($row = mysqli_fetch_array($result))
            {
                array_push($DisList, $row["content"]);
            }
        mysqli_close($con);
        return $DisList;
    }
    function query_movie($movie_id){
        $con = connect();
        $DisList = array();
        $SQL_Command = sprintf("SELECT storyline, link FROM movies WHERE id = %s", $movie_id);
        $result = mysqli_query($con, $SQL_Command);
         while($row = mysqli_fetch_array($result))
            {
                array_push($DisList, $row["storyline"]);
                array_push($DisList, $row["link"]);
            }
        mysqli_close($con);
        return $DisList;
    }
?>