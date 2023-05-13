use crate::driver::{day, leapyear};

pub fn computation(m: i32, d: i32, y: i32, t: [i32; 3]) -> i32 {

    let mut x: i32 = 0;

    // born within current month and year
    if y == t[2] && m == t[0] {
        for _i in (d+1)..= t[1] {
            x+=1;
        }
        return x;
    }


    // born within current year
    if y == t[2] {
        // days within birth month (14 - n)
        for _i in (d+1)..= day()[m as usize - 1] {
            x+=1;
        }
        // months between birth month and current month
        for _i in m.. t[0]-1 {
            x += day()[_i as usize];
        }
        // day of the month (1 - n)
        for _i in 1..= t[1] {
            x += 1;
        }
        // x + 1 or x
        return if leapyear(y) && m <= 2 {x + 1} else {x};
    }


    // born last year
    if y+1 == t[2] {
        // days within birth month (14 - n)
        for _i in (d+1)..= day()[m as usize - 1] {
            x+=1;
        }
        // last year's month (n - n)
        for _i in m.. 12 {
            x += day()[_i as usize];
        }
        // current january - n
        if t[0] > 1 {
            for _i in 0.. t[0]-1 {
                x += day()[_i as usize];
            }
        }
        // x + 1 + t[1] or x + t[1]
        return if leapyear(t[2]) && t[0] >= 2  {(x + 1) + t[1]} else {x + t[1]};
    }


    // 2 years old above
    // days within birth month (14 - n)
    for _i in (d+1)..= day()[m as usize - 1] {
        x+=1;
    }
    // birth month (n - n)
    for _i in m.. 12 {
        x += day()[_i as usize];
    }
    // (y+1) -> (t[2])
    for _i in y+1.. t[2] {
        x += if leapyear(_i) {366} else {365};
    }
    // current january - n
    if t[0] > 1 {
        for _i in 0.. t[0]-1 {
            x += day()[_i as usize];
        }
    }
    // x + 1 + t[1] or x + t[1]
    return if leapyear(t[2]) && t[0] >= 2  {(x + 1) + t[1]} else {x + t[1]}; 
}