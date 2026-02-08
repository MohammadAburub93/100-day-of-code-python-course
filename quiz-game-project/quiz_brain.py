class QuizBrain:

    def __init__(self, q_list):
        self.question_num = 0
        self.question_list = q_list
        self.score = 0

    def still_has_questions(self):
        return self.question_num < len(self.question_list)

    def next_question(self):
        new_q = self.question_list[self.question_num]
        self.question_num += 1
        user_choice = input(f"Q.{self.question_num}: {new_q.text} (True/False)?: ")
        self.check_answer(user_choice, new_q.answer)

    def check_answer(self, user_answer, correct_answer):
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            print(f"You got it right!\nThe correct answer was: {correct_answer}\nYour current score is: "
                  f"{self.score}/{self.question_num}")
        else:
            print(f"That's wrong\nThe correct answer was: {correct_answer}\nYour current score is: "
                  f"{self.score}/{self.question_num}")

        print("\n")

