/*
PROBLEM PART #2:

Design a webpage to display the calculated metrics from Part 1.

You are free to use any technology in your toolbox to implement this (Pronto mostly uses React)
Since the number of unique name isn't fixed, display the top 10 sorted by maximum 'measurement', descending. 
Display all the key metrics as explained in Part 1, along with the number of datapoints that each name has been calculated over.

BONUS PROBLEM:

Visualize a name as its Latitude/Longitude/Heading change. 
  - Animate a sprite as these values change 
  - Design and implementation completely up to you. 
  - Not doing this portion is not a penalty in anyway, but be prepared to explain approaches that you might take to implement this.
*/


const button = document.getElementById("button")
const data = document.getElementById("info")


button.onclick= function(){
    // Get the receiver endpoint from Python using fetch:
    fetch("http://127.0.0.1:5000/receiver", 
        {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-type': 'application/json',
                'Accept': 'application/json'
            }
        }).then(res=>{
            // Did we recieve a Promise?
            if(res.ok){
                return res.json()
            }else{
                alert("Something is wrong!")
            }
        }).then(jsonResponse=>{

          var th =  "<tr> \
                      <th>name</th> \
                      <th>lat</th>  \
                      <th>lon</th>  \
                      <th>heading</th>  \
                      <th>sum</th>  \
                      <th>n</th>  \
                      <th>min</th>  \
                      <th>max</th>  \
                      <th>mean</th> \
                      <th>verif</th>  \
                    </tr>"

          var new_data = "<tr>"
          
          // un-nest the dict to create the entries for the HTML table
          Object.keys(jsonResponse).map(function(item){
            
            new_data += "<td>" + item.toString() + "</td>"

            // 'item' is the 'name', so now we grab all values attached to each 'name'
            var key = jsonResponse[item]
            Object.values(key).map(function(item2){
              new_data += "<td>" + item2.toString() + "</td>"
            })
            new_data += "</tr>"
          })

          // Update the HTML
          data.innerHTML = th + new_data          
        })
    .catch((err) => console.error(err)); 
}
/*
THOUGHTS ON THE BONUS PROBLEM:

  How to represent lat/lon/heading change?
    Dedicate a portion of the webpage to being an image of a globe
    Use basic math to create a grid representing lat/lon coordinates 

  What're the sprites?
    Simple solution:
      We use small arrows to represent the names (probably should have the name on the circle too)
      The arrow will point in a direction corresponding to the name's "heading"
        either 0<heading<360, where 0 and 360 are North
        or -180<heading<180, where 0 is North

      If we've receiving data that updated a name's lat/lon:
        Change the color of the arrow to green (green = go)
      If we've received data that verified that a name's lat/lon has not changed:
        Change the color of the arrow to red (red = stop)

    Ideal solution:
      I'm going to assume that the name's represent vehicles

      Map 2.5 images of a vehicle to basic cardinal directions
        update the image being used to represent a vehicle based on which cardinal direction it's 'heading' is closest to
        make the image 'shake' a little bit whenever the vehicle is in motion
          OR add a small colored outline to each image and do the green/red idea described above, changing the outline color instead
*/


/*
MORE IDEAL SOLUTION IN PROGRESS:


import React, {useState, useEffect} from "react";
import ReactDOM from "react-dom";
// use useState() for tracking updates to the data ?
var [state, setState] = useState()
ReactDOM.render(
  <React>

  </React>,
  document.getElementById("root")
);
*/