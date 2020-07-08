class CsvHelper:
    @staticmethod
    def read_questions(path: str) -> list:
        with open(path, 'r', encoding='utf-8') as file:
            questions = file.read()
            if questions:
                return questions.split(';')
            else:
                raise Exception('Question file is empty')

    @staticmethod
    def read_have_passed(path: str) -> list:
        with open(path, 'r', encoding='utf-8') as file:
            have_passed = file.read()
            if have_passed:
                have_passed = have_passed.split(';')
                if '' in have_passed:
                    have_passed.remove('')
                return have_passed
            else:
                return []

    @staticmethod
    def write_user_have_passed(peer_id: str, path: str) -> None:
        with open(path, 'a', encoding='utf-8') as file:
            file.write(f'{peer_id};')

    @staticmethod
    def delete_user_from_have_passed(peer_id: str, path: str) -> None:
        have_passed = CsvHelper.read_have_passed(path)
        have_passed.remove(peer_id)
        have_passed.append('')
        with open(path, 'w', encoding='utf-8') as file:
            file.write(';'.join(have_passed))
