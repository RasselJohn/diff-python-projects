use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
pub struct DayForm {
    pub city: String,
    pub date: String,
}

#[derive(Deserialize)]
pub struct WeekForm {
    pub city: String,
}


#[derive(Serialize, Deserialize)]
pub struct ResponseForm {
    pub text: String,
}