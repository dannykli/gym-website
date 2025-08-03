document.getElementById("alert").style.display = "none"

function validate_days(array, days)
{
    console.log(array)
    let message = ""
    let sevrating = 0
    let consecDay = 0
    let consecRest = 0
    if (days===0 || days===1 || days===2)
    {
        message = "Select at least 3 days"
        sevrating = 3
    }
    else if (days===7)
    {
        message = "Must have at least one rest day"
        sevrating = 3
    }
    if (days===3)
    {
        for (let i=0; i<array.length; i++)
        {
            if (array[i] === true) 
            {
                consecDay++
                if (i===6)
                {
                    if (array[0] === true)
                    {
                        consecDay++
                        if (array[1] === true)
                        {
                            consecDay++
                        }
                    }
                }
            
                if (consecDay===2)
                {
                    message = "It is better to have a rest day between each of the 3 training days"
                    sevrating = 1
                }
                
                else if (consecDay===3)
                {
                    message = "It is better to have rest inbetween training days"
                    sevrating = 2
                }
            }
            
            else 
            {
                consecDay=0
            }
        }
    }
    else if (days===4)
    {
        // check for more than 2 consec rest days
        for (let i=0; i<array.length; i++)
        {
            if (array[i] === false) 
            {
                consecRest++
                if (i===6)
                {
                    if (array[0] === false)
                    {
                        consecRest++
                    }
                }
            
                if (consecRest===2)
                {
                    message = "It is better to spread out the rest across the week"
                    sevrating = 1
                }
            }
            
            else 
            {
                consecRest=0
            }
        }
    }
    
    return [message, sevrating]
}

async function my_function(event)
{
    event.preventDefault() // prevents form progress from being deleted
    console.log("button clicked")
    console.log(document.getElementById("monday").checked)
    console.log(document.getElementById("time").value)
    const isMon = document.getElementById("monday").checked
    const isTue = document.getElementById("tuesday").checked
    const isWed = document.getElementById("wednesday").checked
    const isThu = document.getElementById("thursday").checked
    const isFri = document.getElementById("friday").checked
    const isSat = document.getElementById("saturday").checked
    const isSun = document.getElementById("sunday").checked
    const time = document.getElementById("time").value
    const daysArray = []
    const days = isMon+isTue+isWed+isThu+isFri+isSat+isSun
    daysArray.push(isMon)
    daysArray.push(isTue)
    daysArray.push(isWed)
    daysArray.push(isThu)
    daysArray.push(isFri)
    daysArray.push(isSat)
    daysArray.push(isSun)
    let warn_sev_array = validate_days(daysArray, days)
    let warning = warn_sev_array[0]
    let severity = warn_sev_array[1]
    if (time==="0")
    {
        warning = "Select how many hours you want to spend per session"
        severity = 3
    }
    console.log(severity)
    if (severity===0)
    {
        // sets up temporary session to transfer variable between two pages
        // call buildProgramme()
        daysArr = [];
        for (const day of ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]) {
            if (document.getElementById(day).checked) {
                daysArr.push(day);
            }
        }
        const timeVal = document.getElementById("time").value;
        const userPreferences = [daysArr, timeVal];
        console.log(JSON.stringify(userPreferences));
        const res = await fetch("https://dbpabt1af4.execute-api.eu-west-2.amazonaws.com/default/generateProgramme", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userPreferences)
        });
        if (res.status !== 200) {
            console.log("ERROR WHEN CALLING PROGRAMME GENERATION VIA API")
        }
        const programme = await res.json(); // comverts to text and parses
        localStorage.setItem("generatedProgramme", JSON.stringify(programme));

        /*
        sessionStorage.setItem("days",days) 
        sessionStorage.setItem("time",time)
        sessionStorage.setItem("mon",isMon)
        sessionStorage.setItem("tue",isTue)
        sessionStorage.setItem("wed",isWed)
        sessionStorage.setItem("thu",isThu)
        sessionStorage.setItem("fri",isFri)
        sessionStorage.setItem("sat",isSat)
        sessionStorage.setItem("sun",isSun)*/
        location.href='./programme_page.html'
    }
    else if (severity===1 || severity===2)
    {
        const isMon = document.getElementById("monday").checked
        const isTue = document.getElementById("tuesday").checked
        const isWed = document.getElementById("wednesday").checked
        const isThu = document.getElementById("thursday").checked
        const isFri = document.getElementById("friday").checked
        const isSat = document.getElementById("saturday").checked
        const isSun = document.getElementById("sunday").checked
        const time = document.getElementById("time").value
        const daysArray = []
        const days = isMon+isTue+isWed+isThu+isFri+isSat+isSun
        daysArray.push(isMon)
        daysArray.push(isTue)
        daysArray.push(isWed)
        daysArray.push(isThu)
        daysArray.push(isFri)
        daysArray.push(isSat)
        daysArray.push(isSun)
        // set up temporary session to transfer variable between two pages
        // call buildProgramme()

        // ---------
        daysArr = [];
        for (const day of ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]) {
            if (document.getElementById(day).checked) {
                daysArr.push(day);
            }
        }
        const timeVal = document.getElementById("time").value;
        const userPreferences = [daysArr, timeVal];
        const res = await fetch("https://your-api-id.amazonaws.com/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userPreferences)
        });
        const programme = await res.json(); // comverts to text and parses
        localStorage.setItem("generatedProgramme", JSON.stringify(programme));
        // ---------

        sessionStorage.setItem("days",days) 
        sessionStorage.setItem("time",time)
        sessionStorage.setItem("mon",isMon)
        sessionStorage.setItem("tue",isTue)
        sessionStorage.setItem("wed",isWed)
        sessionStorage.setItem("thu",isThu)
        sessionStorage.setItem("fri",isFri)
        sessionStorage.setItem("sat",isSat)
        sessionStorage.setItem("sun",isSun)
        if (severity===1)
        {
            // creates style element to change background colour of alert
            var style = document.createElement('style'); 
            document.head.appendChild(style);
            style.sheet.insertRule('#alert {background-color: rgb(249 253 3);;}');
            style.sheet.insertRule('#warning-message {color: black}');
            style.sheet.insertRule('#warning-symbol {color: black}');
        }
        else
        {
            var style = document.createElement('style');
            document.head.appendChild(style);
            style.sheet.insertRule('#alert {background-color: rgb(255 152 0 / 81%);}');
        }
        document.getElementById("alert").style.display = "block";
        document.getElementById("warning-message").innerHTML = warning
        document.getElementById("cont-span").innerHTML = '<button id="cont-button" onclick="continue_Funct()">Continue anyway</button><br>'
    }
    else if (severity===3)
    {
        var style = document.createElement('style');
        document.head.appendChild(style);
        style.sheet.insertRule('#alert {background-color: #df2703e8}');
        style.sheet.insertRule('#warning-message {color: white}');
        style.sheet.insertRule('#warning-symbol {color: white}');
        document.getElementById("alert").style.display = "block";
        document.getElementById("warning-message").innerHTML = warning
        document.getElementById("cont-button").style.display = "none";
        // return false 
    }
    else
    {
        console.log("end of if statements")
    }	
}

