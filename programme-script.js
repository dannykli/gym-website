const days = parseInt(sessionStorage.getItem("days")) // next step: develop help page
const time = sessionStorage.getItem("time")
const isMon = sessionStorage.getItem("mon")
const isTue = sessionStorage.getItem("tue")
const isWed = sessionStorage.getItem("wed")
const isThu = sessionStorage.getItem("thu")
const isFri = sessionStorage.getItem("fri")
const isSat = sessionStorage.getItem("sat")
const isSun = sessionStorage.getItem("sun")
console.log(days + " " + time + " " + isSat)
let i = 0
let j = 0
let numOfExercises = 0
var oldExerciseArr = []

// if 3 days are entered: do day4prog,5 etc. -->
const day3prog = [[["Deadlift","4x(6-10)"],["Squats","4x(6-10)"],["Pull ups","3x(8-12)"],["Tricep dips","3x(8-12)"],["Hammer curls","3x(8-12)"],["Barbell shrugs","3x(8-12)"]],
    [["Deadlift","4x(6-10)"],["Bench press","3x(6-10)"],["Tricep dips","3x(8-12)"],["Shoulder press","3x(6-10)"],["RDLs","3x(6-12)"],["Lateral raises","3x(10-15)"]],
    [["Squats","4x(6-10)"],["Bench press","3x(6-10)"],["Shoulder press","3x(6-10)"],["Pull ups","3x(8-12)"],["Calf raises","3x(10-15)"],["Tricep pushdowns","3x(8-12)"]]]

function writeToTable(weekday, j, exercise, reps)
{
    document.getElementById(weekday+(j+1).toString()).innerHTML = exercise
    document.getElementById("s-"+weekday+(j+1).toString()).innerHTML = exercise
    document.getElementById("reps-"+weekday+(j+1).toString()).innerHTML = " " + reps
    document.getElementById("s-reps-"+weekday+(j+1).toString()).innerHTML = " " + reps
}

function writeRestToTable(weekday)
{
    document.getElementById(weekday+"1").innerHTML = '<span id="rest">Rest</span><style>#rest{font-weight:bold}</style>'
    document.getElementById("s-"+weekday+"1").innerHTML = '<span id="rest">Rest</span><style>#rest{font-weight:bold}</style>'
}

function hideInfoButton(weekday, j)
{
    document.getElementById("button-"+weekday+(j+1).toString()).style.display = 'none'
    document.getElementById("s-button-"+weekday+(j+1).toString()).style.display = 'none'
}

if (time === "1")
{
    numOfExercises = 4
}
else if (time === "2")
{
    numOfExercises = 5
}
else if (time === "3")
{
    numOfExercises = 6
}
else if (time === "4")
{
    numOfExercises = 7
}

function progSort(numOfExercises, myArray, weekday)
{
    for (i=0;i<numOfExercises;i++)
        {
            let temp = 10
            for (j=0;j<numOfExercises;j++)
            {
                if (myArray[j][2] < temp)
                {
                    temp = myArray[j][2]
                    exInd = j
                }
            }
            myArray[exInd][2] = 10
            writeToTable(weekday, i, myArray[exInd][0], myArray[exInd][1])
        }
}

function getArrayD4(day)
{
    const day4prog1 = [["Bench press","3x(6-10)",1],["Shoulder Press","3x(6-10)",3],["Pull Ups","3x(6-10)",5],["Hammer curls","3x(8-12)",6],["Seated row","3x(8-12)",7],["Incline DB press","3x(6-10)",2],["Tricep pushdowns","3x(8-12)",4]]
    const day4prog2 = [["Squats","3x(6-10)",1],["Leg press","3x(8-12)",3],["Leg extensions","3x(8-12)",4],["Rear delt flies","3x(10-15)",7],["Split squats", "3x(8-12)",2],["Lateral raises","3x(10-15)",6],["Calf raises","3x(10-15)",5]]
    const day4prog3 = [["Bench press","3x(6-10)",1],["Tricep dips","3x(8-12)",3],["Lat pulldown","3x(8-12)",5],["Skull crushers","3x(8-12)",4],["Chest flies","3x(6-10)",2],["Preacher curls","3x(8-12)",7],["Seated row","3x(8-12)",6]]
    const day4prog4 = [["Squats","3x(6-10)",1],["Hamstring curls","3x(8-12)",3],["Calf raises","3x(10-15)",5],["Lateral raises","3x(10-15)",7],["Adductor machine","3x(8-12)",4],["RDLs","3x(6-10)",2],["Shoulder press","3x(6-10)",6]] // use numbering to decide order in which exercises appear
    let myarray = [];
    switch (day)
    {
        case 1:
            myArray = day4prog1;
            break;
        case 2:
            myArray = day4prog2;
            break;
        case 3:
            myArray = day4prog3;
            break;
        case 4:
            myArray = day4prog4;
            break;
    }
    return myArray
}

