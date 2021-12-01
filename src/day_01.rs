pub fn part_1(depths: Vec<i64>) -> String {
    let num_increasing = count_increasing_depths(depths);
    format!("Part 1: {}", num_increasing).to_string()
}

pub fn part_2(depths: Vec<i64>) -> String {
    let num_increasing = count_sum_windows(depths);
    format!("Part 2: {}", num_increasing).to_string()
}

fn count_increasing_depths(depths: Vec<i64>) -> i64 {
    let mut iter = depths[..].windows(2);
    let mut num_increasing = 0;
    while let Some([prev, next]) = iter.next() {
        if prev < next {
            num_increasing += 1;
        }
    }
    return num_increasing
}

fn count_sum_windows(depths: Vec<i64>) -> i64 {
    let mut iter = depths[..].windows(3);
    let mut num_increasing = 0;
    let mut prev_sum = std::i64::MAX;
    while let Some([first, second, third]) = iter.next() {
        let current_sum = first + second + third;
        if prev_sum < current_sum {
            num_increasing += 1;
        }
        prev_sum = current_sum;
    }
    return num_increasing
}

#[cfg(test)]
mod day_01_tests {
    use super::*;
    #[test]
    fn test_count_increasing_depths() {
        let depths: Vec<i64> = vec![199, 200, 208, 210, 200, 207, 240, 269, 260, 263];
        assert_eq!(count_increasing_depths(depths), 7);
    }
    #[test]
    fn test_count_sum_windows() {
        let depths: Vec<i64> = vec![199, 200, 208, 210, 200, 207, 240, 269, 260, 263];
        assert_eq!(count_sum_windows(depths), 5);
    }
}