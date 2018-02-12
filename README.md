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
             
   3.) Send a Post request to location to insert data in PostgreSQL tablea `post_location`. You can also see the data you recently stored in database.
   <img src="https://github.com/raghavpatnecha/apitest/blob/master/screens/post_request.png">
   
  4.) There are two get apis: `get_using_self` and `get_using_postgres`. Both calculate and give lat/long along with places within a certain radius. `get_using_postgres` uses the inbuilt earthdistance extension while `get_using_self` uses the haversine formula to calculate distances.
    <img src="https://github.com/raghavpatnecha/apitest/blob/master/screens/get_using_postgre.png">   
    <img src="https://github.com/raghavpatnecha/apitest/blob/master/screens/get_using_self.png">
    
  5.) There is a location table in the PostgreSQL database which has the parsed geoJSON data which is inserted in database with the help of Postgis.
     <img src="https://github.com/raghavpatnecha/apitest/blob/master/screens/geo_2_post.png">
     
     
  ### TODO
  * Write Test cases using framework to test all three APIs.
  * Put validation in the `post_location` to avoid multiple insertions of same data.
  * Pass lat/long to the location table to check in which location a point is falling.