function getArrayD5(day)
{
    const day5prog1 = [["Bench Press","3x(6-10)",1],["Incline DB press","3x(6-10)",3],["Tricep pushdowns","3x(10-15)",7],["Shoulder press","3x(6-10)",2],["Skull crushers","3x(8-12)",6],["Chest flies","3x(6-10)",4],["Tricep dips","3x(6-10)",5]]
    const day5prog2 = [["Lat pulldown","3x(8-12)",1],["Seated rows","3x(8-12)",3],["Hammer curls","3x(8-12)",4],["Rear delt flies","3x(10-15)",7],["Seated bicep curls","3x(8-12)",5],["Bent-over rows","3x(8-12)",2],["Preacher curls","3x(6-10)",6]]
    const day5prog3 = [["Squats","3x(6-10)",1],["Leg extensions","3x(8-12)",4],["Hamstring curls","3x(8-12)",5],["Lateral raises","3x(10-15)",7],["Leg press","3x(6-10)",2],["Calf raises","3x(10-15)",6],["RDLs","3x(6-10)",3]]
    const day5prog4 = [["Bench Press","3x(6-10)",1],["Lat pulldown","3x(8-12)",3],["Hammer curls","3x(8-12)",5],["Tricep pushdowns","3x(10-15)",6],["Barbell shrugs","3x(6-10)",7],["Bent-over rows","3x(8-12)",4],["Incline DB press","3x(6-10)",2]]
    const day5prog5 = [["Squats","3x(6-10)",1],["Lateral raises","3x(10-15)",7],["Adductor machine","3x(8-12)",3],["Split squats","3x(8-12)",2],["Leg extensions","3x(8-12)",4],["Hamstring curls","3x(8-12)",5],["Calf raises","3x(10-15)",6]]
    let myarray = []
    switch (day)
    {
        case 1:
            myArray = day5prog1;
            break;
        case 2:
            myArray = day5prog2;
            break;
        case 3:
            myArray = day5prog3;
            break;
        case 4:
            myArray = day5prog4;
            break;
        case 5:
            myArray = day5prog5;
            break;
    }
    return myArray
}

