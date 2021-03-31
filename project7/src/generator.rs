// Generate suit of numbers.
use rand::{thread_rng, seq::SliceRandom};

pub const LIMIT: usize = 16;

#[derive(Debug)]
pub struct Generator {
    pub numbers: [i8; LIMIT]
}

impl Generator {
    pub fn new() -> Generator {
        let mut generator = Generator { numbers: [0; LIMIT] };

        for i in 0..LIMIT {
            generator.numbers[i] = i as i8;
            // generator.numbers[i] = (i as i8) + 1 as i8;
        }
        // generator.numbers[14] = 0;
        // generator.numbers[15] = 15;
        generator.generate_suit();
        generator
    }

    fn generate_suit(&mut self) {
        loop {
            self.numbers.shuffle(&mut thread_rng());
            let mut check_value: i8 = 0;

            for i in 0..LIMIT - 1 {
                if self.numbers[i] == 0 {
                    check_value += (i as i8) / 4 + 1;
                    continue;
                }

                for j in i + 1..LIMIT {
                    if self.numbers[j] != 0 && self.numbers[i] > self.numbers[j] {
                        check_value += 1;
                    }
                }
            }
            if check_value % 2 == 0 {
                break;
            }
        }
    }

    // Using current element this method finds an index of zero(empty) element.
    // If it's not found - return -1.
    pub fn find_empty_element(&self, current_index: usize) -> i8 {
        let mut index: Option<usize> = None;

        // check left element
        if current_index % 4 != 0 && self.numbers[(current_index - 1)] == 0 {
            index = Some(current_index - 1);
        }

        // check right element
        else if (current_index + 1) % 4 != 0 && self.numbers[(current_index + 1) as usize] == 0 {
            index = Some(current_index + 1);
        }

        // check top element
        if current_index > 3 && self.numbers[(current_index - 4) as usize] == 0 {
            index = Some(current_index - 4);
        }

        // check bottom element
        if current_index < 12 && self.numbers[(current_index + 4) as usize] == 0 {
            index = Some(current_index + 4);
        }

        match index {
            Some(t) => t as i8,
            None => -1
        }
    }

    pub fn swap(&mut self, index_1: usize, index_2: usize) {
        let temp = self.numbers[index_1];
        self.numbers[index_1] = self.numbers[index_2];
        self.numbers[index_2] = temp;
    }

    pub fn index(&self, num: i8) -> Option<usize> {
        self.numbers.iter().position(|&x| x == num)
    }

    pub fn is_sorted(&self) -> bool {
        let mut temp_collection = self.numbers.clone();
        temp_collection.sort();

        let numbers_count: usize = self.numbers.len() - 1;
        self.numbers[..numbers_count] == temp_collection[1..]
    }
}