function continue_Funct()
{
    console.log("continue anyway pressed")
    location.href='./programme_page.html'
}

function dropdownfunc()
{
    const element = document.getElementById("time-div");
    element.scrollIntoView();
}

// FOLLOWING CODE WAS ORIGINALLY IN A DIFFERENT <SCRIPT> TAG TO THE CODE ABOVE


// Modal Image Gallery
function onClick(element) {
  document.getElementById("img01").src = element.src;
  document.getElementById("modal01").style.display = "block";
  var captionText = document.getElementById("caption");
  captionText.innerHTML = element.alt;
}


// Toggle between showing and hiding the sidebar when clicking the menu icon
var mySidebar = document.getElementById("mySidebar");

function w3_open() {
  if (mySidebar.style.display === 'block') {
    mySidebar.style.display = 'none';
  } else {
    mySidebar.style.display = 'block';
  }
}

// Close the sidebar with the close button
function w3_close() {
    mySidebar.style.display = "none";
}

/*Javascript for the dropdown select*/

var x, i, j, l, ll, selElmnt, a, b, c;
// look for any elements with the class "custom-select":
x = document.getElementsByClassName("custom-select");
l = x.length;
for (i = 0; i < l; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  ll = selElmnt.length;
  //for each element, create a new DIV that will act as the selected item:
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  // for each element, create a new DIV that will contain the option list:
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 1; j < ll; j++) {
    // for each option in the original select element,
    // create a new DIV that will act as an option item:
    c = document.createElement("DIV");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.addEventListener("click", function(e) {
        // when an item is clicked, update the original select box,
        // and the selected item:
        var y, i, k, s, h, sl, yl;
        s = this.parentNode.parentNode.getElementsByTagName("select")[0];
        sl = s.length;
        h = this.parentNode.previousSibling;
        for (i = 0; i < sl; i++) {
          if (s.options[i].innerHTML == this.innerHTML) {
            s.selectedIndex = i;
            h.innerHTML = this.innerHTML;
            y = this.parentNode.getElementsByClassName("same-as-selected");
            yl = y.length;
            for (k = 0; k < yl; k++) {
              y[k].removeAttribute("class");
            }
            this.setAttribute("class", "same-as-selected");
            break;
          }
        }
        h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function(e) {
      // when the select box is clicked, close any other select boxes,
      // and open/close the current select box:
	  /*const element = document.getElementById("last-option");
	  element.scrollIntoView();*/ /*trying to show options on screen */
	  e.stopPropagation();
      closeAllSelect(this);
      this.nextSibling.classList.toggle("select-hide");
      this.classList.toggle("select-arrow-active");
    });
}
function closeAllSelect(elmnt) {
  // a function that will close all select boxes in the document,
  // except the current select box:
  var x, y, i, xl, yl, arrNo = [];
  x = document.getElementsByClassName("select-items");
  y = document.getElementsByClassName("select-selected");
  xl = x.length;
  yl = y.length;
  for (i = 0; i < yl; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i)
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < xl; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide");
    }
  }
}
// if the user clicks anywhere outside the select box,
// then close all select boxes:
document.addEventListener("click", closeAllSelect);




