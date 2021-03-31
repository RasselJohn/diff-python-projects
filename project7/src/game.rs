use fltk::*;
// use fltk::{button, enums, window, group, WidgetExt};

use crate::generator::{Generator};

#[derive(Clone, Copy)]
pub enum Message {
    NewGame,
    Help,
    Step(i8),
}

pub struct Game {
    pub game_window: window::DoubleWindow,
    pub new_game_button: button::Button,
    pub help_button: button::Button,
    pub num_buttons: Vec<button::Button>,

    num_generator: Generator,
    sender: app::Sender<Message>,
    receiver: app::Receiver<Message>,
}

impl Game {
    // Public
    pub fn new() -> Game {
        // main window
        let mut game_window: window::DoubleWindow = window::Window::default();
        game_window.set_size(300, 330);
        game_window.set_label("15!");
        game_window.set_color(enums::Color::from_rgb(47, 88, 78));
        game_window.set_pos(700, 400);


        let mut main_layout = group::Pack::new(10, 10, 300, 300, "");
        main_layout.set_spacing(10);

        let (new_game_button, help_button) = Game::add_menu_layout();

        let mut num_buttons = vec![];
        let num_generator = Generator::new();
        Game::add_buttons_layout(&mut num_buttons, &num_generator);

        main_layout.end();
        main_layout.set_type(group::PackType::Vertical);


        let (sender, receiver) = app::channel::<Message>();

        Game {
            game_window,
            new_game_button,
            help_button,
            num_buttons,
            num_generator,
            sender,
            receiver,
        }
    }

    pub fn start_new_game_callback(&mut self) {
        self.num_generator = Generator::new();
        let numbers = self.num_generator.numbers;

        // just change labels for buttons
        for i in 0..numbers.len() {
            let curr_num = numbers[i];
            let num_button = &mut self.num_buttons[i];

            num_button.set_label(&curr_num.to_string());

            if curr_num == 0 {
                num_button.set_label("");
                num_button.deactivate();
            } else {
                num_button.activate();
            }
        }

        // self.num_buttons_layer.redraw();
        self.game_window.redraw();

        self.add_button_events();
    }

    pub fn change_button_position(&mut self, num: i8) {
        // // println!("val :{} ", num);
        // println!("GENERATOR :{:?} ", self.num_generator);
        // println!("NUM :{:?} ", num);
        let pressed_num_index: usize = self.num_generator.index(num).unwrap();
        // println!("PRESSED INDEX:{} ", pressed_num_index);
        let empty_num_index: i8 = self.num_generator.find_empty_element(
            pressed_num_index
        );
        // println!("EMPTY :{} ", empty_num_index);

        if empty_num_index == -1 {
            return;
        }

        self.num_buttons[pressed_num_index].deactivate();
        self.num_buttons[pressed_num_index].set_label("");
        self.num_buttons[empty_num_index as usize].activate();
        self.num_buttons[empty_num_index as usize].set_label(&num.to_string());

        self.num_buttons[empty_num_index as usize].emit(self.sender, Message::Step(num));

        self.num_generator.swap(pressed_num_index, empty_num_index as usize);
    }

    pub fn is_end_game(&self) -> bool {
        self.num_generator.is_sorted()
    }

    pub fn add_events(&mut self) {
        // add events
        self.new_game_button.emit(self.sender, Message::NewGame);
        self.help_button.emit(self.sender, Message::Help);
    }

    pub fn add_button_events(&mut self) {
        for button in &mut self.num_buttons {
            let mut num = 0;
            let val = button.label();

            // ignore event for '0' button
            if val != "" {
                num = val.parse::<i8>().unwrap();
            }

            button.emit(self.sender, Message::Step(num));
        }
    }

    pub fn check_event_loop(&mut self) {
        if let Some(msg) = self.receiver.recv() {
            match msg {
                Message::NewGame => {
                    self.start_new_game_callback();
                }

                Message::Step(label) => {
                    self.change_button_position(label);
                    if self.is_end_game() {
                        let variant = dialog::choice(
                            720, 500, "You win! Start new game ?", "Yes", "No", "",
                        );

                        if variant == 0 {
                            self.start_new_game_callback();
                        } else {
                            app::quit();
                        }
                    }
                }

                Message::Help => dialog::message(
                    720, 500,
                    "Press by button for replace on empty place. \n \
                        ProgUs! , 2021.",
                )
            }
        }
    }

    // Private
    fn add_menu_layout() -> (button::Button, button::Button) {
        let mut menu_layout = group::Pack::new(0, 0, 280, 30, "");
        menu_layout.set_spacing(10);

        let new_game_button = button::Button::default().with_label("New Game");
        let help_button = button::Button::default().with_label("Help");

        menu_layout.end();
        menu_layout.set_type(group::PackType::Horizontal);
        menu_layout.auto_layout();
        (new_game_button, help_button)
    }

    fn add_buttons_layout(num_buttons: &mut Vec<button::Button>, num_generator: &Generator) {
        let numbers = num_generator.numbers;
        let mut main_button_layout = group::Pack::default();

        for i in 0..4 {
            let mut buttons_layout = group::Pack::new(0, 20 + (i as i32 % 4 + 20), 300, 45 + (i as i32 % 4 + 20), "");

            for j in i * 4..(i * 4) + 4 {
                let mut pb = button::Button::default()
                    .with_size(70, 10)
                    .with_label(&num_generator.numbers[j].to_string());
                pb.set_color(enums::Color::from_rgb(195, 179, 145));

                // '0' button - free place
                if numbers[j] == 0 {
                    pb.set_label("");
                    pb.deactivate();
                }

                num_buttons.push(pb);
            }

            buttons_layout.end();
            buttons_layout.set_type(group::PackType::Horizontal);
        }

        main_button_layout.end();
        main_button_layout.set_type(group::PackType::Vertical);
    }
}