function getArrayD6(day)
{
    const day6prog1 = [["Bench Press","3x(6-10)",1],["Incline DB press","3x(6-10)",3],["Tricep pushdowns","3x(10-15)",7],["Shoulder press","3x(6-10)",2],["Skull crushers","3x(8-12)",6],["Chest flies","3x(6-10)",4],["Tricep dips","3x(6-10)",5]]
    const day6prog2 = [["Lat pulldown","3x(8-12)",1],["Seated rows","3x(8-12)",3],["Hammer curls","3x(8-12)",4],["Rear delt flies","3x(10-15)",7],["Seated bicep curls","3x(8-12)",5],["Bent-over rows","3x(8-12)",2],["Preacher curls","3x(6-10)",6]]
    const day6prog3 = [["Squats","3x(6-10)",1],["Leg extensions","3x(8-12)",4],["Hamstring curls","3x(8-12)",5],["Lateral raises","3x(10-15)",7],["Leg press","3x(6-10)",2],["Calf raises","3x(10-15)",6],["RDLs","3x(6-10)",3]]
    const day6prog4 = [["Bench Press","3x(6-10)",1],["Incline DB press","3x(6-10)",3],["Skull crushers","3x(8-12)",6],["Shoulder press","3x(6-10)",2],["Tricep pushdowns","3x(10-15)",7],["Chest flies","3x(6-10)",4],["Tricep dips","3x(6-10)",5]]
    const day6prog5 = [["Lat pulldown","3x(8-12)",1],["Bent-over rows","3x(8-12)",2],["Hammer curls","3x(8-12)",5],["Barbell shrugs","3x(10-15)",4],["Rear delt flies","3x(8-12)",7],["Seated rows","3x(8-12)",3],["Preacher curls","3x(6-10)",6]]
    const day6prog6 = [["Squats","3x(6-10)",1],["Split squats","3x(6-10)",2],["RDLs","3x(6-10)",3],["Calf raises","3x(10-15)",6],["Adductor machine","3x(8-12)",4],["Hamstring curls","3x(8-12)",5],["Lateral raises","3x(10-15)",7]]
    let myarray = []
    switch (day)
    {
        case 1:
            myArray = day6prog1;
            break;
        case 2:
            myArray = day6prog2;
            break;
        case 3:
            myArray = day6prog3;
            break;
        case 4:
            myArray = day6prog4;
            break;
        case 5:
            myArray = day6prog5;
            break;
        case 6:
            myArray = day6prog6;
    }
    return myArray
}

function hideButtons(min, weekday)
{
    for (i=min;i<7;i++)
    {
        hideInfoButton(weekday, i)
    }
}

if (days===6)
{
    document.getElementById("title").innerHTML = "Push/Pull/Legs x2"
    let day=1;
    if (isMon==="true")
    {
        progSort(numOfExercises, getArrayD6(day), "mon")
        hideButtons(numOfExercises, "mon")
        day++
    }
    else
    {
        writeRestToTable("mon")
        hideButtons(0, "mon")
    }
    if (isTue==="true")
    {
        progSort(numOfExercises, getArrayD6(day), "tue")
        hideButtons(numOfExercises, "tue")
        day++
    }
    else
    {
        writeRestToTable("tue")
        hideButtons(0, "tue")
    }
    if (isWed==="true")
    {
        progSort(numOfExercises, getArrayD6(day), "wed")
        hideButtons(numOfExercises, "wed")
        day++
    }
    else
    {
        writeRestToTable("wed")
        hideButtons(0, "wed")
    }
    if (isThu==="true")
    {
        progSort(numOfExercises, getArrayD6(day), "thu")
        hideButtons(numOfExercises, "thu")
        day++
    }
    else
    {
        writeRestToTable("thu")
        hideButtons(0, "thu")
    }
    if (isFri==="true")
    {
        progSort(numOfExercises, getArrayD6(day), "fri")
        hideButtons(numOfExercises, "fri")
        day++
    }
    else
    {
        writeRestToTable("fri")
        hideButtons(0, "fri")
    }
    if (isSat==="true")
    {
        progSort(numOfExercises, getArrayD6(day), "sat")
        hideButtons(numOfExercises, "sat")
        day++
    }
    else
    {
        writeRestToTable("sat")
        hideButtons(0, "sat")
    }
    if (isSun==="true")
    {
        progSort(numOfExercises, getArrayD6(day), "sun")
        hideButtons(numOfExercises, "sun")
        day++
    }
    else
    {
        writeRestToTable("sun")
        hideButtons(0, "sun")
    }
    
}

