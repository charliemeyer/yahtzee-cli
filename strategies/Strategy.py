
class Strategy():
    def get_ranked_keep_numbers(self, roll, available_categories, roll_number):
        raise NotImplementedError("get_keep_numbers method not implemented")
    
    def get_keep_number_choice(self, roll, available_categories, roll_number):
        raise NotImplementedError("get_keep_number_choice method not implemented")
    
    def get_ranked_category_choices(self, available_categories, roll, scoreboard):
        raise NotImplementedError("get_category_choice method not implemented")
    
    def get_category_choice(self, available_categories, roll, scoreboard):
        raise NotImplementedError("get_category_choice method not implemented")