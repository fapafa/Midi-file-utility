# python -m pip install pretty-midi
import tkinter
import tkinter.filedialog
import pretty_midi


def insert_text(str):
    text_edit.insert(tkinter.END, str + '\n')
    text_edit.pack()

def run():

    path = tkinter.filedialog.askopenfilename(
        title="Select file", 
        filetypes=(("midi files", "*.mid"), ("all files", "*.*")))

    insert_text('IN - ' + path)

    midi_data = pretty_midi.PrettyMIDI(path)
    for instrument in midi_data.instruments:
        if instrument.is_drum:
            continue

        temp_note = []
        for note in instrument.notes:
            for pit in range(note.pitch-12, -1, -12):
                temp = pretty_midi.Note(velocity=note.velocity, pitch=pit, start=note.start, end=note.end)
                temp_note.append(temp)

            for pit in range(note.pitch+12, 128, 12):
                temp = pretty_midi.Note(velocity=note.velocity, pitch=pit, start=note.start, end=note.end)
                temp_note.append(temp)
        instrument.notes = instrument.notes + temp_note
    
    path = tkinter.filedialog.asksaveasfilename(
        title="Select file", 
        filetypes=(("midi files", "*.mid"), ("all files", "*.*")))

    midi_data.write(path)
    insert_text('OUT - ' + path)
    insert_text('Complete')


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Midi Voicing")

    button = tkinter.Button(root, text ="Run", command = run, 
        height=2 , width=10, background='#d1d1e0' )
    button.pack()

    text_edit = tkinter.Text(root)
    text_edit.pack()

    root.mainloop()