if (days===5)
{
    document.getElementById("title").innerHTML = "Push/Pull/Legs & Upper/Lower"
    let day=1;
    if (isMon==="true")
    {
        progSort(numOfExercises, getArrayD5(day), "mon")
        hideButtons(numOfExercises, "mon")
        day++
    }
    else
    {
        writeRestToTable("mon")
        hideButtons(0, "mon")
    }
    if (isTue==="true")
    {
        progSort(numOfExercises, getArrayD5(day), "tue")
        hideButtons(numOfExercises, "tue")
        day++
    }
    else
    {
        writeRestToTable("tue")
        hideButtons(0, "tue")
    }
    if (isWed==="true")
    {
        progSort(numOfExercises, getArrayD5(day), "wed")
        hideButtons(numOfExercises, "wed")
        day++
    }
    else
    {
        writeRestToTable("wed")
        hideButtons(0, "wed")
    }
    if (isThu==="true")
    {
        progSort(numOfExercises, getArrayD5(day), "thu")
        hideButtons(numOfExercises, "thu")
        day++
    }
    else
    {
        writeRestToTable("thu")
        hideButtons(0, "thu")
    }
    if (isFri==="true")
    {
        progSort(numOfExercises, getArrayD5(day), "fri")
        hideButtons(numOfExercises, "fri")
        day++
    }
    else
    {
        writeRestToTable("fri")
        hideButtons(0, "fri")
    }
    if (isSat==="true")
    {
        progSort(numOfExercises, getArrayD5(day), "sat")
        hideButtons(numOfExercises, "sat")
        day++
    }
    else
    {
        writeRestToTable("sat")
        hideButtons(0, "sat")
    }
    if (isSun==="true")
    {
        progSort(numOfExercises, getArrayD5(day), "sun")
        hideButtons(numOfExercises, "sun")
        day++
    }
    else
    {
        writeRestToTable("sun")
        hideButtons(0, "sun")
    }
    
}


if (days === 4)// write day4prog2,3,4 arrays and add extra row to table
{
    document.getElementById("title").innerHTML = "Upper/Lower x2"
    let day=1;
    if (isMon==="true")
    {
        progSort(numOfExercises, getArrayD4(day), "mon")
        hideButtons(numOfExercises, "mon")
        day++
    }
    else
    {
        writeRestToTable("mon")
        hideButtons(0, "mon")
    }
    if (isTue==="true")
    {
        progSort(numOfExercises, getArrayD4(day), "tue")
        hideButtons(numOfExercises, "tue")
        day++
    }
    else
    {
        writeRestToTable("tue")
        hideButtons(0, "tue")
    }
    if (isWed==="true")
    {
        progSort(numOfExercises, getArrayD4(day), "wed")
        hideButtons(numOfExercises, "wed")
        day++
    }
    else
    {
        writeRestToTable("wed")
        hideButtons(0, "wed")
    }
    if (isThu==="true")
    {
        progSort(numOfExercises, getArrayD4(day), "thu")
        hideButtons(numOfExercises, "thu")
        day++
    }
    else
    {
        writeRestToTable("thu")
        hideButtons(0, "thu")
    }
    if (isFri==="true")
    {
        progSort(numOfExercises, getArrayD4(day), "fri")
        hideButtons(numOfExercises, "fri")
        day++
    }
    else
    {
        writeRestToTable("fri")
        hideButtons(0, "fri")
    }
    if (isSat==="true")
    {
        progSort(numOfExercises, getArrayD4(day), "sat")
        hideButtons(numOfExercises, "sat")
        day++
    }
    else
    {
        writeRestToTable("sat")
        hideButtons(0, "sat")
    }
    if (isSun==="true")
    {
        progSort(numOfExercises, getArrayD4(day), "sun")
        hideButtons(numOfExercises, "sun")
        day++
    }
    else
    {
        writeRestToTable("sun")
        hideButtons(0, "sun")
    }
    
}

