use std::env;
use reqwest::Client;
use serde_json::Value;

type Result<T, E = Box<dyn std::error::Error>> = std::result::Result<T, E>;

pub async fn get_temperature_for_day(city: &String, date: &String) -> Result<String> {
    let request = Client::new()
        .get("https://api.weatherapi.com/v1/history.json")
        .header("Accepts", "application/json")
        .query(&[("key", &get_api_key()), ("q", city), ("dt", date)]);

    let response = request.send().await?;
    let response_status = response.status();
    println!("{}", response_status);

    if response_status != 200 {
        return Ok(format!("Ошибка API. Пожалуйста, попробуйте позднее."));
    }

    let response_in_vec = response.bytes().await?.to_vec();
    let response_data = String::from_utf8_lossy(&response_in_vec);
    // println!("response: {} ", response_data);

    let weather_collection: Value = serde_json::from_str(&response_data)?;


    Ok(format!("Date:{}, temperature = {}", date, weather_collection["forecast"]["forecastday"][0]["day"]["avgtemp_c"]))
}

pub async fn get_temperatures_for_week(city: &String) -> Result<String> {
    let request = Client::new()
        .get("http://api.weatherapi.com/v1/forecast.json")
        .header("Accepts", "application/json")
        .query(&[("key", &get_api_key()), ("q", &city), ("days", &String::from("5"))]);

    let response = request.send().await?;
    let response_status = response.status();
    println!("{}", response_status);

    if response_status != 200 {
        return Ok(format!("Ошибка API. Пожалуйста, попробуйте позднее."))
    }

    let response_in_vec = response.bytes().await?.to_vec();
    let response_data = String::from_utf8_lossy(&response_in_vec);
    // println!("response: {} ", response_data);

    let weather_collection: Value = serde_json::from_str(&response_data)?;
    let mut temperatures: [String; 5] = Default::default();
    for i in 0..5 {
        temperatures[i] = format!("{}", weather_collection["forecast"]["forecastday"][i]["day"]["avgtemp_c"]);
    }
    // println!("arr: {:?} ", temperatures);

    Ok(format!("Temperatures for week = {:?}", temperatures))
}

fn get_api_key() -> String {
    match env::var("WEATHER_API_KEY") {
        Ok(val) => val,
        Err(_e) => String::from(""),
    }
}
