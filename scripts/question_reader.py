class QuestionReader:
    @staticmethod
    def read_questions(path: str) -> list:
        with open(path, 'r') as file:
            questions = file.read()
            if questions:
                return questions.split(';')
            else:
                raise Exception('Question file is empty')
