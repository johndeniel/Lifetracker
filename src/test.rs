#[cfg(test)]

#[test]
fn a () {
    // * March 10 2023 - March 20 2023
    // * Born within current month and year
    use crate::lifetracker;
    
    let m: i32 = 3;
    let d: i32 = 10;
    let y: i32 = 2023;
    let t: [i32;3] = [3, 20, 2023];
    
    let exp_result: i32 = 10;
    let result: i32 = lifetracker::computation(m, d, y, t);
    assert_eq!(exp_result, result);
}

#[test]
fn b () {
    // * January 10 2023 - March 16 2023
    // * Born within current year 
    use crate::lifetracker;
    
    let m: i32 = 1;
    let d: i32 = 10;
    let y: i32 = 2023;
    let t: [i32;3] = [3, 16, 2023];
    
    let exp_result: i32 = 65;
    let result: i32 = lifetracker::computation(m, d, y, t);
    assert_eq!(exp_result, result);
}

#[test]
fn c () {
    // * Leap Year
    // * January 10 2024 - March 16 2024
    // * Born within current year 
    use crate::lifetracker;
    
    let m: i32 = 1;
    let d: i32 = 10;
    let y: i32 = 2024;
    let t: [i32;3] = [3, 16, 2024];
    
    let exp_result: i32 = 66;
    let result: i32 = lifetracker::computation(m, d, y, t);
    assert_eq!(exp_result, result);
}

#[test]
fn d () {
    // * August 10 2024 - March 7 2025
    // * Born last year
    use crate::lifetracker;
    
    let m: i32 = 8;
    let d: i32 = 10;
    let y: i32 = 2024;
    let t: [i32;3] = [3, 7, 2025];
    
    let exp_result: i32 = 209;
    let result: i32 = lifetracker::computation(m, d, y, t);
    assert_eq!(exp_result, result);
}

#[test]
fn e () {
    // * Leap Year
    // * August 10 2023 - March 7 2024
    // * Born last year
    use crate::lifetracker;
    
    let m: i32 = 8;
    let d: i32 = 10;
    let y: i32 = 2023;
    let t: [i32;3] = [3, 7, 2024];
    
    let exp_result: i32 = 210;
    let result: i32 = lifetracker::computation(m, d, y, t);
    assert_eq!(exp_result, result);
}

#[test]
fn f () {
    // * August 10 2021 - March 7 2023
    // * 2 years old above
    use crate::lifetracker;
    
    let m: i32 = 8;
    let d: i32 = 10;
    let y: i32 = 2021;
    let t: [i32;3] = [3, 7, 2023];
    
    let exp_result: i32 = 574;
    let result: i32 = lifetracker::computation(m, d, y, t);
    assert_eq!(exp_result, result);
}

#[test]
fn g () {
    // * Leap Year
    // * August 10 2022 - March 7 2024
    // * 2 years old above
    use crate::lifetracker;
    
    let m: i32 = 8;
    let d: i32 = 10;
    let y: i32 = 2022;
    let t: [i32;3] = [3, 7, 2024];
    
    let exp_result: i32 = 575;
    let result: i32 = lifetracker::computation(m, d, y, t);
    assert_eq!(exp_result, result);
}