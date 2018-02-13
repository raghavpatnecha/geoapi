# apitest


1.) Import the database in PostgreSQL

2.) Configure the Function in test.py according to your requirements

     `
          POSTGRES = {
           'user': 'postgres',
            'pw': 'postgres',
            'db': 'In',
            'host': 'localhost',
            'port': '5432'
             }  `
             
   3.) Send a Post request to location to insert data in PostgreSQL tablea `post_location`. You can also see the data you recently stored in database. Example request can be seen in the image below:
   <img src="https://github.com/raghavpatnecha/apitest/blob/master/screens/post_request.png">
   
  4.) There are two get apis: `get_using_self` and `get_using_postgres`. Both calculate and give lat/long along with places within a certain radius. `get_using_postgres` uses the inbuilt earthdistance extension while `get_using_self` uses the haversine formula to calculate distances. Example request can be seen in the image below:
    <img src="https://github.com/raghavpatnecha/apitest/blob/master/screens/how%20to%20send%20a%20get%20request.png">   
     <img src="https://github.com/raghavpatnecha/apitest/blob/master/screens/how%20to%20send%20get%20using%20self.png">
     
  5.) There is a location table in the PostgreSQL database which has the parsed geoJSON data which is inserted in database with the help of Postgis.
   
   <img src="https://github.com/raghavpatnecha/apitest/blob/master/screens/how%20to%20send%20geo%20request.png">
     
     
  6.) Test cases is created using Restesr framework to test Rest API. Do `pip install Rester`.
        * You can use any of the file test.json or test.yaml. 
             `apirunner --ts=YOUR_PATH/test.json`
                       or
             `apirunner --ts=YOUTPATH/test.yaml`          
     
  ### TODO
  * Add few test cases.
  * Check for diiference in results in `get_using_self` and `get_using_postgres`.
  * Check for some exception handling and Time complexities.
  