if (days === 3)
{
    numOfExercises--
    document.getElementById("title").innerHTML = "Triple Full Body Split"
    
    
    
    if (isMon==="true")
    {
        for (j=0;j<numOfExercises;j++)
        {
            writeToTable("mon",j,day3prog[i][j][0],day3prog[i][j][1])
            if (oldExerciseArr.includes(day3prog[i][j][0])===false)
            {
                oldExerciseArr.push(day3prog[i][j][0])
            }
            
            
        }
        i = i + 1
    }
    else
    {
        writeRestToTable("mon")
        
    }
    for (j=j;j<7;j++)
        {
            hideInfoButton("mon", j)
        }
    j = 0
    if (isTue==="true")
    {
        for (j=0;j<numOfExercises;j++)
        {
            writeToTable("tue",j,day3prog[i][j][0],day3prog[i][j][1])
            if (oldExerciseArr.includes(day3prog[i][j][0])===false)
            {
                oldExerciseArr.push(day3prog[i][j][0])
            }
        }
        i = i + 1
    }
    else
    {
        writeRestToTable("tue")
    }
    for (j=j;j<7;j++)
        {
            hideInfoButton("tue", j)
        }
    j = 0
    if (isWed==="true")
    {
        for (j=0;j<numOfExercises;j++)
        {
            writeToTable("wed",j,day3prog[i][j][0],day3prog[i][j][1])
            if (oldExerciseArr.includes(day3prog[i][j][0])===false)
            {
                oldExerciseArr.push(day3prog[i][j][0])
            }
        }
        i = i + 1
    }
    else
    {
        writeRestToTable("wed")
    }
    for (j=j;j<7;j++)
        {
            hideInfoButton("wed", j)
        }
    j = 0
    if (isThu==="true")
    {
        for (j=0;j<numOfExercises;j++)
        {
            writeToTable("thu",j,day3prog[i][j][0],day3prog[i][j][1])
            if (oldExerciseArr.includes(day3prog[i][j][0])===false)
            {
                oldExerciseArr.push(day3prog[i][j][0])
            }
        }
        i = i + 1
    }
    else
    {
        writeRestToTable("thu")
    }
    for (j=j;j<7;j++)
        {
            hideInfoButton("thu", j)
        }
    j = 0
    if (isFri==="true")
    {
        for (j=0;j<numOfExercises;j++)
        {
            writeToTable("fri",j,day3prog[i][j][0],day3prog[i][j][1])
            if (oldExerciseArr.includes(day3prog[i][j][0])===false)
            {
                oldExerciseArr.push(day3prog[i][j][0])
            }
        }
        i = i + 1
    }
    else
    {
        writeRestToTable("fri")
    }
    for (j=j;j<7;j++)
        {
            hideInfoButton("fri", j)
        }
    j = 0
    if (isSat==="true")
    {
        for (j=0;j<numOfExercises;j++)
        {
            writeToTable("sat",j,day3prog[i][j][0],day3prog[i][j][1])
            if (oldExerciseArr.includes(day3prog[i][j][0])===false)
            {
                oldExerciseArr.push(day3prog[i][j][0])
            }
        }
        i = i + 1
    }
    else
    {
        writeRestToTable("sat")
    }
    for (j=j;j<7;j++)
        {
            hideInfoButton("sat", j)
        }
    j = 0
    if (isSun==="true")
    {
        for (j=0;j<numOfExercises;j++)
        {
            writeToTable("sun",j,day3prog[i][j][0],day3prog[i][j][1])
            if (oldExerciseArr.includes(day3prog[i][j][0])===false)
            {
                oldExerciseArr.push(day3prog[i][j][0])
            }
        }
        i = i + 1
    }
    else
    {
        writeRestToTable("sun")
    }
    for (j=j;j<7;j++)
        {
            hideInfoButton("sun", j)
        }
    j = 0
}

for (let k=0; k<(7-numOfExercises);k++)
{
    document.getElementById("table").deleteRow(numOfExercises+1)
    document.getElementById("s-table1").deleteRow(numOfExercises+1)
    document.getElementById("s-table2").deleteRow(numOfExercises+1)
    document.getElementById("s-table3").deleteRow(numOfExercises+1)
    document.getElementById("s-table4").deleteRow(numOfExercises+1)
    document.getElementById("s-table5").deleteRow(numOfExercises+1)
    document.getElementById("s-table6").deleteRow(numOfExercises+1)
    document.getElementById("s-table7").deleteRow(numOfExercises+1)
}

function help_funct(tableCellID)
{
	exercise = document.getElementById(tableCellID).innerHTML
	exercise = exercise.replace(/\s+/g,'') // get rids of spaces in a string
	exercise = exercise.toLowerCase()
	location.href="./help_page.html#"+exercise
}

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

