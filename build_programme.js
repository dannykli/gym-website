function buildProgramme(daysArr, timeVal) {
    let noOfExercises;
    switch (timeVal) {
        case "1":
            noOfExercises = 4;
            break;
        case "2":
            noOfExercises = 5;
            break;
        case "3":
            noOfExercises = 6;
            break;
        case "4":
            noOfExercises = 7;
            break;
    }

    const noOfDays = daysArr.length;
    let title;
    let programme = new Array(noOfDays);
   

    // FRONT END RECIPIENT TO DO: hide buttons, write rest to table, write to table
    if (noOfDays === 6) {
        title = "Push/Pull/Legs x2";
        
        for (let i = 0; i < noOfDays; i++) {
            programme[i] = { 
                day: daysArr[i], 
                exercises: getArrayD6(i+1).sort((a, b) => a[2] - b[2]).slice(0, noOfExercises)
            };
        }

    } else if (noOfDays === 5) {
        title = "Push/Pull/Legs & Upper/Lower";

        for (let i = 0; i < noOfDays; i++) {
            programme[i] = { 
                day: daysArr[i], 
                exercises: getArrayD5(i+1).sort((a, b) => a[2] - b[2]).slice(0, noOfExercises)
            };
        }

    } else if (noOfDays === 4) {
        title = "Upper/Lower x2";

        for (let i = 0; i < noOfDays; i++) {
            programme[i] = { 
                day: daysArr[i], 
                exercises: getArrayD4(i+1).sort((a, b) => a[2] - b[2]).slice(0, noOfExercises)
            };
        }
    } else if (noOfDays === 3) {
        title = "Triple Full Body Split"

        for (let i = 0; i < noOfDays; i++) {
            programme[i] = { 
                day: daysArr[i], 
                exercises: getArrayD3(i+1).slice(0, noOfExercises)
            };
        }
    }

    return {
        "title": title,
        "programme": programme 
    }

    function getArrayD3(dayNo) {
        const day3prog1 = [
                ["Deadlift", "4x(6-10)", 1],
                ["Squats", "4x(6-10)", 2],
                ["Pull ups", "3x(8-12)", 3],
                ["Tricep dips", "3x(8-12)", 4],
                ["Hammer curls", "3x(8-12)", 5],
                ["Barbell shrugs", "3x(8-12)", 6]
            ];
        const day3prog2 = [
                ["Deadlift", "4x(6-10)", 1],
                ["Bench press", "3x(6-10)", 2],
                ["Tricep dips", "3x(8-12)", 3],
                ["Shoulder press", "3x(6-10)", 4],
                ["RDLs", "3x(6-12)", 5],
                ["Lateral raises", "3x(10-15)", 6]
            ];
        const day3prog3 = [
                ["Squats", "4x(6-10)", 1],
                ["Bench press", "3x(6-10)", 2],
                ["Shoulder press", "3x(6-10)", 3],
                ["Pull ups", "3x(8-12)", 4],
                ["Calf raises", "3x(10-15)", 5],
                ["Tricep pushdowns", "3x(8-12)", 6]
            ];
        switch (dayNo) {
            case 1:
                return day3prog1;
            case 2:
                return day3prog2;
            case 3:
                return day3prog3;
        }
    }

    function getArrayD4(dayNo) {
        const day4prog1 = [["Bench press","3x(6-10)",1],["Shoulder Press","3x(6-10)",3],["Pull Ups","3x(6-10)",5],["Hammer curls","3x(8-12)",6],["Seated row","3x(8-12)",7],["Incline DB press","3x(6-10)",2],["Tricep pushdowns","3x(8-12)",4]];
        const day4prog2 = [["Squats","3x(6-10)",1],["Leg press","3x(8-12)",3],["Leg extensions","3x(8-12)",4],["Rear delt flies","3x(10-15)",7],["Split squats", "3x(8-12)",2],["Lateral raises","3x(10-15)",6],["Calf raises","3x(10-15)",5]];
        const day4prog3 = [["Bench press","3x(6-10)",1],["Tricep dips","3x(8-12)",3],["Lat pulldown","3x(8-12)",5],["Skull crushers","3x(8-12)",4],["Chest flies","3x(6-10)",2],["Preacher curls","3x(8-12)",7],["Seated row","3x(8-12)",6]];
        const day4prog4 = [["Squats","3x(6-10)",1],["Hamstring curls","3x(8-12)",3],["Calf raises","3x(10-15)",5],["Lateral raises","3x(10-15)",7],["Adductor machine","3x(8-12)",4],["RDLs","3x(6-10)",2],["Shoulder press","3x(6-10)",6]];
        switch (dayNo) {
            case 1:
                return day4prog1;
            case 2:
                return day4prog2;
            case 3:
                return day4prog3;
            case 4:
                return day4prog4;
        }
    }

    function getArrayD5(dayNo) {
        const day5prog1 = [["Bench Press","3x(6-10)",1],["Incline DB press","3x(6-10)",3],["Tricep pushdowns","3x(10-15)",7],["Shoulder press","3x(6-10)",2],["Skull crushers","3x(8-12)",6],["Chest flies","3x(6-10)",4],["Tricep dips","3x(6-10)",5]]
        const day5prog2 = [["Lat pulldown","3x(8-12)",1],["Seated rows","3x(8-12)",3],["Hammer curls","3x(8-12)",4],["Rear delt flies","3x(10-15)",7],["Seated bicep curls","3x(8-12)",5],["Bent-over rows","3x(8-12)",2],["Preacher curls","3x(6-10)",6]]
        const day5prog3 = [["Squats","3x(6-10)",1],["Leg extensions","3x(8-12)",4],["Hamstring curls","3x(8-12)",5],["Lateral raises","3x(10-15)",7],["Leg press","3x(6-10)",2],["Calf raises","3x(10-15)",6],["RDLs","3x(6-10)",3]]
        const day5prog4 = [["Bench Press","3x(6-10)",1],["Lat pulldown","3x(8-12)",3],["Hammer curls","3x(8-12)",5],["Tricep pushdowns","3x(10-15)",6],["Barbell shrugs","3x(6-10)",7],["Bent-over rows","3x(8-12)",4],["Incline DB press","3x(6-10)",2]]
        const day5prog5 = [["Squats","3x(6-10)",1],["Lateral raises","3x(10-15)",7],["Adductor machine","3x(8-12)",3],["Split squats","3x(8-12)",2],["Leg extensions","3x(8-12)",4],["Hamstring curls","3x(8-12)",5],["Calf raises","3x(10-15)",6]]
        switch (dayNo) {
            case 1:
                return day5prog1;
            case 2:
                return day5prog2;
            case 3:
                return day5prog3;
            case 4:
                return day5prog4;
            case 5:
                return day5prog5;
        }
    }

    function getArrayD6(dayNo) {
        const day6prog1 = [["Bench Press","3x(6-10)",1],["Incline DB press","3x(6-10)",3],["Tricep pushdowns","3x(10-15)",7],["Shoulder press","3x(6-10)",2],["Skull crushers","3x(8-12)",6],["Chest flies","3x(6-10)",4],["Tricep dips","3x(6-10)",5]]
        const day6prog2 = [["Lat pulldown","3x(8-12)",1],["Seated rows","3x(8-12)",3],["Hammer curls","3x(8-12)",4],["Rear delt flies","3x(10-15)",7],["Seated bicep curls","3x(8-12)",5],["Bent-over rows","3x(8-12)",2],["Preacher curls","3x(6-10)",6]]
        const day6prog3 = [["Squats","3x(6-10)",1],["Leg extensions","3x(8-12)",4],["Hamstring curls","3x(8-12)",5],["Lateral raises","3x(10-15)",7],["Leg press","3x(6-10)",2],["Calf raises","3x(10-15)",6],["RDLs","3x(6-10)",3]]
        const day6prog4 = [["Bench Press","3x(6-10)",1],["Incline DB press","3x(6-10)",3],["Skull crushers","3x(8-12)",6],["Shoulder press","3x(6-10)",2],["Tricep pushdowns","3x(10-15)",7],["Chest flies","3x(6-10)",4],["Tricep dips","3x(6-10)",5]]
        const day6prog5 = [["Lat pulldown","3x(8-12)",1],["Bent-over rows","3x(8-12)",2],["Hammer curls","3x(8-12)",5],["Barbell shrugs","3x(10-15)",4],["Rear delt flies","3x(8-12)",7],["Seated rows","3x(8-12)",3],["Preacher curls","3x(6-10)",6]]
        const day6prog6 = [["Squats","3x(6-10)",1],["Split squats","3x(6-10)",2],["RDLs","3x(6-10)",3],["Calf raises","3x(10-15)",6],["Adductor machine","3x(8-12)",4],["Hamstring curls","3x(8-12)",5],["Lateral raises","3x(10-15)",7]]
    
        switch (dayNo) {
            case 1:
                return day6prog1;
            case 2:
                return day6prog2;
            case 3:
                return day6prog3;
            case 4:
                return day6prog4;
            case 5:
                return day6prog5;
            case 6:
                return day6prog6;
        }
    }
    
}