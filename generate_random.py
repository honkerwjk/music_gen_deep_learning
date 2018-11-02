import pickle
import random
from music21 import instrument, note, stream, chord

def generate():
    # load the notes used to train the model
    print("Loading the notes used to train the model")
    with open('data/notes', 'rb') as filepath:
        notes = pickle.load(filepath)

    # Get all pitch names
    pitchnames = sorted(set(item for item in notes))
    # Get all pitch names
    n_vocab = len(set(notes))

    print("Generating notes")
    prediction_output = generate_notes(pitchnames, n_vocab)
    print("Creating midi file")
    create_midi(prediction_output)


def generate_notes(pitchnames, n_vocab):
    # pick a random sequence from the input as a starting point for the prediction

    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

    prediction_output = []

    # generate 500 notes
    for note_index in range(500):
        index = random.randrange(0, n_vocab-1, 1)
        result = int_to_note[index]
        prediction_output.append(result)

    return prediction_output


def create_midi(prediction_output):
    offset = 0
    output_notes = []

    print(prediction_output)

    # create note and chord objects based on the values generated by the model
    for pattern in prediction_output:
        # pattern is a chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        elif pattern == 'rest':
            new_note = note.Rest()
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)
        # pattern is a note
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        # increase offset each iteration so that notes do not stack
        offset += 0.25

    midi_stream = stream.Stream(output_notes)

    midi_stream.write('midi', fp='test_output_random.mid')


if __name__ == '__main__':
    generate()