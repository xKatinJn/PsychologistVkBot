class CsvHelper:
    @staticmethod
    def read_questions(path: str) -> list:
        with open(path, 'r') as file:
            questions = file.read()
            if questions:
                return questions.split(';')
            else:
                raise Exception('Question file is empty')

    @staticmethod
    def read_have_passed(path: str) -> list:
        with open(path, 'r') as file:
            have_passed = file.read()
            if have_passed:
                have_passed = have_passed.split(';')
                have_passed.remove('')
                return have_passed
            else:
                return []

    @staticmethod
    def write_user_have_passed(peer_id: str, path: str) -> None:
        with open(path, 'a') as file:
            file.write(f'{peer_id};')
