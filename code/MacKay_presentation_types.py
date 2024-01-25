import json
import pathlib

class PresentationType:

    def __init__ (self,
            parts:int,
            figure_code:str,
            description:str,
            voice_descriptions:list[tuple[int, str]]):

        self.parts = parts
        self.figure = figure_code
        self.description = description
        self.voices = [{'offset': tup[0], 'label': tup[1]} for tup in voice_descriptions]
        self.repr = self.__str__()

    def __str__ (self):

        line_length = 17
        offset = 4
        repr = f'{self.figure}: {self.description}\n'
        for voice in self.voices:
            repr += '\n'
            for i in range(voice['offset']*offset):
                repr += ' '
            repr += f'{voice['label']}\n'
            for i in range(voice['offset']*offset):
                repr += ' '
            for i in range(line_length):
                repr += '_'
            repr += '\n'

        print(repr)

        return repr
            

presentation_types = {
    'A-9': PresentationType(4, 'A-9', 'Two-subject non-imitative module with parallel doubling', [
        (0, 'A (parallel)'),
        (0, 'A (parallel)'),
        (0, 'B (parallel)'),
        (0, 'B (parallel)')
    ]).__dict__,
    'A-10': PresentationType(4, 'A-10', 'Three-subject non-imitative module with parallel doubling', [
        (0, 'A (parallel)'),
        (0, 'A (parallel)'),
        (0, 'B'),
        (0, 'C')
    ]).__dict__,
    'A-11': PresentationType(4, 'A-11', 'Four-subject non-imitative module', [
        (0, 'A'),
        (0, 'B'),
        (0, 'C'),
        (0, 'D')
    ]).__dict__,
    'A-12': PresentationType(4, 'A-12', 'Transposed canon in four voices', [
        (3, 'A'),
        (2, 'A'),
        (1, 'A'),
        (0, 'A')
    ]).__dict__,
    'A-13': PresentationType(4, 'A-13', 'Variably constructed canon, type 1 (pair of imitative duos)', [
        (1, 'A (duo 1)'),
        (0, 'A (duo 1)'),
        (3, 'A (duo 2)'),
        (2, 'A (duo 2)')
    ]).__dict__,
    'A-14': PresentationType(4, 'A-14', 'Variably constructed canon, type 2 (invertible->transposed canon)', [
        (0, 'A'),
        (3, 'A'),
        (2, 'A'),
        (1, 'A')
    ]).__dict__,
    'A-15': PresentationType(4, 'A-15', 'Variably constructed canon, type 3 (transposed->invertible canon)', [
        (2, 'A'),
        (1, 'A'),
        (0, 'A'),
        (3, 'A')
    ]).__dict__,
    'A-16': PresentationType(4, 'A-16', 'Imitative duo with parallel doubling', [
        (0, 'A (parallel)'),
        (1, 'A (parallel)'),
        (0, 'A (parallel)'),
        (1, 'A (parallel)')
    ]).__dict__,
    'A-17': PresentationType(4, 'A-17', 'Overlapping duos', [
        (0, 'A (duo 1)'),
        (1, 'A (duo 2)'),
        (0, 'A (duo 1)'),
        (1, 'A (duo 2)')
    ]).__dict__,
    'A-18': PresentationType(4, 'A-18', 'Transposed canon plus parallel doubling', [
        (0, 'A (parallel)'),
        (0, 'A (parallel)'),
        (1, 'A'),
        (2, 'A')
    ]).__dict__,
    'A-19': PresentationType(4, 'A-19', 'Invertible canon plus parallel doubling', [
        (0, 'A (parallel)'),
        (0, 'A (parallel)'),
        (2, 'A'),
        (1, 'A')
    ]).__dict__,
    'A-20': PresentationType(4, 'A-20', 'Accompanied transposed canon', [
        (0, 'A'),
        (1, 'A'),
        (2, 'A'),
        (0, 'B')
    ]).__dict__,
    'A-21': PresentationType(4, 'A-21', 'Accompanied invertible canon', [
        (1, 'A'),
        (0, 'A'),
        (2, 'A'),
        (0, 'B')
    ]).__dict__,
    'A-22': PresentationType(4, 'A-22', 'Accompanied semi-imitative presentation', [
        (0, 'A'),
        (1, 'A'),
        (0, 'B'),
        (0, 'C')
    ]).__dict__,
    'A-23': PresentationType(4, 'A-23', 'Semi-imitative presentation plus parallel doubling', [
        (0, 'A (parallel)'),
        (0, 'A (parallel)'),
        (1, 'A'),
        (0, 'B')
    ]).__dict__
}

pathlib.Path('data/McKay_presentation_types.json').write_text(json.dumps(presentation_types, indent=1))