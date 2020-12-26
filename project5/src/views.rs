use actix_web::{web,  HttpResponse, Result};

use crate::parser::{get_temperature_for_day, get_temperatures_for_week};
use crate::forms::{DayForm, WeekForm, ResponseForm};

pub async fn temperature_for_day_view(request_params: web::Query<DayForm>) -> Result<HttpResponse> {
    let city = &request_params.city;
    let date = &request_params.date;
    let result = get_temperature_for_day(city, date)
        .await
        .unwrap();
    Ok(HttpResponse::Ok().json(ResponseForm { text: result }))
}

pub async fn temperature_for_week_view(request_params: web::Query<WeekForm>) -> Result<HttpResponse> {
    let result = get_temperatures_for_week(&request_params.city)
        .await
        .unwrap();
    Ok(HttpResponse::Ok().json(ResponseForm { text: result }))
}
